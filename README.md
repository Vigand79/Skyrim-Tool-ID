# 🐉 Skyrim Tool ID (v1.1)
**Dynamic Database Utility for Skyrim SE & AE**

Skyrim Tool ID scans your **personal load order** via SSEEdit to provide 100% working IDs for items, spells, and NPCs, including those from mods.

## ✨ v1.1 New Features
- **Universal Batch System:** Generates `toolid.txt` in your game folder. Use `bat toolid` in-game for complex actions.
- **NPC Action Menu:** Dropdown for Kill, Resurrect, Teleport, and Clone.
- **Physical .PAS Script:** Automatically writes `ExportToolID.pas` to your SSEEdit folder.
- **Localized Races:** Displays races in a clean format (e.g. [Nord], [Imperial]).

## 🛠 How to Use
1. Click **"1. GENERA DATABASE"** and select your SSEEdit folder.
2. In SSEEdit: Right Click mods -> **Apply Script** -> **ExportVigand**.
3. In Game: Click **COPY** for items (CTRL+V) or **APPLICA** for NPCs (`bat toolid`).

## 📂 Security & Build (For Staff)
Complete source code provided in `.py`. Compiled with **PyInstaller** for standalone compatibility.
**Build Command:** 
`python -m PyInstaller --noconsole --onefile --clean --icon=logo.ico --add-data "logo.ico;." Skyrim_Tool_ID.py`
