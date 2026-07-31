import os
import time
import requests

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
        print(f"Telegram xətası: {e}")

def check_and_send_schedule():
    url = "https://ticket.ady.az/api/v1/routes"
    
    # Cloudflare/403 bloklamasını keçmək üçün tam Brauzer başlıqları (Headers)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "az,az-AZ;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://ticket.ady.az/",
        "Origin": "https://ticket.ady.az",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        
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

                if ("baku" in from_st or "bakı" in from_st) and ("tbilisi" in to_st or "tiflis" in to_st):
                    if available_seats > 0:
                        baku_tbilisi_list.append(f"📅 {date_str} — <b>{price} AZN</b>")

                if ("tbilisi" in from_st or "tiflis" in from_st) and ("baku" in to_st or "bakı" in to_st):
                    if available_seats > 0:
                        tbilisi_baku_list.append(f"📅 {date_str} — <b>{price} AZN</b>")

            msg_lines = ["<b>🎫 ADY Biletləri (Test Mesajı)</b>\n"]

            msg_lines.append("🚂 <b>Tbilisi ➔ Bakı:</b>")
            if tbilisi_baku_list:
                msg_lines.extend(tbilisi_baku_list)
            else:
                msg_lines.append("— hazırda bilet yoxdur")

            msg_lines.append("")

            msg_lines.append(f"🚂 <b>Bakı ➔ Tbilisi ({len(baku_tbilisi_list)}):</b>")
            if baku_tbilisi_list:
                msg_lines.extend(baku_tbilisi_list)
            else:
                msg_lines.append("— hazırda bilet yoxdur")

            msg_lines.append("\n👉 <a href='https://ticket.ady.az'>ticket.ady.az</a>")

            full_message = "\n".join(msg_lines)

            res = send_telegram_message(full_message)
            print("Siyahı kanala atıldı:", res)

        else:
            print(f"API xətası: {response.status_code}")
    except Exception as e:
        print(f"Xəta: {e}")

if __name__ == "__main__":
    print("Bot işə düşdü...")
    while True:
        try:
            check_and_send_schedule()
            time.sleep(90)
        except Exception as main_error:
            print(f"Loop xətası: {main_error}")
            time.sleep(30)
