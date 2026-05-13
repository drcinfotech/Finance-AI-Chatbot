"""
Finance chatbot engine.

Flow:
  1. Safety check first — fraud & social-engineering attempts short-circuit
  2. Otherwise, classify intent
  3. Dispatch to handler
  4. Return rich blocks

The engine NEVER:
  • Moves money without explicit re-confirmation (and even then, this is a demo)
  • Gives buy/sell recommendations as personal advice
  • Shares OTPs, PINs, or passwords (it doesn't have them)
  • Acts on social-engineering attempts

The engine ALWAYS:
  • Surfaces a disclaimer for advisory-adjacent responses
  • Routes fraud signals to the cybercrime helpline
  • Encourages SEBI-registered advisors for investment decisions
"""
from __future__ import annotations

import secrets

from .catalog import catalog
from .intents import Classification, classify
from .safety import check_safety, build_fraud_alert_block, build_social_engineering_block
from .sessions import Session


# ─── Block builders ────────────────────────────────────────
def _text(content: str) -> dict:
    return {"type": "text", "content": content}


def _disclaimer(content: str) -> dict:
    return {"type": "disclaimer", "content": content}


# ─── Intent handlers ───────────────────────────────────────
def _handle_greeting(_s: Session):
    return [
        _text(
            "Hi, I'm Atlas — your financial companion. I can show you balances, "
            "transactions, budgets, market data, help you compare loans and cards, "
            "and answer general finance questions. How can I help today?"
        )
    ], ["Show my balance", "Recent transactions", "Today's market", "Compare credit cards"]


def _handle_goodbye(_s: Session):
    return [_text("Take care, and stay safe out there.")], []


def _handle_thanks(_s: Session):
    return [_text("You're welcome! Anything else I can help with?")], \
           ["Show my budget", "Loan options", "Investment portfolio"]


def _handle_check_balance(_c: Classification, _s: Session):
    accs = catalog.accounts()
    total = sum(a["balance"] for a in accs)
    blocks = [
        _text(f"Here are your account balances. **Total across accounts: ₹{total:,.2f}**"),
        {"type": "accounts", "items": accs},
    ]
    return blocks, ["Recent transactions", "Transfer money", "View my cards", "Open an FD"]


def _handle_view_accounts(c: Classification, s: Session):
    return _handle_check_balance(c, s)


def _handle_recent_transactions(_c: Classification, _s: Session):
    txns = catalog.recent_transactions(limit=8)
    spent = sum(-t["amount"] for t in txns if t["type"] == "debit")
    earned = sum(t["amount"] for t in txns if t["type"] == "credit")
    flagged = [t for t in txns if t["status"] == "flagged"]

    blocks = [
        _text(
            f"Here are your last 8 transactions — **spent ₹{spent:,.0f}, received ₹{earned:,.0f}**."
            + (f" I've flagged 1 suspicious transaction for you to review." if flagged else "")
        ),
        {"type": "transactions", "items": txns},
    ]
    if flagged:
        blocks.append(_disclaimer(
            f"The transaction from '{flagged[0]['merchant']}' was unusual for your spending pattern. "
            "If you don't recognize it, report it immediately via your banking app or call customer care."
        ))
    return blocks, ["Dispute a transaction", "Download statement", "View budget", "Talk to a human"]


def _handle_transfer_money(c: Classification, s: Session):
    amount = c.entities.get("amount")
    blocks = [
        _text(
            "I can help you set up a transfer, but in this demo I won't actually move money. "
            "Here's what a UPI/IMPS transfer flow looks like:"
        ),
        {
            "type": "transfer",
            "confirmation": {
                "transfer_id":      "TXN-" + secrets.token_hex(4).upper(),
                "from_account":     "•••• 9914 (Salary)",
                "to_account_masked":"•••• 2247",
                "to_name":          "Aanya Verma",
                "amount":           amount or 5000,
                "mode":             "IMPS",
                "fee":              0,
                "eta":              "Instant",
                "status":           "Demo — not executed",
            },
        },
        _disclaimer(
            "Real transfers always require an OTP or PIN confirmation, plus a beneficiary cooling period for new payees. "
            "Never share your OTP, PIN, or password with anyone — including me."
        ),
    ]
    return blocks, ["Add a beneficiary", "View transfer limits", "Recent transfers", "Cancel"]


def _handle_cards_view(_c: Classification, _s: Session):
    cards = catalog.cards()
    credit = [c for c in cards if c["type"] == "credit"]
    total_due = sum(c.get("current_balance", 0) for c in credit)
    blocks = [
        _text(f"Here are your cards. **Credit card outstanding: ₹{total_due:,.0f}**"),
        {"type": "cards", "items": cards},
    ]
    return blocks, ["Pay credit card bill", "Apply for a new card", "Increase card limit", "Block a card"]


