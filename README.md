# LBO Modeling Tool

A web app that models leveraged buyouts using real financial data. Enter a stock ticker, validate whether the company is a realistic LBO candidate, run a full buyout model, and stress-test returns with a Monte Carlo simulation.

---

## What it does

1. **Validates** a company against 5 LBO suitability criteria — EBITDA margin, revenue scale, debt load, company maturity, and free cash flow — and scores it 0–100
2. **Pulls real financial data** from Yahoo Finance (revenue, EBITDA margin, debt, enterprise value, growth rate)
3. **Models the buyout** — projects revenue, EBITDA, debt paydown, exit value, IRR, and MOIC over a 5-year hold period
4. **Runs Monte Carlo simulation** — 1,000+ randomised scenarios varying growth rate, margin, and exit multiple to show the P10/P50/P90 IRR distribution

---

## Inputs

| Field | Description |
|---|---|
| Ticker | Any public US stock — or leave blank and enter metrics manually |
| Revenue Growth Rate | Annual projected revenue growth |
| EBITDA Margin | Operating profit as % of revenue |
| Debt Financing % | How much of the purchase price is debt |
| Interest Rate | Annual cost of debt |
| Entry Multiple | EV/EBITDA at acquisition (purchase price) |
| Exit Multiple | EV/EBITDA at sale |
| Hold Period | Years before selling (default 5) |

## Outputs

- Levered IRR and Unlevered IRR (business return vs. equity return)
- MOIC (Multiple on Invested Capital)
- Exit enterprise value and equity value
- Annual financials table (revenue, EBITDA, interest, debt balance)
- Credit metrics per year — Debt/EBITDA, Interest Coverage, DSCR
- Sensitivity analysis grid — IRR and MOIC across entry/exit multiple combinations
- Revenue, debt, and cash flow charts
- Monte Carlo IRR distribution with full percentile breakdown (P10–P90)

---

## Tech Stack

- **Backend** — Python, FastAPI, NumPy, yFinance
- **Frontend** — HTML, CSS, JavaScript, Chart.js
- **Data** — Yahoo Finance via yFinance (no API key required)

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Tyler-Morton/lbo-modeling-tool.git
cd lbo-modeling-tool
```

**2. Install backend dependencies**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Start the backend**
```bash
uvicorn main:app --reload
```

**4. Open the frontend**

Open `frontend/index.html` in your browser.

---

## Good tickers to try

Works best with profitable, cash-generative companies. PE firms typically target mid-market businesses ($50M–$500M revenue), but larger public companies work well for learning the model.

**Mid-market style (most realistic PE targets):**
`WEN` `SCI` `TGLS` `YUM` `CRVL`

**Large-cap (good for exploring the model):**
`KO` `MCD` `HLT` `DG` `DELL` `ORLY`

**No ticker? Use these manual inputs for a textbook mid-market deal:**

| Field | Value |
|---|---|
| Revenue | $400M |
| Growth | 7% |
| EBITDA Margin | 22% |
| Debt Financing | 65% |
| Interest Rate | 9% |
| Entry Multiple | 8x |
| Exit Multiple | 10x |

Avoid money-losing or pre-revenue companies (e.g. OPEN, IONQ, most biotech) — the validator will flag these and the model outputs will be meaningless.

---

## Built by

Tyler Morton — Freshman, Computer Science (BS), University of Utah  
Built with [Claude Code](https://claude.ai/code)
