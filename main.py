
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analysis_engine import analyze_stock

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scan")
def scan(tickers: str):
    results = []
    for t in tickers.split(","):
        data = analyze_stock(t.strip())
        if data:
            results.append(data)
    return {"results": results}
