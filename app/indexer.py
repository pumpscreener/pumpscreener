import asyncio, math, time
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from .config import settings
from .models import Base, Token, Pool, Trade
from .services import pumpfun_list_new_tokens, pumpswap_list_pools_for_mint, pumpswap_recent_trades
import httpx

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

def init_db():
    Base.metadata.create_all(engine)

async def sync_once():
    async with httpx.AsyncClient(timeout=20) as client:
        # 1) discover tokens on Pump.fun
        for t in await _ensure_list(pumpfun_list_new_tokens(client)):
            # upsert token
            with SessionLocal() as s:
                token = s.execute(select(Token).where(Token.mint==t["mint"])).scalar_one_or_none()
                if not token:
                    token = Token(
                        chain="sol",
                        mint=t["mint"],
                        symbol=t["symbol"],
                        name=t["name"],
                        decimals=t["decimals"],
                        creator=t.get("creator",""),
                        is_pumpfun=True,
                        created_at=datetime.utcnow(),
                    )
                    s.add(token); s.commit(); s.refresh(token)
                # 2) list PumpSwap pools for the mint
                for p in await _ensure_list(pumpswap_list_pools_for_mint(client, t["mint"])):
                    pool = s.execute(select(Pool).where(Pool.dex=="pumpswap", Pool.address==p["address"])).scalar_one_or_none()
                    if not pool:
                        pool = Pool(
                            dex="pumpswap",
                            address=p["address"],
                            token_id=token.id,
                            base_symbol=p["base_symbol"],
                            quote_symbol=p["quote_symbol"],
                            liquidity_usd=p.get("liquidity_usd",0.0),
                            price=p.get("price",0.0),
                            fdv_usd=p.get("fdv_usd",0.0),
                        )
                        s.add(pool)
                    else:
                        pool.liquidity_usd = p.get("liquidity_usd", pool.liquidity_usd)
                        pool.price = p.get("price", pool.price)
                        pool.fdv_usd = p.get("fdv_usd", pool.fdv_usd)
                    s.commit()

                # 3) for each saved PumpSwap pool → fetch recent trades
                pools = s.query(Pool).filter(Pool.token_id==token.id, Pool.dex=="pumpswap").all()
                for pool in pools:
                    for tr in await _ensure_list(pumpswap_recent_trades(client, pool.address, limit=100)):
                        exists = s.query(Trade).filter(Trade.tx==tr["tx"]).first()
                        if exists: continue
                        s.add(Trade(
                            pool_id=pool.id,
                            ts=tr["ts"],
                            side=tr["side"],
                            price=tr["price"],
                            amount_token=tr["amount_token"],
                            amount_quote=tr["amount_quote"],
                            tx=tr["tx"],
                        ))
                    s.commit()

async def _ensure_list(x):
    if x is None: return []
    if isinstance(x, list): return x
    return list(x)

async def run_forever():
    while True:
        try:
            await sync_once()
        except Exception as e:
            print("index error:", e)
        await asyncio.sleep(int(settings.index_interval_seconds))
