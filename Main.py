import time
import requests
from telegram import Bot

# ===== Данные твоего бота =====
TOKEN = "8475771928:AAF48FGvNohJTfd64I3AN19TXoyQKhYZxQ8"
CHAT_ID = 3765995683   # chat_id твоего канала
CHECK_INTERVAL = 60
API_URL = "https://alerts.in.ua/api/states"

bot = Bot(token=TOKEN)
last_state = False

def check_alert():
    global last_state
    try:
        data = requests.get(API_URL, timeout=10).json()
        alert_now = False

        for region in data:
            if region["name"] == "Одеська область":
                for district in region["districts"]:
                    if district["name"] == "Одеський район":
                        alert_now = district["alert"]

        if alert_now and not last_state:
            bot.send_message(chat_id=CHAT_ID, text="🚨 ПОВІТРЯНА ТРИВОГА")
            last_state = True

        elif not alert_now and last_state:
            bot.send_message(chat_id=CHAT_ID, text="✅ ТРИВОГА ВІДБІЙ")
            last_state = False

    except Exception as e:
        print("Помилка:", e)

while True:
    check_alert()
    time.sleep(CHECK_INTERVAL)