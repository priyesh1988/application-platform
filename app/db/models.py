from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, DateTime
import datetime

class Base(DeclarativeBase):
    pass

class DeploymentRequest(Base):
    __tablename__ = "deployment_requests"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    decision: Mapped[str] = mapped_column(Text)
    request_json: Mapped[str] = mapped_column(Text)
    policy_json: Mapped[str] = mapped_column(Text)
    risk_json: Mapped[str] = mapped_column(Text)
