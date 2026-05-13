"""
Pydantic models for the Finance / Banking / FinTech chatbot.
"""
from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel, Field


# ─── Request ───────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = None


# ─── Domain entities ───────────────────────────────────────
class Account(BaseModel):
    id: str
    type: str
    label: str
    number_masked: str
    balance: float
    currency: str
    ifsc: str
    branch: str


class Card(BaseModel):
    id: str
    type: str
    label: str
    number_masked: str
    status: str
    currency: str
    limit: Optional[int] = None
    current_balance: Optional[float] = None
    available: Optional[float] = None
    due_date: Optional[str] = None
    min_due: Optional[float] = None
    rewards_points: Optional[int] = None
    linked_account: Optional[str] = None
    daily_limit: Optional[int] = None


class Transaction(BaseModel):
    id: str
    date: str
    merchant: str
    category: str
    amount: float
    type: Literal["credit", "debit"]
    account: str
    status: Literal["completed", "pending", "flagged", "failed"]


class Loan(BaseModel):
    id: str
    type: str
    principal: float
    outstanding: float
    emi: float
    rate: float
    tenure_months: int
    remaining_months: int
    next_due: str
    lender: str


class Investment(BaseModel):
    id: str
    symbol: str
    name: str
    shares: int
    avg_buy: float
    current: float
    currency: str
    category: str


class Stock(BaseModel):
    symbol: str
    name: str
    sector: str
    price: float
    change: float
    change_pct: float
    market_cap: str
    pe: float


class MarketIndex(BaseModel):
    symbol: str
    name: str
    value: float
    change: float
    change_pct: float


class BudgetCategory(BaseModel):
    category: str
    spent: float
    limit: float
    icon: str


class CreditCardProduct(BaseModel):
    id: str
    name: str
    category: str
    annual_fee: int
    joining_fee: int
    rewards_rate: str
    best_for: str
    min_income: int
    credit_score_min: int
    perks: list[str]
    highlight: str


class LoanProduct(BaseModel):
    id: str
    type: str
    rate_from: float
    tenure_max_years: int
    max_amount: int
    processing_fee_pct: float
    description: str
    min_credit_score: int


class DepositProduct(BaseModel):
    id: str
    name: str
    rate_pct: float
    min_tenure_months: int
    max_tenure_months: int
    min_amount: int
    senior_citizen_bonus: float
    compounding: str
    premature_penalty_pct: Optional[float] = None
    tax_benefit: Optional[str] = None
    recurring: Optional[bool] = False


class TransferConfirmation(BaseModel):
    transfer_id: str
    from_account: str
    to_account_masked: str
    to_name: str
    amount: float
    mode: str          # UPI | NEFT | IMPS | RTGS
    fee: float
    eta: str
    status: str


class CreditScore(BaseModel):
    score: int
    band: str          # Excellent | Good | Fair | Poor
    last_updated: str
    factors: list[dict]  # [{label, impact: "positive"|"negative"}]


# ─── Rich message blocks ───────────────────────────────────
class TextBlock(BaseModel):
    type: Literal["text"] = "text"
    content: str


class AccountsBlock(BaseModel):
    type: Literal["accounts"] = "accounts"
    title: Optional[str] = None
    items: list[Account]


class CardsBlock(BaseModel):
    type: Literal["cards"] = "cards"
    title: Optional[str] = None
    items: list[Card]


class TransactionsBlock(BaseModel):
    type: Literal["transactions"] = "transactions"
    title: Optional[str] = None
    items: list[Transaction]


class LoansBlock(BaseModel):
    type: Literal["loans"] = "loans"
    title: Optional[str] = None
    items: list[Loan]


class InvestmentsBlock(BaseModel):
    type: Literal["investments"] = "investments"
    title: Optional[str] = None
    items: list[Investment]
    total_invested: float
    total_current: float


class MarketBlock(BaseModel):
    type: Literal["market"] = "market"
    title: Optional[str] = None
    indices: list[MarketIndex]
    stocks: list[Stock]


class BudgetBlock(BaseModel):
    type: Literal["budget"] = "budget"
    title: Optional[str] = None
    month_label: str
    items: list[BudgetCategory]
    total_spent: float
    total_limit: float


class CreditCardProductsBlock(BaseModel):
    type: Literal["credit_card_products"] = "credit_card_products"
    title: Optional[str] = None
    items: list[CreditCardProduct]


class LoanProductsBlock(BaseModel):
    type: Literal["loan_products"] = "loan_products"
    title: Optional[str] = None
    items: list[LoanProduct]


class DepositProductsBlock(BaseModel):
    type: Literal["deposit_products"] = "deposit_products"
    title: Optional[str] = None
    items: list[DepositProduct]


class TransferBlock(BaseModel):
    type: Literal["transfer"] = "transfer"
    confirmation: TransferConfirmation


class CreditScoreBlock(BaseModel):
    type: Literal["credit_score"] = "credit_score"
    score_info: CreditScore


class FraudAlertBlock(BaseModel):
    type: Literal["fraud_alert"] = "fraud_alert"
    headline: str
    message: str
    indicators: list[str]
    helpline: dict   # {label, number}


class DisclaimerBlock(BaseModel):
    type: Literal["disclaimer"] = "disclaimer"
    content: str


MessageBlock = (
    TextBlock | AccountsBlock | CardsBlock | TransactionsBlock | LoansBlock
    | InvestmentsBlock | MarketBlock | BudgetBlock | CreditCardProductsBlock
    | LoanProductsBlock | DepositProductsBlock | TransferBlock | CreditScoreBlock
    | FraudAlertBlock | DisclaimerBlock
)


# ─── Response ──────────────────────────────────────────────
class ChatResponse(BaseModel):
    session_id: str
    intent: str
    confidence: float
    blocks: list[MessageBlock]
    suggestions: list[str] = []
    safety_flag: Optional[str] = None  # None | "fraud" | "social_engineering"
