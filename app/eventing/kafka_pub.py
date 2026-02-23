import os, json
from kafka import KafkaProducer

_producer = None

def _get_producer():
    global _producer
    if _producer:
        return _producer
    broker = os.getenv("KAFKA_BROKER", "kafka:9092")
    _producer = KafkaProducer(bootstrap_servers=broker, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
    return _producer

def publish_event(topic: str, payload: dict):
    try:
        _get_producer().send(topic, payload)
    except Exception:
        # local dev should not hard-fail if kafka isn't ready
        pass
