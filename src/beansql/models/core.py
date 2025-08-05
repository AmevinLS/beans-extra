import datetime
from decimal import Decimal
from typing import Any, Literal, TypeAlias

from pydantic import BaseModel


AccountX: TypeAlias = str
CurrencyX: TypeAlias = str
FlagX: TypeAlias = Literal["*", "!"]
MetaX: TypeAlias = dict[str, Any]


class AmountX(BaseModel):
    number: Decimal | None
    currency: str


class CostX(AmountX):
    date: datetime.date
    label: str | None


class CostSpecX(BaseModel):
    numberperX: Decimal | None
    numbertotalX: Decimal | None
    currency: str
    date: datetime.date | None
    label: str | None
    merge: bool | None


class PostingX(BaseModel):
    account: AccountX
    units: AmountX | None
    cost: CostX | CostSpecX | None
    price: AmountX | None
    flag: FlagX | None
