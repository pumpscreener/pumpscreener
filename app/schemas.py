from pydantic import BaseModel
from typing import Optional, List

class TokenOut(BaseModel):
    chain: str
    mint: str
    symbol: str
    name: str
    decimals: int

class PoolOut(BaseModel):
    id: int
    dex: str
    address: str
    token: TokenOut
    base_symbol: str
    quote_symbol: str
    liquidity_usd: float
    price: float
    fdv_usd: float

class TradeOut(BaseModel):
    ts: int
    side: str
    price: float
    amount_token: float
    amount_quote: float
    tx: str

class CandleOut(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float
    t: int
