import requests, telebot, io, random
TOKEN = "8093135920:AAFGm0JYeytgv4SBpRV-PeYbbiBrmjER0Ew"
CHANNEL = "@st00rg"
bot = telebot.TeleBot(TOKEN)

headers = {"User-Agent": "Mozilla/5.0"}

def download_new_wasata(tiktok_url):
    failed = []
    
    # وسيط جديد 1: musicaldown.com
    try:
        print("[1] musicaldown.com")
        r = requests.post("https://musicaldown.com/api/download", data={"url": tiktok_url}, headers=headers, timeout=20).json()
        video_url = r.get('video') or r.get('data',{}).get('video')
        if video_url:
            data = requests.get(video_url, timeout=30).content
            if len(data) > 300000: return data, "1-musicaldown"
        failed.append("1-musicaldown")
    except Exception as e:
        print(f"فشل 1: {e}"); failed.append("1-musicaldown")

    # وسيط جديد 2: savetik.co
    try:
        print("[2] savetik.co")
        r = requests.post("https://savetik.co/api/ajaxSearch", data={"q": tiktok_url, "lang": "en"}, headers=headers, timeout=20).json()
        video_url = r.get('data') or r.get('links',{}).get('download')
        if video_url and '.mp4' in str(video_url):
            # يستخرج الرابط
            import re
            m = re.search(r'https?://[^"]+\.mp4[^"]*', str(r))
            if m:
                data = requests.get(m.group(0), timeout=30).content
                if len(data) > 300000: return data, "2-savetik"
        failed.append("2-savetik")
    except Exception as e:
        print(f"فشل 2: {e}"); failed.append("2-savetik")

    # وسيط جديد 3: snaptik.app
    try:
        print("[3] snaptik.app")
        s = requests.Session()
        s.get("https://snaptik.app/en", headers=headers, timeout=15)
        r = s.post("https://snaptik.app/abc2.php", data={"url": tiktok_url}, headers=headers, timeout=20)
        import re
        m = re.search(r'https?://[^"]+\.mp4[^"]*', r.text)
        if m:
            data = requests.get(m.group(0), headers=headers, timeout=30).content
            if len(data) > 300000: return data, "3-snaptik"
        failed.append("3-snaptik")
    except Exception as e:
        print(f"فشل 3: {e}"); failed.append("3-snaptik")

    # اذا كل الجدد فشلوا - فيديو مضمون صغير 1MB بيه صوت
    print("كل الجدد فشلوا - احتياطي مضمون")
    url = "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4"
    data = requests.get(url, timeout=20).content
    return data, f"backup - فشلة: {','.join(failed)}"

# نجرب ترند عراقي عن طريق الوسطاء الجدد
tiktok_url = "https://www.tiktok.com/@khaby.lame/video/7188714134102957318"
video_data, waseet_name = download_new_wasata(tiktok_url)

f = io.BytesIO(video_data)
f.name = "video.mp4"
bot.send_video(CHANNEL, f, caption=f"🇮🇶 ترند العراق\n✅ وسيط: {waseet_name}\n@st00rg", supports_streaming=True)
print(f"تم عن طريق: {waseet_name}")
