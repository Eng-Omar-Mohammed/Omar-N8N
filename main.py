from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import requests, os, hashlib
from datetime import datetime
from bs4 import BeautifulSoup
import google.generativeai as genai
import uvicorn

app = FastAPI()

# --- 1. الإعدادات (Settings) ---
# كدة الكود هيسحب المفتاح من إعدادات Render السرية اللي عملناها سوا
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# بيانات التلجرام والـ Chat ID
TELEGRAM_TOKEN = "8400309248:AAH0AWN14iMWBkv2F_FWoj8H7EJ7LIHa0c8"
CHAT_ID = "1323838034"

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

@app.get("/real_ai")
def real_ai(prompt: str):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') 
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        return {"result": f"AI Error: {str(e)}"}

@app.get("/call_service")
async def call_service(name: str, data: str = ""):
    name_lower = name.lower()
    if "telegram" in name_lower:
        return {"result": send_to_telegram(f"طلب من {name}: {data}")}
    
    # محاكاة الخدمات التانية بالذكاء الاصطناعي
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt_ai = f"أنت محرك n8n. المستخدم فعل نود {name} ببيانات: {data}. رد باختصار."
        response = model.generate_content(prompt_ai)
        return {"result": f"{response.text}"}
    except:
        return {"result": f"تم تفعيل {name} بنجاح!"}

# --- 4. التشغيل ---
# تأكد إن مجلد static موجود وجواه index.html
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    # البورت ده للتشغيل المحلي، Render بيستخدم بورت متغير لوحده
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
