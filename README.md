# Py4GW - Guild Wars Python Automation Framework

[![Python](https://img.shields.io/badge/python-3.13.0%20(32--bit)-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Open%20Source-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

**Py4GW** is a comprehensive Python-based automation and play-assist tool for Guild Wars. It provides a sophisticated framework for game interaction, automation scripting, multi-account support, and custom AI through an extensible modular architecture.

---

## 🌟 Features

### Core Capabilities
- **🎮 Direct Game Integration** - Memory-based game state access via native DLL
- **🤖 Advanced Bot Framework** - 100+ configurable automation parameters
- **🧠 Hero AI System** - Intelligent multi-hero combat and party management
- **🗺️ Smart Pathfinding** - NavMesh-based A* pathfinding with obstacle avoidance
- **📦 Inventory Management** - Automated loot filtering, salvaging, and organization
- **🎯 Combat Automation** - Skill rotation, targeting, and buff management
- **🖥️ Rich UI System** - 50+ ImGui-based overlay widgets
- **👥 Multi-Account Support** - IPC-based multiboxing with synchronized actions

### Automation Features
- Combat AI with intelligent targeting and skill usage
- Automated farming, vanquishing, and mission completion
- Party management and hero control
- Quest tracking and completion
- Merchant interaction and trading
- Character switching and account management
- Event-driven automation with behavior trees
- Custom scripting with Python API

### UI & Visualization
- DirectX overlay rendering (2D/3D)
- Customizable ImGui widgets
- In-game calendar and tracker widgets
- Enhanced compass, skillbar, and inventory displays
- Real-time agent and effect visualization
- Frame manipulation for dialog automation

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Core Components](#-core-components)
- [Usage Examples](#-usage-examples)
- [Widgets](#-widgets)
- [Bots](#-bots)
- [Configuration](#-configuration)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [Community](#-community)
- [License](#-license)

---

## 🚀 Installation

### Prerequisites

- **Python 3.13.0 (32-bit)** - **REQUIRED** (64-bit will NOT work)
- **Guild Wars Client** - Installed and running on Windows
- **Windows OS** - Required for DLL support

### Download & Setup

#### Option 1: Download Release (Recommended for Users)

1. Go to the [Releases Page](https://github.com/apoguita/Py4GW/releases/tag/Official)
2. Download the latest release under "Assets"
3. Extract files to your preferred directory
4. Run `Py4GW_Launcher.exe`

#### Option 2: Clone Repository (For Developers)

```bash
# Clone the repository
git clone https://github.com/apoguita/Py4GW.git

# Navigate to directory
cd Py4GW

# All dependencies are bundled - no pip install needed!
# Run the launcher
python Py4GW_LauncherCompact.py
```

### Verification

1. Launch Guild Wars
2. Run `Py4GW_Launcher.exe` or `python Py4GW_LauncherCompact.py`
3. Check that widgets appear in the game overlay
4. Try running a demo script from the `DEMO/` folder

---

## ⚡ Quick Start

### Hello World Example

Create a simple script that interacts with an NPC:

```python
from Py4GWCoreLib import *

MODULE_NAME = "HelloWorld"

def main():
    # Get player agent ID
    player_id = Py4GW.Player.GetAgentID()

    # Get current target
    target_id = Py4GW.Player.GetTargetID()

    if target_id > 0:
        # Interact with targeted agent
        Py4GW.Player.InteractWithAgent(target_id)
        print(f"Interacting with agent {target_id}")
    else:
        print("No target selected!")

if __name__ == "__main__":
    main()
```

### Running Demo Scripts

```bash
# Navigate to DEMO directory
cd DEMO/

# Run agent interaction demo
python DEMO_PyAgent.py

# Run inventory demo
python DEMO_PyInventory.py

# Run ImGui widget demo
python DEMO_PyImGui.py
```

### Creating a Simple Bot

```python
from Py4GWCoreLib import *
from Py4GWCoreLib.Botting import *

class FarmingBot(Bot):
    def __init__(self):
        super().__init__("SimpleFarmer")

    def main_loop(self):
        # Move to farming location
        self.move_to(Vector3(-15000, 20000, 0))

        # Kill nearby enemies
        self.kill_all_in_range(1200)

        # Loot items
        self.pickup_loot()

        # Return to town
        self.return_to_outpost()

bot = FarmingBot()
bot.run()
```

---

## 📂 Project Structure

```
Py4GW/
├── Py4GWCoreLib/              # Core library - game interaction layer
│   ├── Agent.py               # Agent/NPC management
│   ├── Player.py              # Player control
│   ├── Party.py               # Party management
│   ├── Inventory.py           # Inventory operations
│   ├── Skill.py               # Skill definitions
│   ├── Map.py                 # Map/navigation
│   ├── Botting.py             # Bot framework
│   ├── DXOverlay.py           # DirectX rendering
│   ├── ImGui.py               # ImGui wrapper
│   └── py4gwcorelib_src/      # Support modules
│
├── HeroAI/                    # Hero AI automation system
│   ├── combat.py              # Combat handler
│   ├── targeting.py           # Target selection
│   ├── windows.py             # Control UI
│   └── shared_memory_manager.py  # IPC for multiboxing
│
├── Widgets/                   # 50+ UI widgets
│   ├── HeroAI.py              # Hero AI panel
│   ├── LootManager.py         # Loot filtering
│   ├── Travel.py              # Quick travel
│   ├── Calendar.py            # GW calendar
│   └── ...                    # Many more
│
├── Bots/                      # Pre-built bot scripts
│   ├── Proof Of Legend Farmer.py
│   ├── Legendary Guardian.py
│   ├── Vanquish/              # Vanquish bots
│   ├── Challenge Missions/    # Challenge bots
│   └── ...                    # 15+ categories
│
├── DEMO/                      # Example scripts
│   ├── DEMO_PyAgent.py
│   ├── DEMO_PyImGui.py
│   ├── DEMO_PyInventory.py
│   └── ...
│
├── Config/                    # Configuration files
├── Textures/                  # Game textures
├── fonts/                     # Font resources
├── stubs/                     # Type hints for IDE
├── templates/                 # Script templates
│
├── Py4GW.dll                  # Main DLL (4.4MB)
├── Py4GW.ini                  # Configuration
├── Py4GW_Launcher.exe         # GUI launcher
└── Py4GW_LauncherCompact.py   # Python launcher
```

---

## 🔧 Core Components

### Py4GWCoreLib - Core Library

The foundation providing direct access to Guild Wars:

#### Game State Access
- **Agent** - NPCs, enemies, allies, items (spawning, properties, effects)
- **Player** - Character control, status, actions
- **Party** - Party/group management, hero control
- **Map** - Instance information, navigation data
- **Inventory** - Items, bags, storage management
- **Skill** - Skill database (6000+ skills), casting, cooldowns
- **Quest** - Quest information and tracking
- **Effect** - Buffs, debuffs, enchantments

#### Interaction Systems
- **Pathing** - A* pathfinding with NavMesh
- **Camera** - Camera control and positioning
- **UIManager** - In-game UI frame manipulation
- **Merchant** - NPC trading and buying
- **BuildMgr** - Skill template management

#### Automation Framework
- **Botting** - Comprehensive bot base class (100+ methods)
- **ActionQueue** - Reliable action sequencing
- **BehaviorTree** - AI logic trees
- **FSM** - Finite state machines
- **EventSystem** - Event-driven automation

#### Rendering & UI
- **DXOverlay** - DirectX 2D/3D rendering
- **ImGui** - ImGui integration for widgets
- **Overlay** - Overlay window management

### HeroAI - Hero Intelligence System

Advanced multi-hero combat automation:

- **Combat Handler** - Skill usage, targeting, positioning
- **Targeting Logic** - Lowest HP, clustering, priority targets
- **Multibox Support** - Shared memory IPC for multi-instance control
- **Profession-Specific AI** - Custom logic for each class
- **Control Panel** - ImGui UI for configuration

### Widget System

50+ optional UI extensions:

- Dynamic loading from `Widgets/` directory
- ImGui-based overlay widgets
- Per-widget configuration in `Py4GW.ini`
- Hot-reloading support
- Community and official widgets

---

## 💡 Usage Examples

### Basic Agent Interaction

```python
from Py4GWCoreLib import Py4GW

# Get all nearby enemies
agents = Py4GW.Agent.GetAllAgents()
for agent_id in agents:
    agent = Py4GW.Agent.GetAgentByID(agent_id)
    if agent and agent.IsEnemy():
        print(f"Enemy: {agent.GetPlayerName()} HP: {agent.GetHP()}")
```

### Inventory Management

```python
from Py4GWCoreLib import Py4GW

# Iterate through backpack items
backpack = Py4GW.Inventory.GetBackpack()
for slot in range(20):
    item = backpack.GetItem(slot)
    if item:
        print(f"Slot {slot}: {item.GetName()} (Qty: {item.GetQuantity()})")

# Pick up nearby items
loot_ids = Py4GW.Agent.GetLoot()
for loot_id in loot_ids:
    Py4GW.Player.PickupItem(loot_id)
```

### Skill Casting

```python
from Py4GWCoreLib import Py4GW

# Get skillbar
skillbar = Py4GW.Skillbar.GetSkillbar()

# Cast skill by slot (0-7)
target_id = Py4GW.Player.GetTargetID()
Py4GW.Skillbar.UseSkill(3, target_id)  # Cast skill in slot 4

# Check if skill is recharged
if Py4GW.Skillbar.IsSkillReady(3):
    print("Skill ready!")
```

### Movement & Pathing

```python
from Py4GWCoreLib import Py4GW
from Py4GWCoreLib.classes import Vector3

# Move to coordinate
target_pos = Vector3(-15000, 20000, 0)
Py4GW.Player.Move(target_pos.x, target_pos.y)

# Use pathfinding
path = Py4GW.Pathing.FindPath(start_pos, end_pos)
for waypoint in path:
    Py4GW.Player.Move(waypoint.x, waypoint.y)
    time.sleep(0.1)
```

### Creating a Custom Widget

```python
import PyImGui

MODULE_NAME = "MyWidget"
window_open = True

def main():
    global window_open

    if not window_open:
        return

    if PyImGui.begin("My Custom Widget", window_open):
        PyImGui.text("Hello from my widget!")

        if PyImGui.button("Click me"):
            print("Button clicked!")

        player_id = Py4GW.Player.GetAgentID()
        PyImGui.text(f"Player ID: {player_id}")

    PyImGui.end()

def configure():
    PyImGui.text("Configuration panel")
    PyImGui.checkbox("Enable feature", False)
```

---

## 🎨 Widgets

### Major Widgets

| Widget | Description |
|--------|-------------|
| **HeroAI** | Hero AI control panel and configuration |
| **LootManager** | Advanced loot filtering and pickup rules |
| **Messaging** | Chat and whisper management system |
| **Calendar** | Guild Wars event calendar integration |
| **Travel** | Quick travel to outposts and towns |
| **CombatPrep** | Pre-combat preparation and buff management |
| **Mission Map +** | Enhanced mission map with annotations |
| **Compass +** | Improved compass with agent tracking |
| **Skillbar +** | Skillbar enhancements and quick-cast |
| **InventoryPlus** | Advanced inventory management |

### Development Widgets

| Widget | Description |
|--------|-------------|
| **Agent Info** | Real-time agent information viewer |
| **Frame Tester** | UI frame testing and debugging |
| **Icon Explorer** | FontAwesome icon browser |
| **Color Picker** | Color selection tool |
| **ImGui Demo** | Official ImGui demonstration |

### Widget Configuration

Widgets are configured in `Py4GW.ini`:

```ini
[HeroAI]
enabled = 1
auto_target = 1
skill_usage = 1

[LootManager]
enabled = 1
min_rarity = blue
auto_salvage = 1
```

---

## 🤖 Bots

### Pre-built Bot Categories

The `Bots/` directory contains ready-to-use bot scripts:

#### Farming Bots
- **Proof Of Legend Farmer** - Farm legendary weapons (146KB)
- **Legendary Guardian** - Guardian title farming (134KB)
- **COF Bone Farmer** - Catacombs of Hearts bone farming
- **Chahbek Village** - Chahbek Village farming route

#### Specialized Bots
- **Rollerbeetle Racing** - Automated beetle racing
- **Salvager** - Intelligent item salvaging
- **Vanquish Bots** - Area vanquishing (15+ areas)
- **Challenge Missions** - Challenge mission automation
- **Nicholas the Traveler** - Weekly NPC quest automation

#### Bot Usage

```bash
# Run a farming bot
python "Bots/Proof Of Legend Farmer.py"

# Run vanquish bot
python "Bots/Vanquish/area_name.py"
```

### Creating Custom Bots

Inherit from the `Bot` base class:

```python
from Py4GWCoreLib.Botting import Bot

class MyCustomBot(Bot):
    def __init__(self):
        super().__init__("CustomBot")
        self.enabled_combat = True
        self.loot_items = True

    def main_loop(self):
        # Your bot logic here
        self.move_to_area("Farming Location")
        self.kill_all_in_range(1500)
        self.pickup_loot()

    def on_death(self):
        # Handle death
        self.resign()
        self.restart()

if __name__ == "__main__":
    bot = MyCustomBot()
    bot.run()
```

---

## ⚙️ Configuration

### Main Configuration File: `Py4GW.ini`

```ini
[General]
log_level = INFO
auto_load_widgets = 1

[HeroAI]
enabled = 1
combat_range = 1200
target_priority = lowest_hp

[Loot]
enabled = 1
min_rarity = blue
auto_id = 1
auto_salvage = 0
salvage_rarity = purple

[Multibox]
enabled = 0
shared_memory = 1
sync_movement = 1
```

### Loot Configuration: `AutoLoot.ini`

```ini
[Filters]
; Item type filters
weapons = 1
armor = 1
materials = 1
runes = 1

[Rarity]
white = 0
blue = 1
purple = 1
gold = 1
green = 1
```

### Key Bindings: `ConfigManager.py`

Configure hotkeys for automation:

```python
KEY_BINDINGS = {
    "start_bot": "F9",
    "stop_bot": "F10",
    "emergency_stop": "F12",
    "pickup_loot": "F5",
}
```

---

## 📚 Documentation

### Included Documentation

- **[README.md](README.md)** - This file
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture details
- **[USER_GUIDE.md](USER_GUIDE.md)** - Comprehensive user guide
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation
- **[docs/rosetta_stone.txt](docs/rosetta_stone.txt)** - GwA2 to Py4GW migration guide

### Online Resources

- **GitHub Repository**: [apoguita/Py4GW](https://github.com/apoguita/Py4GW)
- **Releases**: [Latest Release](https://github.com/apoguita/Py4GW/releases/tag/Official)
- **Issues**: [Bug Reports & Feature Requests](https://github.com/apoguita/Py4GW/issues)

### Demo Scripts

Explore the `DEMO/` directory for hands-on examples:

- `DEMO_PyAgent.py` - Agent interaction examples
- `DEMO_PyImGui.py` - UI widget examples
- `DEMO_PyInventory.py` - Inventory management
- `DEMO_PyPlayer.py` - Player control
- `DEMO_PySkill.py` - Skill management
- `DEMO_PyPathing.py` - Pathfinding examples

---

## 🤝 Contributing

We welcome contributions from the community! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Areas

- 🐛 Bug fixes and issue resolution
- ✨ New features and enhancements
- 📝 Documentation improvements
- 🤖 New bot scripts
- 🎨 New widgets
- 🧪 Test coverage
- 🌍 Community support

---

## 👥 Community

### Community Scripts

The `Bots/` directory includes community contributions:

- **Ewoog_Scripts/** - Community bot collection
- **Nikon Scripts/** - Advanced automation examples
- **aC_Scripts/** - Contributed scripts
- **oasix/** - Community farming bots

### Sharing Your Work

- Submit bots to the `Bots/` directory
- Share widgets in `Widgets/` directory
- Contribute to documentation
- Help other users in Issues

---

## ⚠️ Disclaimer

**Py4GW** is a third-party tool not affiliated with ArenaNet or Guild Wars. Use at your own risk. Automation and botting may violate the game's Terms of Service. The developers are not responsible for any consequences from using this tool.

**Educational Purpose**: This project is primarily for educational purposes to demonstrate advanced Python programming, game automation techniques, and software architecture patterns.

---

## 📜 License

This project is open source. See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **apoguita** - Project creator and lead developer
- **Community Contributors** - Bot scripts, widgets, and testing
- **GwA2 Project** - Legacy AutoIt automation inspiration
- **ImGui Community** - UI framework
- **Guild Wars Community** - Ongoing support and feedback

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/apoguita/Py4GW/issues)
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the `docs/` directory

---

## 🗺️ Roadmap

### Planned Features
- Enhanced machine learning for combat AI
- Web-based control panel
- Plugin marketplace
- Docker support for automation servers
- Cross-instance synchronization improvements
- Advanced pathfinding with dynamic obstacles

### In Development
- Performance optimizations
- Extended widget library
- Improved documentation
- Additional bot templates

---

<div align="center">

**Made with ❤️ by the Py4GW Community**

[⬆ Back to Top](#py4gw---guild-wars-python-automation-framework)

</div>
