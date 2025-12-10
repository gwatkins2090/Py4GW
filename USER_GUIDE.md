# Py4GW User Guide

Complete guide to using Py4GW for Guild Wars automation and scripting. This guide covers everything from basic setup to advanced bot development.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Understanding the Basics](#understanding-the-basics)
- [Working with Agents](#working-with-agents)
- [Player Control](#player-control)
- [Inventory Management](#inventory-management)
- [Skills and Combat](#skills-and-combat)
- [Movement and Pathfinding](#movement-and-pathfinding)
- [Party and Hero Management](#party-and-hero-management)
- [Creating Widgets](#creating-widgets)
- [Building Bots](#building-bots)
- [Configuration](#configuration)
- [Debugging and Troubleshooting](#debugging-and-troubleshooting)
- [Best Practices](#best-practices)
- [Advanced Topics](#advanced-topics)

---

## Getting Started

### Installation

1. **Download Py4GW:**
   - Visit [Releases Page](https://github.com/apoguita/Py4GW/releases/tag/Official)
   - Download the latest version
   - Extract to a folder (e.g., `C:\Py4GW\`)

2. **Verify Python Version:**
   ```bash
   python --version
   # Must show: Python 3.13.0 (32-bit)
   ```

3. **Launch Guild Wars:**
   - Start your Guild Wars client
   - Log in to a character

4. **Start Py4GW:**
   ```bash
   cd C:\Py4GW
   python Py4GW_LauncherCompact.py
   ```
   Or simply run `Py4GW_Launcher.exe`

### First Script

Create your first script `my_first_script.py`:

```python
from Py4GWCoreLib import *

MODULE_NAME = "MyFirstScript"

def main():
    print("Hello from Py4GW!")

    # Get player information
    player_id = Py4GW.Player.GetAgentID()
    print(f"Player Agent ID: {player_id}")

    # Get player position
    pos = Py4GW.Player.GetPosition()
    print(f"Position: X={pos.x}, Y={pos.y}")

    # Get map ID
    map_id = Py4GW.Map.GetMapID()
    print(f"Current Map ID: {map_id}")

if __name__ == "__main__":
    main()
```

Run it:
```bash
python my_first_script.py
```

---

## Understanding the Basics

### The Py4GW Object

All core functionality is accessed through the `Py4GW` object:

```python
from Py4GWCoreLib import Py4GW

# Player operations
Py4GW.Player.GetAgentID()
Py4GW.Player.GetTargetID()
Py4GW.Player.Move(x, y)

# Agent operations
Py4GW.Agent.GetAgentByID(agent_id)
Py4GW.Agent.GetAllAgents()

# Inventory operations
Py4GW.Inventory.GetBackpack()
Py4GW.Inventory.GetStorageChest()

# Skill operations
Py4GW.Skillbar.UseSkill(slot, target_id)
Py4GW.Skillbar.GetSkillbar()

# Map operations
Py4GW.Map.GetMapID()
Py4GW.Map.Travel(map_id)

# Party operations
Py4GW.Party.GetPartySize()
Py4GW.Party.GetHeroes()
```

### Module Structure

```python
# Always start with this import
from Py4GWCoreLib import *

# MODULE_NAME identifies your script
MODULE_NAME = "YourScriptName"

# Main function
def main():
    # Your code here
    pass

# Entry point
if __name__ == "__main__":
    main()
```

### Data Types

**Vector3:**
```python
from Py4GWCoreLib.classes import Vector3

pos = Vector3(x=-15000, y=20000, z=0)
distance = pos.distance_to(other_pos)
```

**Agent:**
```python
agent = Py4GW.Agent.GetAgentByID(agent_id)
hp = agent.GetHP()  # 0.0 to 1.0
position = agent.GetPosition()  # Vector3
```

**Item:**
```python
item = Py4GW.Inventory.GetItemBySlot(bag, slot)
name = item.GetName()
quantity = item.GetQuantity()
rarity = item.GetRarity()
```

---

## Working with Agents

### Getting Agents

**All Agents:**
```python
all_agents = Py4GW.Agent.GetAllAgents()
for agent_id in all_agents:
    agent = Py4GW.Agent.GetAgentByID(agent_id)
    if agent:
        print(f"Agent {agent_id}: {agent.GetPlayerName()}")
```

**Player Agent:**
```python
player_id = Py4GW.Player.GetAgentID()
player_agent = Py4GW.Agent.GetAgentByID(player_id)
```

**Target Agent:**
```python
target_id = Py4GW.Player.GetTargetID()
if target_id > 0:
    target = Py4GW.Agent.GetAgentByID(target_id)
```

**Nearby Agents:**
```python
def get_agents_in_range(center_pos, range_distance):
    """Get all agents within range of a position"""
    nearby = []
    all_agents = Py4GW.Agent.GetAllAgents()

    for agent_id in all_agents:
        agent = Py4GW.Agent.GetAgentByID(agent_id)
        if agent:
            distance = center_pos.distance_to(agent.GetPosition())
            if distance <= range_distance:
                nearby.append(agent)

    return nearby
```

### Agent Properties

**Basic Info:**
```python
agent = Py4GW.Agent.GetAgentByID(agent_id)

# Identity
name = agent.GetPlayerName()
model_id = agent.GetModelID()
agent_id = agent.GetAgentID()

# Position
position = agent.GetPosition()  # Vector3
x, y = position.x, position.y

# Status
hp = agent.GetHP()  # 0.0 to 1.0 (percentage)
energy = agent.GetEnergy()  # 0.0 to 1.0
is_alive = agent.IsAlive()
is_dead = agent.IsDead()

# Type checking
is_player = agent.IsPlayer()
is_npc = agent.IsNPC()
is_item = agent.IsItem()
is_gadget = agent.IsGadget()

# Allegiance
is_enemy = agent.IsEnemy()
is_ally = agent.IsAlly()
is_neutral = agent.IsNeutral()
```

**Combat Info:**
```python
# Targeting
is_attacking = agent.IsAttacking()
is_casting = agent.IsCasting()
is_knocked_down = agent.IsKnockedDown()

# Effects
effects = agent.GetEffects()
for effect in effects:
    print(f"Effect: {effect.GetSkillID()}")
```

### Filtering Agents

**Find Enemies:**
```python
def get_all_enemies():
    enemies = []
    all_agents = Py4GW.Agent.GetAllAgents()

    for agent_id in all_agents:
        agent = Py4GW.Agent.GetAgentByID(agent_id)
        if agent and agent.IsEnemy() and agent.IsAlive():
            enemies.append(agent)

    return enemies
```

**Find NPCs:**
```python
def find_npc_by_model_id(model_id):
    all_agents = Py4GW.Agent.GetAllAgents()

    for agent_id in all_agents:
        agent = Py4GW.Agent.GetAgentByID(agent_id)
        if agent and agent.GetModelID() == model_id:
            return agent

    return None
```

**Find Closest Enemy:**
```python
def find_closest_enemy():
    player_pos = Py4GW.Player.GetPosition()
    enemies = get_all_enemies()

    if not enemies:
        return None

    closest = min(enemies, key=lambda e: player_pos.distance_to(e.GetPosition()))
    return closest
```

---

## Player Control

### Player Information

```python
# Identity
player_id = Py4GW.Player.GetAgentID()
player_name = Py4GW.Player.GetName()

# Position
position = Py4GW.Player.GetPosition()
x, y = position.x, position.y

# Status
hp = Py4GW.Player.GetHP()
energy = Py4GW.Player.GetEnergy()
is_alive = Py4GW.Player.IsAlive()
is_moving = Py4GW.Player.IsMoving()
is_casting = Py4GW.Player.IsCasting()

# Connection
is_connected = Py4GW.Player.IsConnected()
is_loading = Py4GW.Player.IsLoading()
```

### Movement

**Basic Movement:**
```python
# Move to coordinates
Py4GW.Player.Move(x=-15000, y=20000)

# Move to agent
target_id = Py4GW.Player.GetTargetID()
target = Py4GW.Agent.GetAgentByID(target_id)
target_pos = target.GetPosition()
Py4GW.Player.Move(target_pos.x, target_pos.y)

# Stop moving
current_pos = Py4GW.Player.GetPosition()
Py4GW.Player.Move(current_pos.x, current_pos.y)
```

**Movement with Wait:**
```python
def move_and_wait(x, y, timeout=10.0):
    """Move to position and wait for arrival"""
    import time
    Py4GW.Player.Move(x, y)

    start_time = time.time()
    target_pos = Vector3(x, y, 0)

    while time.time() - start_time < timeout:
        current_pos = Py4GW.Player.GetPosition()
        distance = current_pos.distance_to(target_pos)

        if distance < 100:  # Arrival threshold
            return True

        time.sleep(0.1)

    return False  # Timeout
```

### Targeting

```python
# Get current target
target_id = Py4GW.Player.GetTargetID()

# Set target
Py4GW.Player.ChangeTarget(agent_id)

# Clear target
Py4GW.Player.ChangeTarget(0)

# Call target
Py4GW.Player.CallTarget()
```

### Interaction

```python
# Interact with agent
Py4GW.Player.InteractWithAgent(agent_id)

# Talk to NPC
npc_id = find_npc_by_model_id(12345)
if npc_id:
    Py4GW.Player.InteractWithAgent(npc_id)
```

### Actions

```python
# Attack
Py4GW.Player.Attack(target_id)

# Use skill
Py4GW.Player.UseSkill(skill_slot=3, target_id=target_id)

# Pickup item
loot_ids = Py4GW.Agent.GetLoot()
for loot_id in loot_ids:
    Py4GW.Player.PickupItem(loot_id)

# Drop item
item = Py4GW.Inventory.GetItemBySlot(bag=1, slot=5)
if item:
    Py4GW.Player.DropItem(item.GetItemID())
```

---

## Inventory Management

### Accessing Bags

```python
# Backpack (bag 1)
backpack = Py4GW.Inventory.GetBackpack()

# Belt pouch (bag 2)
belt = Py4GW.Inventory.GetBeltPouch()

# Bag 3
bag3 = Py4GW.Inventory.GetBag3()

# Bag 4
bag4 = Py4GW.Inventory.GetBag4()

# Storage
storage = Py4GW.Inventory.GetStorageChest()

# Material storage
material_storage = Py4GW.Inventory.GetMaterialStorage()
```

### Working with Items

**Get Item:**
```python
# By slot
item = Py4GW.Inventory.GetItemBySlot(bag=1, slot=0)

# By item ID
item_id = 12345
item = Py4GW.Inventory.GetItemByID(item_id)
```

**Item Properties:**
```python
item = Py4GW.Inventory.GetItemBySlot(1, 0)

if item:
    # Basic info
    name = item.GetName()
    model_id = item.GetModelID()
    quantity = item.GetQuantity()

    # Status
    is_equipped = item.IsEquipped()
    is_customized = item.IsCustomized()

    # Quality
    rarity = item.GetRarity()  # Rarity enum
    modifier = item.GetModifier()  # +damage or armor

    # Type
    item_type = item.GetType()
```

**Iterate Through Bag:**
```python
def print_backpack_contents():
    backpack = Py4GW.Inventory.GetBackpack()

    for slot in range(20):  # Backpack has 20 slots
        item = backpack.GetItem(slot)
        if item:
            print(f"Slot {slot}: {item.GetName()} x{item.GetQuantity()}")
```

### Inventory Operations

**Find Items:**
```python
def find_items_by_model_id(model_id):
    """Find all items with given model ID"""
    items = []

    # Search all bags
    for bag_num in range(1, 5):
        bag = Py4GW.Inventory.GetBag(bag_num)
        bag_size = bag.GetSize()

        for slot in range(bag_size):
            item = bag.GetItem(slot)
            if item and item.GetModelID() == model_id:
                items.append(item)

    return items
```

**Count Items:**
```python
def count_item(model_id):
    """Count total quantity of an item"""
    total = 0
    items = find_items_by_model_id(model_id)

    for item in items:
        total += item.GetQuantity()

    return total
```

**Find Free Slots:**
```python
def get_free_slots(bag_num=1):
    """Get list of free slot indices in bag"""
    free_slots = []
    bag = Py4GW.Inventory.GetBag(bag_num)
    bag_size = bag.GetSize()

    for slot in range(bag_size):
        item = bag.GetItem(slot)
        if item is None:
            free_slots.append(slot)

    return free_slots
```

### Item Actions

**Use Item:**
```python
item = Py4GW.Inventory.GetItemBySlot(1, 5)
if item:
    Py4GW.Inventory.UseItem(item.GetItemID())
```

**Drop Item:**
```python
item = Py4GW.Inventory.GetItemBySlot(1, 10)
if item:
    Py4GW.Player.DropItem(item.GetItemID())
```

**Move Item:**
```python
# Move from backpack slot 0 to bag 3 slot 5
Py4GW.Inventory.MoveItem(
    from_bag=1,
    from_slot=0,
    to_bag=3,
    to_slot=5
)
```

**Identify Item:**
```python
item = Py4GW.Inventory.GetItemBySlot(1, 0)
if item and item.NeedsIdentification():
    Py4GW.Inventory.IdentifyItem(item.GetItemID())
```

**Salvage Item:**
```python
# Use salvage kit in slot 0 on item in slot 5
salvage_kit = Py4GW.Inventory.GetItemBySlot(1, 0)
target_item = Py4GW.Inventory.GetItemBySlot(1, 5)

if salvage_kit and target_item:
    Py4GW.Inventory.SalvageItem(
        salvage_kit.GetItemID(),
        target_item.GetItemID()
    )
```

### Loot Management

**Pick Up Loot:**
```python
def pickup_all_loot():
    loot_ids = Py4GW.Agent.GetLoot()
    for loot_id in loot_ids:
        Py4GW.Player.PickupItem(loot_id)
        time.sleep(0.5)  # Wait between pickups
```

**Filtered Loot:**
```python
def pickup_filtered_loot(min_rarity="blue"):
    rarity_map = {"white": 0, "blue": 1, "purple": 2, "gold": 3, "green": 4}
    min_rarity_value = rarity_map.get(min_rarity, 0)

    loot_ids = Py4GW.Agent.GetLoot()

    for loot_id in loot_ids:
        loot_agent = Py4GW.Agent.GetAgentByID(loot_id)
        if not loot_agent:
            continue

        # Check item rarity (if available)
        # Note: Rarity check may require picking up first
        Py4GW.Player.PickupItem(loot_id)
        time.sleep(0.3)
```

---

## Skills and Combat

### Skillbar Access

```python
# Get skillbar
skillbar = Py4GW.Skillbar.GetSkillbar()

# Get skill in slot
skill = Py4GW.Skillbar.GetSkill(slot=3)  # Slot 0-7

# Skill info
skill_id = skill.GetSkillID()
recharge = skill.GetRecharge()  # Seconds remaining
is_ready = skill.IsRecharged()
energy_cost = skill.GetEnergyCost()
```

### Using Skills

**Cast Skill:**
```python
# Cast on target
target_id = Py4GW.Player.GetTargetID()
Py4GW.Skillbar.UseSkill(slot=3, target_id=target_id)

# Cast on self
player_id = Py4GW.Player.GetAgentID()
Py4GW.Skillbar.UseSkill(slot=5, target_id=player_id)

# Cast ground-targeted skill
Py4GW.Skillbar.UseSkill(slot=7, x=-15000, y=20000)
```

**Wait for Cast:**
```python
def cast_and_wait(slot, target_id):
    """Cast skill and wait for completion"""
    Py4GW.Skillbar.UseSkill(slot, target_id)

    # Wait for casting to finish
    while Py4GW.Player.IsCasting():
        time.sleep(0.05)

    return True
```

**Check Skill Ready:**
```python
def use_skill_when_ready(slot, target_id, timeout=10.0):
    """Wait for skill to be ready, then use it"""
    start_time = time.time()

    while time.time() - start_time < timeout:
        if Py4GW.Skillbar.IsSkillReady(slot):
            Py4GW.Skillbar.UseSkill(slot, target_id)
            return True
        time.sleep(0.1)

    return False  # Timeout
```

### Skill Database

```python
from Py4GWCoreLib import SkillManager

# Get skill info by ID
skill_info = SkillManager.GetSkill(skill_id=123)

if skill_info:
    name = skill_info['name']
    description = skill_info['description']
    profession = skill_info['profession']
    energy_cost = skill_info['energy']
    cast_time = skill_info['cast_time']
    recharge = skill_info['recharge']
```

### Combat Patterns

**Basic Attack Loop:**
```python
def attack_enemy(target_id):
    # Target enemy
    Py4GW.Player.ChangeTarget(target_id)

    # Attack
    Py4GW.Player.Attack(target_id)

    # Use skills
    while True:
        target = Py4GW.Agent.GetAgentByID(target_id)

        # Check if target is dead
        if not target or target.IsDead():
            break

        # Use skill rotation
        for skill_slot in [3, 4, 5]:  # Skills 4, 5, 6
            if Py4GW.Skillbar.IsSkillReady(skill_slot):
                Py4GW.Skillbar.UseSkill(skill_slot, target_id)
                time.sleep(0.5)

        time.sleep(0.1)
```

**Skill Priority System:**
```python
def use_priority_skills(target_id):
    """Use skills in priority order"""
    skill_priority = [
        (7, 5.0),  # Elite (slot 8) - high priority
        (4, 3.0),  # Skill 5 - medium priority
        (3, 2.0),  # Skill 4 - low priority
        (5, 1.0),  # Skill 6 - lowest priority
    ]

    for slot, priority in skill_priority:
        if Py4GW.Skillbar.IsSkillReady(slot):
            player_energy = Py4GW.Player.GetEnergy()
            skill = Py4GW.Skillbar.GetSkill(slot)
            energy_cost = skill.GetEnergyCost()

            if player_energy >= energy_cost:
                Py4GW.Skillbar.UseSkill(slot, target_id)
                return True

    return False
```

**Buff Maintenance:**
```python
def maintain_buffs():
    """Keep enchantments and stances active"""
    buff_skills = [0, 1, 2]  # Slots with buff skills

    for slot in buff_skills:
        if Py4GW.Skillbar.IsSkillReady(slot):
            player_id = Py4GW.Player.GetAgentID()
            Py4GW.Skillbar.UseSkill(slot, player_id)
            time.sleep(0.3)
```

---

## Movement and Pathfinding

### Basic Movement

```python
from Py4GWCoreLib.classes import Vector3

# Move to coordinates
target = Vector3(x=-15000, y=20000, z=0)
Py4GW.Player.Move(target.x, target.y)

# Move relative to current position
current = Py4GW.Player.GetPosition()
new_pos = Vector3(current.x + 1000, current.y + 500, 0)
Py4GW.Player.Move(new_pos.x, new_pos.y)
```

### Pathfinding

```python
from Py4GWCoreLib import Pathing

# Find path from A to B
start = Py4GW.Player.GetPosition()
goal = Vector3(-15000, 20000, 0)

path = Pathing.FindPath(start, goal)

if path:
    # Follow path
    for waypoint in path:
        Py4GW.Player.Move(waypoint.x, waypoint.y)

        # Wait for arrival
        while True:
            current = Py4GW.Player.GetPosition()
            distance = current.distance_to(waypoint)

            if distance < 100:
                break

            time.sleep(0.1)
```

### Advanced Movement

**Move with Obstacle Avoidance:**
```python
def move_with_avoidance(target_x, target_y):
    """Move to target, recalculating path if stuck"""
    timeout = 30.0
    start_time = time.time()
    stuck_counter = 0
    last_position = Py4GW.Player.GetPosition()

    while time.time() - start_time < timeout:
        current = Py4GW.Player.GetPosition()
        target = Vector3(target_x, target_y, 0)
        distance = current.distance_to(target)

        if distance < 100:
            return True  # Arrived

        # Check if stuck
        moved = current.distance_to(last_position)
        if moved < 50:  # Barely moved
            stuck_counter += 1
            if stuck_counter > 10:
                # Try to unstuck
                random_offset = Vector3(
                    current.x + random.randint(-500, 500),
                    current.y + random.randint(-500, 500),
                    0
                )
                Py4GW.Player.Move(random_offset.x, random_offset.y)
                time.sleep(1.0)
                stuck_counter = 0
        else:
            stuck_counter = 0

        last_position = current
        Py4GW.Player.Move(target_x, target_y)
        time.sleep(0.5)

    return False  # Timeout
```

**Follow Path with Waypoints:**
```python
def follow_waypoint_path(waypoints):
    """Follow a predefined list of waypoints"""
    for i, waypoint in enumerate(waypoints):
        print(f"Moving to waypoint {i + 1}/{len(waypoints)}")

        success = move_and_wait(waypoint.x, waypoint.y, timeout=30.0)

        if not success:
            print(f"Failed to reach waypoint {i + 1}")
            return False

    return True

# Example usage
waypoints = [
    Vector3(-15000, 20000, 0),
    Vector3(-14000, 21000, 0),
    Vector3(-13000, 22000, 0),
]

follow_waypoint_path(waypoints)
```

### Map Travel

```python
# Get current map
current_map = Py4GW.Map.GetMapID()

# Travel to another map
target_map_id = 77  # Ascalon City
Py4GW.Map.Travel(target_map_id)

# Wait for loading
while Py4GW.Player.IsLoading():
    time.sleep(0.1)

print("Arrived at destination")
```

---

## Party and Hero Management

### Party Information

```python
# Get party size
party_size = Py4GW.Party.GetPartySize()

# Get party members
members = Py4GW.Party.GetPartyMembers()

for member_id in members:
    member = Py4GW.Agent.GetAgentByID(member_id)
    if member:
        print(f"Party member: {member.GetPlayerName()}")
```

### Hero Control

**Get Heroes:**
```python
heroes = Py4GW.Party.GetHeroes()

for hero_id in heroes:
    hero = Py4GW.Agent.GetAgentByID(hero_id)
    if hero:
        print(f"Hero: {hero.GetPlayerName()}, HP: {hero.GetHP()}")
```

**Flag Heroes:**
```python
# Flag all heroes to position
flag_pos = Vector3(-15000, 20000, 0)
Py4GW.Party.FlagHero(0, flag_pos.x, flag_pos.y)  # Hero 1

# Flag individual hero
hero_index = 0  # First hero
Py4GW.Party.FlagHero(hero_index, x=-15000, y=20000)

# Unflag heroes
Py4GW.Party.UnflagHero(hero_index)
Py4GW.Party.UnflagAllHeroes()
```

**Hero Commands:**
```python
# Set hero behavior
Py4GW.Party.SetHeroBehavior(hero_index=0, behavior="guard")
# Behaviors: "fight", "guard", "avoid"

# Lock hero target
target_id = Py4GW.Player.GetTargetID()
Py4GW.Party.LockHeroTarget(hero_index=0, target_id=target_id)

# Unlock hero target
Py4GW.Party.UnlockHeroTarget(hero_index=0)
```

### Party Management

**Invite to Party:**
```python
# Invite player by name
Py4GW.Party.InvitePlayer("PlayerName")

# Invite hero
Py4GW.Party.AddHero(hero_id)
```

**Kick from Party:**
```python
# Kick party member
Py4GW.Party.KickMember(member_id)

# Kick all heroes
heroes = Py4GW.Party.GetHeroes()
for hero_id in heroes:
    Py4GW.Party.KickMember(hero_id)
```

**Leave Party:**
```python
Py4GW.Party.LeaveParty()
```

---

## Creating Widgets

### Widget Template

Create `Widgets/MyWidget.py`:

```python
import PyImGui
from Py4GWCoreLib import Py4GW

MODULE_NAME = "MyWidget"

# Widget state
window_open = True
counter = 0

def main():
    """Called every frame - render your widget here"""
    global window_open, counter

    if not window_open:
        return

    # Begin window
    window_open = PyImGui.begin("My Custom Widget", window_open)

    if window_open:
        # Display text
        PyImGui.text("Hello from my widget!")

        # Display player info
        player_id = Py4GW.Player.GetAgentID()
        player_hp = Py4GW.Player.GetHP()
        PyImGui.text(f"Player ID: {player_id}")
        PyImGui.text(f"HP: {player_hp * 100:.1f}%")

        # Button
        if PyImGui.button("Click Me"):
            counter += 1

        PyImGui.text(f"Button clicked {counter} times")

        # Separator
        PyImGui.separator()

        # Checkbox
        global show_advanced
        show_advanced = PyImGui.checkbox("Show Advanced", show_advanced)

        if show_advanced:
            PyImGui.text("Advanced options here")

    PyImGui.end()

def configure():
    """Optional: Configuration panel"""
    PyImGui.text("Widget Configuration")
    PyImGui.text("Add configuration options here")

def on_load():
    """Optional: Called when widget loads"""
    print("MyWidget loaded!")

def on_unload():
    """Optional: Called when widget unloads"""
    print("MyWidget unloaded!")

# Initialize state
show_advanced = False
```

### ImGui Components

**Text:**
```python
PyImGui.text("Simple text")
PyImGui.text_colored("Colored text", 1.0, 0.0, 0.0, 1.0)  # RGBA
```

**Buttons:**
```python
if PyImGui.button("Click Me"):
    print("Button clicked!")

if PyImGui.button("Large Button", width=200, height=50):
    print("Large button clicked!")
```

**Checkboxes:**
```python
checked = PyImGui.checkbox("Enable Feature", checked)
```

**Sliders:**
```python
value = PyImGui.slider_int("Integer", value, min=0, max=100)
value_f = PyImGui.slider_float("Float", value_f, min=0.0, max=1.0)
```

**Input Fields:**
```python
text = PyImGui.input_text("Enter text", text, max_length=256)
value = PyImGui.input_int("Enter number", value)
```

**Combo Box:**
```python
items = ["Option 1", "Option 2", "Option 3"]
selected = PyImGui.combo("Select", selected, items)
```

**Trees:**
```python
if PyImGui.tree_node("Expandable Section"):
    PyImGui.text("Content inside tree")
    PyImGui.tree_pop()
```

### Advanced Widget Example

```python
import PyImGui
from Py4GWCoreLib import Py4GW

MODULE_NAME = "EnemyTracker"

window_open = True
track_range = 1500
show_dead = False

def main():
    global window_open, track_range, show_dead

    if not window_open:
        return

    window_open = PyImGui.begin("Enemy Tracker", window_open)

    if window_open:
        # Configuration
        PyImGui.text("Configuration:")
        track_range = PyImGui.slider_int("Track Range", track_range, 500, 5000)
        show_dead = PyImGui.checkbox("Show Dead Enemies", show_dead)

        PyImGui.separator()

        # Enemy list
        PyImGui.text("Nearby Enemies:")

        player_pos = Py4GW.Player.GetPosition()
        all_agents = Py4GW.Agent.GetAllAgents()
        enemy_count = 0

        for agent_id in all_agents:
            agent = Py4GW.Agent.GetAgentByID(agent_id)

            if not agent or not agent.IsEnemy():
                continue

            if not show_dead and agent.IsDead():
                continue

            distance = player_pos.distance_to(agent.GetPosition())

            if distance > track_range:
                continue

            # Display enemy
            enemy_count += 1
            name = agent.GetPlayerName() or f"Enemy {agent_id}"
            hp = agent.GetHP() * 100
            status = "Dead" if agent.IsDead() else "Alive"

            PyImGui.text(f"{name} - HP: {hp:.0f}% - Dist: {distance:.0f} - {status}")

            # Target button
            PyImGui.same_line()
            if PyImGui.small_button(f"Target##{agent_id}"):
                Py4GW.Player.ChangeTarget(agent_id)

        if enemy_count == 0:
            PyImGui.text("No enemies in range")
        else:
            PyImGui.separator()
            PyImGui.text(f"Total: {enemy_count} enemies")

    PyImGui.end()

def configure():
    PyImGui.text("Enemy Tracker Configuration")
    PyImGui.text("Adjust settings in the main window")
```

---

## Building Bots

### Bot Base Class

```python
from Py4GWCoreLib.Botting import Bot

class MyBot(Bot):
    def __init__(self):
        super().__init__("MyBot")

        # Configuration
        self.enabled_combat = True
        self.combat_range = 1200
        self.enabled_loot = True
        self.loot_timeout = 5.0

    def main_loop(self):
        """Main bot logic - called continuously"""
        # Your bot logic here
        pass

    def on_start(self):
        """Called when bot starts"""
        print("Bot starting...")

    def on_stop(self):
        """Called when bot stops"""
        print("Bot stopping...")

    def on_death(self):
        """Called when player dies"""
        print("Player died!")
        self.resign()

if __name__ == "__main__":
    bot = MyBot()
    bot.run()
```

### Simple Farming Bot

```python
from Py4GWCoreLib.Botting import Bot
from Py4GWCoreLib.classes import Vector3

class SimpleFarmer(Bot):
    def __init__(self):
        super().__init__("SimpleFarmer")

        self.enabled_combat = True
        self.enabled_loot = True
        self.farm_location = Vector3(-15000, 20000, 0)
        self.return_location = Vector3(-14000, 19000, 0)

    def main_loop(self):
        # Move to farming location
        self.log("Moving to farm location")
        self.move_to(self.farm_location.x, self.farm_location.y)

        # Kill all enemies in range
        self.log("Clearing enemies")
        self.kill_all_in_range(self.combat_range)

        # Loot items
        self.log("Looting")
        self.pickup_loot()

        # Return to starting location
        self.log("Returning")
        self.move_to(self.return_location.x, self.return_location.y)

        # Wait a bit
        self.wait(2.0)

    def on_death(self):
        self.log("Died! Resigning and restarting")
        self.resign()
        self.wait(5.0)

if __name__ == "__main__":
    bot = SimpleFarmer()
    bot.run()
```

### Bot with State Machine

```python
from Py4GWCoreLib.Botting import Bot
from Py4GWCoreLib.py4gwcorelib_src.FSM import FSM
from enum import Enum

class BotState(Enum):
    TRAVELING = 1
    FIGHTING = 2
    LOOTING = 3
    RETURNING = 4

class AdvancedFarmer(Bot):
    def __init__(self):
        super().__init__("AdvancedFarmer")

        # Setup FSM
        self.fsm = FSM()
        self.setup_states()

        self.farm_location = Vector3(-15000, 20000, 0)
        self.spawn_location = Vector3(-14000, 19000, 0)

    def setup_states(self):
        # Add states
        self.fsm.add_state(
            BotState.TRAVELING,
            on_enter=self.enter_traveling,
            on_update=self.update_traveling,
            on_exit=None
        )

        self.fsm.add_state(
            BotState.FIGHTING,
            on_enter=self.enter_fighting,
            on_update=self.update_fighting,
            on_exit=None
        )

        self.fsm.add_state(
            BotState.LOOTING,
            on_enter=None,
            on_update=self.update_looting,
            on_exit=None
        )

        # Add transitions
        self.fsm.add_transition(
            BotState.TRAVELING,
            BotState.FIGHTING,
            lambda: self.has_nearby_enemies()
        )

        self.fsm.add_transition(
            BotState.FIGHTING,
            BotState.LOOTING,
            lambda: not self.has_nearby_enemies()
        )

        self.fsm.add_transition(
            BotState.LOOTING,
            BotState.RETURNING,
            lambda: not self.has_loot()
        )

        # Start in traveling state
        self.fsm.transition_to(BotState.TRAVELING)

    def main_loop(self):
        self.fsm.update()

    def enter_traveling(self):
        self.log("Traveling to farm location")
        self.move_to(self.farm_location.x, self.farm_location.y)

    def update_traveling(self):
        # Wait for arrival
        distance = self.get_distance_to(self.farm_location)
        if distance < 100:
            self.log("Arrived at farm location")

    def enter_fighting(self):
        self.log("Engaging enemies")

    def update_fighting(self):
        self.kill_all_in_range(self.combat_range)

    def update_looting(self):
        self.pickup_loot()

    def has_nearby_enemies(self):
        enemies = self.get_all_enemies()
        return len(enemies) > 0

    def has_loot(self):
        loot = Py4GW.Agent.GetLoot()
        return len(loot) > 0

if __name__ == "__main__":
    bot = AdvancedFarmer()
    bot.run()
```

---

## Configuration

### Config Files

**Py4GW.ini:**
```ini
[General]
log_level = INFO
auto_load_widgets = 1

[Widgets]
HeroAI = 1
LootManager = 1
Travel = 1
Calendar = 0

[Combat]
auto_target = 1
target_range = 1200
skill_usage = 1

[Loot]
enabled = 1
min_rarity = blue
auto_pickup = 1
pickup_delay = 0.5

[Multibox]
enabled = 0
shared_memory_id = 12345
sync_movement = 1
```

### Loading Configuration

```python
from Py4GWCoreLib.py4gwcorelib_src.IniHandler import IniHandler

# Load config
config = IniHandler("Py4GW.ini")

# Read values
log_level = config.get("General", "log_level", default="INFO")
auto_load = config.get_bool("General", "auto_load_widgets", default=True)
combat_range = config.get_int("Combat", "target_range", default=1200)

# Write values
config.set("Combat", "target_range", "1500")
config.save()
```

---

## Debugging and Troubleshooting

### Enable Logging

```python
from Py4GWCoreLib.py4gwcorelib_src.Console import Console

# Set log level
Console.SetLogLevel("DEBUG")

# Log messages
Console.Log("Info message")
Console.Warning("Warning message")
Console.Error("Error message")
Console.Debug("Debug message")
```

### Common Issues

**Issue: "Python version mismatch"**
- Solution: Ensure Python 3.13.0 32-bit is installed

**Issue: "DLL not found"**
- Solution: Make sure `Py4GW.dll` is in the same directory as your script

**Issue: "Agent ID returns 0"**
- Solution: Ensure you're logged in to a character and not in loading screen

**Issue: "Skills not casting"**
- Solution: Check skill is recharged, you have enough energy, and target is valid

### Debugging Tools

**Agent Info Widget:**
```python
# Widgets/Agent Info.py - Shows detailed agent information
```

**Frame Tester:**
```python
# Widgets/Frame_Tester.py - Test UI frame manipulation
```

**Console Output:**
```python
import sys

# Redirect output to file
sys.stdout = open('bot_log.txt', 'w')
sys.stderr = sys.stdout

# All print() calls now go to file
print("Bot starting...")
```

---

## Best Practices

### Code Organization

```python
# Good: Organized imports
from Py4GWCoreLib import Py4GW
from Py4GWCoreLib.Botting import Bot
from Py4GWCoreLib.classes import Vector3
import time

# Good: Constants at top
COMBAT_RANGE = 1200
LOOT_TIMEOUT = 5.0
FARM_LOCATION = Vector3(-15000, 20000, 0)

# Good: Helper functions
def find_closest_enemy():
    # ...
    pass

# Good: Main class
class MyBot(Bot):
    # ...
    pass
```

### Performance

```python
# Good: Cache frequently accessed data
player_pos = Py4GW.Player.GetPosition()  # Cache once
for agent in agents:
    distance = player_pos.distance_to(agent.GetPosition())

# Bad: Repeated calls
for agent in agents:
    distance = Py4GW.Player.GetPosition().distance_to(agent.GetPosition())


# Good: Batch operations
all_agents = Py4GW.Agent.GetAllAgents()  # Single call

# Bad: Individual queries in loop
for i in range(100):
    agent = Py4GW.Agent.GetAgentByID(i)  # Many calls
```

### Error Handling

```python
# Good: Check return values
target_id = Py4GW.Player.GetTargetID()
if target_id > 0:
    target = Py4GW.Agent.GetAgentByID(target_id)
    if target and target.IsAlive():
        # Safe to use target
        Py4GW.Player.Attack(target_id)

# Good: Try-except for critical sections
try:
    item = Py4GW.Inventory.GetItemBySlot(1, 0)
    Py4GW.Inventory.UseItem(item.GetItemID())
except Exception as e:
    Console.Error(f"Failed to use item: {e}")
```

---

## Advanced Topics

### Multi-Threading

```python
import threading

class MultiThreadBot(Bot):
    def __init__(self):
        super().__init__("MultiThread")
        self.combat_thread = None

    def on_start(self):
        # Start combat thread
        self.combat_thread = threading.Thread(target=self.combat_loop)
        self.combat_thread.daemon = True
        self.combat_thread.start()

    def combat_loop(self):
        while self.running:
            self.kill_all_in_range(1200)
            time.sleep(0.1)

    def main_loop(self):
        # Main thread handles movement
        self.move_to(-15000, 20000)
        self.wait(5.0)
```

### Behavior Trees

```python
from Py4GWCoreLib.py4gwcorelib_src.BehaviorTree import *

# Create behavior tree for combat
combat_tree = Selector([
    # Priority 1: Heal if low HP
    Sequence([
        Condition(lambda: Py4GW.Player.GetHP() < 0.3),
        Action(use_healing_skill)
    ]),

    # Priority 2: Use elite skill if available
    Sequence([
        Condition(lambda: has_target()),
        Condition(lambda: Py4GW.Skillbar.IsSkillReady(7)),
        Action(lambda: Py4GW.Skillbar.UseSkill(7, Py4GW.Player.GetTargetID()))
    ]),

    # Priority 3: Attack with regular skills
    Sequence([
        Condition(lambda: has_target()),
        Action(use_attack_skills)
    ]),

    # Default: Find new target
    Action(find_target)
])

# Execute tree each frame
def main_loop():
    combat_tree.tick()
```

### Shared Memory (Multiboxing)

```python
from HeroAI.shared_memory_manager import SharedMemoryManager

# Initialize shared memory
shm = SharedMemoryManager(session_id="farming_session")

# Write command (master instance)
shm.write_command(
    instance_id=1,
    command="move",
    data={"x": -15000, "y": 20000}
)

# Read command (slave instance)
command, data = shm.read_command(instance_id=1)
if command == "move":
    Py4GW.Player.Move(data['x'], data['y'])
```

---

## Conclusion

This guide covers the essential aspects of using Py4GW. For more information:

- Check the [API Reference](API_REFERENCE.md) for detailed API documentation
- Explore the `DEMO/` directory for working examples
- Read the [Architecture Documentation](ARCHITECTURE.md) for technical details
- Join the community and share your scripts!

Happy botting! 🎮

---

**Last Updated:** 2025-12-10
