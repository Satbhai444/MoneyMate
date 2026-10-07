import os
import logging
import asyncio
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
from pydantic import BaseModel, Field
from db import upsert_user, save_transaction
# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    genai_client = genai.Client(api_key=GEMINI_API_KEY)
else:
    genai_client = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_msg = (
        f"Namaste {user.mention_html()}! 🙏\n\n"
        f"Main <b>MoneyMate</b> hoon - aapka apna personal AI finance manager. 💼\n\n"
        f"Paison ka hisaab rakhna hamesha boring lagta hai na? Apps open karo, form bharo, category select karo... ab ye sab chhod dijiye!\n\n"
        f"Ab se aapko sirf mujhe text karna hai, jaise aap apne kisi dost ko WhatsApp ya Telegram pe karte hain. "
        f"Chahe aap Hindi me likhein, Hinglish me, ya English me... Main sab samajh jaunga! 🧠💡\n\n"
        f"<b>Aap aise try kar sakte hain:</b>\n"
        f"📝 <i>\"Aaj subah chai aur nashte pe ₹150 kharch hue\"</i>\n"
        f"📝 <i>\"Lent 500 to Rahul for movie tickets\"</i>\n"
        f"📝 <i>\"Got 2000 from client as advance\"</i>\n\n"
        f"Bataiye, aaj ka pehla hisaab kya hai? 💸"
    )
    await update.message.reply_html(welcome_msg)

async def process_with_gemini(text: str, user) -> str:
    if not genai_client:
        return "⚠️ <b>Gemini API Key missing!</b>\n\nPlease add your `GEMINI_API_KEY` to the `.env` file and restart the bot."
    
    prompt = f"""
    You are an AI financial assistant. Extract ALL transactions from the following user message:
    "{text}"
    
    Respond STRICTLY in JSON format as a list of objects matching the following schema. Even if there is only one transaction, return a list.
    [
      {{
          "amount": 0.0,
          "currency": "INR",
          "category": "String (e.g., Food, Travel, Rent, Salary)",
          "transaction_type": "expense|income|lent|borrowed",
          "description": "String (Detailed info like 'gave to anant' or 'lunch at mcdonalds')"
      }}
    ]
    Do not include markdown blocks like ```json ... ```, just output the raw JSON string.
    """
    try:
        # Run synchronous Gemini call in a thread to prevent blocking
        response = await asyncio.to_thread(
            genai_client.models.generate_content,
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        response_text = response.text.strip()
        
        # Clean up potential markdown formatting just in case
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        data_list = json.loads(response_text.strip())
        if not isinstance(data_list, list):
            data_list = [data_list] # Fallback
            
        # Ensure user exists in DB
        db_user = upsert_user(user.id, user.full_name)
        db_user_id = db_user.get("id") if db_user else None
            
        reply = "✅ <b>Transaction Parsed Successfully!</b>\n\n"
        for i, data in enumerate(data_list):
            if db_user_id:
                save_transaction(db_user_id, data)
                
            emoji = "🔴" if data.get("transaction_type") in ["expense", "lent"] else "🟢"
            reply += (
                f"<b>{i+1}. Type:</b> {emoji} {str(data.get('transaction_type', '')).capitalize()}\n"
                f"   <b>Amount:</b> {data.get('currency', 'INR')} {data.get('amount')}\n"
                f"   <b>Category:</b> 🏷️ {data.get('category')}\n"
                f"   <b>Details:</b> 📝 {data.get('description')}\n\n"
            )
            
        if db_user_id:
            reply += f"<i>(✅ Data saved to database successfully)</i>"
        else:
            reply += f"<i>(⚠️ Database saving features coming soon...)</i>"
        return reply
    except Exception as e:
        logger.error(f"Error calling Gemini: {e}")
        return "❌ Maaf karna, main aapka message theek se samajh nahi paya. Kya aap thoda details de sakte hain?"

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a link to the web dashboard when /report is issued."""
    user = update.effective_user
    db_user = upsert_user(user.id, user.full_name)
    token = db_user.get("dashboard_token") if db_user else ""
    
    dashboard_url = os.getenv("DASHBOARD_BASE_URL", "http://localhost:3000").rstrip("/")
    if token:
        full_url = f"{dashboard_url}/dashboard.html?token={token}"
    else:
        full_url = f"{dashboard_url}/dashboard.html"
        
    await update.message.reply_html(
        f"📊 <b>Aapka Finance Report yahan hai:</b>\n\n"
        f"Is link par click karein aur apna pura dashboard dekhein:\n"
        f"🔗 <a href='{full_url}'>{full_url}</a>\n\n"
        f"<i>(Dashboard is live!)</i>"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parse user message using Gemini AI."""
    text = update.message.text
    
    # 1. Send quick waiting message so user doesn't feel it's slow
    wait_message = await update.message.reply_text("⏳ AI aapka message padh raha hai...")
    
    # 2. Show typing indicator
    await update.message.chat.send_action(action="typing")
    
    # 3. Process text
    reply_html = await process_with_gemini(text, update.effective_user)
    
    # 4. Edit the waiting message with the actual parsed result
    await wait_message.edit_text(reply_html, parse_mode="HTML")

def main() -> None:
    """Start the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        logger.error("TELEGRAM_BOT_TOKEN is not set in .env file!")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("report", report))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
