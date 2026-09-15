from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RSI Monitor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "LIVE", "service": "RSI Monitor API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"ok": True}

# Keep your old logic below this line if you want
# from monitor import RSIMonitor
# from detector import RSIDetector
