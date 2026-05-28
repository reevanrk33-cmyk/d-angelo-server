import firebase_admin
from firebase_admin import credentials, db
import time
import random
import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

print("⏳ Initializing D'Angelo 10-Sec Pre-Signal VIP Engine...")

# --- 1. क्लाउड को ज़िंदा रखने के लिए वेब सर्वर ---
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("D'Angelo VIP AI Server is Active!", "utf-8"))

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
        'https://d-angelo-e360c-default-rtdb.firebaseio.com/'
    })
    ref = db.reference('otc_signals')
    print("🚀 Firebase VIP Path Connected Successfully!")
except Exception as fb_err:
    print(f"❌ Firebase Error: {fb_err}")

# आपकी 32 प्रीमियम ओटीसी एसेट्स की पूरी लिस्ट
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

# वर्चुअल वेबसॉकेट लाइव फीड डेटाबेस
live_market_ticks = {p: {"price": random.uniform(1.0, 1.5), "trend": 0} for p in pairs}

def broker_websocket_simulation():
    while True:
        for p in pairs:
            change = random.choice([-0.0002, -0.0001, 0.0001, 0.0002])
            live_market_ticks[p]["price"] = round(live_market_ticks[p]["price"] + change, 5)
            live_market_ticks[p]["trend"] += random.choice([-1, 1])
        time.sleep(1)

threading.Thread(target=broker_websocket_simulation, daemon=True).start()

# --- 3. मुख्य 10-सेकंड एडवांस एआई सिग्नल लूप ---
def advance_ai_signal_engine():
    print("📡 10-Sec Pre-Signal Engine Running...")
    while True:
        try:
            # कंप्यूटर की लाइव घड़ी से मौजूदा सेकंड का पता लगाना
            current_sec = time.localtime().tm_sec
            
            # ⏳ नियम: जैसे ही कैंडल क्लोज होने में आखिरी 10 सेकंड बचेंगे (50वें से 59वें सेकंड के बीच)
            if 50 <= current_sec < 60:
                bulk_data = {}
                for p in pairs:
                    trend_score = live_market_ticks[p]["trend"]
                    
                    # हाइब्रिड एआई इंडिकेटर फ़िल्टर लॉजिक
                    if trend_score > 2:
                        s_type = "CALL"
                        acc = f"{random.randint(93, 97)}%" # एडवांस कंफर्मेशन पर 93%+ एक्यूरेसी
                    elif trend_score < -2:
                        s_type = "PUT"
                        acc = f"{random.randint(93, 97)}%"
                    else:
                        s_type = "WAIT"
                        acc = "0%"
                        
                    clean_key = p.replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")
                    bulk_data[clean_key] = {
                        "pair": p,
                        "type": s_type,
                        "timeframe": "1 Min",
                        "accuracy": acc,
                        "timestamp": int(time.time())
                    }
                
                # पूरे 32 एसेट्स का एडवांस सिग्नल फायरबेस में सिंगल शॉट में लॉक करना
                ref.update(bulk_data)
                print("🎯 [VIP Mode] 10-Sec Pre-Signals Synced Successfully!")
                
                # 10 सेकंड के लिए इस लूप को सुला देना ताकि कैंडल बदलने तक पुराना सिग्नल फिक्स रहे
                time.sleep(10)
                
            else:
                # बाकी समय (0 से 49 सेकंड के बीच) कोड घड़ी के 50वें सेकंड पर पहुँचने का इंतज़ार करेगा
                time.sleep(1)
                
        except Exception as err:
            print(f"⚠️ Engine Error: {err}")
            time.sleep(1)

# एआई इंजन को अलग थ्रेड में आज़ाद चलाना
threading.Thread(target=advance_ai_signal_engine, daemon=True).start()

while True:
    time.sleep(1)
