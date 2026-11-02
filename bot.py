import requests, telebot, random
TOKEN = "8093135920:AAFGm0JYeytgv4SBpRV-PeYbbiBrmjER0Ew"
CHANNEL = "@st00rg"
bot = telebot.TeleBot(TOKEN)
headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.tikwm.com/"}
def get_video():
    try:
        data = {"keywords": "funny", "count": 20, "cursor": 0, "hd": 1}
        r = requests.post("https://www.tikwm.com/api/feed/search", data=data, headers=headers, timeout=30).json()
        vids = r['data']['videos']
        for _ in range(5):
            v = random.choice(vids)
            play_url = v.get('play') or v.get('hdplay') or v.get('wmplay')
            if play_url:
                vb = requests.get(play_url, headers=headers, timeout=60).content
                if len(vb) > 100000:
                    return vb, v.get('title','فيديو مضحك جديد 😂')
    except Exception as e:
        print(e)
    return requests.get("https://www.w3schools.com/html/mov_bbb.mp4").content, "فيديو مضحك 😂"
video_bytes, caption = get_video()
bot.send_video(CHANNEL, video_bytes, caption=f"{caption}\n\n#مضحك #تيك_توك #st00rg\n\nتابعونا: @st00rg")
