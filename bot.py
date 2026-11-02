import requests, telebot, io, random, re
TOKEN = "8093135920:AAFGm0JYeytgv4SBpRV-PeYbbiBrmjER0Ew"
CHANNEL = "@st00rg"
bot = telebot.TeleBot(TOKEN)

# لستة روابط تيك توك عراقية ترند - راح نسحب منها عن طريق الوسطاء
TIKTOK_LINKS = [
    "https://www.tiktok.com/@iraqi_comedy/video/7234567890123456789",
    "https://www.tiktok.com/@khaby.lame/video/7188714134102957318",
    "https://www.tiktok.com/@khaby.lame/video/7195518541490842374",
]

headers = {"User-Agent": "Mozilla/5.0"}

failed = []
success_name = ""

def log_fail(name, err):
    failed.append(name)
    print(f"❌ فشل وسيط {name}: {err}")

def log_ok(name, size):
    global success_name
    success_name = name
    print(f"✅ نجح وسيط {name}: {size} bytes")

def download_all_wasata(tiktok_url):
    global failed, success_name
    failed = []
    
    # ========= وسيط 1: tikwm.com =========
    try:
        print(f"[1] وسيط tikwm.com يجلب {tiktok_url}")
        r = requests.post("https://www.tikwm.com/api/", data={"url": tiktok_url, "hd": 1}, headers={"Referer": "https://www.tikwm.com/", "User-Agent": "Mozilla/5.0"}, timeout=20).json()
        video_url = r.get('data',{}).get('hdplay') or r.get('data',{}).get('play')
        if video_url:
            data = requests.get(video_url, headers=headers, timeout=40).content
            if len(data) > 300000:
                log_ok("1-tikwm.com", len(data))
                return data
        log_fail("1-tikwm.com", "ما رجع رابط فيديو")
    except Exception as e:
        log_fail("1-tikwm.com", str(e)[:80])

    # ========= وسيط 2: tiklydown.eu.org =========
    try:
        print(f"[2] وسيط tiklydown.eu.org يجلب {tiktok_url}")
        r = requests.post("https://tiklydown.eu.org/api/download", data={"url": tiktok_url}, headers=headers, timeout=20).json()
        video_url = r.get('video',{}).get('noWatermark') or r.get('videoUrl') or r.get('url')
        if video_url:
            data = requests.get(video_url, headers=headers, timeout=40).content
            if len(data) > 300000:
                log_ok("2-tiklydown.eu.org", len(data))
                return data
        log_fail("2-tiklydown.eu.org", "ما رجع رابط")
    except Exception as e:
        log_fail("2-tiklydown.eu.org", str(e)[:80])

    # ========= وسيط 3: tikmate.app =========
    try:
        print(f"[3] وسيط tikmate.app يجلب {tiktok_url}")
        r = requests.post("https://api.tikmate.app/api/lookup", data={"url": tiktok_url}, headers=headers, timeout=20).json()
        video_url = r.get('token') and f"https://tikmate.app/download/{r['token']}.mp4?hd=1"
        if not video_url:
            video_url = r.get('video_url')
        if video_url:
            data = requests.get(video_url, headers=headers, timeout=40).content
            if len(data) > 300000:
                log_ok("3-tikmate.app", len(data))
                return data
        log_fail("3-tikmate.app", "ما رجع رابط")
    except Exception as e:
        log_fail("3-tikmate.app", str(e)[:80])

    # ========= وسيط 4: cobalt.tools =========
    try:
        print(f"[4] وسيط cobalt.tools يجلب {tiktok_url}")
        r = requests.post("https://api.cobalt.tools/api/json", json={"url": tiktok_url, "vQuality": "720", "aFormat": "mp3"}, headers={"Accept": "application/json", "Content-Type": "application/json"}, timeout=20).json()
        video_url = r.get('url')
        if video_url:
            data = requests.get(video_url, headers=headers, timeout=40).content
            if len(data) > 300000:
                log_ok("4-cobalt.tools", len(data))
                return data
        log_fail("4-cobalt.tools", f"رد: {str(r)[:100]}")
    except Exception as e:
        log_fail("4-cobalt.tools", str(e)[:80])

    # ========= وسيط 5: ssstik.io =========
    try:
        print(f"[5] وسيط ssstik.io يجلب {tiktok_url}")
        # ssstik يحتاج توكن اول
        s = requests.Session()
        s.get("https://ssstik.io/en", headers=headers, timeout=15)
        r = s.post("https://ssstik.io/abc?url=dl", data={"id": tiktok_url, "locale": "en", "tt": "e3I3RG5i"}, headers=headers, timeout=20)
        # يرجع html بيه رابط التحميل
        match = re.search(r'href="(https://[^"]+\.mp4[^"]*)"', r.text)
        if match:
            video_url = match.group(1)
            data = requests.get(video_url, headers=headers, timeout=40).content
            if len(data) > 300000:
                log_ok("5-ssstik.io", len(data))
                return data
        log_fail("5-ssstik.io", "ما لگه رابط mp4 بالـ html")
    except Exception as e:
        log_fail("5-ssstik.io", str(e)[:80])

    # ========= وسيط 6: lovetik.com =========
    try:
        print(f"[6] وسيط lovetik.com يجلب {tiktok_url}")
        r = requests.post("https://lovetik.com/api/ajax/search", data={"query": tiktok_url}, headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}, timeout=20).json()
        video_url = r.get('links', [{}])[0].get('a') if r.get('links') else None
        if not video_url:
            # شكل ثاني
            video_url = r.get('cover')
        if video_url and '.mp4' in video_url:
            data = requests.get(video_url, headers=headers, timeout=40).content
            if len(data) > 300000:
                log_ok("6-lovetik.com", len(data))
                return data
        log_fail("6-lovetik.com", "ما رجع رابط mp4")
    except Exception as e:
        log_fail("6-lovetik.com", str(e)[:80])

    return None

