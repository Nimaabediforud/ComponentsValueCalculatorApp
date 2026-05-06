# 🔧 ComponentsValueCalculatorApp

A **multi‑platform electronic component calculator** – starting with resistors. The core logic is separated from the interface, allowing easy expansion to other components and platforms.

## 🎯 Project Vision

This repository is designed as a **flexible, expandable framework**:

- **Core engine** – `convertors/` module (resistor decoder, room for capacitors, inductors, etc.)
- **Interfaces** – Currently a **Telegram/Bale bot**; a website or mobile app can be added later in separate folders.

## ✨ Current Features (Resistor Module)

### Core Engine (`convertors/`)
- Decodes DIP resistors (3, 4, 5, 6 bands)
- Decodes SMD resistors (3‑digit, 4‑digit with `R` and tolerance letters)
- Detects jumpers (`black`, `o`, `000`)
- Unit conversion (Ω, kΩ, MΩ, GΩ, TΩ)

### Bot Interface (`bot/`)
- **Modular, registry‑based design** – easy to add new components
- Inline keyboard navigation (component → subtype → input)
- Rate limiting, help command, result action buttons
- Works on **Telegram** and **Bale** (Iranian platform) with a simple API change

## 💬 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and select a component |
| `/help`  | Show help message |

## ⚙️ Usage

1. Send `/start`
2. Choose a component (Resistor – more coming soon)
3. Choose subtype (DIP or SMD)
4. Enter the color bands (e.g., `brown-black-red-gold`) or SMD label (e.g., `103` or `4R7`)

## 💡 Example

**DIP:**  
Input: `brown-black-red-gold`  
Output: `1000 Ω ± 5%`

**SMD:**  
Input: `103`  
Output: `10 kΩ`

## 📁 Project Structure (Current)

```
ComponentsValueCalculatorApp/
├── convertors/ # Core calculation engine
│ ├── notebook/
│ │ └── Prototyping.ipynb # Initial experiments
│ └── utils/
│ ├── Convertors.py # Resistor logic (class Resistor)
│ ├── utilities.py # Helper functions (Validate class)
│ └── main.py # (optional test script)
├── bot/ # Bot interface
│ ├── main.py # Entry point
│ ├── handlers.py # Class‑based handlers (BotHandlers)
│ ├── keyboards.py # Inline keyboards (generic)
│ ├── utils.py # Rate limiter, helpers, welcome message
│ ├── state.py # In‑memory user_data dict
│ ├── config.py # Tokens (gitignored)
│ └── modules/
│ ├── init.py # COMPONENTS registry, get_component()
│ └── components.py # All component classes (ResistorComponent, etc.)
├── requirements.txt
└── README.md
```

## 📄 License

MIT


