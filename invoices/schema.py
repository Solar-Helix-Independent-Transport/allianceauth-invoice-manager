from datetime import datetime
from ninja import Schema

from typing import Optional, List, Dict


class Message(Schema):
    message: str


class WalletEvent(Schema):
    amount: int
    date: datetime


class Character(Schema):
    character_name: str
    corporation_name: str
    alliance_name: Optional[str]


class Corporation(Schema):
    corporation_name: str
    alliance_name: Optional[str]
    corporation_id: int
    alliance_id: Optional[int]


class Invoice(Schema):
    due_date: datetime
    paid: bool
    note: str
    invoice_ref: str
    amount: float
    character: Character
    payment: Optional[WalletEvent]
