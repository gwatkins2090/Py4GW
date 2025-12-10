# Py4GW API Reference

Complete API reference documentation for Py4GW Python automation framework. This document covers all core modules, classes, methods, and data structures.

---

## Table of Contents

- [Overview](#overview)
- [Py4GW.Player](#py4gwplayer)
- [Py4GW.Agent](#py4gwagent)
- [Py4GW.Party](#py4gwparty)
- [Py4GW.Inventory](#py4gwinventory)
- [Py4GW.Skillbar](#py4gwskillbar)
- [Py4GW.Map](#py4gwmap)
- [Py4GW.Pathing](#py4gwpathing)
- [Py4GW.Camera](#py4gwcamera)
- [Py4GW.UIManager](#py4gwuimanager)
- [Py4GW.Merchant](#py4gwmerchant)
- [Py4GW.Effects](#py4gweffects)
- [Classes](#classes)
- [Botting Framework](#botting-framework)
- [Behavior Trees](#behavior-trees)
- [Action Queue](#action-queue)
- [ImGui API](#imgui-api)
- [Enums and Constants](#enums-and-constants)

---

## Overview

All core functionality is accessed through the `Py4GW` object:

```python
from Py4GWCoreLib import Py4GW
```

Most methods return native Python types (int, float, bool, str) or custom classes (Vector3, Agent, Item, etc.).

**Return Values:**
- Methods returning IDs return `int` (0 if invalid/not found)
- Methods returning status return `bool`
- Methods returning positions return `Vector3` objects
- Methods returning percentages return `float` (0.0 to 1.0)

---

## Py4GW.Player

Player character control and information.

### Connection and Status

#### `GetAgentID() -> int`
Get the player's agent ID.

**Returns:** Agent ID (int), or 0 if not connected

**Example:**
```python
player_id = Py4GW.Player.GetAgentID()
```

---

#### `IsConnected() -> bool`
Check if connected to game server.

**Returns:** `True` if connected, `False` otherwise

---

#### `IsLoading() -> bool`
Check if map is currently loading.

**Returns:** `True` if loading, `False` otherwise

---

#### `IsInCinematic() -> bool`
Check if currently in a cinematic.

**Returns:** `True` if in cinematic, `False` otherwise

---

### Position and Movement

#### `GetPosition() -> Vector3`
Get player's current position.

**Returns:** `Vector3` object with x, y, z coordinates

**Example:**
```python
pos = Py4GW.Player.GetPosition()
print(f"X: {pos.x}, Y: {pos.y}")
```

---

#### `Move(x: float, y: float) -> None`
Move player to coordinates.

**Parameters:**
- `x` (float): Target X coordinate
- `y` (float): Target Y coordinate

**Example:**
```python
Py4GW.Player.Move(-15000, 20000)
```

---

#### `IsMoving() -> bool`
Check if player is currently moving.

**Returns:** `True` if moving, `False` otherwise

---

### Health and Energy

#### `GetHP() -> float`
Get player's current health percentage.

**Returns:** HP percentage (0.0 to 1.0)

**Example:**
```python
hp = Py4GW.Player.GetHP()
if hp < 0.5:
    print("Health below 50%!")
```

---

#### `GetMaxHP() -> int`
Get player's maximum health points.

**Returns:** Maximum HP (int)

---

#### `GetEnergy() -> float`
Get player's current energy percentage.

**Returns:** Energy percentage (0.0 to 1.0)

---

#### `GetMaxEnergy() -> int`
Get player's maximum energy points.

**Returns:** Maximum energy (int)

---

#### `IsAlive() -> bool`
Check if player is alive.

**Returns:** `True` if alive, `False` if dead

---

#### `IsDead() -> bool`
Check if player is dead.

**Returns:** `True` if dead, `False` if alive

---

### Targeting

#### `GetTargetID() -> int`
Get currently targeted agent ID.

**Returns:** Target agent ID, or 0 if no target

**Example:**
```python
target_id = Py4GW.Player.GetTargetID()
if target_id > 0:
    print(f"Targeting agent {target_id}")
```

---

#### `ChangeTarget(agent_id: int) -> None`
Change current target.

**Parameters:**
- `agent_id` (int): Agent ID to target, or 0 to clear target

**Example:**
```python
# Target enemy
Py4GW.Player.ChangeTarget(enemy_id)

# Clear target
Py4GW.Player.ChangeTarget(0)
```

---

#### `CallTarget() -> None`
Call your current target to party.

---

### Actions

#### `Attack(target_id: int) -> None`
Attack a target.

**Parameters:**
- `target_id` (int): Agent ID to attack

**Example:**
```python
target_id = Py4GW.Player.GetTargetID()
Py4GW.Player.Attack(target_id)
```

---

#### `InteractWithAgent(agent_id: int) -> None`
Interact with an agent (NPC, chest, etc.).

**Parameters:**
- `agent_id` (int): Agent ID to interact with

**Example:**
```python
# Talk to NPC
npc_id = find_npc_by_model_id(12345)
Py4GW.Player.InteractWithAgent(npc_id)
```

---

#### `PickupItem(item_id: int) -> None`
Pick up an item from the ground.

**Parameters:**
- `item_id` (int): Agent ID of item to pick up

**Example:**
```python
loot_ids = Py4GW.Agent.GetLoot()
for loot_id in loot_ids:
    Py4GW.Player.PickupItem(loot_id)
```

---

#### `DropItem(item_id: int) -> None`
Drop an item from inventory.

**Parameters:**
- `item_id` (int): Item ID to drop

---

#### `DropGold(amount: int) -> None`
Drop gold from inventory.

**Parameters:**
- `amount` (int): Amount of gold to drop

---

### Combat Status

#### `IsAttacking() -> bool`
Check if player is currently attacking.

**Returns:** `True` if attacking, `False` otherwise

---

#### `IsCasting() -> bool`
Check if player is currently casting a skill.

**Returns:** `True` if casting, `False` otherwise

---

#### `IsKnockedDown() -> bool`
Check if player is knocked down.

**Returns:** `True` if knocked down, `False` otherwise

---

### Attributes

#### `GetLevel() -> int`
Get player's level.

**Returns:** Level (1-20)

---

#### `GetExperience() -> int`
Get player's current experience points.

**Returns:** Experience points (int)

---

#### `GetMorale() -> int`
Get player's morale boost.

**Returns:** Morale percentage (can be negative)

---

---

## Py4GW.Agent

Agent (entities in game world) management.

### Getting Agents

#### `GetAllAgents() -> list[int]`
Get list of all agent IDs in the current instance.

**Returns:** List of agent IDs (list[int])

**Example:**
```python
all_agents = Py4GW.Agent.GetAllAgents()
for agent_id in all_agents:
    agent = Py4GW.Agent.GetAgentByID(agent_id)
```

---

#### `GetAgentByID(agent_id: int) -> Agent | None`
Get agent object by ID.

**Parameters:**
- `agent_id` (int): Agent ID

**Returns:** `Agent` object, or `None` if not found

**Example:**
```python
agent = Py4GW.Agent.GetAgentByID(12345)
if agent:
    print(f"Agent HP: {agent.GetHP()}")
```

---

#### `GetLoot() -> list[int]`
Get list of all loot item agent IDs on the ground.

**Returns:** List of item agent IDs (list[int])

**Example:**
```python
loot_ids = Py4GW.Agent.GetLoot()
print(f"Found {len(loot_ids)} items on ground")
```

---

### Agent Class

Returned by `GetAgentByID()`. All methods are instance methods.

#### Agent Properties

##### `GetAgentID() -> int`
Get the agent's ID.

**Returns:** Agent ID (int)

---

##### `GetPlayerName() -> str`
Get agent's name.

**Returns:** Name string, or empty string if unavailable

---

##### `GetModelID() -> int`
Get agent's model ID.

**Returns:** Model ID (int)

---

##### `GetPosition() -> Vector3`
Get agent's position.

**Returns:** `Vector3` with position

---

##### `GetHP() -> float`
Get agent's health percentage.

**Returns:** HP (0.0 to 1.0)

---

##### `GetMaxHP() -> int`
Get agent's maximum health.

**Returns:** Maximum HP (int)

---

##### `GetEnergy() -> float`
Get agent's energy percentage.

**Returns:** Energy (0.0 to 1.0)

---

##### `GetMaxEnergy() -> int`
Get agent's maximum energy.

**Returns:** Maximum energy (int)

---

##### `GetLevel() -> int`
Get agent's level.

**Returns:** Level (int)

---

#### Agent Type Checking

##### `IsPlayer() -> bool`
Check if agent is a player.

**Returns:** `True` if player, `False` otherwise

---

##### `IsNPC() -> bool`
Check if agent is an NPC.

**Returns:** `True` if NPC, `False` otherwise

---

##### `IsItem() -> bool`
Check if agent is an item on the ground.

**Returns:** `True` if item, `False` otherwise

---

##### `IsGadget() -> bool`
Check if agent is a gadget (chest, lever, etc.).

**Returns:** `True` if gadget, `False` otherwise

---

#### Agent Allegiance

##### `IsEnemy() -> bool`
Check if agent is hostile.

**Returns:** `True` if enemy, `False` otherwise

---

##### `IsAlly() -> bool`
Check if agent is friendly.

**Returns:** `True` if ally, `False` otherwise

---

##### `IsNeutral() -> bool`
Check if agent is neutral.

**Returns:** `True` if neutral, `False` otherwise

---

#### Agent Status

##### `IsAlive() -> bool`
Check if agent is alive.

**Returns:** `True` if alive, `False` otherwise

---

##### `IsDead() -> bool`
Check if agent is dead.

**Returns:** `True` if dead, `False` otherwise

---

##### `IsAttacking() -> bool`
Check if agent is attacking.

**Returns:** `True` if attacking, `False` otherwise

---

##### `IsCasting() -> bool`
Check if agent is casting.

**Returns:** `True` if casting, `False` otherwise

---

##### `IsKnockedDown() -> bool`
Check if agent is knocked down.

**Returns:** `True` if knocked down, `False` otherwise

---

##### `IsMoving() -> bool`
Check if agent is moving.

**Returns:** `True` if moving, `False` otherwise

---

##### `GetEffects() -> list[Effect]`
Get list of effects (buffs/debuffs) on agent.

**Returns:** List of `Effect` objects

**Example:**
```python
effects = agent.GetEffects()
for effect in effects:
    print(f"Effect: {effect.GetSkillID()}")
```

---

---

## Py4GW.Party

Party and hero management.

### Party Information

#### `GetPartySize() -> int`
Get number of party members (including player).

**Returns:** Party size (int, 1-12)

---

#### `GetPartyMembers() -> list[int]`
Get list of all party member agent IDs.

**Returns:** List of agent IDs (list[int])

**Example:**
```python
members = Py4GW.Party.GetPartyMembers()
for member_id in members:
    member = Py4GW.Agent.GetAgentByID(member_id)
    print(f"Party member: {member.GetPlayerName()}")
```

---

#### `GetHeroes() -> list[int]`
Get list of hero agent IDs.

**Returns:** List of hero agent IDs (list[int])

---

#### `GetHenchmen() -> list[int]`
Get list of henchman agent IDs.

**Returns:** List of henchman agent IDs (list[int])

---

#### `GetPartyLeaderID() -> int`
Get agent ID of party leader.

**Returns:** Leader agent ID (int)

---

#### `IsPartyLeader() -> bool`
Check if player is party leader.

**Returns:** `True` if leader, `False` otherwise

---

### Party Management

#### `InvitePlayer(player_name: str) -> None`
Invite a player to party by name.

**Parameters:**
- `player_name` (str): Name of player to invite

---

#### `AddHero(hero_id: int) -> None`
Add a hero to party.

**Parameters:**
- `hero_id` (int): Hero ID

---

#### `KickMember(agent_id: int) -> None`
Kick a party member.

**Parameters:**
- `agent_id` (int): Agent ID of member to kick

---

#### `LeaveParty() -> None`
Leave the current party.

---

### Hero Control

#### `FlagHero(hero_index: int, x: float, y: float) -> None`
Flag a hero to a position.

**Parameters:**
- `hero_index` (int): Hero index (0-6, based on order in party)
- `x` (float): X coordinate
- `y` (float): Y coordinate

**Example:**
```python
# Flag first hero to position
Py4GW.Party.FlagHero(0, -15000, 20000)
```

---

#### `FlagAllHeroes(x: float, y: float) -> None`
Flag all heroes to a position.

**Parameters:**
- `x` (float): X coordinate
- `y` (float): Y coordinate

---

#### `UnflagHero(hero_index: int) -> None`
Remove hero flag.

**Parameters:**
- `hero_index` (int): Hero index (0-6)

---

#### `UnflagAllHeroes() -> None`
Remove all hero flags.

---

#### `SetHeroBehavior(hero_index: int, behavior: str) -> None`
Set hero's combat behavior.

**Parameters:**
- `hero_index` (int): Hero index (0-6)
- `behavior` (str): Behavior mode: `"fight"`, `"guard"`, or `"avoid"`

---

#### `LockHeroTarget(hero_index: int, target_id: int) -> None`
Lock hero's target.

**Parameters:**
- `hero_index` (int): Hero index (0-6)
- `target_id` (int): Target agent ID

---

#### `UnlockHeroTarget(hero_index: int) -> None`
Unlock hero's target.

**Parameters:**
- `hero_index` (int): Hero index (0-6)

---

---

## Py4GW.Inventory

Inventory and item management.

### Bags

#### `GetBackpack() -> Bag`
Get player's backpack (bag 1).

**Returns:** `Bag` object

---

#### `GetBeltPouch() -> Bag`
Get player's belt pouch (bag 2).

**Returns:** `Bag` object

---

#### `GetBag3() -> Bag`
Get bag 3.

**Returns:** `Bag` object

---

#### `GetBag4() -> Bag`
Get bag 4.

**Returns:** `Bag` object

---

#### `GetBag(bag_num: int) -> Bag`
Get bag by number.

**Parameters:**
- `bag_num` (int): Bag number (1-4)

**Returns:** `Bag` object

---

#### `GetStorageChest() -> Storage`
Get storage chest.

**Returns:** `Storage` object

---

#### `GetMaterialStorage() -> MaterialStorage`
Get material storage.

**Returns:** `MaterialStorage` object

---

### Items

#### `GetItemBySlot(bag: int, slot: int) -> Item | None`
Get item at specific bag and slot.

**Parameters:**
- `bag` (int): Bag number (1-4)
- `slot` (int): Slot number (0-based)

**Returns:** `Item` object, or `None` if slot is empty

**Example:**
```python
item = Py4GW.Inventory.GetItemBySlot(1, 0)  # Backpack slot 1
if item:
    print(f"Item: {item.GetName()}")
```

---

#### `GetItemByID(item_id: int) -> Item | None`
Get item by its unique item ID.

**Parameters:**
- `item_id` (int): Item ID

**Returns:** `Item` object, or `None` if not found

---

#### `GetGold() -> int`
Get amount of gold in inventory.

**Returns:** Gold amount (int)

---

#### `GetStorageGold() -> int`
Get amount of gold in storage.

**Returns:** Storage gold amount (int)

---

### Item Operations

#### `UseItem(item_id: int) -> None`
Use an item (consume, equip, etc.).

**Parameters:**
- `item_id` (int): Item ID to use

---

#### `MoveItem(from_bag: int, from_slot: int, to_bag: int, to_slot: int) -> None`
Move item between slots.

**Parameters:**
- `from_bag` (int): Source bag number
- `from_slot` (int): Source slot number
- `to_bag` (int): Destination bag number
- `to_slot` (int): Destination slot number

---

#### `IdentifyItem(item_id: int) -> None`
Identify an unidentified item.

**Parameters:**
- `item_id` (int): Item ID to identify

---

#### `SalvageItem(salvage_kit_id: int, item_id: int) -> None`
Salvage an item using salvage kit.

**Parameters:**
- `salvage_kit_id` (int): Salvage kit item ID
- `item_id` (int): Item to salvage

---

#### `DepositMaterials() -> None`
Deposit all materials into material storage.

---

### Bag Class

#### `GetSize() -> int`
Get number of slots in bag.

**Returns:** Slot count (int)

---

#### `GetItem(slot: int) -> Item | None`
Get item in slot.

**Parameters:**
- `slot` (int): Slot number (0-based)

**Returns:** `Item` object, or `None` if empty

---

### Item Class

#### Item Properties

##### `GetItemID() -> int`
Get unique item ID.

**Returns:** Item ID (int)

---

##### `GetModelID() -> int`
Get item's model ID.

**Returns:** Model ID (int)

---

##### `GetName() -> str`
Get item name.

**Returns:** Name string

---

##### `GetQuantity() -> int`
Get item quantity (for stackable items).

**Returns:** Quantity (int)

---

##### `GetRarity() -> int`
Get item rarity.

**Returns:** Rarity (0=white, 1=blue, 2=purple, 3=gold, 4=green)

---

##### `GetModifier() -> int`
Get item modifier (+damage or armor).

**Returns:** Modifier value (int)

---

##### `GetType() -> int`
Get item type.

**Returns:** Item type ID (int)

---

##### `IsEquipped() -> bool`
Check if item is equipped.

**Returns:** `True` if equipped, `False` otherwise

---

##### `IsCustomized() -> bool`
Check if item is customized.

**Returns:** `True` if customized, `False` otherwise

---

##### `NeedsIdentification() -> bool`
Check if item is unidentified.

**Returns:** `True` if needs ID, `False` otherwise

---

---

## Py4GW.Skillbar

Skillbar management and skill usage.

### Skillbar Access

#### `GetSkillbar() -> Skillbar`
Get player's skillbar.

**Returns:** `Skillbar` object

---

#### `GetSkill(slot: int) -> Skill`
Get skill in a specific slot.

**Parameters:**
- `slot` (int): Skill slot (0-7)

**Returns:** `Skill` object

**Example:**
```python
skill = Py4GW.Skillbar.GetSkill(3)  # Skill in slot 4
print(f"Skill ID: {skill.GetSkillID()}")
```

---

### Skill Usage

#### `UseSkill(slot: int, target_id: int = 0, x: float = 0, y: float = 0) -> None`
Use a skill from skillbar.

**Parameters:**
- `slot` (int): Skill slot (0-7)
- `target_id` (int, optional): Target agent ID for targeted skills
- `x` (float, optional): X coordinate for ground-targeted skills
- `y` (float, optional): Y coordinate for ground-targeted skills

**Examples:**
```python
# Use skill on target
target_id = Py4GW.Player.GetTargetID()
Py4GW.Skillbar.UseSkill(3, target_id)

# Use skill on self
player_id = Py4GW.Player.GetAgentID()
Py4GW.Skillbar.UseSkill(5, player_id)

# Use ground-targeted skill
Py4GW.Skillbar.UseSkill(7, x=-15000, y=20000)

# Use skill (auto-target)
Py4GW.Skillbar.UseSkill(2)
```

---

#### `IsSkillReady(slot: int) -> bool`
Check if skill is recharged and ready to use.

**Parameters:**
- `slot` (int): Skill slot (0-7)

**Returns:** `True` if ready, `False` otherwise

---

#### `GetSkillRecharge(slot: int) -> float`
Get remaining recharge time for skill.

**Parameters:**
- `slot` (int): Skill slot (0-7)

**Returns:** Recharge time in seconds (float)

---

### Skill Class

#### `GetSkillID() -> int`
Get skill's ID.

**Returns:** Skill ID (int)

---

#### `GetRecharge() -> float`
Get remaining recharge time.

**Returns:** Seconds until ready (float, 0 if ready)

---

#### `IsRecharged() -> bool`
Check if skill is recharged.

**Returns:** `True` if recharged, `False` otherwise

---

#### `GetEnergyCost() -> int`
Get skill's energy cost.

**Returns:** Energy cost (int)

---

#### `GetAdrenaline() -> int`
Get skill's adrenaline requirement.

**Returns:** Adrenaline required (0 if not adrenaline skill)

---

### Skill Database

```python
from Py4GWCoreLib import SkillManager

# Get skill info by ID
skill_info = SkillManager.GetSkill(skill_id)
```

**Skill Info Dictionary:**
```python
{
    'id': int,
    'name': str,
    'description': str,
    'profession': str,
    'attribute': str,
    'type': str,  # "spell", "skill", "enchantment", etc.
    'energy': int,
    'cast_time': float,
    'recharge': int,
    'activation': float,
}
```

---

---

## Py4GW.Map

Map and instance information.

### Map Information

#### `GetMapID() -> int`
Get current map ID.

**Returns:** Map ID (int)

**Example:**
```python
map_id = Py4GW.Map.GetMapID()
print(f"Current map: {map_id}")
```

---

#### `GetMapName() -> str`
Get current map name.

**Returns:** Map name string

---

#### `GetInstanceType() -> int`
Get instance type.

**Returns:** Instance type (0=outpost, 1=explorable, 2=mission)

---

#### `IsOutpost() -> bool`
Check if in an outpost.

**Returns:** `True` if in outpost, `False` otherwise

---

#### `IsExplorable() -> bool`
Check if in explorable area.

**Returns:** `True` if explorable, `False` otherwise

---

### Travel

#### `Travel(map_id: int, district: int = 0, region: int = 0, language: int = 0) -> None`
Travel to a map.

**Parameters:**
- `map_id` (int): Destination map ID
- `district` (int, optional): District number (0=current, 1-4=districts)
- `region` (int, optional): Region (0=current, 1=America, 2=Europe, 3=Asia)
- `language` (int, optional): Language (0=English, etc.)

**Example:**
```python
# Travel to Lion's Arch
Py4GW.Map.Travel(77)

# Travel to specific district
Py4GW.Map.Travel(77, district=1)
```

---

#### `EnterInstance() -> None`
Enter an instance (mission/explorable).

---

#### `LeaveInstance() -> None`
Return to outpost.

---

---

## Py4GW.Pathing

Pathfinding and navigation.

### Pathfinding

#### `FindPath(start: Vector3, goal: Vector3) -> list[Vector3] | None`
Find path from start to goal using A* algorithm.

**Parameters:**
- `start` (Vector3): Starting position
- `goal` (Vector3): Goal position

**Returns:** List of waypoints (`list[Vector3]`), or `None` if no path found

**Example:**
```python
from Py4GWCoreLib import Pathing
from Py4GWCoreLib.classes import Vector3

start = Py4GW.Player.GetPosition()
goal = Vector3(-15000, 20000, 0)

path = Pathing.FindPath(start, goal)

if path:
    for waypoint in path:
        Py4GW.Player.Move(waypoint.x, waypoint.y)
        # Wait for arrival...
```

---

#### `IsPathable(x: float, y: float) -> bool`
Check if a position is pathable (walkable).

**Parameters:**
- `x` (float): X coordinate
- `y` (float): Y coordinate

**Returns:** `True` if pathable, `False` if blocked

---

#### `GetNearestPathablePosition(x: float, y: float) -> Vector3`
Find nearest pathable position to given coordinates.

**Parameters:**
- `x` (float): X coordinate
- `y` (float): Y coordinate

**Returns:** `Vector3` with nearest pathable position

---

---

## Py4GW.Camera

Camera control.

### Camera Control

#### `GetPosition() -> Vector3`
Get camera position.

**Returns:** `Vector3` with camera position

---

#### `SetPosition(x: float, y: float, z: float) -> None`
Set camera position.

**Parameters:**
- `x` (float): X coordinate
- `y` (float): Y coordinate
- `z` (float): Z coordinate (height)

---

#### `GetYaw() -> float`
Get camera yaw (horizontal rotation).

**Returns:** Yaw in radians

---

#### `SetYaw(yaw: float) -> None`
Set camera yaw.

**Parameters:**
- `yaw` (float): Yaw in radians

---

#### `GetPitch() -> float`
Get camera pitch (vertical rotation).

**Returns:** Pitch in radians

---

#### `SetPitch(pitch: float) -> None`
Set camera pitch.

**Parameters:**
- `pitch` (float): Pitch in radians

---

---

## Py4GW.UIManager

UI frame manipulation.

### Frame Access

#### `GetFrameByID(frame_id: int) -> Frame | None`
Get UI frame by ID.

**Parameters:**
- `frame_id` (int): Frame ID

**Returns:** `Frame` object, or `None` if not found

---

#### `SendUIMessage(message_id: int, *args) -> None`
Send a message to game UI.

**Parameters:**
- `message_id` (int): Message ID
- `*args`: Variable arguments depending on message type

---

---

## Py4GW.Merchant

NPC merchant interaction.

### Merchant Operations

#### `GetMerchantItems() -> list[Item]`
Get list of items merchant is selling.

**Returns:** List of `Item` objects

---

#### `BuyItem(item_id: int, quantity: int = 1) -> None`
Buy item from merchant.

**Parameters:**
- `item_id` (int): Item ID to buy
- `quantity` (int, optional): Quantity to buy (default: 1)

---

#### `SellItem(item_id: int, quantity: int = 1) -> None`
Sell item to merchant.

**Parameters:**
- `item_id` (int): Item ID to sell
- `quantity` (int, optional): Quantity to sell (default: 1)

---

---

## Py4GW.Effects

Effect (buff/debuff) management.

### Effect Access

#### `GetEffects(agent_id: int) -> list[Effect]`
Get list of effects on an agent.

**Parameters:**
- `agent_id` (int): Agent ID

**Returns:** List of `Effect` objects

---

### Effect Class

#### `GetSkillID() -> int`
Get skill ID of the effect.

**Returns:** Skill ID (int)

---

#### `GetDuration() -> float`
Get remaining duration.

**Returns:** Duration in seconds (float)

---

#### `GetType() -> int`
Get effect type.

**Returns:** Effect type (1=buff, 2=condition, 3=hex, 4=enchantment, 5=stance, 6=well, 7=spirit)

---

---

## Classes

### Vector3

3D position vector.

**Constructor:**
```python
from Py4GWCoreLib.classes import Vector3

pos = Vector3(x=-15000, y=20000, z=0)
```

**Properties:**
- `x` (float): X coordinate
- `y` (float): Y coordinate
- `z` (float): Z coordinate

**Methods:**

##### `distance_to(other: Vector3) -> float`
Calculate distance to another vector.

**Example:**
```python
pos1 = Vector3(-15000, 20000, 0)
pos2 = Vector3(-14000, 21000, 0)
distance = pos1.distance_to(pos2)
```

---

##### `distance_to_2d(other: Vector3) -> float`
Calculate 2D distance (ignoring Z).

---

##### `normalize() -> Vector3`
Get normalized (unit length) vector.

---

##### `__add__(other: Vector3) -> Vector3`
Add two vectors.

**Example:**
```python
result = pos1 + pos2
```

---

##### `__sub__(other: Vector3) -> Vector3`
Subtract two vectors.

---

##### `__mul__(scalar: float) -> Vector3`
Multiply vector by scalar.

---

---

## Botting Framework

### Bot Base Class

```python
from Py4GWCoreLib.Botting import Bot

class MyBot(Bot):
    def __init__(self):
        super().__init__("BotName")
```

### Configuration Properties

#### `enabled_combat: bool`
Enable automatic combat (default: `True`)

---

#### `combat_range: int`
Combat engagement range in distance units (default: `1200`)

---

#### `enabled_loot: bool`
Enable automatic looting (default: `True`)

---

#### `loot_timeout: float`
Timeout for loot pickup in seconds (default: `5.0`)

---

#### `auto_salvage: bool`
Enable automatic salvaging (default: `False`)

---

#### `auto_identify: bool`
Enable automatic identification (default: `False`)

---

### Lifecycle Methods

#### `main_loop()`
Main bot logic loop - override this method.

**Example:**
```python
def main_loop(self):
    self.move_to(-15000, 20000)
    self.kill_all_in_range(1200)
    self.pickup_loot()
```

---

#### `on_start()`
Called when bot starts.

---

#### `on_stop()`
Called when bot stops.

---

#### `on_death()`
Called when player dies.

**Example:**
```python
def on_death(self):
    self.log("Died! Resigning...")
    self.resign()
```

---

### Movement Methods

#### `move_to(x: float, y: float, timeout: float = 30.0) -> bool`
Move to coordinates with timeout.

**Parameters:**
- `x` (float): X coordinate
- `y` (float): Y coordinate
- `timeout` (float): Timeout in seconds

**Returns:** `True` if arrived, `False` if timeout

---

#### `follow_path(waypoints: list[Vector3]) -> bool`
Follow a list of waypoints.

**Parameters:**
- `waypoints` (list[Vector3]): List of positions

**Returns:** `True` if completed, `False` on error

---

### Combat Methods

#### `kill_all_in_range(range: int = 1200) -> None`
Kill all enemies within range.

**Parameters:**
- `range` (int): Combat range

---

#### `attack_target(target_id: int) -> None`
Attack a specific target.

**Parameters:**
- `target_id` (int): Agent ID to attack

---

#### `use_skill_rotation(skills: list[int]) -> None`
Use skills in rotation.

**Parameters:**
- `skills` (list[int]): List of skill slots (0-7)

---

### Loot Methods

#### `pickup_loot(timeout: float = 5.0) -> None`
Pick up all nearby loot.

**Parameters:**
- `timeout` (float): Timeout in seconds

---

#### `filter_loot(min_rarity: str = "blue") -> None`
Pick up loot with minimum rarity.

**Parameters:**
- `min_rarity` (str): Minimum rarity ("white", "blue", "purple", "gold", "green")

---

### Inventory Methods

#### `organize_inventory() -> None`
Organize inventory (stack items, move to proper bags).

---

#### `salvage_items(rarity: str = "blue") -> None`
Salvage items of specified rarity.

**Parameters:**
- `rarity` (str): Target rarity

---

#### `identify_items() -> None`
Identify all unidentified items.

---

### Map Methods

#### `travel_to(map_id: int) -> None`
Travel to a map.

**Parameters:**
- `map_id` (int): Destination map ID

---

#### `resign() -> None`
Resign from current instance.

---

### Utility Methods

#### `wait(seconds: float) -> None`
Wait for specified time.

**Parameters:**
- `seconds` (float): Time to wait

---

#### `log(message: str) -> None`
Log a message.

**Parameters:**
- `message` (str): Message to log

---

---

## Behavior Trees

### Node Types

```python
from Py4GWCoreLib.py4gwcorelib_src.BehaviorTree import *
```

### Composite Nodes

#### `Sequence(children: list[Node])`
Execute children in order until one fails.

**Example:**
```python
heal_sequence = Sequence([
    Condition(lambda: Py4GW.Player.GetHP() < 0.3),
    Action(use_healing_skill)
])
```

---

#### `Selector(children: list[Node])`
Execute children until one succeeds.

**Example:**
```python
combat_selector = Selector([
    heal_if_low_hp,
    attack_enemy,
    find_target
])
```

---

#### `Parallel(children: list[Node])`
Execute all children concurrently.

---

### Decorator Nodes

#### `Inverter(child: Node)`
Invert child's result.

---

#### `Repeater(child: Node, count: int)`
Repeat child N times.

---

### Leaf Nodes

#### `Condition(func: Callable) -> Node`
Check a condition.

**Example:**
```python
low_hp_check = Condition(lambda: Py4GW.Player.GetHP() < 0.5)
```

---

#### `Action(func: Callable) -> Node`
Execute an action.

**Example:**
```python
heal_action = Action(lambda: Py4GW.Skillbar.UseSkill(5, Py4GW.Player.GetAgentID()))
```

---

### Tree Execution

#### `tick() -> NodeStatus`
Execute the tree.

**Returns:** `NodeStatus` (SUCCESS, FAILURE, RUNNING)

---

---

## Action Queue

### ActionQueue Class

```python
from Py4GWCoreLib.py4gwcorelib_src.ActionQueue import ActionQueue

queue = ActionQueue()
```

### Methods

#### `add_action(action, priority: int = 0) -> None`
Add action to queue.

**Parameters:**
- `action`: Action to execute (callable or Action object)
- `priority` (int): Priority (higher = earlier, default: 0)

**Example:**
```python
queue.add_action(lambda: Py4GW.Player.Move(-15000, 20000))
queue.add_action(lambda: Py4GW.Skillbar.UseSkill(3, target_id), priority=1)
```

---

#### `process() -> None`
Process next action in queue.

---

#### `clear() -> None`
Clear all actions from queue.

---

---

## ImGui API

### Window Management

#### `begin(title: str, open: bool = True) -> bool`
Begin ImGui window.

**Parameters:**
- `title` (str): Window title
- `open` (bool): Is window open

**Returns:** `True` if window is open

**Example:**
```python
import PyImGui

window_open = True
if PyImGui.begin("My Window", window_open):
    PyImGui.text("Content here")
PyImGui.end()
```

---

#### `end() -> None`
End ImGui window.

---

### Widgets

#### `text(text: str) -> None`
Display text.

---

#### `button(label: str, width: float = 0, height: float = 0) -> bool`
Display button.

**Returns:** `True` if clicked

---

#### `checkbox(label: str, checked: bool) -> bool`
Display checkbox.

**Returns:** New checked state

---

#### `slider_int(label: str, value: int, min: int, max: int) -> int`
Integer slider.

**Returns:** New value

---

#### `slider_float(label: str, value: float, min: float, max: float) -> float`
Float slider.

**Returns:** New value

---

#### `input_text(label: str, text: str, max_length: int = 256) -> str`
Text input field.

**Returns:** New text value

---

#### `combo(label: str, selected: int, items: list[str]) -> int`
Combo box (dropdown).

**Returns:** Selected index

---

#### `tree_node(label: str) -> bool`
Collapsible tree node.

**Returns:** `True` if expanded

---

#### `tree_pop() -> None`
End tree node.

---

#### `separator() -> None`
Horizontal separator line.

---

#### `same_line() -> None`
Place next widget on same line.

---

---

## Enums and Constants

### Rarity

```python
class Rarity:
    WHITE = 0
    BLUE = 1
    PURPLE = 2
    GOLD = 3
    GREEN = 4
```

### Profession

```python
class Profession:
    NONE = 0
    WARRIOR = 1
    RANGER = 2
    MONK = 3
    NECROMANCER = 4
    MESMER = 5
    ELEMENTALIST = 6
    ASSASSIN = 7
    RITUALIST = 8
    PARAGON = 9
    DERVISH = 10
```

### Allegiance

```python
class Allegiance:
    ALLY = 1
    NEUTRAL = 2
    ENEMY = 3
    SPIRIT = 4
    MINION = 5
    NPC = 6
```

### Instance Type

```python
class InstanceType:
    OUTPOST = 0
    EXPLORABLE = 1
    MISSION = 2
```

---

## Error Handling

Most methods return default values on error:
- `0` for invalid IDs
- `None` for objects not found
- `False` for failed status checks
- Empty lists `[]` for collections

Always check return values:

```python
# Good
agent_id = Py4GW.Player.GetTargetID()
if agent_id > 0:
    agent = Py4GW.Agent.GetAgentByID(agent_id)
    if agent:
        # Safe to use agent
        Py4GW.Player.Attack(agent_id)

# Bad (may crash)
agent = Py4GW.Agent.GetAgentByID(Py4GW.Player.GetTargetID())
agent.GetHP()  # May be None!
```

---

## Threading Considerations

- Most Py4GW methods are **not** thread-safe
- Call Py4GW functions from the **main thread** only
- Use locks when accessing shared data from multiple threads
- Background threads should only perform computation, not game interaction

---

## Performance Tips

1. **Cache frequently accessed data:**
   ```python
   # Good
   player_pos = Py4GW.Player.GetPosition()
   for agent in agents:
       distance = player_pos.distance_to(agent.GetPosition())

   # Bad
   for agent in agents:
       distance = Py4GW.Player.GetPosition().distance_to(agent.GetPosition())
   ```

2. **Batch operations:**
   ```python
   # Good
   all_agents = Py4GW.Agent.GetAllAgents()

   # Bad
   for i in range(1000):
       agent = Py4GW.Agent.GetAgentByID(i)
   ```

3. **Avoid polling:**
   - Use event callbacks when available
   - Add delays between checks

---

## Conclusion

This API reference covers the core Py4GW functionality. For usage examples, see the [User Guide](USER_GUIDE.md). For architectural details, see [Architecture Documentation](ARCHITECTURE.md).

---

**Last Updated:** 2025-12-10
