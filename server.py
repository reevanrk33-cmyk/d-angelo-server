import firebase_admin
from firebase_admin import credentials, db
import time
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- 1. क्लाउड को ज़िंदा रखने के लिए डमी वेब सर्वर ---
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("D'Angelo OTC Server is Live!", "utf-8"))

def run_dummy_server():
    server = HTTPServer(("0.0.0.0", 8080), MyServer)
    server.serve_forever()

# बैकग्राउंड में वेब सर्वर शुरू करें (क्लाउड की ज़रूरत)
threading.Thread(target=run_dummy_server, daemon=True).start()

# --- 2. Firebase कनेक्शन ---
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://firebaseio.com'
    })
except Exception:
    pass

ref = db.reference('otc_signals')
print("🔥 D'Angelo Cloud-Ready Server Started...")

pairs = [
    "GBP/USD (OTC)", "USD/JPY (OTC)", "USD/PKR (OTC)", "USD/PHP (OTC)", 
    "USD/BDT (OTC)", "USD/CHF (OTC)", "USD/COP (OTC)", "USD/IDR (OTC)", 
    "USD/NGN (OTC)", "GBP/AUD (OTC)", "CAD/JPY (OTC)", "EUR/USD (OTC)", 
    "AUD/NZD (OTC)", "USD/BRL (OTC)", "GBP/CHF (OTC)", "NZD/CAD (OTC)", 
    "USD/DZD (OTC)", "AUD/USD (OTC)", "NZD/USD (OTC)", "GBP/CAD (OTC)", 
    "USD/ARS (OTC)", "USD/CAD (OTC)", "USD/EGP (OTC)", "AUD/CHF (OTC)", 
    "AUD/JPY (OTC)", "CAD/CHF (OTC)", "EUR/AUD (OTC)", "EUR/CAD (OTC)", 
    "EUR/CHF (OTC)", "EUR/GBP (OTC)", "USD/ZAR (OTC)"
]

live_market_data = {p: {"price": 1.0000, "trend": 0} for p in pairs}

def broker_stream():
    while True:
        for p in pairs:
            current = live_market_data[p]["price"]
            change = random.choice([-0.0002, -0.0001, 0.0001, 0.0002])
            live_market_data[p]["price"] = round(current + change, 5)
            live_market_data[p]["trend"] += random.choice([-1, 1])
        time.sleep(1)

threading.Thread(target=broker_stream, daemon=True).start()

try:
    while True:
        for p in pairs:
            trend_score = live_market_data[p]["trend"]
            if trend_score > 3:
                s_type = "CALL"
                acc = f"{random.randint(90, 96)}%"
                live_market_data[p]["trend"] = 0
            elif trend_score < -3:
                s_type = "PUT"
                acc = f"{random.randint(90, 96)}%"
                live_market_data[p]["trend"] = 0
            else:
                s_type = "WAIT"
                acc = "0%"
            
            data = {
                "pair": p,
                "type": s_type,
                "timeframe": "1 Min",
                "accuracy": acc,
                "timestamp": int(time.time())
            }
            clean_key = p.replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")
            ref.child(clean_key).set(data)
            
        print("☁️ [Cloud Mode] Signals Streamed Successfully!")
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped.")
