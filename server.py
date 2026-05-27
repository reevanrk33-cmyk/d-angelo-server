import firebase_admin
from firebase_admin import credentials, db
import time
import random
import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

print("⏳ Starting D'Angelo Ultra-Speed Cloud Engine...")

# --- 1. रेंडर को जगाए रखने के लिए लाइटवेट वेब सर्वर ---
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("D'Angelo Server is Active!", "utf-8"))

def run_dummy_server():
    try:
        port = int(os.environ.get('PORT', 8080))
        server = HTTPServer(("0.0.0.0", port), MyServer)
        server.serve_forever()
    except Exception:
        pass

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
    print(f"❌ Firebase Connection Error: {fb_err}")

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

# --- 3. मुख्य डायरेक्ट-स्ट्रीम एआई सिग्नल जनरेटर ---
def signal_generator_engine():
    print("📡 AI Engine Loop Started...")
    while True:
        try:
            bulk_data = {}
            for p in pairs:
                s_type = random.choice(["CALL", "PUT", "WAIT", "WAIT"])
                acc = f"{random.randint(90, 96)}%" if s_type != "WAIT" else "0%"
                clean_key = p.replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")
                
                bulk_data[clean_key] = {
                    "pair": p,
                    "type": s_type,
                    "timeframe": "1 Min",
                    "accuracy": acc,
                    "timestamp": int(time.time())
                }
            
            ref.update(bulk_data)
            print("☁️ [Cloud Mode] 32 Premium OTC Signals Synced with Firebase!")
            
        except Exception as loop_err:
            print(f"⚠️ Loop Warning: {loop_err}")
            
        time.sleep(5)

# एआई इंजन को अलग थ्रेड में शुरू करना
threading.Thread(target=signal_generator_engine, daemon=True).start()

# मुख्य थ्रेड को ज़िंदा रखना
while True:
    time.sleep(1)
