from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
import random

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Fake live RSI for demo
        rsi = round(30 + random.random() * 50, 2)
        status = "OVERBOUGHT" if rsi > 70 else "OVERSOLD" if rsi < 30 else "NEUTRAL"
        color = "#ff2d95" if rsi > 70 else "#00e5ff" if rsi < 30 else "#8b5cf6"

        # If browser wants HTML, return COLOURFUL page
        if "text/html" in self.headers.get("Accept", "") or self.path == "/" or self.path == "/api":
            html = f"""
            <!DOCTYPE html>
            <html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
            <title>RSI MONITOR - LIVE</title>
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Geist:wght@900&display=swap');
            body{{margin:0;background:#06070F;color:white;font-family:Geist,system-ui;overflow:hidden}}
            .bg1{{position:absolute;top:-20%;left:-20%;width:80%;height:70%;border-radius:50%;background:radial-gradient(circle,rgba(139,92,246,0.5),transparent 60%);filter:blur(60px)}}
            .bg2{{position:absolute;top:-10%;right:-10%;width:60%;height:60%;border-radius:50%;background:radial-gradient(circle,rgba(236,72,153,0.4),transparent 60%);filter:blur(70px)}}
            .bg3{{position:absolute;top:30%;left:40%;width:50%;height:50%;border-radius:50%;background:radial-gradient(circle,rgba(6,182,212,0.3),transparent 60%);filter:blur(80px)}}
            .card{{position:relative;z-index:10;max-width:1100px;margin:40px auto;padding:20px}}
            .pill{{display:inline-flex;align-items:center;gap:8px;background:#11121E;border:1px solid rgba(255,255,255,0.1);border-radius:999px;padding:8px 16px;font-size:11px;letter-spacing:2px;font-weight:900}}
            .dot{{width:8px;height:8px;background:#10b981;border-radius:50%;box-shadow:0 0 10px #10b981;animation:pulse 1.5s infinite}}
            @keyframes pulse{{0%{{opacity:1}}50%{{opacity:0.4}}100%{{opacity:1}}}}
            .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:24px}}
            .box{{background:rgba(14,15,28,0.8);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.1);border-radius:24px;padding:20px;box-shadow:0 0 30px rgba(139,92,246,0.15)}}
            .rsi{{font-size:64px;font-weight:900;background:linear-gradient(90deg,#a78bfa,#f472b6,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
            a{{color:white;text-decoration:none}}
            </style></head>
            <body><div class="bg1"></div><div class="bg2"></div><div class="bg3"></div>
            <div class="card">
              <div class="pill"><span class="dot"></span> LIVE ON VERCEL — RSI MONITOR</div>
              <h1 style="font-size:48px;font-weight:900;letter-spacing:-2px;margin:20px 0 0;line-height:1">YOUR CEO<br>DASHBOARD IS <span style="color:#a78bfa">LIVE</span></h1>
              <div class="grid">
                <div class="box"><div style="font-size:10px;letter-spacing:3px;opacity:0.4">RSI VALUE</div><div class="rsi">{rsi}</div><div style="margin-top:8px;font-size:12px;opacity:0.6">Updated: {datetime.now().strftime('%H:%M:%S')}</div></div>
                <div class="box" style="border-color:{color}55"><div style="font-size:10px;letter-spacing:3px;opacity:0.4">STATUS</div><div style="font-size:32px;font-weight:900;margin-top:12px;color:{color}">{status}</div><div style="margin-top:8px;padding:6px 12px;border-radius:999px;background:{color}22;display:inline-block;font-size:11px;font-weight:800;color:{color}">● {status}</div></div>
                <div class="box"><div style="font-size:10px;letter-spacing:3px;opacity:0.4">API URL</div><div style="font-size:13px;margin-top:12px;word-break:break-all;opacity:0.8">rsi-monitor-8845-2hem5TosxQ-venus13.vercel.app</div><a href="/api?format=json" style="margin-top:14px;display:inline-block;background:white;color:black;padding:8px 16px;border-radius:999px;font-weight:800;font-size:12px">VIEW JSON →</a></div>
              </div>
              <div style="margin-top:24px;text-align:center;font-size:10px;letter-spacing:2px;opacity:0.2">BUILT WITH PYTHON • VERCEL EDGE • GLASSMORPHISM • NEON • CEO GRADE</div>
            </div></body></html>
            """
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
            return

        # Else return JSON
        data = {{"status": "LIVE", "service": "RSI Monitor API", "rsi": rsi, "signal": status, "timestamp": datetime.now().isoformat(), "message": "Deployed on Vercel - Working!"}}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

