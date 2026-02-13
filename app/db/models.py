from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, JSON, Integer

class Base(DeclarativeBase):
    pass

class DeploymentRequest(Base):
    __tablename__ = "deployment_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    app_name: Mapped[str] = mapped_column(String(128))
    environment: Mapped[str] = mapped_column(String(32))
    data_classification: Mapped[str] = mapped_column(String(32))
    exposure: Mapped[str] = mapped_column(String(32))
    config: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(32), default="PENDING")

