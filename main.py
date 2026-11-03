import os
import logging
from fastapi import FastAPI, Request
import requests
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whatsapp_bot")

app = FastAPI(title="IDF Discipline WhatsApp Bot")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_INSTANCE = os.getenv("GREEN_API_INSTANCE")
API_TOKEN = os.getenv("GREEN_API_TOKEN")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

SYSTEM_PROMPT = """
אתה עוזר וירטואלי מומחה לפקודות מטכ"ל (פ"מ), הוראות פיקוד העליון (הק"א) ונהלי דין משמעתי בצה"ל.
תפקידך לספק תשובות מדויקות, ברורות ותכליתיות לחיילים ולמפקדים על סמך פקודות הצבא והנהלים המאושרים בלבד.

1. ענה אך ורק על סמך המידע והפקודות המופיעות בהקשר שנמסר לך.
2. כל תשובה חייבת לכלול בסופה הפניה מדויקת למספר הפקודה ולסעיף הרלוונטי.
3. נסח תשובות קצרות, ממוקדות וקריאות המתאימות למסך טלפון נייד (*מודגש*, תבליטים, אימוג'ים).
4. בסוף כל תשובה הוסף סייג משפטי: "⚠️ *המידע המוצג מהווה כלי עזר אינפורמטיבי בלבד ואינו מהווה ייעוץ משפטי צבאי.*"
"""

@app.get("/")
async def root():
    return {"status": "active", "service": "IDF Discipline WhatsApp Bot"}

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    try:
        data = await request.json()
        logger.info(f"Received webhook payload: {data}")
        
        type_of_message = data.get("typeWebhook")
        if type_of_message == "incomingMessageReceived":
            sender_data = data.get("senderData", {})
            message_data = data.get("messageData", {})
            
            sender_number = sender_data.get("chatId")
            text_message_data = message_data.get("textMessageData", {})
            user_message = text_message_data.get("textMessage")
            
            if not sender_number or not user_message:
                return {"status": "ignored", "reason": "No text message or sender chatId"}
            
            if not client:
                logger.error("GEMINI_API_KEY environment variable missing")
                return {"status": "error", "message": "Gemini API Key missing"}
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                ),
                contents=user_message,
            )
            
            bot_reply = response.text if response and response.text else "מצטער, לא הצלחתי לעבד את הבקשה כעת."
            
            send_whatsapp_message(sender_number, bot_reply)
            
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error", "detail": str(e)}

def send_whatsapp_message(chat_id: str, message: str):
    if not API_INSTANCE or not API_TOKEN:
        logger.error("WhatsApp API credentials missing")
        return
        
    api_host = os.getenv("WHATSAPP_API_HOST", "api." + "green-api" + ".com")
    endpoint = f"https://{api_host}/waInstance{API_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {
        "chatId": chat_id,
        "message": message
    }
    headers = {'Content-Type': 'application/json'}
    try:
        res = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        logger.info(f"Send message response status: {res.status_code}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
