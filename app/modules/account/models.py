from datetime import datetime
from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.settings import Base
from sqlalchemy import ForeignKey

class AccountModel(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    num_account: Mapped[str | None] = mapped_column(
        String, unique=True, nullable=True
    )

    amount: Mapped[float] = mapped_column(Float, nullable=False)

    user_identity: Mapped[str] = mapped_column(String, nullable=False)

    register_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    extracts: Mapped[list["ExtractModel"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan"
    )

class ExtractModel(Base):
    __tablename__ = "extract"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    amount: Mapped[float] = mapped_column(Float, nullable=False)

    balance: Mapped[float] = mapped_column(Float, nullable=False)

    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id"),
        nullable=False
    )

    account: Mapped["AccountModel"] = relationship(
        back_populates="extracts"
    )

    register_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )