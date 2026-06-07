from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import statistics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Telemetry data embedded directly (Vercel serverless cannot read files)
DATA = [
  {"region":"apac","service":"checkout","latency_ms":202.99,"uptime_pct":98.473,"timestamp":20250301},
  {"region":"apac","service":"payments","latency_ms":159.03,"uptime_pct":98.59,"timestamp":20250302},
  {"region":"apac","service":"recommendations","latency_ms":198.03,"uptime_pct":99.167,"timestamp":20250303},
  {"region":"apac","service":"payments","latency_ms":196.2,"uptime_pct":97.237,"timestamp":20250304},
  {"region":"apac","service":"catalog","latency_ms":178.34,"uptime_pct":98.819,"timestamp":20250305},
  {"region":"apac","service":"support","latency_ms":158.09,"uptime_pct":97.505,"timestamp":20250306},
  {"region":"apac","service":"analytics","latency_ms":154.1,"uptime_pct":98.724,"timestamp":20250307},
  {"region":"apac","service":"analytics","latency_ms":115.65,"uptime_pct":98.563,"timestamp":20250308},
  {"region":"apac","service":"checkout","latency_ms":204.08,"uptime_pct":97.108,"timestamp":20250309},
  {"region":"apac","service":"payments","latency_ms":207.5,"uptime_pct":98.153,"timestamp":20250310},
  {"region":"apac","service":"recommendations","latency_ms":199.91,"uptime_pct":97.663,"timestamp":20250311},
  {"region":"apac","service":"catalog","latency_ms":206.95,"uptime_pct":97.856,"timestamp":20250312},
  {"region":"emea","service":"payments","latency_ms":174.98,"uptime_pct":97.298,"timestamp":20250301},
  {"region":"emea","service":"catalog","latency_ms":220.92,"uptime_pct":99.015,"timestamp":20250302},
  {"region":"emea","service":"recommendations","latency_ms":162.62,"uptime_pct":98.696,"timestamp":20250303},
  {"region":"emea","service":"checkout","latency_ms":164.96,"uptime_pct":99.037,"timestamp":20250304},
  {"region":"emea","service":"payments","latency_ms":230.55,"uptime_pct":99.079,"timestamp":20250305},
  {"region":"emea","service":"analytics","latency_ms":173.89,"uptime_pct":99.322,"timestamp":20250306},
  {"region":"emea","service":"catalog","latency_ms":173.65,"uptime_pct":98.938,"timestamp":20250307},
  {"region":"emea","service":"recommendations","latency_ms":156.61,"uptime_pct":97.22,"timestamp":20250308},
  {"region":"emea","service":"checkout","latency_ms":184.5,"uptime_pct":98.185,"timestamp":20250309},
  {"region":"emea","service":"catalog","latency_ms":178.06,"uptime_pct":98.38,"timestamp":20250310},
  {"region":"emea","service":"payments","latency_ms":166.2,"uptime_pct":98.595,"timestamp":20250311},
  {"region":"emea","service":"checkout","latency_ms":204.0,"uptime_pct":98.445,"timestamp":20250312},
  {"region":"amer","service":"analytics","latency_ms":221.79,"uptime_pct":97.984,"timestamp":20250301},
  {"region":"amer","service":"recommendations","latency_ms":135.76,"uptime_pct":99.092,"timestamp":20250302},
  {"region":"amer","service":"checkout","latency_ms":140.16,"uptime_pct":98.464,"timestamp":20250303},
  {"region":"amer","service":"recommendations","latency_ms":226.06,"uptime_pct":99.05,"timestamp":20250304},
  {"region":"amer","service":"payments","latency_ms":173.82,"uptime_pct":97.337,"timestamp":20250305},
  {"region":"amer","service":"payments","latency_ms":219.39,"uptime_pct":97.61,"timestamp":20250306},
  {"region":"amer","service":"analytics","latency_ms":178.47,"uptime_pct":99.485,"timestamp":20250307},
  {"region":"amer","service":"payments","latency_ms":125.51,"uptime_pct":98.903,"timestamp":20250308},
  {"region":"amer","service":"payments","latency_ms":189.58,"uptime_pct":98.148,"timestamp":20250309},
  {"region":"amer","service":"payments","latency_ms":221.43,"uptime_pct":97.757,"timestamp":20250310},
  {"region":"amer","service":"payments","latency_ms":173.01,"uptime_pct":97.674,"timestamp":20250311},
  {"region":"amer","service":"catalog","latency_ms":102.98,"uptime_pct":98.112,"timestamp":20250312},
]


class AnalyticsRequest(BaseModel):
    regions: List[str]
    threshold_ms: float


@app.get("/")
def root():
    return {"status": "ok", "message": "eShopCo Latency Analytics API"}


@app.post("/analytics")
def analytics(req: AnalyticsRequest):
    result = {}
    for region in req.regions:
        records = [r for r in DATA if r["region"] == region]
        if not records:
            result[region] = None
            continue
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]
        sorted_lat = sorted(latencies)
        n = len(sorted_lat)
        p95_idx = int(n * 0.95)
        result[region] = {
            "avg_latency": round(statistics.mean(latencies), 4),
            "p95_latency": sorted_lat[p95_idx],
            "avg_uptime": round(statistics.mean(uptimes), 4),
            "breaches": sum(1 for l in latencies if l > req.threshold_ms),
        }
    return result
