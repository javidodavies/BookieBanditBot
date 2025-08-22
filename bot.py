import requests
import datetime
import pytz
import schedule
import time
from telegram import Bot

# ==============================
# CONFIGURATION
# ==============================

API_KEY = "cf3eda70df4892406c2ae4c8c0e3edc3"   # API-Football key
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"

TELEGRAM_TOKEN = "8126200866:AAHIKHfsNnbCfO99kPJXDvOyHgpFjLS-dV4"
CHAT_ID = "@BookieBanditBot"   # channel username (must add bot as admin!)

TIMEZONE = "Europe/London"
bot = Bot(token=TELEGRAM_TOKEN)

# ==============================
# FETCH FIXTURES
# ==============================
def get_fixtures():
    today = datetime.date.today()
    three_days = today + datetime.timedelta(days=3)
    
    url = f"{BASE_URL}/fixtures"
    headers = {
        "x-apisports-key": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "from": str(today),
        "to": str(three_days),
        "season": "2025",
        "timezone": "Europe/London"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# ==============================
# STRATEGY LOGIC
# ==============================
def generate_ticket(fixtures):
    matches = fixtures.get("response", [])[:10]
    
    ticket = "🏆 *Golden Goal Daily Ticket*\n\n"
    for i, match in enumerate(matches, start=1):
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        league = match["league"]["name"]
        
        if "Championship" in league or "Ligue 2" in league or "Serie B" in league:
            market = "Double Chance + Under 4.5 ✅"
        else:
            market = "Over 1.5 Goals ⚽"
        
        ticket += f"{i}. {home} vs {away} ({league}) → {market}\n"
    
    return ticket

# ==============================
# TELEGRAM SEND
# ==============================
def send_to_telegram(message):
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

# ==============================
# MAIN JOB
# ==============================
def job():
    fixtures = get_fixtures()
    ticket = generate_ticket(fixtures)
    send_to_telegram(ticket)
    print("✅ Ticket sent to Telegram at", datetime.datetime.now())

# ==============================
# SCHEDULER – RUN AT 8 AM DAILY
# ==============================
schedule.every().day.at("08:00").do(job)

print("📅 Bot started. Will post every day at 08:00.")

while True:
    schedule.run_pending()
    time.sleep(30)
