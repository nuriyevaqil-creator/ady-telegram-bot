import os
import time
import threading
import requests
from flask import Flask

# --- WEB SERVER (Render üçün) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "ADY Bilet Monitorinq Botu Aktivdir!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- TELEGRAM VƏ BOT TƏNZİMLƏMƏLƏRİ ---
BOT_TOKEN = "8203977390:AAGX4V3sdaDE_OQRQ8njTuI-M5UwcG1qqKU"
CHANNEL_ID = "@tezBiletTap"

# Son göndərilən mətni yadda saxlayırıq ki, eyni siyahını təkrar atmayaq
last_sent_message = ""

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

def check_and_send_schedule():
    global last_sent_message
    
    url = "https://ticket.ady.az/api/v1/routes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            routes = data.get("data", []) if isinstance(data, dict) else []
            
            baku_tbilisi_list = []
            tbilisi_baku_list = []

            for route in routes:
                from_st = str(route.get("from_station_name", "")).lower()
                to_st = str(route.get("to_station_name", "")).lower()
                date_str = route.get("date", "")
                price = route.get("min_price", route.get("price", "---"))
                available_seats = route.get("available_seats", 0)

                # Bakı -> Tiflis
                if ("baku" in from_st or "bakı" in from_st) and ("tbilisi" in to_st or "tiflis" in to_st):
                    if available_seats > 0:
                        baku_tbilisi_list.append(f"📅 {date_str} — <b>{price} AZN</b>")

                # Tiflis -> Bakı
                if ("tbilisi" in from_st or "tiflis" in from_st) and ("baku" in to_st or "bakı" in to_st):
                    if available_seats > 0:
                        tbilisi_baku_list.append(f"📅 {date_str} — <b>{price} AZN</b>")

            # --- MESAJIN HAZIRLANMASI ---
            msg_lines = ["<b>🎫 ADY Biletləri</b>\n"]

            # 1. Tbilisi -> Bakı hissəsi
            msg_lines.append("🚂 <b>Tbilisi ➔ Bakı:</b>")
            if tbilisi_baku_list:
                msg_lines.extend(tbilisi_baku_list)
            else:
                msg_lines.append("— hazırda bilet yoхdur")

            msg_lines.append("")  # Boşluq

            # 2. Bakı -> Tbilisi hissəsi
            msg_lines.append(f"🚂 <b>Bakı ➔ Tbilisi ({len(baku_tbilisi_list)}):</b>")
            if baku_tbilisi_list:
                msg_lines.extend(baku_tbilisi_list)
            else:
                msg_lines.append("— hazırda bilet yoхdur")

            msg_lines.append("\n👉 <a href='https://ticket.ady.az'>ticket.ady.az</a>")

            full_message = "\n".join(msg_lines)

            # Əgər məlumat dəyişibsə (və ya ilk dəfədirsə), kanala atır
            if full_message != last_sent_message:
                send_telegram_message(full_message)
                last_sent_message = full_message
                print("Yenilənmiş siyahı kanala gönderildi.")
            else:
                print("Məlumatda dəyişiklik yoxdur, təkrar mesaj atılmadı.")

        else:
            print(f"ADY API xətası: {response.status_code}")
    except Exception as e:
        print(f"Xəta yarandı: {e}")

def bot_loop():
    time.sleep(5)
    while True:
        try:
            check_and_send_schedule()
            time.sleep(600)  # Hər 10 dəqiqədən bir yoxlayır
        except Exception as main_error:
            print(f"Loop xətası: {main_error}")
            time.sleep(60)

if __name__ == "__main__":
    t = threading.Thread(target=bot_loop)
    t.daemon = True
    t.start()
    
    run_web_server()
