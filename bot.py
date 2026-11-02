import requests, telebot, io, random
TOKEN = "8093135920:AAFGm0JYeytgv4SBpRV-PeYbbiBrmjER0Ew"
CHANNEL = "@st00rg"
bot = telebot.TeleBot(TOKEN)

headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.tikwm.com/"}

def get_trending_video():
    # 3 طرق لسحب الترند
    apis_to_try = [
        # 1- ترند العراق
        {"url": "https://www.tikwm.com/api/feed/list", "data": {"count": 30, "region": "IQ", "hd": 1}},
        # 2- ترند عالمي مضحك
        {"url": "https://www.tikwm.com/api/feed/search", "data": {"keywords": "funny fyp viral", "count": 30, "hd": 1}},
        # 3- ترند هاشتاك fyp
        {"url": "https://www.tikwm.com/api/hashtag/posts", "data": {"hashtag": "fyp", "count": 30}},
    ]
    
    for api in apis_to_try:
        try:
            print(f"Trying trending from: {api['url']}")
            r = requests.post(api['url'], data=api['data'], headers=headers, timeout=25).json()
            
            videos = []
            if 'data' in r:
                if 'videos' in r['data']:
                    videos = r['data']['videos']
                elif isinstance(r['data'], list):
                    videos = r['data']
                elif 'data' in r['data']:
                    videos = r['data']['data']
            
            if not videos and 'data' in r and 'videos' not in r['data']:
                # بعض الاحيان يرجع مصفوفة مباشرة
                videos = r.get('data', []) if isinstance(r.get('data'), list) else []

            print(f"Found {len(videos)} trending videos")
            random.shuffle(videos)
            
            for v in videos[:10]: # نجرب 10 فيديوهات من الترند
                video_url = v.get('hdplay') or v.get('play') or v.get('wmplay')
                if not video_url:
                    continue
                data = requests.get(video_url, headers=headers, timeout=40).content
                # نتأكد فيديو حقيقي وبيه صوت (اكبر من 500KB وبيه ftyp)
                if len(data) > 500000 and b'ftyp' in data[:30]:
                    title = v.get('title') or v.get('desc') or "🔥 فيديو ترند مضحك"
                    print(f"Got trending video: {title[:30]} - {len(data)} bytes")
                    return data, title
        except Exception as e:
            print(f"Trending API failed: {e}")
            continue
    return None, None

video_data, title = get_trending_video()

# اذا فشل الترند لسبب ما، جيب من البحث المضحك
if not video_data:
    print("Trending failed, fallback to funny search")
    try:
        r = requests.post("https://www.tikwm.com/api/feed/search", data={"keywords":"funny cat iraq", "count":"20", "hd":"1"}, headers=headers, timeout=20).json()
        v = random.choice(r['data']['videos'])
        url = v.get('hdplay') or v.get('play')
        video_data = requests.get(url, headers=headers, timeout=40).content
        title = v.get('title','فيديو مضحك ترند 😂')
    except:
        video_data = None

if not video_data:
    # اخر حل
    raise Exception("No video found")

f = io.BytesIO(video_data)
f.name = "video.mp4"

# كابشن ترند
caption = f"🔥 {title}\n\n😂 من ترند تيك توك اليوم\n#ترند #مضحك #تيك_توك #fyp #viral\nتابعونا: @st00rg"

bot.send_video(CHANNEL, f, caption=caption, supports_streaming=True)
print("Posted trending video!")
