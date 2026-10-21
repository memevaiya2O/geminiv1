from fastapi import FastAPI, Query
from gemini_webapi import GeminiClient
import os

app = FastAPI()

# আপনার দেওয়া __Secure-1PSID
SECURE_1PSID = os.getenv(
    "SECURE_1PSID", 
    "g.a000DwnqSkZ70ZlTzLK0sKWIcDdOE8ximB2ZGrU57__aDCs54t0py6YRPXNSPNCfXYKkgnYErgACgYKAXwSARISFQHGX2MiyznkX_SvmRF01m1zuH0Z7BoVAUF8yKrUpS2d0G-3l5MME43jY8O90076"
)

# যদি ব্রাউজারে __Secure-1PSIDTS পান, তবে নিচের ফাঁকা কোটেশনের ভেতর বসাবেন
SECURE_1PSIDTS = os.getenv("SECURE_1PSIDTS", "")

@app.get("/")
def home():
    return {"message": "Gemini API is running! Use /gem?text=your_question"}

@app.get("/gem")
async def ask_gemini(text: str = Query(..., description="আপনার প্রশ্ন লিখুন")):
    try:
        if SECURE_1PSIDTS:
            client = GeminiClient(SECURE_1PSID, SECURE_1PSIDTS)
        else:
            client = GeminiClient(SECURE_1PSID)
            
        await client.init(timeout=30, auto_close=False, auto_refresh=False)
        
        response = await client.generate_content(text)
        
        return {
            "status": "success",
            "prompt": text,
            "reply": response.text
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "hint": "যদি কুকি এরর দেখায়, তবে ব্রাউজার থেকে __Secure-1PSIDTS কুকিটিও কপি করে SECURE_1PSIDTS এ বসান।"
        }
