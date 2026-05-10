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
| Ticker | Any public US stock (e.g. KO, MCD, DELL) |
| Revenue Growth Rate | Annual projected revenue growth |
| EBITDA Margin | Operating profit as % of revenue |
| Debt Financing % | How much of the purchase price is debt |
| Interest Rate | Annual cost of debt |
| Exit Multiple | EV/EBITDA at exit |
| Hold Period | Years before selling (default 5) |

## Outputs

- IRR (Internal Rate of Return)
- MOIC (Multiple on Invested Capital)
- Exit enterprise value and equity value
- Annual financials table (revenue, EBITDA, interest, debt balance)
- Revenue, debt, and cash flow charts
- Monte Carlo IRR distribution with full percentile breakdown

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

Works best with profitable, cash-generative companies:
`KO` `MCD` `DELL` `HLT` `DG` `ORLY`

Avoid pre-revenue or money-losing companies (IonQ, biotech startups) — the validator will flag these.

---

## Built by

Tyler Morton — Freshman, Computer Science (BS), University of Utah  
Built with [Claude Code](https://claude.ai/code)
