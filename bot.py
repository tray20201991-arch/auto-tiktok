import telebot, requests, random, time, threading
from flask import Flask

TOKEN = "8093135920:AAGqzb8HIOE1Pda1vIoyFlGXx1xtOVPc490"
CHANNEL_ID = "@st00rg"
BOT_TAG = "@st00rg" # بصمتك

CATEGORIES = [
    {"name": "مضحك", "tags": "#مضحك #ضحك #نكات #فيديو_مضحك #ترند_العراق #st00rg"},
    {"name": "افلام", "tags": "#افلام #فلم #سينما #افلام_قصيرة #ترند_افلام #st00rg"},
    {"name": "كرة", "tags": "#كرة_قدم #رياضة #اهداف #ترند_رياضي #st00rg"},
    {"name": "ترند", "tags": "#ترند #اكسبلور #تيك_توك #ترند_اليوم #viral #st00rg"},
]

bot = telebot.TeleBot(TOKEN)
posted = set()
app = Flask(__name__)

@app.route('/')
def home():
    return f"✅ بوت {CHANNEL_ID} شغال - ينشر كل 5 دقايق<br>القناة: https://t.me/st00rg"

def get_video():
    try:
        r = requests.get("https://www.tikwm.com/api/feed/list?count=30", 
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=15).json()
        videos = [v for v in r['data']['videos'] if v['video_id'] not in posted]
        if not videos:
            posted.clear()
            videos = r['data']['videos']
        v = random.choice(videos)
        posted.add(v['video_id'])
        return v
    except Exception as e:
        print(f"جلب فشل: {e}")
        return None

def auto_poster():
    print(f"🚀 بدأ النشر لقناة {CHANNEL_ID}")
    while True:
        for cat in CATEGORIES:
            try:
                v = get_video()
                if not v:
                    time.sleep(30)
                    continue
                
                caption = f"""{v['title'][:120]}

{cat['tags']}
📌 الفئة: {cat['name']} | ترند
🔗 https://t.me/st00rg
"""
                bot.send_video(CHANNEL_ID, v['wmplay'], caption=caption)
                print(f"✅ نشر {cat['name']}")
                time.sleep(300) # 5 دقايق بين فيديو
            except Exception as e:
                print(f"خطأ: {e}")
                time.sleep(60)

threading.Thread(target=auto_poster, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
