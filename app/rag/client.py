import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import hashlib

COLLECTION = "platform_kb"

def _client():
    host = os.getenv("QDRANT_HOST", "qdrant")
    port = int(os.getenv("QDRANT_PORT", "6333"))
    return QdrantClient(host=host, port=port)

def ensure_collection(dim: int = 1536):
    c = _client()
    existing = [col.name for col in c.get_collections().collections]
    if COLLECTION not in existing:
        c.create_collection(COLLECTION, vectors_config=VectorParams(size=dim, distance=Distance.COSINE))

def _embed(text: str):
    # OpenAI embeddings if available; else deterministic pseudo-embedding for local dev
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        import random
        random.seed(int(hashlib.sha256(text.encode()).hexdigest(), 16) % (2**32))
        return [random.random() for _ in range(128)]  # smaller dim for local stub
    from openai import OpenAI
    client = OpenAI(api_key=key)
    model = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")
    emb = client.embeddings.create(model=model, input=text).data[0].embedding
    return emb

def ingest(text: str, source: str):
    vec = _embed(text)
    dim = len(vec)
    ensure_collection(dim=dim)
    pid = int(hashlib.sha256((source + text).encode()).hexdigest(), 16) % (2**63-1)
    _client().upsert(
        COLLECTION,
        points=[PointStruct(id=pid, vector=vec, payload={"source": source, "text": text})],
    )
    return {"id": pid, "dim": dim}

def rag_answer(question: str) -> str:
    # Retrieve 1 nearest doc and return a concise answer (LLM if available)
    vec = _embed(question)
    ensure_collection(dim=len(vec))
    hits = _client().search(COLLECTION, query_vector=vec, limit=1)
    if not hits:
        return "KB is empty. Ingest runbooks/policies via POST /rag/ingest."

    ctx = hits[0].payload.get("text", "")
    source = hits[0].payload.get("source", "")

    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return f"Top match from {source}: {ctx[:400]}..."

    from openai import OpenAI
    client = OpenAI(api_key=key)
    prompt = (
        "Answer the question using ONLY the context. If not in context, say you don't know.\n"
        f"Question: {question}\nContext: {ctx}\n"
        f"Return a short answer and cite source: {source}."
    )
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "system", "content": "You are a platform knowledge assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return resp.choices[0].message.content
