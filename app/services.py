import httpx
from typing import Optional, Iterable
from .config import settings

# --------- Pump.fun ----------
async def pumpfun_list_new_tokens(client: httpx.AsyncClient) -> Iterable[dict]:
    """
    Replace this with Pump.fun discovery feed.
    Return items like: {mint, symbol, name, decimals, creator, created_at}
    """
    # Placeholder — yield nothing or some mocks
    return []

# --------- PumpSwap ----------
async def pumpswap_list_pools_for_mint(client: httpx.AsyncClient, mint: str) -> Iterable[dict]:
    """
    Replace with PumpSwap API that lists pools for a token mint.
    Return items like: {address, base_symbol, quote_symbol, liquidity_usd, price, fdv_usd}
    """
    return []

async def pumpswap_recent_trades(client: httpx.AsyncClient, pool_address: str, limit: int = 100) -> Iterable[dict]:
    """
    Replace with PumpSwap trades endpoint for a pool.
    Return items like: {ts, side, price, amount_token, amount_quote, tx}
    """
    return []
