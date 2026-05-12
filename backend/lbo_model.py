import numpy as np
import numpy_financial as npf


def project_revenue(initial_revenue, growth_rate, years):
    revenues = []
    for year in range(1, years + 1):
        revenues.append(initial_revenue * (1 + growth_rate) ** year)
    return revenues


def calculate_ebitda(revenues, margin):
    return [rev * margin for rev in revenues]


def calculate_debt_schedule(initial_debt, interest_rate, years):
    annual_principal = initial_debt / years
    debt_balances = []
    interest_payments = []
    remaining = initial_debt
    for _ in range(years):
        interest = remaining * interest_rate
        interest_payments.append(interest)
        remaining -= annual_principal
        debt_balances.append(max(remaining, 0))
    return debt_balances, interest_payments, annual_principal


def calculate_exit_value(final_ebitda, exit_multiple):
    return final_ebitda * exit_multiple


def calculate_irr(cash_flows):
    try:
        result = npf.irr(cash_flows)
        return float(result) if not np.isnan(result) else None
    except Exception:
        return None


def run_lbo(data):
    revenue        = float(data["revenue"])
    growth_rate    = float(data["growth_rate"])
    ebitda_margin  = float(data["ebitda_margin"])
    debt_percent   = float(data["debt_percent"])
    interest_rate  = float(data["interest_rate"])
    exit_multiple  = float(data["exit_multiple"])
    entry_multiple = float(data.get("entry_multiple", exit_multiple))
    years          = int(data["years"])

    # 1. Purchase price based on entry multiple
    entry_ebitda   = revenue * ebitda_margin
    purchase_price = entry_ebitda * entry_multiple

    # 2. Debt + equity split
    initial_debt   = purchase_price * debt_percent
    initial_equity = purchase_price * (1 - debt_percent)

    # 3. Revenue + EBITDA projections
    revenues    = project_revenue(revenue, growth_rate, years)
    ebitda_list = calculate_ebitda(revenues, ebitda_margin)

    # 4. Debt schedule
    debt_balances, interest_payments, annual_principal = calculate_debt_schedule(
        initial_debt, interest_rate, years
    )

    # 5. Exit value
    exit_value     = calculate_exit_value(ebitda_list[-1], exit_multiple)
    remaining_debt = debt_balances[-1]
    equity_value   = exit_value - remaining_debt

    # 6. Levered cash flows (equity perspective)
    levered_cfs = [-initial_equity]
    for i in range(years - 1):
        levered_cfs.append(max(ebitda_list[i] - interest_payments[i], 0))
    levered_cfs.append(equity_value)

    irr         = calculate_irr(levered_cfs)
    moic        = round(equity_value / initial_equity, 2) if initial_equity > 0 else None

    # 7. Unlevered IRR (business return ignoring debt — as if 100% equity deal)
    unlevered_cfs = [-purchase_price]
    for i in range(years - 1):
        unlevered_cfs.append(ebitda_list[i])
    unlevered_cfs.append(ebitda_list[-1] + exit_value)
    unlevered_irr = calculate_irr(unlevered_cfs)

    # 8. Credit metrics — per year
    credit_metrics = []
    for i in range(years):
        debt_bal     = debt_balances[i]
        ebitda_val   = ebitda_list[i]
        interest     = interest_payments[i]
        debt_service = interest + annual_principal

        credit_metrics.append({
            "year":             i + 1,
            "total_debt":       round(debt_bal, 2),
            "debt_ebitda":      round(debt_bal / ebitda_val, 2)      if ebitda_val > 0  else None,
            "interest_coverage":round(ebitda_val / interest, 2)      if interest > 0    else None,
            "dscr":             round(ebitda_val / debt_service, 2)  if debt_service > 0 else None,
        })

    return {
        "irr":              round(irr * 100, 2)          if irr is not None          else None,
        "unlevered_irr":    round(unlevered_irr * 100, 2) if unlevered_irr is not None else None,
        "moic":             moic,
        "exit_value":       round(exit_value, 2),
        "equity_value":     round(equity_value, 2),
        "initial_equity":   round(initial_equity, 2),
        "initial_debt":     round(initial_debt, 2),
        "purchase_price":   round(purchase_price, 2),
        "entry_multiple":   round(entry_multiple, 1),
        "exit_multiple":    round(exit_multiple, 1),
        "revenues":         [round(r, 2) for r in revenues],
        "ebitda":           [round(e, 2) for e in ebitda_list],
        "debt_balances":    [round(d, 2) for d in debt_balances],
        "interest_payments":[round(p, 2) for p in interest_payments],
        "cash_flows":       [round(c, 2) for c in levered_cfs],
        "years":            list(range(1, years + 1)),
        "credit_metrics":   credit_metrics,
    }
