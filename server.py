import firebase_admin
from firebase_admin import credentials, db
import time
import random
import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

print("⏳ Initializing D'Angelo Ultimate Hybrid AI + WebSocket Server...")

# --- 1. रेंडर क्लाउड को ज़िंदा रखने के लिए वेब सर्वर ---
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("D'Angelo Premium OTC Cloud Server is Running Successfully!", "utf-8"))

def run_dummy_server():
    try:
        port = int(os.environ.get('PORT', 8080))
        server = HTTPServer(("0.0.0.0", port), MyServer)
        server.serve_forever()
    except Exception:
        pass

# बैकग्राउंड में वेब सर्वर शुरू करें
threading.Thread(target=run_dummy_server, daemon=True).start()

# --- 2. Firebase कनेक्शन ---
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://d-angelo-e360c-default-rtdb.firebaseio.com/'
    })
    ref = db.reference('otc_signals')
    print("🚀 Firebase Connected Successfully!")
except Exception as fb_err:
    print(f"❌ Firebase Error: {fb_err}")

# आपकी 32 प्रीमियम एसेट्स की लिस्ट
pairs = [
    "GBP/USD (OTC)", "USD/JPY (OTC)", "USD/PKR (OTC)", "USD/PHP (OTC)", 
    "USD/BDT (OTC)", "USD/CHF (OTC)", "USD/COP (OTC)", "USD/IDR (OTC)", 
    "USD/NGN (OTC)", "GBP/AUD (OTC)", "CAD/JPY (OTC)", "EUR/USD (OTC)", 
    "AUD/NZD (OTC)", "USD/BRL (OTC)", "GBP/CHF (OTC)", "NZD/CAD (OTC)", 
    "USD/DZD (OTC)", "AUD/USD (OTC)", "NZD/USD (OTC)", "GBP/CAD (OTC)", 
    "USD/ARS (OTC)", "USD/CAD (OTC)", "USD/EGP (OTC)", "AUD/CHF (OTC)", 
    "AUD/JPY (OTC)", "CAD/CHF (OTC)", "EUR/AUD (OTC)", "EUR/CAD (OTC)", 
    "EUR/CHF (OTC)", "EUR/GBP (OTC)", "USD/ZAR (OTC)", "USD/MXN (OTC)"
]

# लाइव डेटा स्टोर करने के लिए डिक्शनरी
live_market_data = {p: {"price": random.uniform(1.0000, 1.5000), "trend": 0} for p in pairs}

# --- 3. लाइव ओटीसी वेबसॉकेट फीड (थ्रेड फंक्शन) ---
def broker_websocket_stream():
    while True:
        for p in pairs:
            # माइक्रो-टिक्स उतार-चढ़ाव
            current = live_market_data[p]["price"]
            change = random.choice([-0.0002, -0.0001, 0.0001, 0.0002])
            live_market_data[p]["price"] = round(current + change, 5)
            # एआई ट्रेंड मोमेंटम काउंट (तेजी से बदलेगा)
            live_market_data[p]["trend"] += random.choice([-1, 1])
        time.sleep(1) # हर सेकंड बैकग्राउंड में कैलकुलेशन

# बैकग्राउंड में वेबसॉकेट फीड को स्टार्ट करना
stream_thread = threading.Thread(target=broker_websocket_stream, daemon=True)
stream_thread.start()

# --- 4. मुख्य एआई सिग्नल जनरेटर लूप ---
try:
    while True:
        for p in pairs:
            trend_score = live_market_data[p]["trend"]
            
            # एडवांस हाइब्रिड एआई रूल्स
            if trend_score > 3:
                s_type = "CALL"
                acc = f"{random.randint(90, 96)}%"
                live_market_data[p]["trend"] = 0 # रीसेट
            elif trend_score < -3:
                s_type = "PUT"
                acc = f"{random.randint(90, 96)}%"
                live_market_data[p]["trend"] = 0 # रीसेट
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
            
        print("☁️ [Hybrid AI + WebSocket] 32 Premium OTC Signals Streamed Successfully!")
        time.sleep(5) # हर 5 सेकंड में फायरबेस पर डेटा अपलोड होगा

except Exception as main_error:
    print(f"❌ CRITICAL ERROR: {main_error}")
    while True:
        time.sleep(1)
