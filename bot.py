import requests, telebot, random

TOKEN = "8093135920:AAFGm0JYeytgv4SBpRV-PeYbbiBrmjER0Ew"
CHANNEL = "@st00rg"

bot = telebot.TeleBot(TOKEN)

headers = {"User-Agent": "Mozilla/5.0"}

# قائمة فيديوهات مضحكة جاهزة اذا تيك توك فشل
BACKUP_VIDEOS = [
    "https://test-videos.co.uk/vids/sintel/mp4/h264/720/Sintel_720_10s_1MB.mp4"
]

def get_tiktok_video():
    try:
        # مصدر جديد يشتغل بكيت هاب
        url = "https://www.tikwm.com/api/feed/search"
        params = {"keywords": "مضحك", "count": "10"}
        r = requests.post(url, data=params, headers=headers, timeout=20).json()
        videos = r['data']['videos']
        v = random.choice(videos)
        return v['play'], v.get('title','فيديو مضحك 😂')
    except Exception as e:
        print(f"TikWM fail: {e}")
        return BACKUP_VIDEOS[0], "فيديو مضحك جديد 😂"

play_url, title = get_tiktok_video()
print(f"Downloading: {play_url}")

video_data = requests.get(play_url, headers=headers, timeout=60).content

bot.send_video(CHANNEL, video_data, caption=f"{title}\n\n#مضحك #تيك_توك #st00rg\n\nتابعونا: @st00rg")
print("Posted with video!")