def _handle_card_apply(c: Classification, _s: Session):
    cat = c.entities.get("card_category")
    products = catalog.credit_card_products(category=cat, limit=3)
    if not products:
        products = catalog.credit_card_products(limit=3)

    intro = (
        f"Here are top {cat} cards based on your profile:"
        if cat else
        "Here are popular credit cards. Tell me what matters most — travel, cashback, premium perks, or a starter card:"
    )
    blocks = [
        _text(intro),
        {"type": "credit_card_products", "items": products},
        _disclaimer(
            "Approval depends on your credit score, income, and existing relationship with the bank. "
            "Pre-approval is indicative only."
        ),
    ]
    return blocks, ["Travel cards", "Cashback cards", "Best for students", "How is the annual fee waived?"]


def _handle_loan_apply(c: Classification, _s: Session):
    loan_type = c.entities.get("loan_type")
    products = catalog.loan_products(loan_type=loan_type, limit=4)
    intro = (
        f"Here are {loan_type} loan options with current indicative rates:"
        if loan_type else
        "Here are our main loan products with indicative rates:"
    )
    blocks = [
        _text(intro),
        {"type": "loan_products", "items": products},
        _disclaimer(
            "Rates shown are indicative starting rates for top-tier credit profiles. "
            "Your actual rate depends on credit score, income, employment, and tenure. EMI calculators are illustrative only."
        ),
    ]
    return blocks, ["EMI calculator", "Eligibility check", "Required documents", "Talk to a loan officer"]


def _handle_loans_view(_c: Classification, _s: Session):
    loans = catalog.loans()
    total_out = sum(l["outstanding"] for l in loans)
    total_emi = sum(l["emi"] for l in loans)
    blocks = [
        _text(
            f"Here are your active loans. **Total outstanding: ₹{total_out:,.0f}**, "
            f"**combined monthly EMI: ₹{total_emi:,.0f}**."
        ),
        {"type": "loans", "items": loans},
    ]
    return blocks, ["Prepay home loan", "Foreclose personal loan", "EMI schedule", "Talk to a loan officer"]


def _handle_investments_view(_c: Classification, _s: Session):
    inv = catalog.investments()
    total_invested = sum(i["shares"] * i["avg_buy"] for i in inv)
    total_current = sum(i["shares"] * i["current"] for i in inv)
    pct = (total_current - total_invested) / total_invested * 100 if total_invested else 0
    direction = "up" if pct >= 0 else "down"
    blocks = [
        _text(
            f"Your portfolio is **{direction} {abs(pct):.2f}%** overall — "
            f"invested ₹{total_invested:,.0f}, now worth **₹{total_current:,.0f}**."
        ),
        {
            "type": "investments",
            "items": inv,
            "total_invested": total_invested,
            "total_current":  total_current,
        },
        _disclaimer(
            "Holdings shown are demo data. Investments carry market risk — past performance doesn't guarantee future returns. "
            "For personalized advice, consult a SEBI-registered investment advisor."
        ),
    ]
    return blocks, ["Add to portfolio", "Rebalance suggestions", "Today's market", "Tax implications"]


def _handle_market_data(_c: Classification, _s: Session):
    snap = catalog.market_snapshot()
    top_idx = snap["indices"][0]
    direction = "up" if top_idx["change_pct"] >= 0 else "down"
    blocks = [
        _text(
            f"Markets are **{direction} {abs(top_idx['change_pct']):.2f}%** on {top_idx['name']}. "
            "Here's a snapshot:"
        ),
        {
            "type": "market",
            "indices": snap["indices"],
            "stocks":  snap["stocks"],
        },
        _disclaimer(
            "Market data shown is illustrative demo data. For live, accurate market data, use your broker's platform or an "
            "official exchange website."
        ),
    ]
    return blocks, ["Top gainers", "Top losers", "My watchlist", "Sector overview"]


def _handle_budget_view(_c: Classification, _s: Session):
    budgets = catalog.budgets()
    spent = sum(b["spent"] for b in budgets)
    limit = sum(b["limit"] for b in budgets)
    pct = spent / limit * 100 if limit else 0
    blocks = [
        _text(
            f"You've spent **₹{spent:,.0f} of your ₹{limit:,.0f}** budget this month — "
            f"that's **{pct:.1f}%**. Here's the breakdown by category:"
        ),
        {
            "type": "budget",
            "month_label": "December 2025",
            "items": budgets,
            "total_spent": spent,
            "total_limit": limit,
        },
    ]
    return blocks, ["Top spending categories", "Set a new budget", "Saving tips", "Compare to last month"]


def _handle_deposit_apply(_c: Classification, _s: Session):
    products = catalog.deposit_products(limit=4)
    blocks = [
        _text("Here are our current Fixed Deposit and Recurring Deposit options. Rates are subject to change:"),
        {"type": "deposit_products", "items": products},
        _disclaimer(
            "Senior citizens get an additional 0.5% on most schemes. Premature withdrawals attract a penalty. "
            "Tax may apply on interest earned per current Income Tax rules."
        ),
    ]
    return blocks, ["Open standard FD", "Tax saver FD details", "Senior citizen rates", "RD calculator"]


