import requests, telebot, io, random
TOKEN = "8093135920:AAFGm0JYeytgv4SBpRV-PeYbbiBrmjER0Ew"
CHANNEL = "@st00rg"
bot = telebot.TeleBot(TOKEN)

headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.tikwm.com/"}

def get_tiktok():
    try:
        r = requests.post("https://www.tikwm.com/api/feed/search", data={"keywords":"funny cat dog","count":"20","hd":"1"}, headers=headers, timeout=20).json()
        videos = r['data']['videos']
        random.shuffle(videos)
        for v in videos[:5]:
            url = v.get('hdplay') or v.get('play')
            if not url: continue
            data = requests.get(url, headers=headers, timeout=40).content
            if len(data) > 500000 and b'ftyp' in data[:30]: # فيديو حقيقي وبيه صوت
                return data, v.get('title','فيديو مضحك جديد 😂')
    except Exception as e:
        print(e)
    return None, None

video_data, title = get_tiktok()

# اذا فشل تيك توك، استخدم فيديو مضمون
if not video_data:
    print("Fallback to backup")
    video_data = requests.get("https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4", timeout=20).content
    title = "فيديو مضحك جديد 😂"

f = io.BytesIO(video_data)
f.name = "video.mp4"
bot.send_video(CHANNEL, f, caption=f"{title}\n\n#مضحك #تيك_توك #st00rg\nتابعونا: @st00rg", supports_streaming=True)
print("Posted!")
