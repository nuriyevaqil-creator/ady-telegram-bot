import requests
import time

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

def check_ady_tickets():
    url = "https://ticket.ady.az/api/v1/routes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("ADY saytından məlumatlar uğurla yoxlanıldı.")
        else:
            print(f"ADY saytına qoşulmaq olmadı. Status: {response.status_code}")
    except Exception as e:
        print(f"Məlumat çəkərkən xəta yarandı: {e}")

print("Bot Render platformasında işə düşdü...")
send_telegram_message("🤖 ADY Bilet Monitorinq Botu aktivdir!\n\nRender platformasından fasiləsiz monitorinq başladı.")

while True:
    try:
        check_ady_tickets()
        time.sleep(900)  # Hər 15 dəqiqədən bir yoxlayır
    except Exception as main_error:
        print(f"Ümumi xəta: {main_error}")
        time.sleep(60)
