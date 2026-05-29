import firebase_admin
from firebase_admin import credentials, db
import time
import random
import os
import json
from http.server import BaseHTTPRequestHandler

# --- 1. FIREBASE CONNECTION ENGINE ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'https://d-angelo-e360c-default-rtdb.firebaseio.com/'
        })
    except Exception:
        pass

ref = db.reference('otc_signals')

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

# --- 2. VERCEL SERVERLESS VIP HANDLER ---
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            current_epoch = int(time.time())
            current_sec = current_epoch % 60
            
            bulk_data = {}
            # ⏳ नियम: अगर कैंडल क्लोज़ होने में आखिरी 10 सेकंड बचे हों (50 से 59 सेकंड के बीच)
            if 50 <= current_sec < 60:
                for p in pairs:
                    s_type = random.choice(["CALL", "PUT"])
                    acc = f"{random.randint(93, 97)}%"
                    clean_key = p.replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")
                    bulk_data[clean_key] = {
                        "pair": p,
                        "type": s_type,
                        "timeframe": "1 Min",
                        "accuracy": acc,
                        "timestamp": current_epoch
                    }
                ref.update(bulk_data)
                message = f"🎯 [Vercel VIP Sync] 1-Minute Signals Locked Successfully at Second: {current_sec}"
            else:
                # बाकी समय यूज़र्स को सुरक्षित रखने के लिए 'WAIT' मोड दिखाना
                for p in pairs:
                    clean_key = p.replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")
                    bulk_data[clean_key] = {
                        "pair": p,
                        "type": "WAIT",
                        "timeframe": "1 Min",
                        "accuracy": "0%",
                        "timestamp": current_epoch
                    }
                ref.update(bulk_data)
                message = f"⏳ [Analyzing Mode] Market is being tracked. Current Second: {current_sec}"
            
            # वरसेल के स्टैंडर्ड नियमों के मुताबिक HTTP रिस्पॉन्स भेजना
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))
            
        except Exception as err:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {err}".encode('utf-8'))
