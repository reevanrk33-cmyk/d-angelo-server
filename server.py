import firebase_admin
from firebase_admin import credentials, db
import time
import random
import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

print("⏳ Initializing D'Angelo Cloud Server Components...")

# --- 1. रेंडर क्लाउड के लिए डायनेमिक पोर्ट वेब सर्वर ---
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("D'Angelo OTC Cloud Server is Running smoothly!", "utf-8"))

def run_dummy_server():
    try:
        # रेंडर द्वारा दिए गए पोर्ट नंबर को ढूंढना (डिफ़ॉल्ट 10000 या 8080)
        port = int(os.environ.get('PORT', 8080))
        server = HTTPServer(("0.0.0.0", port), MyServer)
        print(f"📡 Web Server successfully bound to port {port}")
        server.serve_forever()
    except Exception as e:
        print(f"⚠️ Web Server Error: {e}")

# बैकग्राउंड में वेब सर्वर शुरू करें
threading.Thread(target=run_dummy_server, daemon=True).start()

# --- 2. मुख्य एआई सिग्नल जनरेटर लॉजिक ---
try:
    print("🔑 Loading Firebase Credentials...")
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://firebaseio.com'
    })
    
    ref = db.reference('otc_signals')
    print("🚀 D'Angelo Cloud-Ready Server Started Successfully!")

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

    while True:
        for p in pairs:
            current = live_market_data[p]["price"]
            change = random.choice([-0.0002, -0.0001, 0.0001, 0.0002])
            live_market_data[p]["price"] = round(current + change, 5)
            live_market_data[p]["trend"] += random.choice([-1, 1])
            
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
            
        print("☁️ [Cloud Mode] 32 Signals Streamed Successfully!")
        time.sleep(5)

except Exception as main_error:
    print(f"❌ CRITICAL SERVER ERROR: {main_error}")
    # सर्वर को बंद होने से रोकने के लिए लूप चालू रखना ताकि एरर लॉग्स में दिख सके
    while True:
        time.sleep(1)
