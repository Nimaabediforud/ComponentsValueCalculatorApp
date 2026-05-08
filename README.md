# 🔧 ComponentsValueCalculatorApp

A **multi‑platform electronic component calculator** – starting with resistors. The core logic is separated from the interface, allowing easy expansion to other components and platforms.

## 🎯 Project Vision

This repository is designed as a **flexible, expandable framework**:

- **Core engine** – `convertors/` module (resistor decoder, room for capacitors, inductors, etc.)
- **Interfaces** – Currently a **Telegram/Bale bot**; a website or mobile app can be added later in separate folders.

## ✨ Current Features

### Core Engine (`convertors/`)
- Decodes DIP resistors (3, 4, 5, 6 bands)
- Decodes SMD resistors (3‑digit, 4‑digit with `R` and tolerance letters)
- Detects jumpers (`black`, `o`, `000`)
- Unit conversion (Ω, kΩ, MΩ, GΩ, TΩ)

### Bot Interface (`bot/`)
- **Modular, registry‑based design** – easy to add new components
- **Inline keyboards** – component selection, subtype, result actions (New Calculation, Save, Help)
- **Persistent reply keyboard (main menu)** – buttons for My Saved, Help, Clear All Saved, New Calc, Start
- **SQLite database** – users table, saved results table, duplicate prevention
- **Rate limiting** – prevents spam
- **Save & recall** – save calculation results, list them with `/saved`, clear with `/clear_saved`
- Works on **Telegram** and **Bale** (Iranian platform) with a simple API change

## 💬 Commands & Buttons

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and show main menu |
| `/help`  | Show detailed help |
| `/saved` | List your saved calculation results |
| `/clear_saved` | Delete all your saved results |

**Persistent menu buttons** (appear above keyboard after `/start`):
- 📋 My Saved → `/saved`
- ❓ Help → `/help`
- 🗑️ Clear All Saved → `/clear_saved`
- 🧮 New Calc → Start a new calculation
- ✅ Start → Same as `/start`

## ⚙️ Usage

1. Send `/start` (or tap ✅ Start)
2. Choose a component (Resistor – more coming soon)
3. Choose subtype (DIP or SMD)
4. Enter the color bands (e.g., `brown-black-red-gold`) or SMD label (e.g., `103` or `4R7`)
5. After result, use inline buttons to **New** (start over), **Save** (store in database), or **Help**

## 💡 Example

**DIP:**  
Input: `brown-black-red-gold`  
Output: `1000 Ω ± 5%`

**SMD:**  
Input: `103`  
Output: `10 kΩ`

## 📁 Project Structure

```
ComponentsValueCalculatorApp/
├── convertors/ # Core calculation engine
│ ├── notebook/
│ │ └── Prototyping.ipynb
│ └── utils/
│ ├── Convertors.py # Resistor class
│ ├── utilities.py # Validate class
│ └── main.py
├── bot/ # Bot interface
│ ├── main.py # Entry point
│ ├── handlers.py # BotHandlers class (all logic)
│ ├── keyboards.py # Inline keyboards
│ ├── utils.py # Rate limiter, help, welcome message
│ ├── state.py # In-memory user_data
│ ├── config.py # Tokens (gitignored)
│ ├── database/
│ │ ├── init.py
│ │ └── db.py # SQLite helpers
│ └── modules/
│ ├── init.py # Registry, get_component()
│ └── components.py # ResistorComponent (others in future)
├── requirements.txt
└── README.md
```

## 📄 License

MIT

