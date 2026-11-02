import requests, telebot, random, os

TOKEN = "8093135920:AAFGm0JYeytgv4SBpRV-PeYbbiBrmjER0Ew"
CHANNEL = "@st00rg"

bot = telebot.TeleBot(TOKEN)

def post_one():
    try:
        # مصدر ما ينحجب بكيت هاب
        api = "https://www.tikwm.com/api/feed/list?count=5"
        data = requests.get(api, timeout=20).json()
        videos = data['data']['videos']
        v = random.choice(videos)
        
        video_url = v['play']
        caption = v.get('title', 'فيديو جديد 🔥')[:200]
        
        video_bytes = requests.get(video_url, timeout=40).content
        
        bot.send_video(CHANNEL, video_bytes, caption=f"{caption}\n\n@st00rg")
        print("DONE")
    except Exception as e:
        print(f"Error: {e}")
        # اذا فشل يحاول مصدر ثاني
        try:
            bot.send_message(CHANNEL, f"فيديو جديد 🔥\n\n@st00rg")
        except: pass

post_one()
