import {
  AlertTriangle, Phone, Wallet, CreditCard, TrendingUp, TrendingDown,
  ArrowUpRight, ArrowDownRight, Info, Shield, Building2, ChevronRight,
  Banknote, LineChart, Receipt, PieChart, Sparkles, Target, BadgeCheck,
  AlertCircle, Star, Award, Briefcase,
} from "lucide-react";

const ACCENT = "#FFD787";

const fmt = (n) => "₹" + Math.abs(Number(n)).toLocaleString("en-IN", { maximumFractionDigits: 2 });
const fmt0 = (n) => "₹" + Math.abs(Number(n)).toLocaleString("en-IN", { maximumFractionDigits: 0 });
const fmtSigned = (n) => (n >= 0 ? "+" : "−") + fmt(Math.abs(n));

/* ─── TextBlock ────────────────────────────────────────── */
export function TextBlock({ content }) {
  const parts = content.split(/(\*\*[^*]+\*\*)/g);
  return (
    <div
      className="text-sm leading-relaxed px-4 py-2.5 rounded-2xl rounded-tl-md"
      style={{ background: "rgba(255,255,255,0.03)", color: "rgba(255,255,255,0.88)" }}
    >
      {parts.map((p, i) =>
        p.startsWith("**") && p.endsWith("**") ? (
          <strong key={i} className="text-white font-medium">{p.slice(2, -2)}</strong>
        ) : (
          <span key={i}>{p.split("\n").map((line, j, arr) => (
            <span key={j}>{line}{j < arr.length - 1 && <br />}</span>
          ))}</span>
        )
      )}
    </div>
  );
}

/* ─── DisclaimerBlock ──────────────────────────────────── */
export function DisclaimerBlock({ content }) {
  return (
    <div
      className="flex items-start gap-2.5 px-4 py-2.5 rounded-2xl border"
      style={{ background: "rgba(250, 204, 21, 0.04)", borderColor: "rgba(250, 204, 21, 0.18)", color: "rgba(250, 204, 21, 0.85)" }}
    >
      <Info size={14} className="mt-0.5 flex-shrink-0" />
      <div className="text-11 leading-relaxed">{content}</div>
    </div>
  );
}

/* ─── FraudAlertBlock ──────────────────────────────────── */
export function FraudAlertBlock({ headline, message, indicators, helpline }) {
  return (
    <div
      className="rounded-2xl border-2 p-4 fraud-pulse"
      style={{
        background: "linear-gradient(180deg, rgba(248,113,113,0.10), rgba(248,113,113,0.02))",
        borderColor: "rgba(248,113,113,0.4)",
      }}
    >
      <div className="flex items-center gap-2 mb-2">
        <Shield size={18} style={{ color: "#fca5a5" }} />
        <div className="text-sm font-semibold" style={{ color: "#fca5a5" }}>{headline}</div>
      </div>
      <div className="text-xs leading-relaxed mb-3" style={{ color: "rgba(255,255,255,0.85)" }}>{message}</div>
      <div className="space-y-1 mb-3">
        {indicators.map((it, i) => (
          <div key={i} className="flex items-start gap-2 text-11" style={{ color: "rgba(255,255,255,0.7)" }}>
            <AlertCircle size={10} style={{ color: "#fca5a5", marginTop: 3, flexShrink: 0 }} />
            <span>{it}</span>
          </div>
        ))}
      </div>
      <a
        href={`tel:${helpline.number.replace(/[^+0-9]/g, "")}`}
        className="flex items-center justify-between px-3 py-2 rounded-lg border transition hover:bg-white/5"
        style={{ background: "rgba(255,255,255,0.04)", borderColor: "rgba(248,113,113,0.25)" }}
      >
        <div className="flex items-center gap-2">
          <Phone size={12} style={{ color: "#fca5a5" }} />
          <span className="text-xs" style={{ color: "rgba(255,255,255,0.85)" }}>{helpline.label}</span>
        </div>
        <span className="text-xs font-mono font-medium" style={{ color: "#fca5a5" }}>{helpline.number}</span>
      </a>
    </div>
  );
}

