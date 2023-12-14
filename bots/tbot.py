import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
        InlineKeyboardButton("⭐️", callback_data='2'),
        InlineKeyboardButton("⭐️⭐️", callback_data='3'),
        InlineKeyboardButton("⭐️⭐️⭐️", callback_data='4')],
        [InlineKeyboardButton("🗑", callback_data='1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    #await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi!", reply_markup=reply_markup)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo="/Users/d.katargin/Pictures/IMG_1342.JPG", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("PUSH THE BUTTON!")

if __name__ == '__main__':
    application = ApplicationBuilder().token('***').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()