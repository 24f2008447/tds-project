import json
import statistics
from http.server import BaseHTTPRequestHandler

DATA = [
  {"region":"apac","latency_ms":202.99,"uptime_pct":98.473},
  {"region":"apac","latency_ms":159.03,"uptime_pct":98.59},
  {"region":"apac","latency_ms":198.03,"uptime_pct":99.167},
  {"region":"apac","latency_ms":196.2,"uptime_pct":97.237},
  {"region":"apac","latency_ms":178.34,"uptime_pct":98.819},
  {"region":"apac","latency_ms":158.09,"uptime_pct":97.505},
  {"region":"apac","latency_ms":154.1,"uptime_pct":98.724},
  {"region":"apac","latency_ms":115.65,"uptime_pct":98.563},
  {"region":"apac","latency_ms":204.08,"uptime_pct":97.108},
  {"region":"apac","latency_ms":207.5,"uptime_pct":98.153},
  {"region":"apac","latency_ms":199.91,"uptime_pct":97.663},
  {"region":"apac","latency_ms":206.95,"uptime_pct":97.856},
  {"region":"emea","latency_ms":174.98,"uptime_pct":97.298},
  {"region":"emea","latency_ms":220.92,"uptime_pct":99.015},
  {"region":"emea","latency_ms":162.62,"uptime_pct":98.696},
  {"region":"emea","latency_ms":164.96,"uptime_pct":99.037},
  {"region":"emea","latency_ms":230.55,"uptime_pct":99.079},
  {"region":"emea","latency_ms":173.89,"uptime_pct":99.322},
  {"region":"emea","latency_ms":173.65,"uptime_pct":98.938},
  {"region":"emea","latency_ms":156.61,"uptime_pct":97.22},
  {"region":"emea","latency_ms":184.5,"uptime_pct":98.185},
  {"region":"emea","latency_ms":178.06,"uptime_pct":98.38},
  {"region":"emea","latency_ms":166.2,"uptime_pct":98.595},
  {"region":"emea","latency_ms":204.0,"uptime_pct":98.445},
  {"region":"amer","latency_ms":221.79,"uptime_pct":97.984},
  {"region":"amer","latency_ms":135.76,"uptime_pct":99.092},
  {"region":"amer","latency_ms":140.16,"uptime_pct":98.464},
  {"region":"amer","latency_ms":226.06,"uptime_pct":99.05},
  {"region":"amer","latency_ms":173.82,"uptime_pct":97.337},
  {"region":"amer","latency_ms":219.39,"uptime_pct":97.61},
  {"region":"amer","latency_ms":178.47,"uptime_pct":99.485},
  {"region":"amer","latency_ms":125.51,"uptime_pct":98.903},
  {"region":"amer","latency_ms":189.58,"uptime_pct":98.148},
  {"region":"amer","latency_ms":221.43,"uptime_pct":97.757},
  {"region":"amer","latency_ms":173.01,"uptime_pct":97.674},
  {"region":"amer","latency_ms":102.98,"uptime_pct":98.112},
]

def compute(region, threshold_ms):
    records = [r for r in DATA if r["region"] == region]
    if not records:
        return None
    latencies = sorted(r["latency_ms"] for r in records)
    uptimes = [r["uptime_pct"] for r in records]
    p95 = latencies[int(len(latencies) * 0.95)]
    return {
        "avg_latency": round(statistics.mean(latencies), 4),
        "p95_latency": p95,
        "avg_uptime": round(statistics.mean(uptimes), 4),
        "breaches": sum(1 for l in latencies if l > threshold_ms),
    }

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        regions = body.get("regions", [])
        threshold = body.get("threshold_ms", 180)
        result = {r: compute(r, threshold) for r in regions}
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