/* ─── AccountsBlock ────────────────────────────────────── */
export function AccountsBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (
        <div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>
      )}
      <div className="space-y-2">
        {items.map((a) => (
          <div key={a.id} className="rounded-xl p-3 border"
            style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
            <div className="flex items-start gap-3">
              <div className="rounded-lg flex items-center justify-center flex-shrink-0"
                style={{ width: 44, height: 44, background: ACCENT + "14" }}>
                <Wallet size={18} style={{ color: ACCENT }} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <div>
                    <div className="text-sm font-medium" style={{ color: "rgba(255,255,255,0.92)" }}>{a.label}</div>
                    <div className="text-11 font-mono" style={{ color: "rgba(255,255,255,0.5)" }}>
                      {a.number_masked} · {a.type}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-base font-medium font-mono" style={{ color: "white" }}>{fmt(a.balance)}</div>
                    <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Available</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── CardsBlock ───────────────────────────────────────── */
export function CardsBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (
        <div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>
      )}
      <div className="space-y-2">
        {items.map((c) => (
          <div key={c.id} className="rounded-xl p-3 border"
            style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
            <div className="flex items-start gap-3">
              <div className="rounded-lg flex items-center justify-center flex-shrink-0"
                style={{ width: 44, height: 44, background: ACCENT + "14" }}>
                <CreditCard size={18} style={{ color: ACCENT }} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <div className="text-sm font-medium" style={{ color: "rgba(255,255,255,0.92)" }}>{c.label}</div>
                  <span className="text-9 px-1.5 py-0.5 rounded-full font-medium uppercase"
                    style={{ background: c.type === "credit" ? ACCENT + "22" : "rgba(96,165,250,0.15)", color: c.type === "credit" ? ACCENT : "#93c5fd" }}>
                    {c.type}
                  </span>
                </div>
                <div className="text-11 font-mono mb-2" style={{ color: "rgba(255,255,255,0.5)" }}>{c.number_masked}</div>
                {c.type === "credit" ? (
                  <>
                    <div className="grid grid-cols-3 gap-2 text-10 mb-2">
                      <div>
                        <div style={{ color: "rgba(255,255,255,0.4)" }}>Limit</div>
                        <div className="font-mono" style={{ color: "rgba(255,255,255,0.85)" }}>{fmt0(c.limit)}</div>
                      </div>
                      <div>
                        <div style={{ color: "rgba(255,255,255,0.4)" }}>Outstanding</div>
                        <div className="font-mono" style={{ color: "rgba(255,255,255,0.85)" }}>{fmt0(c.current_balance)}</div>
                      </div>
                      <div>
                        <div style={{ color: "rgba(255,255,255,0.4)" }}>Available</div>
                        <div className="font-mono" style={{ color: ACCENT }}>{fmt0(c.available)}</div>
                      </div>
                    </div>
                    <div className="flex items-center justify-between pt-2 border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
                      <div className="text-10" style={{ color: "rgba(255,255,255,0.6)" }}>
                        Due: <span style={{ color: "white" }}>{c.due_date}</span> · Min: <span className="font-mono" style={{ color: "white" }}>{fmt0(c.min_due)}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Award size={9} style={{ color: ACCENT }} />
                        <span className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.7)" }}>
                          {c.rewards_points?.toLocaleString("en-IN")} pts
                        </span>
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="text-10" style={{ color: "rgba(255,255,255,0.6)" }}>
                    Daily limit: <span className="font-mono" style={{ color: "white" }}>{fmt0(c.daily_limit)}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── TransactionsBlock ────────────────────────────────── */
export function TransactionsBlock({ title, items }) {
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center gap-2 mb-3">
        <Receipt size={14} style={{ color: ACCENT }} />
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>
          {title || "Recent transactions"}
        </div>
      </div>
      <div className="space-y-0.5">
        {items.map((t) => {
          const flagged = t.status === "flagged";
          const isCredit = t.type === "credit";
          return (
            <div key={t.id} className="flex items-center justify-between px-3 py-2 rounded-md"
              style={{ background: flagged ? "rgba(248,113,113,0.06)" : "rgba(255,255,255,0.02)" }}>
              <div className="flex items-center gap-3 flex-1 min-w-0">
                <div className="rounded-full flex items-center justify-center flex-shrink-0"
                  style={{ width: 26, height: 26, background: isCredit ? "rgba(74,222,128,0.12)" : "rgba(255,255,255,0.05)" }}>
                  {isCredit ? <ArrowDownRight size={11} style={{ color: "#86efac" }} /> : <ArrowUpRight size={11} style={{ color: "rgba(255,255,255,0.6)" }} />}
                </div>
                <div className="min-w-0">
                  <div className="text-xs flex items-center gap-1.5" style={{ color: "rgba(255,255,255,0.9)" }}>
                    <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{t.merchant}</span>
                    {flagged && (
                      <span className="text-9 px-1 py-0.5 rounded-full font-medium" style={{ background: "rgba(248,113,113,0.18)", color: "#fca5a5" }}>FLAGGED</span>
                    )}
                  </div>
                  <div className="text-10" style={{ color: "rgba(255,255,255,0.4)" }}>{t.category} · {t.date}</div>
                </div>
              </div>
              <div className="text-sm font-mono font-medium" style={{ color: isCredit ? "#86efac" : "rgba(255,255,255,0.9)" }}>
                {isCredit ? "+" : "−"}{fmt0(t.amount)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─── LoansBlock ───────────────────────────────────────── */
export function LoansBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (<div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>)}
      {items.map((l) => {
        const paid_pct = ((l.principal - l.outstanding) / l.principal) * 100;
        return (
          <div key={l.id} className="rounded-xl p-3 border"
            style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
            <div className="flex items-center justify-between mb-2">
              <div>
                <div className="text-sm font-medium" style={{ color: "white" }}>{l.type}</div>
                <div className="text-10" style={{ color: "rgba(255,255,255,0.5)" }}>{l.lender} · {l.rate}% p.a.</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-mono" style={{ color: "white" }}>{fmt0(l.outstanding)}</div>
                <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Outstanding</div>
              </div>
            </div>
            <div className="h-1 rounded-full overflow-hidden mb-2" style={{ background: "rgba(255,255,255,0.06)" }}>
              <div style={{ width: `${paid_pct}%`, height: "100%", background: ACCENT, borderRadius: 999 }} />
            </div>
            <div className="flex items-center justify-between text-10" style={{ color: "rgba(255,255,255,0.55)" }}>
              <span>{paid_pct.toFixed(1)}% paid · {l.remaining_months} EMIs left</span>
              <span>Next EMI <span className="font-mono" style={{ color: "white" }}>{fmt0(l.emi)}</span> · {l.next_due}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* ─── InvestmentsBlock ─────────────────────────────────── */
export function InvestmentsBlock({ title, items, total_invested, total_current }) {
  const pct = ((total_current - total_invested) / total_invested) * 100;
  const up = pct >= 0;
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Briefcase size={14} style={{ color: ACCENT }} />
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>
            {title || "Your portfolio"}
          </div>
        </div>
        <div className="text-right">
          <div className="text-base font-mono font-medium" style={{ color: "white" }}>{fmt0(total_current)}</div>
          <div className="flex items-center justify-end gap-1 text-10 font-mono" style={{ color: up ? "#86efac" : "#fca5a5" }}>
            {up ? <TrendingUp size={9} /> : <TrendingDown size={9} />}
            {up ? "+" : ""}{(total_current - total_invested).toLocaleString("en-IN", { maximumFractionDigits: 0 })} ({pct.toFixed(2)}%)
          </div>
        </div>
      </div>
      <div className="space-y-1">
        {items.map((i) => {
          const value = i.shares * i.current;
          const invested = i.shares * i.avg_buy;
          const gain_pct = ((i.current - i.avg_buy) / i.avg_buy) * 100;
          const iup = gain_pct >= 0;
          return (
            <div key={i.id} className="flex items-center justify-between px-3 py-2 rounded-md"
              style={{ background: "rgba(255,255,255,0.02)" }}>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-medium" style={{ color: ACCENT }}>{i.symbol}</span>
                  <span className="text-xs" style={{ color: "rgba(255,255,255,0.85)" }}>{i.name}</span>
                </div>
                <div className="text-10" style={{ color: "rgba(255,255,255,0.45)" }}>
                  {i.shares} × {fmt(i.current)} · {i.category}
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs font-mono" style={{ color: "white" }}>{fmt0(value)}</div>
                <div className="text-10 font-mono" style={{ color: iup ? "#86efac" : "#fca5a5" }}>
                  {iup ? "+" : ""}{gain_pct.toFixed(2)}%
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─── MarketBlock ──────────────────────────────────────── */
export function MarketBlock({ title, indices, stocks }) {
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center gap-2 mb-3">
        <LineChart size={14} style={{ color: ACCENT }} />
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>
          {title || "Market snapshot"}
        </div>
      </div>
      <div className="grid grid-cols-3 gap-2 mb-3">
        {indices.map((idx) => {
          const up = idx.change_pct >= 0;
          return (
            <div key={idx.symbol} className="px-3 py-2 rounded-lg" style={{ background: "rgba(255,255,255,0.02)" }}>
              <div className="text-10 uppercase tracking-tightest2 mb-1" style={{ color: "rgba(255,255,255,0.45)" }}>{idx.name}</div>
              <div className="text-sm font-mono font-medium" style={{ color: "white" }}>{idx.value.toLocaleString("en-IN", { maximumFractionDigits: 2 })}</div>
              <div className="text-10 font-mono flex items-center gap-1" style={{ color: up ? "#86efac" : "#fca5a5" }}>
                {up ? <TrendingUp size={9} /> : <TrendingDown size={9} />}
                {up ? "+" : ""}{idx.change_pct.toFixed(2)}%
              </div>
            </div>
          );
        })}
      </div>
      <div className="space-y-0.5">
        {stocks.map((s) => {
          const up = s.change_pct >= 0;
          return (
            <div key={s.symbol} className="flex items-center justify-between px-3 py-1.5 rounded-md"
              style={{ background: "rgba(255,255,255,0.02)" }}>
              <div className="flex items-center gap-2 flex-1 min-w-0">
                <span className="text-xs font-mono font-medium" style={{ color: ACCENT, minWidth: 50 }}>{s.symbol}</span>
                <span className="text-xs" style={{ color: "rgba(255,255,255,0.8)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{s.name}</span>
                <span className="text-10" style={{ color: "rgba(255,255,255,0.4)" }}>{s.sector}</span>
              </div>
              <div className="flex items-center gap-3 flex-shrink-0">
                <span className="text-xs font-mono" style={{ color: "white" }}>{fmt(s.price)}</span>
                <span className="text-10 font-mono" style={{ color: up ? "#86efac" : "#fca5a5", minWidth: 50, textAlign: "right" }}>
                  {up ? "+" : ""}{s.change_pct.toFixed(2)}%
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─── BudgetBlock ──────────────────────────────────────── */
export function BudgetBlock({ month_label, items, total_spent, total_limit }) {
  const pct = (total_spent / total_limit) * 100;
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <PieChart size={14} style={{ color: ACCENT }} />
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>{month_label}</div>
        </div>
        <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.7)" }}>
          <span style={{ color: "white" }}>{fmt0(total_spent)}</span> / {fmt0(total_limit)} ({pct.toFixed(0)}%)
        </div>
      </div>
      <div className="space-y-2">
        {items.map((b, i) => {
          const p = (b.spent / b.limit) * 100;
          const over = p > 90;
          return (
            <div key={i}>
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span style={{ fontSize: 14 }}>{b.icon}</span>
                  <span className="text-xs" style={{ color: "rgba(255,255,255,0.85)" }}>{b.category}</span>
                </div>
                <span className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.6)" }}>
                  <span style={{ color: over ? "#fca5a5" : "white" }}>{fmt0(b.spent)}</span> / {fmt0(b.limit)}
                </span>
              </div>
              <div className="h-1 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.06)" }}>
                <div style={{
                  width: `${Math.min(100, p)}%`,
                  height: "100%",
                  background: over ? "#fca5a5" : (p > 70 ? "#fde047" : ACCENT),
                  borderRadius: 999,
                }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─── CreditCardProductsBlock ──────────────────────────── */
export function CreditCardProductsBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (<div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>)}
      {items.map((c) => (
        <div key={c.id} className="rounded-xl p-3 border"
          style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
          <div className="flex items-start gap-3">
            <div className="rounded-lg flex items-center justify-center flex-shrink-0"
              style={{ width: 44, height: 44, background: ACCENT + "14" }}>
              <CreditCard size={18} style={{ color: ACCENT }} />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2 mb-1">
                <div className="text-sm font-medium" style={{ color: "white" }}>{c.name}</div>
                <span className="text-9 px-1.5 py-0.5 rounded-full font-medium uppercase"
                  style={{ background: ACCENT + "22", color: ACCENT }}>{c.category}</span>
              </div>
              <div className="flex items-center gap-1.5 mb-2">
                <Sparkles size={10} style={{ color: ACCENT }} />
                <span className="text-11" style={{ color: "rgba(255,255,255,0.85)" }}>{c.highlight}</span>
              </div>
              <div className="text-11 mb-2" style={{ color: "rgba(255,255,255,0.55)" }}>{c.best_for}</div>
              <div className="grid grid-cols-2 gap-2 text-10 mb-2">
                <div>
                  <span style={{ color: "rgba(255,255,255,0.4)" }}>Annual fee: </span>
                  <span className="font-mono" style={{ color: "white" }}>{c.annual_fee === 0 ? "Free" : fmt0(c.annual_fee)}</span>
                </div>
                <div>
                  <span style={{ color: "rgba(255,255,255,0.4)" }}>Joining: </span>
                  <span className="font-mono" style={{ color: "white" }}>{c.joining_fee === 0 ? "Free" : fmt0(c.joining_fee)}</span>
                </div>
              </div>
              <div className="flex items-center justify-between pt-2 border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
                <div className="text-10" style={{ color: "rgba(255,255,255,0.55)" }}>
                  Min income {fmt0(c.min_income)}/yr · Score ≥ {c.credit_score_min}
                </div>
                <button className="flex items-center gap-1 text-10 font-medium px-2.5 py-1 rounded-md"
                  style={{ background: ACCENT, color: "#0A0A0A" }}>
                  Apply <ChevronRight size={10} />
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── LoanProductsBlock ────────────────────────────────── */
export function LoanProductsBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (<div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>)}
      {items.map((l) => (
        <div key={l.id} className="rounded-xl p-3 border"
          style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
          <div className="flex items-start gap-3">
            <div className="rounded-lg flex items-center justify-center flex-shrink-0"
              style={{ width: 44, height: 44, background: ACCENT + "14" }}>
              <Banknote size={18} style={{ color: ACCENT }} />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2 mb-1">
                <div className="text-sm font-medium" style={{ color: "white" }}>{l.type}</div>
                <div className="text-sm font-mono" style={{ color: ACCENT }}>{l.rate_from.toFixed(2)}%<span className="text-10" style={{ color: "rgba(255,255,255,0.4)" }}> p.a.</span></div>
              </div>
              <div className="text-11 mb-2" style={{ color: "rgba(255,255,255,0.6)" }}>{l.description}</div>
              <div className="grid grid-cols-3 gap-2 text-10 mb-2">
                <div>
                  <div style={{ color: "rgba(255,255,255,0.4)" }}>Max amount</div>
                  <div className="font-mono" style={{ color: "white" }}>{fmt0(l.max_amount)}</div>
                </div>
                <div>
                  <div style={{ color: "rgba(255,255,255,0.4)" }}>Tenure</div>
                  <div className="font-mono" style={{ color: "white" }}>Up to {l.tenure_max_years}y</div>
                </div>
                <div>
                  <div style={{ color: "rgba(255,255,255,0.4)" }}>Processing</div>
                  <div className="font-mono" style={{ color: "white" }}>{l.processing_fee_pct}%</div>
                </div>
              </div>
              <div className="flex items-center justify-between pt-2 border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
                <div className="text-10" style={{ color: "rgba(255,255,255,0.55)" }}>Min credit score {l.min_credit_score}</div>
                <button className="flex items-center gap-1 text-10 font-medium px-2.5 py-1 rounded-md"
                  style={{ background: ACCENT, color: "#0A0A0A" }}>
                  Apply <ChevronRight size={10} />
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── DepositProductsBlock ─────────────────────────────── */
export function DepositProductsBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (<div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>)}
      {items.map((d) => (
        <div key={d.id} className="rounded-xl p-3 border"
          style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
          <div className="flex items-center justify-between mb-2">
            <div>
              <div className="text-sm font-medium" style={{ color: "white" }}>{d.name}</div>
              <div className="text-11" style={{ color: "rgba(255,255,255,0.55)" }}>
                {d.min_tenure_months === d.max_tenure_months ? `${d.min_tenure_months} months` : `${d.min_tenure_months}–${d.max_tenure_months} months`} · {d.compounding} compounding
              </div>
            </div>
            <div className="text-right">
              <div className="text-base font-mono font-medium" style={{ color: ACCENT }}>{d.rate_pct.toFixed(2)}%</div>
              <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>p.a.</div>
            </div>
          </div>
          {d.tax_benefit && (
            <div className="flex items-center gap-1.5 text-10 mb-2">
              <BadgeCheck size={10} style={{ color: "#86efac" }} />
              <span style={{ color: "rgba(255,255,255,0.7)" }}>{d.tax_benefit}</span>
            </div>
          )}
          <div className="flex items-center justify-between pt-2 border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
            <div className="text-10" style={{ color: "rgba(255,255,255,0.55)" }}>
              Min {fmt0(d.min_amount)} · +{d.senior_citizen_bonus}% for seniors
            </div>
            <button className="flex items-center gap-1 text-10 font-medium px-2.5 py-1 rounded-md"
              style={{ background: ACCENT, color: "#0A0A0A" }}>
              Open <ChevronRight size={10} />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── TransferBlock ────────────────────────────────────── */
export function TransferBlock({ confirmation }) {
  const c = confirmation;
  return (
    <div className="rounded-xl p-4 border-2"
      style={{
        background: "linear-gradient(180deg, rgba(255,215,135,0.10), rgba(255,215,135,0.02))",
        borderColor: ACCENT + "44",
      }}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <ArrowUpRight size={16} style={{ color: ACCENT }} />
          <div className="text-sm font-medium" style={{ color: "white" }}>Transfer summary</div>
        </div>
        <span className="text-10 font-mono px-2 py-0.5 rounded-full" style={{ background: "rgba(250,204,21,0.15)", color: "#fde047" }}>
          {c.status}
        </span>
      </div>
      <div className="text-2xl font-mono font-medium mb-3" style={{ color: "white" }}>{fmt(c.amount)}</div>
      <div className="space-y-1.5 text-xs">
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>From</span>
          <span className="font-mono" style={{ color: "white" }}>{c.from_account}</span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>To</span>
          <span style={{ color: "white" }}>{c.to_name} <span className="font-mono" style={{ color: "rgba(255,255,255,0.5)" }}>· {c.to_account_masked}</span></span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Mode</span>
          <span style={{ color: "white" }}>{c.mode} · {c.eta}</span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Fee</span>
          <span className="font-mono" style={{ color: "white" }}>{c.fee === 0 ? "Free" : fmt(c.fee)}</span>
        </div>
        <div className="flex justify-between pt-1.5 border-t" style={{ borderColor: "rgba(255,255,255,0.08)" }}>
          <span style={{ color: "rgba(255,255,255,0.5)" }}>Ref ID</span>
          <span className="font-mono" style={{ color: ACCENT }}>{c.transfer_id}</span>
        </div>
      </div>
    </div>
  );
}

/* ─── CreditScoreBlock ─────────────────────────────────── */
export function CreditScoreBlock({ score_info }) {
  const s = score_info;
  // Score arc — 300 to 900 range
  const pct = Math.max(0, Math.min(100, ((s.score - 300) / 600) * 100));
  return (
    <div className="rounded-xl p-4 border" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center gap-2 mb-3">
        <Target size={14} style={{ color: ACCENT }} />
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Credit score</div>
      </div>
      <div className="flex items-center gap-4 mb-3">
        <div className="text-center">
          <div className="text-3xl font-mono font-medium" style={{ color: ACCENT }}>{s.score}</div>
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "#86efac" }}>{s.band}</div>
        </div>
        <div className="flex-1">
          <div className="h-1.5 rounded-full overflow-hidden mb-1" style={{ background: "rgba(255,255,255,0.06)" }}>
            <div style={{ width: `${pct}%`, height: "100%", background: ACCENT, borderRadius: 999 }} />
          </div>
          <div className="flex justify-between text-9 font-mono" style={{ color: "rgba(255,255,255,0.4)" }}>
            <span>300</span><span>600</span><span>900</span>
          </div>
          <div className="text-10 mt-1" style={{ color: "rgba(255,255,255,0.5)" }}>{s.last_updated}</div>
        </div>
      </div>
      <div className="space-y-1">
        {s.factors.map((f, i) => (
          <div key={i} className="flex items-center justify-between px-2 py-1.5 rounded-md" style={{ background: "rgba(255,255,255,0.02)" }}>
            <div className="text-11" style={{ color: "rgba(255,255,255,0.8)" }}>{f.label}</div>
            <span className={`text-9 font-medium uppercase px-1.5 py-0.5 rounded-full`}
              style={{
                background: f.impact === "positive" ? "rgba(74,222,128,0.15)" : "rgba(248,113,113,0.15)",
                color: f.impact === "positive" ? "#86efac" : "#fca5a5",
              }}>
              {f.impact}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── Dispatcher ───────────────────────────────────────── */
export default function Block({ block }) {
  switch (block.type) {
    case "text":                  return <TextBlock {...block} />;
    case "disclaimer":            return <DisclaimerBlock {...block} />;
    case "fraud_alert":           return <FraudAlertBlock {...block} />;
    case "accounts":              return <AccountsBlock {...block} />;
    case "cards":                 return <CardsBlock {...block} />;
    case "transactions":          return <TransactionsBlock {...block} />;
    case "loans":                 return <LoansBlock {...block} />;
    case "investments":           return <InvestmentsBlock {...block} />;
    case "market":                return <MarketBlock {...block} />;
    case "budget":                return <BudgetBlock {...block} />;
    case "credit_card_products":  return <CreditCardProductsBlock {...block} />;
    case "loan_products":         return <LoanProductsBlock {...block} />;
    case "deposit_products":      return <DepositProductsBlock {...block} />;
    case "transfer":              return <TransferBlock {...block} />;
    case "credit_score":          return <CreditScoreBlock {...block} />;
    default:
      return (
        <div className="text-xs px-3 py-2 rounded-md" style={{ background: "rgba(255,255,255,0.04)", color: "rgba(255,255,255,0.5)" }}>
          [Unknown block type: {block.type}]
        </div>
      );
  }
}
