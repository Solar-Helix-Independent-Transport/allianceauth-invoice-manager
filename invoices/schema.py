from datetime import datetime
from decimal import Decimal
from typing import Optional

from ninja import Schema


class Message(Schema):
    message: str


class WalletEvent(Schema):
    amount: Decimal
    date: datetime


class Character(Schema):
    character_name: str
    corporation_name: str
    alliance_name: Optional[str] = None


class Corporation(Schema):
    corporation_name: str
    alliance_name: Optional[str] = None
    corporation_id: int
    alliance_id: Optional[int] = None


class Invoice(Schema):
    pk: int
    due_date: datetime
    paid: bool
    note: str
    invoice_ref: str
    amount: float
    character: Character
    payment: Optional[WalletEvent] = None
    action: Optional[bool] = None
