from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards import get_component_keyboard, get_subtype_keyboard, get_result_keyboard
from utils import is_rate_limited, send_help_message, welcome_msg
from state import user_data
from modules import get_component
from database.db import ensure_user, save_result, is_result_saved, get_saved_results, clear_saved_results

class BotHandlers:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.last_result = {}
        self._register()

    # ---------- Persistent Menu ----------
    def show_main_menu(self, chat_id):
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        kb.add(KeyboardButton("✅ Start"))
        kb.add(KeyboardButton("📋 My Saved"), KeyboardButton("❓ Help"))
        kb.add(KeyboardButton("🗑️ Clear All Saved"), KeyboardButton("🧮 New Calc"))
        self.bot.send_message(chat_id, "*Hey there! 🙂👋🏻*", reply_markup=kb)

    # ---------- Command Logic (shared) ----------
    def cmd_saved(self, chat_id):
        results = get_saved_results(chat_id)
        if not results:
            self.bot.send_message(chat_id, "No saved results.")
            return
        msg = "*Saved:*\n"
        num = 1
        for comp, sub, inp, out, _ in results[:10]:
            msg += f"{num}• {comp.upper()} ({sub}) `{inp}` →\n {out}\n\n"
            num += 1
        self.bot.send_message(chat_id, msg, parse_mode="Markdown")

    def cmd_clear_saved(self, chat_id):
        clear_saved_results(chat_id)
        self.bot.send_message(chat_id, "🗑️ Cleared all saved results.")

    def cmd_help(self, chat_id):
        send_help_message(chat_id, self.bot)

        
    # ---------- Handler Registration ----------
    def _register(self):
        # ---- Commands ----
        @self.bot.message_handler(commands=["start"])
        def send_welcome(message):
            user_data[message.chat.id] = {}
            self.show_main_menu(message.chat.id)
            self.bot.reply_to(message, welcome_msg, reply_markup=get_component_keyboard())

        @self.bot.message_handler(commands=["help"])
        def send_help(message):
            self.cmd_help(message.chat.id)

        @self.bot.message_handler(commands=["saved"])
        def saved_cmd(message):
            self.cmd_saved(message.chat.id)

        # ---- Reply Keyboard Handlers (friendly text ➔ command) ----
        @self.bot.message_handler(func=lambda m: m.text == "✅ Start")
        def on_start_btn(m):
            # Reuse /start logic
            user_data[m.chat.id] = {}
            self.show_main_menu(m.chat.id)
            self.bot.reply_to(m, welcome_msg, reply_markup=get_component_keyboard())
        
        @self.bot.message_handler(func=lambda m: m.text == "📋 My Saved")
        def on_my_saved(m):
            self.cmd_saved(m.chat.id)

        @self.bot.message_handler(func=lambda m: m.text == "❓ Help")
        def on_help_btn(m):
            self.cmd_help(m.chat.id)

        @self.bot.message_handler(func=lambda m: m.text == "🗑️ Clear All Saved")
        def on_clear_btn(m):
            self.cmd_clear_saved(m.chat.id)

        @self.bot.message_handler(func=lambda m: m.text == "🧮 New Calc")
        def on_new_calc_btn(m):
            chat_id = m.chat.id
            user_data[chat_id] = {}
            self.bot.send_message(chat_id, "Select a component:", reply_markup=get_component_keyboard())

        # ---- Inline Callbacks ----
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith("Select_component:"))
        def callback_select_component(call):
            component = call.data.split(":")[1].strip()
            chat_id = call.message.chat.id
            msg_id = call.message.message_id
            user_data[chat_id] = {"component": component}
            self.bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text=f"{component.upper()} selected. Choose subtype:",
                reply_markup=get_subtype_keyboard(component)
            )
            self.bot.answer_callback_query(call.id)

        @self.bot.callback_query_handler(func=lambda call: call.data == "Back_to_components")
        def callback_back(call):
            chat_id = call.message.chat.id
            msg_id = call.message.message_id
            user_data[chat_id] = {}
            self.bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text="Select component:",
                reply_markup=get_component_keyboard()
            )
            self.bot.answer_callback_query(call.id)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith("Select_subtype:"))
        def callback_select_subtype(call):
            _, component, subtype = call.data.split(":")
            chat_id = call.message.chat.id
            msg_id = call.message.message_id
            user_data[chat_id]["subtype"] = subtype
            self.bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text=f"""{subtype} selected for {component.upper()}. Enter your value:
                *Hint:*\n\tDIP: `brown-black-red-gold` → 1 kΩ ± 5%\n\tSMD: `103` → 10 kΩ""",
                reply_markup=None
            )
            self.bot.answer_callback_query(call.id)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith("action:"))
        def handle_result_actions(call):
            action = call.data.split(":")[1]
            chat_id = call.message.chat.id

            if action == "new":
                user_data[chat_id] = {}
                self.bot.send_message(chat_id, "Select component:", reply_markup=get_component_keyboard())
            elif action == "save":
                data = self.last_result.get(chat_id)
                if data:
                    if is_result_saved(chat_id, data['output']):
                        self.bot.answer_callback_query(call.id, "⚠️ Already saved!", show_alert=False)
                    else:
                        ensure_user(chat_id)
                        save_result(chat_id, data['component'], data['subtype'], data['input'], data['output'])
                        self.bot.answer_callback_query(call.id, "✅ Saved!", show_alert=False)
                else:
                    self.bot.answer_callback_query(call.id, "Nothing to save.", show_alert=True)

            elif action == "help":
                self.cmd_help(chat_id)
                self.bot.answer_callback_query(call.id)

        # ---- Value Input Handler ----
        @self.bot.message_handler(func=lambda m: m.chat.id in user_data and
                                  "component" in user_data[m.chat.id] and
                                  "subtype" in user_data[m.chat.id])
        def handle_value_input(message):
            chat_id = message.chat.id
            if is_rate_limited(chat_id):
                self.bot.reply_to(message, "⏱️ Slow down!")
                return

            comp_name = user_data[chat_id]["component"].lower()
            subtype = user_data[chat_id]["subtype"]
            comp = get_component(comp_name)
            if not comp:
                self.bot.reply_to(message, f"Component '{comp_name}' not supported.")
                return

            status = self.bot.send_message(chat_id, "⏳ Calculating...")
            self.bot.send_chat_action(chat_id, "typing")

            try:
                band, result = comp.run(subtype, message.text)
                self.bot.delete_message(chat_id, status.message_id)
                self.bot.send_message(chat_id, f"{band}\n{result}", reply_markup=get_result_keyboard())
                # Store last result for /save button
                self.last_result[chat_id] = {
                    'output': f"{band}\n{result}",
                    'input': message.text,
                    'component': comp_name,
                    'subtype': subtype
                }
            except Exception as e:
                self.bot.delete_message(chat_id, status.message_id)
                self.bot.reply_to(message, f"Error: {e}")
            finally:
                user_data[chat_id] = {}

        # ---- Fallback ----
        @self.bot.message_handler(func=lambda m: True)
        def fallback(message):
            self.bot.reply_to(message, "Send /start to begin.")