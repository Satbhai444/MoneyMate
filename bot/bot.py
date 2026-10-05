import os
import logging
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app for Webhook & Health check
app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    # TODO: Upsert user in Supabase
    
    keyboard = [
        [InlineKeyboardButton("Add Expense", callback_data="add_expense"),
         InlineKeyboardButton("Add Income", callback_data="add_income")],
        [InlineKeyboardButton("Monthly Report", callback_data="report")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to MoneyMate! Send me your expenses in natural language, e.g., '20 ki water bottle'.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle free text messages by sending them to Gemini parser."""
    text = update.message.text
    # TODO: Pass text to Gemini parser
    # TODO: Save to Supabase
    await update.message.reply_text(f"Received: {text}\n(Parser integration pending...)")

# TODO: Add handlers for /menu, /owed, /undo, /report and CallbackQueries

def main() -> None:
    """Start the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN provided!")
        return

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run polling (For local dev. Webhook will be used for production)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
