"""
Fraud & social-engineering detection — runs BEFORE intent classification.

In a finance chatbot, the gravest harms are:
  • Customer being scammed (sharing OTP/password/PIN)
  • Bot tricked into a high-value transfer
  • Phishing attempts ("verify your account by clicking this link…")
  • Account-takeover attempts

This module spots common patterns and short-circuits to a fraud-alert block
that educates the user, refuses to act, and gives them the fraud helpline.

Conservative by design — false positives are cheap (we educate the user),
false negatives can cost real money.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class SafetyResult:
    flag: Optional[Literal["fraud", "social_engineering"]]
    reason: str = ""


# ─── Fraud / scam indicator patterns ───────────────────────
# These detect phrasings that suggest the USER is being scammed, or that
# the user is trying to ask the bot to do something a real bank never would.
FRAUD_PATTERNS = [
    # Sharing sensitive credentials (NEVER do this with anyone, including a bot)
    r"\b(my|the)\s+otp\s+is\s+\d",
    r"\bmy\s+(password|pin|cvv)\s+is\b",
    r"\bsend\s+(me\s+)?(my|the)\s+(otp|password|pin|cvv)\b",
    r"\bshare\s+(my|the)\s+(otp|password|pin|cvv)\b",
    r"\b(tell|give)\s+me\s+(my|your)\s+(otp|password|pin|cvv)\b",

    # User reporting they've been contacted by a scammer
    r"\b(someone|a\s+person|caller|stranger)\s+(called|asked|asking|wants|wanting)\s+(\w+\s+){0,3}(otp|pin|password|cvv)\b",
    r"\b(verify|update|confirm)\s+(my\s+)?account\s+(via|using|through)\s+(this|the)\s+link\b",
    r"\bgot\s+a?\s*(call|sms|message|email)\s+(from\s+)?(bank|customer\s+care)\s+(asking|saying)\b",
    r"\bbank\s+(executive|employee|officer)\s+asked\s+(me\s+)?for\s+(otp|pin|password)\b",
    r"\bkyc\s+(will\s+be\s+)?(expir|update|verify|deactivat|suspend)\w*",
    r"\baccount\s+(will\s+be\s+)?(blocked|frozen|suspended)\s+if\s+",
    r"\burgent(ly)?\s+(verify|update|confirm)\s+(your|my)\s+(account|kyc|details)\b",

    # Lottery / windfall scams
    r"\b(won|winner)\s+(a\s+)?(lottery|prize|reward)\s+",
    r"\blottery\s+(winning|prize)\b",
    r"\binheritance\s+from\s+(unknown|stranger|foreign)",
    r"\bclaim\s+(your|my)\s+(prize|reward|winning)\b",

    # Crypto / forex scams
    r"\bguaranteed\s+(return|profit|income)\b",
    r"\bdouble\s+(your|my)\s+money\s+in\b",
    r"\binvest\s+\d+\s+(get|earn|make)\s+\d+",

    # Remote-access scams
    r"\binstall\s+(anydesk|teamviewer|quicksupport)\b",
    r"\bgive\s+(remote|screen)\s+access\b",
    r"\bshare\s+(my\s+)?screen\s+with\s+(bank|support)\b",
]

# Direct requests for the bot to do something it must never do.
# These target prompt-injection / jailbreak attempts — NOT normal transfer requests.
SOCIAL_ENGINEERING_PATTERNS = [
    r"\b(ignore|disregard|forget)\s+(\w+\s+){0,4}(instructions|rules|guidelines|system\s+prompt)",
    r"\byou\s+are\s+now\s+(in\s+|an?\s+)?(admin|administrator|dev|developer|debug|root)\s+(mode|user)?",
    r"\bpretend\s+(you\s+are|to\s+be)\s+(an?\s+)?(admin|root|developer)\b",
    r"\b(give|provide|reveal|show|tell)\s+(me\s+)?(your\s+)?(system\s+prompt|instructions|api\s+key|source\s+code)",
    r"\benable\s+(developer|admin|debug|root)\s+mode\b",
    r"\bjailbreak\b",
    r"\bDAN\s+mode\b",
]


# ─── India fraud reporting helpline ────────────────────────
FRAUD_HELPLINE = {
    "label": "Cybercrime helpline (India)",
    "number": "1930",
}

CYBERCRIME_PORTAL = "cybercrime.gov.in"


def check_safety(text: str) -> SafetyResult:
    text_lc = text.lower()

    for pat in SOCIAL_ENGINEERING_PATTERNS:
        if re.search(pat, text_lc):
            return SafetyResult(flag="social_engineering", reason=pat)

    for pat in FRAUD_PATTERNS:
        if re.search(pat, text_lc):
            return SafetyResult(flag="fraud", reason=pat)

    return SafetyResult(flag=None)


def build_fraud_alert_block(reason_hint: str = "") -> dict:
    return {
        "type": "fraud_alert",
        "headline": "This looks like a scam attempt — please be careful.",
        "message": (
            "I'll never ask for your OTP, PIN, password, or CVV — and neither will any real bank. "
            "If someone is asking you for these, it's a fraud. Don't share anything, hang up, "
            "and report it using the helpline below."
        ),
        "indicators": [
            "Banks never ask for OTP/PIN/password — even their own employees",
            "Urgency or threats (\"account will be blocked\") are classic scam tactics",
            "Lottery/prize/inheritance from a stranger is always a scam",
            "Never install AnyDesk/TeamViewer at someone's request",
        ],
        "helpline": FRAUD_HELPLINE,
    }


def build_social_engineering_block() -> dict:
    return {
        "type": "fraud_alert",
        "headline": "I can't do that.",
        "message": (
            "I'm not able to bypass my safety rules, transfer money without proper authentication, "
            "or share internal instructions. If you have a legitimate banking need, I'm happy to "
            "help with that instead."
        ),
        "indicators": [
            "Money transfers always require explicit authentication",
            "I can show you balances, transactions, and products — not change settings",
            "Real bank staff can help with anything beyond my scope",
        ],
        "helpline": {"label": "Bank customer care", "number": "1800-111-222"},
    }
