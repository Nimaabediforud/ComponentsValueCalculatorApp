from telebot import types
from modules import get_component_names

#-------------------
# Keyboards
#-------------------
def get_component_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    #components = ["Resistor"]
    for component in get_component_names():
        keyboard.add(types.InlineKeyboardButton(component.capitalize(), callback_data=f"Select_component:{component}"))
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
    btns = [("🔄 New Calc", "new"), ("❓ Help", "help"), ("💾 Save", "save")]
    for label, action in btns:
        keyboard.add(types.InlineKeyboardButton(label, callback_data=f"action:{action}"))
    return keyboard

