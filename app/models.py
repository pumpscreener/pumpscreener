from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, UniqueConstraint, Index, BigInteger, DateTime, Text, Boolean
from datetime import datetime

class Base(DeclarativeBase): pass

class Token(Base):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    chain: Mapped[str] = mapped_column(String(16), default="sol")      # Pump.fun is Solana
    mint: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    symbol: Mapped[str] = mapped_column(String(24))
    name: Mapped[str] = mapped_column(String(128))
    decimals: Mapped[int] = mapped_column(Integer)
    creator: Mapped[str] = mapped_column(String(64))
    is_pumpfun: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    pools: Mapped[list["Pool"]] = relationship(back_populates="token")

class Pool(Base):
    __tablename__ = "pools"
    id: Mapped[int] = mapped_column(primary_key=True)
    dex: Mapped[str] = mapped_column(String(32))         # "pumpswap"
    address: Mapped[str] = mapped_column(String(64), index=True)
    token_id: Mapped[int] = mapped_column(ForeignKey("tokens.id"))
    base_symbol: Mapped[str] = mapped_column(String(24))  # e.g., SOL
    quote_symbol: Mapped[str] = mapped_column(String(24))
    liquidity_usd: Mapped[float] = mapped_column(Float, default=0.0)
    price: Mapped[float] = mapped_column(Float, default=0.0)           # token/quote
    fdv_usd: Mapped[float] = mapped_column(Float, default=0.0)
    last_synced: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    token: Mapped["Token"] = relationship(back_populates="pools")

    __table_args__ = (
        UniqueConstraint("dex", "address", name="uq_dex_pool"),
        Index("ix_pool_token_dex", "token_id", "dex"),
    )

class Trade(Base):
    __tablename__ = "trades"
    id: Mapped[int] = mapped_column(primary_key=True)
    pool_id: Mapped[int] = mapped_column(ForeignKey("pools.id"), index=True)
    ts: Mapped[int] = mapped_column(BigInteger)      # unix ms
    side: Mapped[str] = mapped_column(String(4))     # buy/sell
    price: Mapped[float] = mapped_column(Float)
    amount_token: Mapped[float] = mapped_column(Float)
    amount_quote: Mapped[float] = mapped_column(Float)
    tx: Mapped[str] = mapped_column(String(128))

class Candle(Base):
    __tablename__ = "candles"
    id: Mapped[int] = mapped_column(primary_key=True)
    pool_id: Mapped[int] = mapped_column(ForeignKey("pools.id"), index=True)
    timeframe: Mapped[str] = mapped_column(String(8))    # '1m','5m','1h'
    open_time: Mapped[int] = mapped_column(BigInteger)    # unix ms bucket
    o: Mapped[float] = mapped_column(Float)
    h: Mapped[float] = mapped_column(Float)
    l: Mapped[float] = mapped_column(Float)
    c: Mapped[float] = mapped_column(Float)
    v: Mapped[float] = mapped_column(Float)              # token volume
    __table_args__ = (UniqueConstraint("pool_id","timeframe","open_time", name="uq_candle_bucket"),)
