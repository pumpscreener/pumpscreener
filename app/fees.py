from dataclasses import dataclass

@dataclass
class DexFeePolicy:
    # fee as % of token transfer/mint, taken in TOKEN units, routed to DEX treasury
    # Example: 0.20% = 20 bps
    transfer_fee_bps: int = 20
    mint_fee_bps: int = 50

    def tokens_due_on_transfer(self, token_amount: float) -> float:
        return token_amount * self.transfer_fee_bps / 10_000

    def tokens_due_on_mint(self, token_amount: float) -> float:
        return token_amount * self.mint_fee_bps / 10_000
