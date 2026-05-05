""" 
Since this bot is written with 'PyTelegramBotAPI', typically will be ran in Telegram
but by changing API Helper of this library, it also can be used for Bale app,
which here it is our case.
* For Telegram the api should be: https://api.telegram.org
* For Bale the api should be: https://tapi.bale.ai
"""

from telebot import TeleBot, types
from config import BOT_Bale_TOKEN, BOT_TEL_TOKEN
from Convertors.utils.Convertors import Resistor
from time import time
from collections import defaultdict

# Bot's token
bot = TeleBot(token=BOT_Bale_TOKEN)

# A dict to store user's data and status - ideally we use database
user_data = {}


welcome_msg = """
    📟 *Hey there! Please select your component*
    For now only - *Resistor* - is available but other components will be added soon too.
    *Need help?* Send /help to learn how to use this Bot!
    """

#-------------------
# Helper Functions
#-------------------

# Rate limiting storage
last_command_time = defaultdict(float)

def is_rate_limited(chat_id, cooldown_seconds=2):
    now = time()
    if now - last_command_time[chat_id] < cooldown_seconds:
        return True
    last_command_time[chat_id] = now
    return False


def send_help_message(chat_id):
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



#-------------------
# Keyboards
#-------------------
def get_component_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    components = ["Resistor"]
    for component in components:
        keyboard.add(types.InlineKeyboardButton(component, callback_data=f"Select_component:{component}"))
    return keyboard

def get_subtype_keyboard(component):
    keyboard = types.InlineKeyboardMarkup()
    subtypes = ["DIP", "SMD"]
    for subtype in subtypes:
        keyboard.add(types.InlineKeyboardButton(subtype, callback_data=f"Select_subtype:{component}:{subtype}"))
    keyboard.add(types.InlineKeyboardButton("Back", callback_data="Back_to_components"))
    return keyboard

def get_result_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    btns = [("🔄 New Calculation", "new"), ("❓ Help", "help")]
    for label, action in btns:
        keyboard.add(types.InlineKeyboardButton(label, callback_data=f"action:{action}"))
    return keyboard


#-------------------
# Handlers
#-------------------
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_data[message.chat.id] = {}
    bot.reply_to(message, welcome_msg,
                  reply_markup=get_component_keyboard())

@bot.message_handler(commands=["help"])
def send_help(message):
    send_help_message(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith(("Select_component:")))
def callback_select_component(call):
    component = call.data.split(":")[1].strip()
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    user_data[chat_id] = {"component": component}

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f"{component} was selected, Now select its subtype.",
        reply_markup=get_subtype_keyboard(component)
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "Back_to_components")
def callback_back_to_component(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_data[chat_id] = {}  # removed duplicate line

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Please select your component; For now only *Resistor* is available but other components will be added soon too.",
        reply_markup=get_component_keyboard()
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith(("Select_subtype:")))
def callback_select_subtype(call):
    _, component, subtype = call.data.split(":")
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    user_data[chat_id]["subtype"] = subtype

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f"{subtype} was selected for {component.strip()}, Now enter your band.\nHint:\n- DIP: brown-black-red-gold\n- SMD: 103",
        reply_markup=None
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("action:"))
def handle_result_actions(call):
    action = call.data.split(":")[1]
    chat_id = call.message.chat.id
    
    if action == "new":
        user_data[chat_id] = {}
        bot.send_message(
            chat_id=chat_id,
            text="Select a component (Only resistor available):",
            reply_markup=get_component_keyboard()
        )
    elif action == "help":
        send_help_message(chat_id)
    
    bot.answer_callback_query(call.id)  # single answer at the end


@bot.message_handler(
        func=lambda message: message.chat.id in user_data and
          "component" in user_data[message.chat.id] and
            "subtype" in user_data[message.chat.id])
def handle_value_input(message):
    chat_id = message.chat.id

    # Rate limiting check
    if is_rate_limited(chat_id):
        bot.reply_to(message, "⏱️ Please slow down. Wait a moment before sending another command.")
        return
    
    component = (user_data[chat_id]["component"]).lower()
    subtype = user_data[chat_id]["subtype"]
    value = message.text

    status_msg = bot.send_message(chat_id, "⏳ Calculating...")
    bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        if component == "resistor":
            band, result = Resistor().Run(type=subtype, value=value, stat=False)

            bot.delete_message(chat_id, status_msg.message_id)
            
            bot.send_message(
                chat_id,
                f"{band}\n{result}",
                reply_markup=get_result_keyboard()
                )

    except Exception as e:
        bot.delete_message(chat_id, status_msg.message_id)
        bot.reply_to(message, f"Calculation failed. Please check your input format.\n{e}")

    finally:
        user_data[chat_id] = {}


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(message, "To start, Send /start command!")


if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()

