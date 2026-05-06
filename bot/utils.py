from telebot import TeleBot
from time import time
from collections import defaultdict


#-------------------
# Helper Functions
#-------------------

welcome_msg = """
    📟 *Hey there! Please select your component*
    For now only - *Resistor* - is available but other components will be added soon too.
    *Need help?* Send /help to learn how to use this Bot!
    """

# Rate limiting storage
last_command_time = defaultdict(float)

def is_rate_limited(chat_id, cooldown_seconds=2):
    now = time()
    if now - last_command_time[chat_id] < cooldown_seconds:
        return True
    last_command_time[chat_id] = now
    return False


def send_help_message(chat_id: int, bot: TeleBot):
    help_text = """
    📟 *Components Value Calculator Bot*

    *Commands:*
    /start - Start the bot and select component
    /help - Show this help message

    *How to use:*
    1. Select component (Resistor)
    2. Choose subtype (DIP or SMD)
    3. Enter color bands or label

    *Examples:*
    • DIP: `brown-black-red-gold`
    • SMD: `103` or `4R7` or `2210`

    *Supported:* 3-6 band DIP resistors, 3-4 digit SMD resistors with R and tolerance letters.

    Send /start to begin.
    """
    bot.send_message(chat_id, help_text, parse_mode="Markdown")