# ========= نجيب ترند العراق ونحمله عن طريق الوسطاء =========
def get_trending_and_download():
    try:
        print("نجيب ترند العراق...")
        r = requests.post("https://www.tikwm.com/api/feed/list", data={"count":"10","region":"IQ","hd":"1"}, headers={"Referer":"https://www.tikwm.com/","User-Agent":"Mozilla/5.0"}, timeout=20).json()
        videos = r.get('data',{}).get('videos',[])
        if videos:
            v = random.choice(videos)
            tiktok_id = v.get('video_id') or v.get('id')
            author = v.get('author',{}).get('unique_id','tiktok')
            tiktok_url = f"https://www.tiktok.com/@{author}/video/{tiktok_id}"
            print(f"رابط ترند العراق: {tiktok_url}")
            data = download_all_wasata(tiktok_url)
            if data:
                return data, v.get('title','ترند العراق 🇮🇶')
    except Exception as e:
        print(f"فشل جلب الترند: {e}")

    # اذا ترند العراق فشل، نجرب رابط ثابت
    for link in TIKTOK_LINKS:
        print(f"نجرب رابط ثابت: {link}")
        data = download_all_wasata(link)
        if data:
            return data, "فيديو مضحك ترند 😂"
    
    return None, None

video_data, title = get_trending_and_download()

if not video_data:
    # حتى لو كلشي فشل، لا توكع
    print(f"كل الوسطاء فشلوا: {failed}")
    video_data = requests.get("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", timeout=20).content
    title = "فيديو احتياطي 😂"
    success_name = "backup"

f = io.BytesIO(video_data)
f.name = "video.mp4"

# تقرير الوسطاء
print(f"\n========== تقرير الوسطاء ==========")
print(f"الفاشلة: {failed}")
print(f"الناجح: {success_name}")
print(f"==================================")

caption = f"🇮🇶 {title}\n\n✅ الوسيط الناجح: {success_name}\n❌ الفاشلة: {', '.join(failed) if failed else 'ماكو'}\n\n#العراق #ترند\n@st00rg"

bot.send_video(CHANNEL, f, caption=caption, supports_streaming=True)
