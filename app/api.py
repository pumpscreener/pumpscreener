from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import sessionmaker
from .config import settings
from .models import Token, Pool, Trade
from .schemas import PoolOut, TradeOut, TokenOut

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)
router = APIRouter(prefix="/api")

@router.get("/pairs", response_model=list[PoolOut])
def list_pairs(limit: int = 100, min_liq: float = 500.0):
    with SessionLocal() as s:
        q = s.query(Pool).options(joinedload(Pool.token)).filter(
            Pool.dex=="pumpswap",
            Pool.liquidity_usd >= min_liq
        ).order_by(Pool.liquidity_usd.desc()).limit(limit)
        rows = q.all()
        return [
            PoolOut(
                id=p.id, dex=p.dex, address=p.address,
                token=TokenOut(chain=p.token.chain, mint=p.token.mint, symbol=p.token.symbol, name=p.token.name, decimals=p.token.decimals),
                base_symbol=p.base_symbol, quote_symbol=p.quote_symbol,
                liquidity_usd=p.liquidity_usd, price=p.price, fdv_usd=p.fdv_usd
            ) for p in rows
        ]

@router.get("/pairs/{pool_id}/trades", response_model=list[TradeOut])
def pair_trades(pool_id: int, limit: int = 100):
    with SessionLocal() as s:
        t = s.query(Trade).filter(Trade.pool_id==pool_id).order_by(desc(Trade.ts)).limit(limit).all()
        return [TradeOut(ts=x.ts, side=x.side, price=x.price, amount_token=x.amount_token, amount_quote=x.amount_quote, tx=x.tx) for x in t]
