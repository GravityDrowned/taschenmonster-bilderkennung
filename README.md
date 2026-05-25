# Pokémon Auto Battle Bot

OCR-driven Nintendo Switch controller automation for Pokémon battles.

---

## How It Works

```
Webcam
      │
      ▼
OpenCV — captures live frames (frame skips 59/60)
      │
      ▼
python-doctr OCR — extracts text from frame
      │
      ▼
State Machine — matches OCR text → game state
      │
      ▼
nxbt — emits Pro Controller button presses over Bluetooth
      │
      ▼
Nintendo Switch
```

Each 60th frame captured from the webcam is passed to a pre-trained docTR OCR model. The resulting text is checked for known substrings to identify the current game state. Based on detected states, the bot triggers the appropriate Pro Controller button sequences via an `nxbt` virtual controller connected over Bluetooth.

---

## Detected States

| State Key | Trigger Text (OCR) | Controller Action |
|-----------|-------------------|-------------------|
| `in_progress` | `Matchmaking` | No action (detection only) |
| `team_selection` | `send into battle` | Selects 3 Pokémon, navigates down 4, confirms team |
| `combat_fight_or_team` | `Battle info` | No action (detection only) |
| `mega_evolve` | `MEGA EVOLVE` | Presses R |
| `combat_attack` | `FIGHT` | Presses A twice |
| `combat_switch` | `Moves` | D-pad down, then A twice |
| `continue` | `Continue Battling` | Presses A twice |

---

## Requirements

- Python ≥ 3.11
- [`uv`](https://github.com/astral-sh/uv) package manager
- **Linux only** — `nxbt` depends on BlueZ and dbus; macOS and Windows are not supported
- Bluetooth adapter on the host machine

---

## Installation

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install nxbt separately (not in pyproject.toml)
pip install nxbt
# nxbt may also require dbus permissions — see nxbt documentation

# Install project dependencies
uv sync

# Run the bot
uv run main.py
```

---

## Project Structure

```
pkmn/
├── main.py          # Entry point: video capture loop and OCR
├── state_machine.py # Substring-based text → game state mapping
├── controller.py    # nxbt Pro Controller button sequences per state
└── pyproject.toml   # Project dependencies (managed by uv)
```

---

## Known Limitations

- `nxbt` is not declared in `pyproject.toml` and must be installed separately
- OCR accuracy depends on video resolution and quality; low-quality captures may fail to trigger states
- Only the default webcam (device index 0) is used — no CLI option to select a different capture device
