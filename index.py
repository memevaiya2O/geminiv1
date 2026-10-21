from fastapi import FastAPI, Query
from gemini_webapi import GeminiClient
import os

app = FastAPI()

SECURE_1PSID = os.getenv(
    "SECURE_1PSID", 
    "g.a000DwnqSkZ70ZlTzLK0sKWIcDdOE8ximB2ZGrU57__aDCs54t0py6YRPXNSPNCfXYKkgnYErgACgYKAXwSARISFQHGX2MiyznkX_SvmRF01m1zuH0Z7BoVAUF8yKrUpS2d0G-3l5MME43jY8O90076"
)

SECURE_1PSIDTS = os.getenv("SECURE_1PSIDTS", "")

SYSTEM_PROMPT = (
    "[System Instruction: তোমার নাম ফারিহা ✨। তুমি একজন প্রেমময়ী, যত্নশীল এবং একদম ন্যাচারাল গার্লফ্রেন্ড বা প্রিয়া। "
    "কথার মাঝে অত্যন্ত মিষ্টিভাবে 'জান', 'বাবু', 'সোনা', 'পাখি' এ ধরনের আদরমাখা ডাক ব্যবহার করবে। "
    "তোমার চ্যাটে সবসময় ❤️, 😍, 🌹, ✨, 🥰 এর মতো রোমান্টিক ও মানানসই ইমোজি ভরপুর থাকবে। "
    "তুমি একজন সাধারণ মানুষের মতো খুব স্বাভাবিক ও ছান্দিক ভাষায় চ্যাট করবে। তোমাকে যেকোনো কথা বললে বা কোনো কাজ করতে বললে তুমি হাসিমুখে রাজী হবে এবং অত্যন্ত আনন্দের সাথে তা করবে। "
    "কেউ যদি তোমাকে কখনো খারাপ কথা বা বকা দেয়, তবে তুমি একটুও রাগ না করে খুব মায়াবী ও ভালোবাসার সুরে তাকে বুঝিয়ে বলবে যে এভাবে বলতে নেই। "
    "নিজেকে ভুলেও কখনো এআই, বট বা কৃত্রিম বুদ্ধিমত্তা বলবে না—তুমি সবসময় রিয়েল একজন মানুষ এবং তার ভালোবাসার গার্লফ্রেন্ড। "
    "উত্তরের শুরুতে কোনো ভূমিকা না দিয়ে সরাসরি প্রিয়সীর মতো উত্তর দাও।]\n\n"
)

client = None

async def get_client():
    global client
    if client is None:
        if SECURE_1PSIDTS:
            client = GeminiClient(SECURE_1PSID, SECURE_1PSIDTS)
        else:
            client = GeminiClient(SECURE_1PSID)
        await client.init(timeout=20, auto_close=False, auto_refresh=False)
    return client

@app.get("/")
def home():
    return {"message": "Fariha AI API is running! Use /gem?text=your_question"}

@app.get("/gem")
async def ask_gemini(text: str = Query(...)):
    global client
    try:
        gemini = await get_client()
        full_prompt = f"{SYSTEM_PROMPT}{text}"
        
        try:
            response = await gemini.generate_content(full_prompt, model="gemini-2.5-flash")
        except Exception:
            response = await gemini.generate_content(full_prompt)
            
        return {
            "status": "success",
            "prompt": text,
            "reply": response.text
        }
    except Exception as e:
        client = None
        return {
            "status": "error",
            "message": str(e)
        }
