from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "LIVE",
            "service": "RSI Monitor API",
            "message": "Deployed on Vercel - Working!",
            "endpoints": ["/", "/api/rsi", "/health"]
        }
        
        self.wfile.write(json.dumps(response).encode())
        return
