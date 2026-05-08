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
    /start     – Start the bot and show main menu
    /help      – Show this help message
    /saved     – List your saved calculation results
    /clear_saved – Delete all your saved results

    *Persistent Menu (buttons below text input):*
    📋 My Saved     – Same as /saved
    🗑️ Clear All Saved – Same as /clear_saved
    ❓ Help         – This message
    🧮 New Calc    – Start a new calculation
    ✅ Start       – Same as /start

    *How to calculate:*
    1. Choose a component (Resistor, etc.)
    2. Choose subtype (DIP or SMD)
    3. Enter color bands (e.g., brown-black-red-gold) or SMD code (e.g., 103)

    *After a result:*
    Use inline buttons to New, Save, or get Help.

    *Examples:*
    DIP: `brown-black-red-gold` → 1 kΩ ±5%
    SMD: `103` → 10 kΩ

    Send /start to begin.
    """
    bot.send_message(chat_id, help_text, parse_mode="Markdown")

