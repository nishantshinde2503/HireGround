from flask import Flask, jsonify
from main import fetch_and_save_jobs
from threading import Thread
import time
from datetime import datetime
import pytz

app = Flask(__name__)

# 🌏 IST Timezone
IST = pytz.timezone('Asia/Kolkata')

# 🌀 Smart Refresh Logic
def smart_auto_refresher():
    while True:
        now = datetime.now(IST)
        hour = now.hour

        if 8 <= hour < 22:
            interval = 20 * 60  # ✅ 20 mins (Daytime)
            print(f"🕒 {now.strftime('%H:%M')} — Day Refresh: Every 20 mins")
        else:
            interval = 60 * 60  # ✅ 60 mins (Night)
            print(f"🌙 {now.strftime('%H:%M')} — Night Refresh: Every 1 hour")

        result = fetch_and_save_jobs()
        print(f"✅ {len(result.get('results', []))} jobs fetched @ {now.strftime('%d-%b %I:%M %p')}")

        time.sleep(interval)

# 🚀 Background auto-refresh thread
def start_background_refresh():
    thread = Thread(target=smart_auto_refresher, daemon=True)
    thread.start()

# 🧠 Manual refresh trigger (if needed)
@app.route("/refresh", methods=["GET"])
def manual_refresh():
    result = fetch_and_save_jobs()
    return jsonify({"status": "triggered", "fetched": len(result.get('results', []))})

if __name__ == "__main__":
    start_background_refresh()
    app.run(debug=True)
