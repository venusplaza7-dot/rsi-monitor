from http.server import BaseHTTPRequestHandler
import json
# Now you can import your logic
from monitor import RSIMonitor

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        monitor = RSIMonitor()
        data = monitor.get_latest() # your real function
        
        self.wfile.write(json.dumps(data).encode())
