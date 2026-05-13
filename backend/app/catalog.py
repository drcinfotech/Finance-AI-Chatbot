"""
Data catalog — loads accounts/transactions/products/market data from JSON.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


DATA_DIR = Path(__file__).parent.parent / "data"


class Catalog:
    def __init__(self):
        with open(DATA_DIR / "accounts.json", "r", encoding="utf-8") as f:
            self._user = json.load(f)
        with open(DATA_DIR / "products.json", "r", encoding="utf-8") as f:
            self._products = json.load(f)
        with open(DATA_DIR / "market.json", "r", encoding="utf-8") as f:
            self._market = json.load(f)

    # ── User accounts & history ────────────────────────
    def accounts(self) -> list[dict]:
        return list(self._user["accounts"])

    def cards(self) -> list[dict]:
        return list(self._user["cards"])

    def credit_cards_owned(self) -> list[dict]:
        return [c for c in self._user["cards"] if c["type"] == "credit"]

    def recent_transactions(self, limit: int = 8) -> list[dict]:
        return list(self._user["recent_transactions"])[:limit]

    def loans(self) -> list[dict]:
        return list(self._user["loans"])

    def investments(self) -> list[dict]:
        return list(self._user["investments"])

    def budgets(self) -> list[dict]:
        return list(self._user["budgets"])

    # ── Product catalog ────────────────────────────────
    def credit_card_products(self, category: Optional[str] = None, limit: int = 3) -> list[dict]:
        cards = self._products["credit_cards"]
        if category:
            cards = [c for c in cards if c["category"].lower() == category.lower()]
        return cards[:limit]

    def loan_products(self, loan_type: Optional[str] = None, limit: int = 4) -> list[dict]:
        loans = self._products["loans"]
        if loan_type:
            loans = [l for l in loans if loan_type.lower() in l["type"].lower()]
        return loans[:limit]

    def deposit_products(self, limit: int = 4) -> list[dict]:
        return self._products["deposits"][:limit]

    # ── Market data ────────────────────────────────────
    def market_snapshot(self) -> dict:
        return {
            "indices": self._market["indices"],
            "stocks":  self._market["stocks"][:6],
        }


catalog = Catalog()