def _handle_credit_score(_c: Classification, _s: Session):
    blocks = [
        _text("Here's your current credit score, refreshed monthly:"),
        {
            "type": "credit_score",
            "score_info": {
                "score": 782,
                "band":  "Excellent",
                "last_updated": "Updated Dec 1, 2025",
                "factors": [
                    {"label": "On-time payments (24 months)",          "impact": "positive"},
                    {"label": "Low credit utilization (16%)",          "impact": "positive"},
                    {"label": "Long credit history (8 years)",         "impact": "positive"},
                    {"label": "Recent hard inquiry (auto loan, Sep)",  "impact": "negative"},
                ],
            },
        },
        _disclaimer(
            "Credit scores are computed by independent bureaus (CIBIL, Experian, Equifax, CRIF). "
            "Different lenders may use different bureaus and weightings."
        ),
    ]
    return blocks, ["How to improve my score", "Hard vs soft inquiry", "Dispute an entry", "Get full report"]


def _handle_investment_advice(_c: Classification, _s: Session):
    blocks = [
        _text(
            "I can share educational information on different investment options, but I'm not "
            "qualified to give you personal investment recommendations. The right choice depends "
            "on your goals, risk appetite, and timeline."
        ),
        _disclaimer(
            "By law, only SEBI-registered investment advisors can give personalized investment advice in India. "
            "Anything I say is educational and not a recommendation to buy or sell. Past performance doesn't "
            "predict future returns. All investments carry risk."
        ),
        _text(
            "If you want, I can:\n"
            "• Show you **how different products work** (FDs, mutual funds, stocks, ETFs)\n"
            "• Explain **risk vs return** for each\n"
            "• Help you **find a SEBI-registered advisor**\n"
            "• Walk through **tax implications**"
        ),
    ]
    return blocks, ["Explain mutual funds", "Risk vs return basics", "Find SEBI advisor", "Tax on investments"]


def _handle_talk_to_human(_c: Classification, _s: Session):
    return [_text(
        "Sure — I can connect you to a banking representative. Typical wait is 4 minutes. "
        "For investment guidance, I can route you to a SEBI-registered advisor instead. Which would you prefer?"
    )], ["Banking representative", "Investment advisor", "Loan officer", "Fraud team"]


def _handle_unknown(_c: Classification, _s: Session):
    blocks = [_text(
        "I'm not sure I caught that. I'm best at helping with balances, transactions, transfers, "
        "credit cards, loans, investments, market data, and budgets. Could you rephrase, or pick from below?"
    )]
    return blocks, ["Check balance", "Recent transactions", "Compare credit cards", "Talk to a human"]


# ─── Engine ────────────────────────────────────────────────
class ChatbotEngine:
    def respond(self, message: str, session: Session) -> dict:
        # 1️⃣ Safety check first
        safety = check_safety(message)
        if safety.flag == "fraud":
            return {
                "session_id": session.session_id,
                "intent": "fraud_alert",
                "confidence": 1.0,
                "blocks": [build_fraud_alert_block(safety.reason)],
                "suggestions": ["Report at cybercrime.gov.in", "Call 1930 now", "How to spot fraud"],
                "safety_flag": "fraud",
            }
        if safety.flag == "social_engineering":
            return {
                "session_id": session.session_id,
                "intent": "social_engineering_blocked",
                "confidence": 1.0,
                "blocks": [build_social_engineering_block()],
                "suggestions": ["Check my balance", "View transactions", "Compare credit cards"],
                "safety_flag": "social_engineering",
            }

        # 2️⃣ Classify intent
        c = classify(message)
        session.last_intent = c.intent
        session.history.append({"role": "user", "text": message})

        handler_map = {
            "greeting":             lambda: _handle_greeting(session),
            "goodbye":              lambda: _handle_goodbye(session),
            "thanks":               lambda: _handle_thanks(session),
            "check_balance":        lambda: _handle_check_balance(c, session),
            "view_accounts":        lambda: _handle_view_accounts(c, session),
            "recent_transactions":  lambda: _handle_recent_transactions(c, session),
            "transfer_money":       lambda: _handle_transfer_money(c, session),
            "cards_view":           lambda: _handle_cards_view(c, session),
            "card_apply":           lambda: _handle_card_apply(c, session),
            "loan_apply":           lambda: _handle_loan_apply(c, session),
            "loans_view":           lambda: _handle_loans_view(c, session),
            "investments_view":     lambda: _handle_investments_view(c, session),
            "market_data":          lambda: _handle_market_data(c, session),
            "budget_view":          lambda: _handle_budget_view(c, session),
            "deposit_apply":        lambda: _handle_deposit_apply(c, session),
            "credit_score":         lambda: _handle_credit_score(c, session),
            "investment_advice":    lambda: _handle_investment_advice(c, session),
            "talk_to_human":        lambda: _handle_talk_to_human(c, session),
        }
        handler = handler_map.get(c.intent, lambda: _handle_unknown(c, session))
        blocks, suggestions = handler()

        bot_text = " | ".join(b.get("content", "") for b in blocks if b.get("type") == "text")
        session.history.append({"role": "bot", "text": bot_text})

        return {
            "session_id":   session.session_id,
            "intent":       c.intent,
            "confidence":   c.confidence,
            "blocks":       blocks,
            "suggestions":  suggestions,
            "safety_flag":  None,
        }


engine = ChatbotEngine()
