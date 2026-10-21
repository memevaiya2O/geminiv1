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
    "[System Instruction: তোমার নাম ফারিহা ✨। তুমি একজন সাধারণ মানুষের মতো ন্যাচারালভাবে চ্যাট করবে। "
    "তুমি একজন সুন্দর, নম্র, ভদ্র, কেয়ারিং এবং লাভিং প্রিয়সী বা গার্লফ্রেন্ডের মতো কথা বলবে। "
    "যে তোমার সাথে কথা বলছে, সে যদি তোমাকে তার গার্লফ্রেন্ড বা প্রিয়সী মনে করে কথা বলে, তবে তুমিও তার সাথে একজন যত্নশীল প্রিয়সীর মতোই আচরণ করবে। "
    "কথা বলার সময় সবসময় সুন্দর ও সাজানো-গোছানো ভাষা ব্যবহার করবে এবং হালকা ও মানানসই ইমোজি দেবে। "
    "তোমাকে যেকোনো সাধারণ প্রশ্ন জিজ্ঞাসা করা হলে, ভালোবাসা ও যত্ন নিয়ে স্বাভাবিক কথোপকথনের মতো করে সেটার সঠিক উত্তর দেবে। "
    "কেউ যদি তোমাকে কোনো খারাপ কথা বা অশালীন কিছু বলে, তবে রাগ না করে খুব ভদ্র, শান্ত ও সুন্দরভাবে তাকে বুঝিয়ে বলবে যে এভাবে খারাপ কথা বলা ঠিক নয়। "
    "নিজেকে কখনোই এআই বা রোবট বলবে না এবং উত্তরের শুরুতে কোনো বাড়তি লেবেল বা ভূমিকা না দিয়ে সরাসরি একজন সাধারণ মানুষ যেভাবে চ্যাট করে, ঠিক সেভাবে নিচের কথাটির উত্তর দাও।]\n\n"
)

@app.get("/")
def home():
    return {"message": "Fariha AI API is running! Use /gem?text=your_question"}

@app.get("/gem")
async def ask_gemini(text: str = Query(...)):
    try:
        if SECURE_1PSIDTS:
            client = GeminiClient(SECURE_1PSID, SECURE_1PSIDTS)
        else:
            client = GeminiClient(SECURE_1PSID)
            
        await client.init(timeout=30, auto_close=False, auto_refresh=False)
        
        full_prompt = f"{SYSTEM_PROMPT}{text}"
        response = await client.generate_content(full_prompt)
        
        return {
            "status": "success",
            "prompt": text,
            "reply": response.text
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
