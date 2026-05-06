from telebot import TeleBot
from keyboards import get_component_keyboard, get_subtype_keyboard, get_result_keyboard
from utils import is_rate_limited, send_help_message, welcome_msg
from state import user_data
from modules import get_component


class BotHandlers:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self._register()

    def _register(self):
        # Commands
        @self.bot.message_handler(commands=["start"])
        def send_welcome(message):
            user_data[message.chat.id] = {}
            self.bot.reply_to(message, welcome_msg,
                        reply_markup=get_component_keyboard())

        @self.bot.message_handler(commands=["help"])
        def send_help(message):
            send_help_message(message.chat.id, self.bot)


        # Component Selection
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(("Select_component:")))
        def callback_select_component(call):
            component = call.data.split(":")[1].strip()
            chat_id = call.message.chat.id
            message_id = call.message.message_id

            user_data[chat_id] = {"component": component}

            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"{component} was selected, Now select its subtype.",
                reply_markup=get_subtype_keyboard(component)
            )
            self.bot.answer_callback_query(call.id)

        @self.bot.callback_query_handler(func=lambda call: call.data == "Back_to_components")
        def callback_back_to_component(call):
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            user_data[chat_id] = {}  # removed duplicate line

            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="Please select your component; For now only *Resistor* is available but other components will be added soon too.",
                reply_markup=get_component_keyboard()
            )
            self.bot.answer_callback_query(call.id)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(("Select_subtype:")))
        def callback_select_subtype(call):
            _, component, subtype = call.data.split(":")
            chat_id = call.message.chat.id
            message_id = call.message.message_id

            user_data[chat_id]["subtype"] = subtype

            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"{subtype} was selected for {component.strip()}, Now enter your band.\nHint:\n- DIP: brown-black-red-gold\n- SMD: 103",
                reply_markup=None
            )
            self.bot.answer_callback_query(call.id)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith("action:"))
        def handle_result_actions(call):
            action = call.data.split(":")[1]
            chat_id = call.message.chat.id
            
            if action == "new":
                user_data[chat_id] = {}
                self.bot.send_message(
                    chat_id=chat_id,
                    text="Select a component (Only resistor available):",
                    reply_markup=get_component_keyboard()
                )
            elif action == "help":
                send_help_message(chat_id, self.bot)
            
            self.bot.answer_callback_query(call.id)  # single answer at the end


        @self.bot.message_handler(
                func=lambda message: message.chat.id in user_data and
                "component" in user_data[message.chat.id] and
                    "subtype" in user_data[message.chat.id])
        def handle_value_input(message):
            chat_id = message.chat.id

            # Rate limiting check
            if is_rate_limited(chat_id):
                self.bot.reply_to(message, "⏱️ Please slow down. Wait a moment before sending another command.")
                return
            
            comp_name = user_data[chat_id]["component"].lower()
            subtype = user_data[chat_id]["subtype"]
            comp = get_component(comp_name)
            value = message.text

            if not comp:
                self.bot.reply_to(message, f"Component '{comp_name}' not supported.")
                return

            status_msg = self.bot.send_message(chat_id, "⏳ Calculating...")
            self.bot.send_chat_action(chat_id=chat_id, action="typing")

            try:
                
                band, result = comp.run(subtype, value)

                self.bot.delete_message(chat_id, status_msg.message_id)
                
                self.bot.send_message(
                    chat_id,
                    f"{band}\n{result}",
                    reply_markup=get_result_keyboard()
                    )

            except Exception as e:
                self.bot.delete_message(chat_id, status_msg.message_id)
                self.bot.reply_to(message, f"Calculation failed. Please check your input format.\n{e}")

            finally:
                user_data[chat_id] = {}

        # Fallback
        @self.bot.message_handler(func=lambda message: True)
        def handle_other_messages(message):
            self.bot.reply_to(message, "To start, Send /start command!")

