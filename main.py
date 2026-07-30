import os
import time
import threading
import requests
from flask import Flask

# --- WEB SERVER (Render-in sönməməsi üçün) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "ADY Bilet Monitorinq Botu Aktivdir!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- TELEGRAM VƏ MONITORİNQ BOTU ---
BOT_TOKEN = "8203977390:AAGX4V3sdaDE_OQRQ8njTuI-M5UwcG1qqKU"
CHANNEL_ID = "@tezBiletTap"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Telegrama mesaj göndərərkən xəta: {e}")

def check_baku_tbilisi_route():
    """
    Bakı - Tiflis reyslərini yoxlayan funksiya
    """
    url = "https://ticket.ady.az/api/v1/routes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("Bakı - Tiflis reysləri uğurla yoxlanıldı.")
        else:
            print(f"ADY sisteminə qoşulmaq olmadı. Status: {response.status_code}")
    except Exception as e:
        print(f"Məlumat çəkərkən xəta yarandı: {e}")

def bot_loop():
    time.sleep(5)  # Serverin tam işə düşməsini gözləyirik
    send_telegram_message(
        "<b>🚆 Bakı ⇆ Tiflis Reys Monitorinqi Aktivdir!</b>\n\n"
        "Bu kanalda Bakı – Tiflis istiqamətində açılan yeni bilet satışı və reyslər haqqında anlıq bildirişlər paylaşılacaq."
    )
    
    while True:
        try:
            check_baku_tbilisi_route()
            time.sleep(600)  # Hər 10 dəqiqədən bir yoxlayır
        except Exception as main_error:
            print(f"Ümumi xəta: {main_error}")
            time.sleep(60)

if __name__ == "__main__":
    # Botu arxa fonda işə salırıq
    t = threading.Thread(target=bot_loop)
    t.daemon = True
    t.start()
    
    # Web serveri işə salırıq ki Render portu görsün
    run_web_server()
