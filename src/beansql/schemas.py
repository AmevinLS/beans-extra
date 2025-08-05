from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import Date, String, Uuid, Double
from uuid import UUID, uuid4
import datetime
from beansql.models.core import AccountX


class Base(DeclarativeBase):
    pass


class TransactionDB(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid4)
    trans_date: Mapped[datetime.date] = mapped_column(Date())
    flag: Mapped[str] = mapped_column(String(1))
    payee: Mapped[str | None] = mapped_column(String(), nullable=True)
    narration: Mapped[str] = mapped_column(String())

    tags: Mapped[list["TransactionTagDB"]] = relationship(back_populates="transaction")
    links: Mapped[list["TransactionLinkDB"]] = relationship(
        back_populates="transaction"
    )
    postings: Mapped[list["PostingDB"]] = relationship(back_populates="transaction")


class TransactionTagDB(Base):
    __tablename__ = "transaction_tags"

    transaction_id: Mapped[UUID] = mapped_column(ForeignKey("transactions.id"))
    tag_name: Mapped[str] = mapped_column(String())

    transaction: Mapped[TransactionDB] = relationship(back_populates="tags")

    __table_args__ = (PrimaryKeyConstraint("transaction_id", "tag_name"),)


class TransactionLinkDB(Base):
    __tablename__ = "transaction_links"

    transaction_id: Mapped[UUID] = mapped_column(ForeignKey("transactions.id"))
    link_name: Mapped[str] = mapped_column(String())

    transaction: Mapped[TransactionDB] = relationship(back_populates="links")

    __table_args__ = (PrimaryKeyConstraint("transaction_id", "link_name"),)


class PostingDB(Base):
    __tablename__ = "postings"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid4)
    account: Mapped[AccountX] = mapped_column(String())
    units_number: Mapped[float | None] = mapped_column(Double(), nullable=True)
    units_currency: Mapped[str | None] = mapped_column(String(), nullable=True)
    cost_number: Mapped[float | None] = mapped_column(Double(), nullable=True)
    cost_currency: Mapped[str | None] = mapped_column(String(), nullable=True)
    price_number: Mapped[float | None] = mapped_column(Double(), nullable=True)
    price_currency: Mapped[str | None] = mapped_column(String(), nullable=True)
    flag: Mapped[str | None] = mapped_column(String(1), nullable=True)
    transaction_id: Mapped[UUID] = mapped_column(ForeignKey("transactions.id"))
    # meta: TODO

    transaction: Mapped[TransactionDB] = relationship(back_populates="postings")
