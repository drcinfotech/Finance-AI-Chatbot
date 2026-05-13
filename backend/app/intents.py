"""
Intent classifier for the Finance / Banking / FinTech chatbot.

Safety detection (see safety.py) runs BEFORE this classifier.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IntentSpec:
    name: str
    patterns: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)


INTENTS: list[IntentSpec] = [
    IntentSpec(
        "greeting",
        patterns=[r"^\s*(hi|hello|hey|hola|namaste|good (morning|afternoon|evening))\b"],
        keywords=["hi", "hello", "hey", "hola", "namaste"],
    ),
    IntentSpec(
        "goodbye",
        patterns=[r"\b(bye|goodbye|see ya|see you|cya|take care)\b"],
        keywords=["bye", "goodbye"],
    ),
    IntentSpec(
        "thanks",
        patterns=[r"^\s*(thanks|thank you|thx|ty|appreciate it)\b"],
        keywords=["thanks", "thank"],
    ),
    IntentSpec(
        "check_balance",
        patterns=[
            r"\b(what'?s|show|check|see|view|tell\s+me)\s+(my\s+)?(account\s+)?balance\b",
            r"\bhow\s+much\s+(money|do\s+i\s+have|is\s+in\s+my\s+account)\b",
            r"\b(account|bank)\s+balance\b",
            r"\bmy\s+balance\b",
        ],
        keywords=["balance", "how much money"],
    ),
    IntentSpec(
        "view_accounts",
        patterns=[
            r"\b(show|view|list|all)\s+(my\s+)?accounts\b",
            r"\bmy\s+accounts\b",
        ],
        keywords=["my accounts", "list accounts"],
    ),
    IntentSpec(
        "recent_transactions",
        patterns=[
            r"\b(recent|last|latest|view|show|see)\s+(my\s+)?transactions?\b",
            r"\btransaction\s+history\b",
            r"\bwhere\s+did\s+(my\s+)?money\s+go\b",
            r"\bspend(ing)?\s+(history|report)\b",
            r"\b(my|recent)\s+spending\b",
            r"\bstatement\b",
        ],
        keywords=["transactions", "spending history", "statement"],
    ),
    IntentSpec(
        "transfer_money",
        patterns=[
            r"\b(transfer|send|pay)\s+(money|rs|inr|₹|\d+)\s+(to|via)\b",
            r"\b(transfer|send)\s+\d+\s+(rs|inr|rupees)?\s+to\b",
            r"\bmove\s+money\s+(to|from)\b",
            r"\b(upi|neft|imps|rtgs)\s+(transfer|payment|send)\b",
        ],
        keywords=["transfer money", "send money", "neft", "imps", "rtgs", "upi"],
    ),
    IntentSpec(
        "cards_view",
        patterns=[
            r"\b(show|view|list|my)\s+(credit\s+|debit\s+)?cards?\b",
            r"\bcredit\s+card\s+(balance|due|statement)\b",
            r"\bcard\s+(dues?|payment|outstanding)\b",
        ],
        keywords=["my cards", "credit card", "debit card"],
    ),
    IntentSpec(
        "card_apply",
        patterns=[
            r"\b(apply|get|need|recommend)\s+(for\s+)?(a\s+)?(new\s+)?(credit|debit)?\s*card\b",
            r"\bwhich\s+credit\s+card\s+(should|is\s+best)\b",
            r"\bbest\s+credit\s+card\s+for\b",
        ],
        keywords=["apply card", "new credit card", "best credit card"],
    ),
    IntentSpec(
        "loan_apply",
        patterns=[
            r"\b(apply|get|need|take)\s+(a\s+)?(home|personal|auto|car|education|business)?\s*loan\b",
            r"\bloan\s+(rates|interest|emi)\b",
            r"\bemi\s+calculator\b",
            r"\b(what'?s|tell\s+me)\s+(the\s+)?(home|personal|auto|car|education)\s+loan\s+rate\b",
        ],
        keywords=["loan", "home loan", "personal loan", "emi"],
    ),
    IntentSpec(
        "loans_view",
        patterns=[
            r"\b(my|view|show|current)\s+loans?\b",
            r"\bloan\s+(status|balance|outstanding)\b",
            r"\b(active|existing|current)\s+(my\s+)?loans?\b",
        ],
        keywords=["my loans", "loan status"],
    ),
    IntentSpec(
        "investments_view",
        patterns=[
            r"\b(my|view|show)\s+(investments?|portfolio|holdings|stocks?|mutual\s+funds?)\b",
            r"\bportfolio\s+(value|performance)\b",
            r"\bhow\s+(are|is)\s+(my\s+)?(investments?|stocks?|portfolio)\s+(doing|performing)\b",
        ],
        keywords=["my investments", "portfolio", "my holdings", "my stocks"],
    ),
    IntentSpec(
        "market_data",
        patterns=[
            r"\b(market|stock|index|nifty|sensex|bridica)\s+(today|now|update|status|movers)\b",
            r"\b(today'?s|current)\s+market\b",
            r"\bstock\s+(price|quote)\b",
            r"\bhow\s+is\s+the\s+market\b",
        ],
        keywords=["market", "stock price", "market today"],
    ),
    IntentSpec(
        "budget_view",
        patterns=[
            r"\b(my|view|show|current)\s+budget\b",
            r"\b(monthly|month'?s)\s+(spending|budget|expenses)\b",
            r"\bbudget\s+(status|tracker|report)\b",
            r"\bhow\s+(much\s+)?am\s+i\s+spending\b",
        ],
        keywords=["budget", "monthly spending", "expenses"],
    ),
    IntentSpec(
        "deposit_apply",
        patterns=[
            r"\b(open|start|create)\s+(a\s+)?(fixed\s+deposit|fd|recurring\s+deposit|rd)\b",
            r"\b(fd|fixed\s+deposit|rd|recurring\s+deposit)\s+(rates?|interest)\b",
            r"\binvest\s+in\s+(fd|fixed\s+deposit|rd)\b",
        ],
        keywords=["fixed deposit", "fd", "recurring deposit", "rd"],
    ),
    IntentSpec(
        "credit_score",
        patterns=[
            r"\b(my|check|view|show)\s+(credit\s+score|cibil)\b",
            r"\b(credit\s+score|cibil)\b",
            r"\bhow'?s\s+my\s+credit\b",
        ],
        keywords=["credit score", "cibil"],
    ),
    IntentSpec(
        "investment_advice",
        patterns=[
            r"\bshould\s+i\s+(invest|buy|sell)\b",
            r"\bwhat\s+(should\s+i|to)\s+(invest|buy|sell)\b",
            r"\b(investment|stock)\s+(advice|recommendation|tip|suggestion)\b",
            r"\bwhich\s+(stock|fund|mutual\s+fund)\s+(should|is\s+best)\b",
        ],
        keywords=["investment advice", "stock recommendation", "should i buy"],
    ),
    IntentSpec(
        "talk_to_human",
        patterns=[
            r"\b(speak|talk|connect)\s+to\s+(a\s+)?(human|agent|person|representative|advisor)\b",
            r"\b(real|live)\s+(person|agent|advisor)\b",
            r"\bcustomer\s+(care|support|service)\b",
        ],
        keywords=["human", "agent", "customer care"],
    ),
]


# ─── Entity extraction ─────────────────────────────────────
LOAN_TYPES = {
    "home":      ["home loan", "housing loan", "mortgage"],
    "personal":  ["personal loan"],
    "auto":      ["auto loan", "car loan", "vehicle loan"],
    "education": ["education loan", "student loan", "study loan"],
    "business":  ["business loan"],
}

CARD_CATEGORIES = {
    "travel":   ["travel", "miles", "flight", "hotel"],
    "cashback": ["cashback", "cash back"],
    "premium":  ["premium", "platinum", "elite"],
    "student":  ["student"],
}

INVESTMENT_TERMS = {
    "stocks":      ["stock", "stocks", "equity", "shares"],
    "mutual_fund": ["mutual fund", "mf", "sip"],
    "etf":         ["etf"],
    "gold":        ["gold"],
    "fd":          ["fd", "fixed deposit"],
}

AMOUNT_RE = re.compile(r"(?:₹|rs\.?|inr)?\s*([0-9]+(?:[,.][0-9]+)*)\s*(crore|cr|lakh|l|k|thousand)?", re.IGNORECASE)


def extract_loan_type(text: str) -> Optional[str]:
    t = text.lower()
    for key, words in LOAN_TYPES.items():
        if any(w in t for w in words):
            return key
    return None


def extract_card_category(text: str) -> Optional[str]:
    t = text.lower()
    for key, words in CARD_CATEGORIES.items():
        if any(w in t for w in words):
            return key
    return None


def extract_investment_type(text: str) -> Optional[str]:
    t = text.lower()
    for key, words in INVESTMENT_TERMS.items():
        if any(w in t for w in words):
            return key
    return None


def extract_amount(text: str) -> Optional[float]:
    """Pull a rupee amount from text. Handles 'lakh', 'crore', 'k'."""
    m = AMOUNT_RE.search(text)
    if not m:
        return None
    try:
        raw = float(m.group(1).replace(",", ""))
        suffix = (m.group(2) or "").lower()
        if suffix in ("crore", "cr"):
            return raw * 10_000_000
        if suffix in ("lakh", "l"):
            return raw * 100_000
        if suffix in ("k", "thousand"):
            return raw * 1_000
        return raw
    except ValueError:
        return None


# ─── Classifier ────────────────────────────────────────────
@dataclass
class Classification:
    intent: str
    confidence: float
    entities: dict


def classify(text: str) -> Classification:
    raw = text
    text_lc = text.lower().strip()

    scores: dict[str, float] = {}
    for spec in INTENTS:
        score = 0.0
        for p in spec.patterns:
            if re.search(p, text_lc, re.IGNORECASE):
                score += 2.0
        for kw in spec.keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text_lc):
                score += 0.6
        if score > 0:
            scores[spec.name] = score

    if not scores:
        intent, conf = "unknown", 0.0
    else:
        intent = max(scores, key=scores.get)
        top = scores[intent]
        rest = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0.1
        conf = min(1.0, top / (top + rest))

    entities = {
        "loan_type":       extract_loan_type(raw),
        "card_category":   extract_card_category(raw),
        "investment_type": extract_investment_type(raw),
        "amount":          extract_amount(raw),
    }
    return Classification(intent=intent, confidence=round(conf, 2), entities=entities)
