# JarNox Stock Market Dashboard Made with using Python, FastAPI, HTML, CSS, JS, Chart.js
A full-stack stock market dashboard project.

A clean, responsive stock dashboard with a **FastAPI** backend, **SQLite** caching, **yfinance** live data, optional **mock fallback**, and a simple **AI prediction** using `LinearRegression`. Frontend is vanilla **HTML/CSS/JS** with **Chart.js**.

## Features
- Left panel with a scrollable list of 10+ companies
- Live historical data via yfinance (NSE examples included: `TCS.NS`, `RELIANCE.NS`)
- SQLite cache to reduce API calls
- Chart.js line chart for closing price
- 52-week high/low and average volume
- Simple next-day close prediction (LinearRegression on lag features)
- Mock dataset fallback (`data/sample_prices.csv`)
- Dockerfile for backend; easy deploy to Render/Railway

Quick Start (Local)  Backend
```bash:
    cd backend
    python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn main:app --reload
```
API: http://127.0.0.1:8000  (See `/docs` for Swagger)

### Frontend
Just open `frontend/index.html` in a browser while backend is running.
If hosted statically (GitHub Pages), edit `API_BASE` in `frontend/app.js` to your backend URL.

## Endpoints
- `GET /companies` — list of symbols
- `GET /history?symbol=TSLA&period=1y&interval=1d&mock=false` — OHLCV
- `GET /stats?symbol=TSLA` — 52w high/low/avg volume
- `GET /predict?symbol=TSLA` — simple next-day close prediction

## Deployment
- **Railway**: Use the Dockerfile in `backend/`. Expose port `8000`.
- **Vercel/Static Frontend**: Deploy `frontend/` and set `API_BASE` to the backend URL.

## Notes & Limitations
- yfinance data depends on Yahoo availability. The app falls back to mock CSV if live fetch fails.
- Prediction is **for demo only**; not financial advice.

## Short Note
I built a full‑stack stock dashboard to demonstrate clean structure and end‑to‑end integration. The **backend** uses FastAPI for simple REST endpoints and **yfinance** to fetch historical OHLCV data. To make the app robust and efficient, I adt`ded a **SQLite cache** and created endpoints for `/companies`, `/history`, `/stats`, and `/predic. The stats endpoint computes 52‑week high/low and average volume (approx. last 252 trading days). For a light **AI** touch, the prediction endpoint trains a **LinearRegression** model on the last five lagged closes to estimate the next day’s close; it’s intentionally simple but shows model wiring and inference.

The **frontend** is a minimal, responsive HTML/CSS/JS app that keeps focus on UX: a searchable, scrollable company list on the left; a toolbar for period/interval; and a Chart.js line plot in the main area. Selecting a ticker triggers data fetches for history, stats, and prediction. I included **NSE tickers** like `TCS.NS` and `RELIANCE.NS` to show BSE/NSE support via Yahoo symbols. A small **mock dataset** serves as a fallback and for quick demos without network access. 

Challenges included normalizing different intervals/periods, handling empty responses, and designing a simple yet useful prediction that avoids overfitting while staying easy to explain. If given more time, I would add technical indicators (EMA, RSI), candlestick charts, and CI/CD for automatic deployment.