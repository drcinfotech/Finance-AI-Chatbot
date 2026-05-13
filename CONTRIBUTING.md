# Contributing to Atlas

Thanks for your interest in contributing! This project is a demo of conversational AI for the financial-services domain, so contributions are welcome — but **safety-critical code paths have extra rules** that apply on top of the usual code-review.

## Code of conduct

Be kind. Disagree on technical merits, not on people. Maintainers reserve the right to close issues and PRs that violate this.

## Quick start for contributors

```bash
git clone https://github.com/drcinfotech/Finance-AI-Chatbot.git
cd Finance-AI-Chatbot

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest -v       # must be 42/42 green before you start

# Frontend
cd ../frontend
npm install
npm run dev
```

## What we accept

✅ **Good contributions:**

- New intents with corresponding tests
- New block renderers in `Blocks.jsx` with corresponding Pydantic models
- New fraud-pattern detection (with both a positive test and a no-false-positive test)
- Documentation, README improvements, screenshots
- Accessibility improvements (keyboard nav, ARIA, contrast)
- i18n / localization support
- Tighter test coverage

❌ **What we do NOT accept:**

- Real bank, fintech, or financial-product trademarks anywhere in the codebase. The CI test `test_no_real_bank_brands_in_data` will fail your PR.
- Removing the SEBI-advisor disclaimer from investment-related handlers
- Making the bot execute actual money transfers (this is a demo)
- Weakening fraud detection without strong justification (false-negative is much worse than false-positive)
- Removing or relaxing prompt-injection / social-engineering blocks
- Adding personal API keys or credentials
- Code that calls real banking, payment, or market-data APIs without explicit opt-in and clear documentation of risks

## Safety-rule changes (require extra review)

Any PR that modifies the following files **must** include test coverage and a written rationale in the PR description:

- `backend/app/safety.py` — fraud and social-engineering detection
- `backend/app/chatbot.py` — disclaimer injection logic
- `backend/data/*.json` — particularly anything that resembles a real brand

The maintainers will request changes to any safety-weakening PR unless the justification is strong.

## Style

- Python: PEP 8, type hints on public functions, docstrings on modules
- JS/JSX: 2-space indent, no semicolons-after-JSX, prefer functional components
- Commits: imperative present tense ("Add X", "Fix Y"), not past tense
- One logical change per PR

## Reporting a security issue

For anything that looks like a real security issue (not just a demo limitation), please email the maintainers privately rather than opening a public issue. Real exploits in this demo are unlikely (no auth, no real money) but please err on the side of private disclosure.

## Reporting fraud (real-world)

If you came here because you've been a victim of financial fraud, this project cannot help you. Please call **1930** (India cybercrime helpline) or visit **cybercrime.gov.in** immediately.
