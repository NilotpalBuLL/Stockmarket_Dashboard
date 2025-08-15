
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json, os, math
from datetime import datetime, timedelta

app = FastAPI(title="JarNox Stock Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
with open(os.path.join(DATA_DIR, "companies.json")) as f:
    COMPANIES = json.load(f)
with open(os.path.join(DATA_DIR, "history.json")) as f:
    HISTORY = json.load(f)

@app.get("/api/companies")
def get_companies():
    return {"companies": COMPANIES}

@app.get("/api/history")
def get_history(symbol: str):
    symbol = symbol.upper()
    if symbol not in HISTORY:
        raise HTTPException(404, "Symbol not found")
    return {"symbol": symbol, "history": HISTORY[symbol]}

def sma(values, window):
    if window <= 0:
        return []
    out = []
    for i in range(len(values)):
        if i+1 < window:
            out.append(None)
        else:
            window_vals = values[i+1-window:i+1]
            out.append(sum(window_vals)/window)
    return out

@app.get("/api/metrics")
def get_metrics(symbol: str):
    symbol = symbol.upper()
    if symbol not in HISTORY:
        raise HTTPException(404, "Symbol not found")
    hist = HISTORY[symbol]
    closes = [row["close"] for row in hist]
    volumes = [row["volume"] for row in hist]
    last_252 = closes[-252:] if len(closes) >= 252 else closes
    hi_52w = max(last_252) if last_252 else None
    lo_52w = min(last_252) if last_252 else None
    avg_vol = sum(volumes[-30:]) / min(30, len(volumes)) if volumes else None

    # Simple next-day forecast using last 5-day SMA trend
    if len(closes) >= 5:
        sma5 = sum(closes[-5:]) / 5
        forecast = closes[-1] + (closes[-1] - sma5) * 0.5
    else:
        forecast = closes[-1] if closes else None

    return {
        "symbol": symbol,
        "last_close": closes[-1] if closes else None,
        "hi_52w": hi_52w,
        "lo_52w": lo_52w,
        "avg_volume_30d": avg_vol,
        "forecast_next_close": round(forecast, 2) if forecast is not None else None
    }
