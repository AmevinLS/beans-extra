import datetime
from decimal import Decimal
import enum
from typing import FrozenSet, TypeAlias

from pydantic import BaseModel
from beansql.models.core import AmountX, MetaX, FlagX, PostingX, AccountX, CurrencyX

TagX: TypeAlias = str
LinkX: TypeAlias = str


class BaseDirectiveX(BaseModel):
    meta: MetaX
    date: datetime.date


class TransactionX(BaseDirectiveX):
    flag: FlagX
    payee: str | None
    narration: str
    tags: FrozenSet[TagX]
    links: FrozenSet[LinkX]
    postings: list[PostingX]


class BalanceX(BaseDirectiveX):
    account: AccountX
    amount: AmountX
    tolerance: Decimal | None
    diff_amount: AmountX | None


class PadX(BaseDirectiveX):
    account: AccountX
    source_account: AccountX


@enum.unique
class BookingX(enum.Enum):
    # Reject ambiguous matches with an error.
    STRICT = "STRICT"
    # Strict booking method, but disambiguate further with sizes. Reject
    # ambiguous matches with an error but if a lot matches the size exactly,
    # accept it the oldest.
    STRICT_WITH_SIZE = "STRICT_WITH_SIZE"
    # Disable matching and accept the creation of mixed inventories.
    NONE = "NONE"
    # Average cost booking: merge all matching lots before and after.
    AVERAGE = "AVERAGE"
    # First-in first-out in the case of ambiguity.
    FIFO = "FIFO"
    # Last-in first-out in the case of ambiguity.
    LIFO = "LIFO"
    # Highest-in first-out in the case of ambiguity.
    HIFO = "HIFO"


class OpenX(BaseDirectiveX):
    account: AccountX
    currencies: list[CurrencyX]
    booking: BookingX | None


class CloseX(BaseDirectiveX):
    account: AccountX


class CommodityX(BaseDirectiveX):
    currency: CurrencyX


class NoteX(BaseDirectiveX):
    account: AccountX
    comment: str
    tags: set[TagX] | None
    links: set[LinkX] | None


class EventX(BaseDirectiveX):
    type: str
    description: str


class PriceX(BaseDirectiveX):
    currency: CurrencyX
    amount: AmountX


class Document(BaseDirectiveX):
    account: AccountX
    filename: str
    tags: set[TagX] | None
    links: set[LinkX] | None
