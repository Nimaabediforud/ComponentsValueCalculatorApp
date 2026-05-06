""" 
Since this bot is written with 'PyTelegramBotAPI', typically will be ran in Telegram
but by changing API Helper of this library, it also can be used for Bale app,
which here it is our case.
* For Telegram the api should be: https://api.telegram.org
* For Bale the api should be: https://tapi.bale.ai
"""

from telebot import TeleBot
from config import BOT_Bale_TOKEN, BOT_TEL_TOKEN
from handlers import BotHandlers


# Bot's token
bot = TeleBot(token=BOT_Bale_TOKEN)
BotHandlers(bot)   # registers all handlers

if __name__ == "__main__":
    print("Bot running...")
    bot.infinity_polling()

