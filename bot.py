import requests, telebot, io
TOKEN = "8093135920:AAFGm0JYeytgv4SBpRV-PeYbbiBrmjER0Ew"
CHANNEL = "@st00rg"
bot = telebot.TeleBot(TOKEN)

# فيديو مضحك حقيقي مضمون بيه صوت ويشتغل بتيليجرام
BACKUP_URL = "https://www.w3schools.com/html/mov_bbb.mp4"

def get_valid_video():
    # نحاول نجيب من تيك توك
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.tikwm.com/"}
        r = requests.post("https://www.tikwm.com/api/feed/search", data={"keywords":"funny","count":"5","hd":"1"}, headers=headers, timeout=20).json()
        url = r['data']['videos'][0]['hdplay']
        data = requests.get(url, headers=headers, timeout=40).content
        # نتأكد انه فيديو حقيقي مو صفحة خطأ
        if data[:4] != b'\x00\x00\x00' and b'ftyp' not in data[:20]:
            raise Exception("not mp4")
        if len(data) > 300000:
            return data, r['data']['videos'][0].get('title','فيديو مضحك 😂')
    except Exception as e:
        print(f"TikTok fail: {e}")
    
    # اذا فشل، نجيب الفيديو المضمون الي بيه صوت
    print("Using backup")
    return requests.get(BACKUP_URL, timeout=20).content, "فيديو مضحك جديد 😂"

video_data, caption = get_valid_video()

# هاي الحركة المهمة الي تصلح 00:00
video_file = io.BytesIO(video_data)
video_file.name = "video.mp4"

bot.send_video(CHANNEL, video_file, caption=f"{caption}\n\n#مضحك #تيك_توك\nتابعونا: @st00rg", supports_streaming=True)
print("Done!")
