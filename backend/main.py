"""
FastAPI entry point for the Finance / Banking / FinTech AI Chatbot.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.catalog import catalog
from app.chatbot import engine
from app.models import ChatRequest, ChatResponse
from app.sessions import store

app = FastAPI(
    title="Finance AI Chatbot",
    description=(
        "A demo conversational AI for banking, finance, and FinTech. Includes intent classification, "
        "fraud detection guardrails, and rich response blocks for accounts, cards, loans, investments, "
        "market data, and budgets. NOT a substitute for a SEBI-registered advisor or bank staff."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "accounts": len(catalog.accounts()),
        "cards":    len(catalog.cards()),
        "loans":    len(catalog.loans()),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session = store.get_or_create(req.session_id)
    return engine.respond(req.message, session)


@app.get("/accounts")
def list_accounts():
    return catalog.accounts()


@app.get("/cards")
def list_cards():
    return catalog.cards()


@app.get("/transactions")
def list_transactions(limit: int = 20):
    return catalog.recent_transactions(limit=limit)


@app.get("/loans")
def list_loans():
    return catalog.loans()


@app.get("/investments")
def list_investments():
    return catalog.investments()


@app.get("/market")
def market_snapshot():
    return catalog.market_snapshot()


@app.get("/products/credit-cards")
def list_credit_cards(category: str | None = None):
    return catalog.credit_card_products(category=category, limit=10)


@app.get("/products/loans")
def list_loan_products(loan_type: str | None = None):
    return catalog.loan_products(loan_type=loan_type, limit=10)


@app.get("/products/deposits")
def list_deposit_products():
    return catalog.deposit_products(limit=10)


@app.get("/")
def root():
    return {
        "name":       "Finance AI Chatbot",
        "version":    app.version,
        "docs":       "/docs",
        "disclaimer": "Demo only. Not a substitute for a registered financial advisor or bank staff.",
    }
