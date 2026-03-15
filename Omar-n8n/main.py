from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import requests, os, pyautogui, hashlib
from datetime import datetime
from bs4 import BeautifulSoup
import google.generativeai as genai
import uvicorn

app = FastAPI()

# --- 1. الإعدادات (Settings) ---
# الـ API Key بتاعك يا بطل
genai.configure(api_key="AIzaSyCOlMDub2JPNwZaSOwf3LTNFMezLhUWPRM")

# بيانات التلجرام والـ Chat ID
TELEGRAM_TOKEN = "8400309248:AAH0AWN14iMWBkv2F_FWoj8H7EJ7LIHa0c8"
CHAT_ID = "1323838034"

# التأكد من وجود مجلد حفظ لقطات الشاشة
if not os.path.exists("static/screenshots"):
    os.makedirs("static/screenshots")

# --- 2. الوظائف المساعدة ---
def send_to_telegram(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        payload = {"chat_id": CHAT_ID, "text": text}
        response = requests.post(url, json=payload, timeout=10)
        return "وصلت موبايلك! ✈️" if response.status_code == 200 else "خطأ في التلجرام"
    except:
        return "فشل الاتصال بتلجرام"

# --- 3. المسارات (Routes) ---

# أ) نود الذكاء الاصطناعي الحقيقي (تصليح الـ 404)
@app.get("/real_ai")
def real_ai(prompt: str):
    try:
        # استخدام الموديل الصحيح والمستقر
        model = genai.GenerativeModel('gemini-1.5-flash') 
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        print(f"AI Debug Error: {str(e)}")
        # لو الفلاش لسه عامل مشكلة، السيرفر هيرد بالسبب الحقيقي
        return {"result": f"AI Error: {str(e)}"}

# ب) المحرك الشامل للطريق التاني
@app.get("/call_service")
async def call_service(name: str, data: str = ""):
    name_lower = name.lower()
    
    if "telegram" in name_lower:
        return {"result": send_to_telegram(f"طلب من {name}: {data}")}
    
    if "screenshot" in name_lower:
        path = f"static/screenshots/auto_{datetime.now().strftime('%H%M%S')}.png"
        pyautogui.screenshot(path)
        return {"result": "تم تصوير الشاشة بنجاح 📸"}

    # محاكاة الـ 450 نود بالذكاء الاصطناعي
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt_ai = f"أنت محرك n8n. المستخدم فعل نود {name} ببيانات: {data}. رد باختصار كأنك الخدمة."
        response = model.generate_content(prompt_ai)
        return {"result": f"{response.text} (ذكاء {name})"}
    except:
        return {"result": f"تم تفعيل {name} بنجاح!"}

# ج) باقي العمليات (منطق وتلخيص)
@app.get("/core_logic")
def core_logic(node_type: str, data: str):
    if node_type == "If Condition":
        res = "True ✅" if "مهم" in data or "run" in data.lower() else "False ❌"
        return {"result": res}
    return {"result": "تمت المعالجة"}

@app.get("/summarize")
def summarize(url: str):
    try:
        res = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        text = " ".join([p.text for p in soup.find_all('p')][:2])
        return {"result": f"الملخص: {text[:100]}..."}
    except:
        return {"result": "خطأ في الرابط"}

# --- 4. التشغيل ---
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    # تنبيه: لو بورت 8000 مشغول، غيره لـ 8001
    uvicorn.run(app, host="0.0.0.0", port=8000)