import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
TOKEN = os.getenv("BOT_TOKEN")
async def reply_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower() if update.message.text else ""
    if "hello" in text or "hi" in text:
        await update.message.reply_text("Hello! 👋 How can I help you?")
    else:
        await update.message.reply_text(f"You said: {update.message.text}")
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_hello))
    print("Bot is running...")
    app.run_polling()
