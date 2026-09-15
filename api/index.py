from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "LIVE",
        "service": "RSI Monitor API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api")
def api_root():
    return {"live": True, "message": "RSI Monitor API working on Vercel!"}

@app.get("/health")
def health():
    return {"ok": True}
