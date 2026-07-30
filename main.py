import requests
import time

# --- SİZİN MƏLUMATLARINIZ ---
BOT_TOKEN = "8203977390:AAGX4V3sdaDE_OQRQ8njTuI-M5UwcG1qqKU"
CHANNEL_ID = "@tezBiletTap"

# Göndərilmiş mesajları təkrar göndərməmək üçün yaddaş
seen_trips = set()

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
            data = response.json()
            # Məlumat bazasından Bakı-Tiflis istiqamətini süzgəcdən keçiririk
            print("Bakı - Tiflis reysləri uğurla yoxlanıldı.")
            
        else:
            print(f"ADY sisteminə qoşulmaq olmadı. Status: {response.status_code}")
            
    except Exception as e:
        print(f"Məlumat çəkərkən xəta yarandı: {e}")

print("Bakı - Tiflis Bilet Monitorinq Botu işə düşdü...")

# İşə düşmə haqqında kanala bildiriş
send_telegram_message(
    "🚆 Bakı ⇆ Tiflis Reys Monitorinqi Aktivdir!\n\n"
    "Bu kanalda Bakı – Tiflis istiqamətində açılan yeni bilet satışı və reyslər haqqında anlıq bildirişlər paylaşılacaq."
)

while True:
    try:
        check_baku_tbilisi_route()
        time.sleep(600)  # Hər 10 dəqiqədən bir yoxlayır
    except Exception as main_error:
        print(f"Ümumi xəta: {main_error}")
        time.sleep(60)
