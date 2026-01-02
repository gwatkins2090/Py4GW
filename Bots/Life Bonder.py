"""
Life Bonder Bot - Standalone Bot for Py4GW
Automatically maintains bonds on the player using a hero life bonder.
"""

from Py4GWCoreLib import *
import math
import time

# Bot state
bot_started = False
template_loaded = False
hero_index = 0  # First hero (0-indexed)
flag_distance = 350.0
last_flag_position = (0.0, 0.0)
current_bond_index = 0  # Track which bond to cast next
next_cast_time = 0  # Time when next cast is allowed (ms since bot started)

# Skill template: OwAS8YIPpE5B9Ie4QCJX/DC
# Slots: 1-Balthazar's Spirit, 2-Life Attunement, 3-Life Bond, 4-Life Barrier,
#        5-Vital Blessing, 6-Purifying Veil, 7-Protective Bond, 8-Blessed Signet
BONDER_TEMPLATE = "OwAS8YIPpE5B9Ie4QCJX/DC"

# Bond configuration - includes cast time in ms
# Cast times: Balthazar's Spirit=2s, Life Attunement=2s, Life Bond=2s,
#             Life Barrier=2s, Vital Blessing=1s, Purifying Veil=1s, Protective Bond=2s
bond_skills = [
    {"name": "Balthazars_Spirit", "slot": 1, "enabled": True, "display": "Balthazar's Spirit", "cast_time": 2000},
    {"name": "Life_Attunement", "slot": 2, "enabled": True, "display": "Life Attunement", "cast_time": 2000},
    {"name": "Life_Bond", "slot": 3, "enabled": True, "display": "Life Bond", "cast_time": 2000},
    {"name": "Life_Barrier", "slot": 4, "enabled": True, "display": "Life Barrier", "cast_time": 2000},
    {"name": "Vital_Blessing", "slot": 5, "enabled": True, "display": "Vital Blessing", "cast_time": 1000},
    {"name": "Purifying_Veil", "slot": 6, "enabled": True, "display": "Purifying Veil", "cast_time": 1000},
    {"name": "Protective_Bond", "slot": 7, "enabled": True, "display": "Protective Bond", "cast_time": 2000},
]
BLESSED_SIGNET_SLOT = 8

# Timers
bond_timer = Timer()
bond_timer.Start()
BOND_CAST_DELAY = 500  # Base delay - will add cast time after each cast
AFTERCAST_BUFFER = 1000  # Buffer for aftercast + ping (1 second)

flag_timer = Timer()
flag_timer.Start()
FLAG_UPDATE_DELAY = 1000  # ms between flag updates

signet_timer = Timer()
signet_timer.Start()
SIGNET_DELAY = 3000  # ms between blessed signet casts

# Colors for UI
GREEN = (0.0, 1.0, 0.0, 1.0)
RED = (1.0, 0.3, 0.3, 1.0)
YELLOW = (1.0, 1.0, 0.0, 1.0)
CYAN = (0.4, 0.8, 1.0, 1.0)
ORANGE = (1.0, 0.5, 0.0, 1.0)


def get_hero_agent_id():
    """Get the agent ID of the life bonder hero."""
    global hero_index
    try:
        heroes = GLOBAL_CACHE.Party.GetHeroes()
        if len(heroes) > hero_index:
            return GLOBAL_CACHE.Party.Heroes.GetHeroAgentIDByPartyPosition(hero_index)
    except:
        pass
    return 0


def calculate_position_behind_player(distance):
    """Calculate a position behind the player based on their facing direction."""
    try:
        player_id = GLOBAL_CACHE.Player.GetAgentID()
        player_x, player_y = GLOBAL_CACHE.Player.GetXY()
        player_angle = GLOBAL_CACHE.Agent.GetRotationAngle(player_id)

        # Calculate position behind player (opposite of facing direction)
        behind_angle = player_angle + math.pi  # Add 180 degrees

        flag_x = player_x + distance * math.cos(behind_angle)
        flag_y = player_y + distance * math.sin(behind_angle)

        return (flag_x, flag_y)
    except:
        return None


def check_bond_on_player(skill_name):
    """Check if a specific bond is active on the player using BuffExists/EffectExists."""
    try:
        player_id = GLOBAL_CACHE.Player.GetAgentID()
        skill_id = GLOBAL_CACHE.Skill.GetID(skill_name)
        if skill_id == 0:
            return False  # If skill not found, assume it's not active
        # Check both buffs and effects
        return (GLOBAL_CACHE.Effects.BuffExists(player_id, skill_id) or
                GLOBAL_CACHE.Effects.EffectExists(player_id, skill_id))
    except:
        return False


def get_hero_energy_points(hero_id):
    """Get the hero's current energy in actual points (not percentage)."""
    try:
        energy_pct = GLOBAL_CACHE.Agent.GetEnergy(hero_id)
        max_energy = GLOBAL_CACHE.Agent.GetMaxEnergy(hero_id)
        if energy_pct is not None and max_energy is not None:
            return int(energy_pct * max_energy)
    except:
        pass
    return 0


def get_next_missing_bond():
    """Get the next bond that needs to be cast on the player."""
    global bond_skills
    for bond in bond_skills:
        if bond["enabled"] and not check_bond_on_player(bond["name"]):
            return bond
    return None


def update_hero_flag():
    """Update the flag position for the life bonder hero."""
    global last_flag_position, flag_timer, flag_distance

    if not flag_timer.HasElapsed(FLAG_UPDATE_DELAY):
        return

    hero_id = get_hero_agent_id()
    if hero_id == 0:
        return

    new_pos = calculate_position_behind_player(flag_distance)
    if new_pos is None:
        return

    # Only update if position has changed significantly (more than 50 units)
    dx = new_pos[0] - last_flag_position[0]
    dy = new_pos[1] - last_flag_position[1]
    distance_moved = math.sqrt(dx*dx + dy*dy)

    if distance_moved > 50.0:
        GLOBAL_CACHE.Party.Heroes.FlagHero(hero_id, new_pos[0], new_pos[1])
        last_flag_position = new_pos
        flag_timer.Reset()


def maintain_bonds():
    """Cycle through bonds and cast them on the player - skip if already active."""
    global bond_timer, hero_index, current_bond_index, bond_skills, next_cast_time

    # Check if we're still waiting for the previous cast to finish
    current_time = int(time.time() * 1000)
    if current_time < next_cast_time:
        return

    hero_id = get_hero_agent_id()
    if hero_id == 0:
        return

    # Check if hero is alive
    if not GLOBAL_CACHE.Agent.IsLiving(hero_id):
        return

    # Check hero energy - don't cast bonds if below 20 energy
    hero_energy = get_hero_energy_points(hero_id)
    if hero_energy < 20:
        return  # Let use_blessed_signet handle energy recovery

    # Get player (target for bonds)
    player_id = GLOBAL_CACHE.Player.GetAgentID()
    if player_id == 0:
        return

    # Find the next enabled bond that's NOT already on the player
    attempts = 0
    while attempts < len(bond_skills):
        bond = bond_skills[current_bond_index]

        # Move to next bond for next iteration
        current_bond_index = (current_bond_index + 1) % len(bond_skills)

        if bond["enabled"]:
            # Check if this bond is already active on the player
            if check_bond_on_player(bond["name"]):
                attempts += 1
                continue  # Skip - already has this bond

            # HeroUseSkill uses 1-indexed hero numbers (1-7)
            hero_number = hero_index + 1
            skill_slot = bond["slot"]

            # Cast the bond on the player
            GLOBAL_CACHE.SkillBar.HeroUseSkill(player_id, skill_slot, hero_number)

            # Set the next cast time based on this skill's cast time + buffer
            cast_time = bond.get("cast_time", 2000)
            next_cast_time = current_time + cast_time + AFTERCAST_BUFFER

            Py4GW.Console.Log("Life Bonder", f"Casting {bond['display']} (slot {skill_slot}) - waiting {cast_time + AFTERCAST_BUFFER}ms", Py4GW.Console.MessageType.Info)
            return

        attempts += 1


def use_blessed_signet():
    """Use Blessed Signet for energy management when below 20 energy."""
    global signet_timer, hero_index, next_cast_time

    # Check if we're still waiting for a cast to finish
    current_time = int(time.time() * 1000)
    if current_time < next_cast_time:
        return False  # Return False to indicate we didn't cast

    hero_id = get_hero_agent_id()
    if hero_id == 0:
        return False

    if not GLOBAL_CACHE.Agent.IsLiving(hero_id):
        return False

    try:
        hero_energy = get_hero_energy_points(hero_id)
        # Cast Blessed Signet when energy drops below 20
        if hero_energy < 20:
            # HeroUseSkill uses 1-indexed hero numbers (1-7)
            hero_number = hero_index + 1
            # Blessed Signet targets self (hero's own ID)
            GLOBAL_CACHE.SkillBar.HeroUseSkill(hero_id, BLESSED_SIGNET_SLOT, hero_number)

            # Blessed Signet is instant cast (0.25s activation) but add buffer
            next_cast_time = current_time + 500  # Small delay for signet

            Py4GW.Console.Log("Life Bonder", f"Using Blessed Signet (energy: {hero_energy})", Py4GW.Console.MessageType.Info)
            signet_timer.Reset()
            return True  # Return True to indicate we cast
    except:
        pass
    return False


def load_template():
    """Load the life bonder template on the hero."""
    global template_loaded, hero_index
    try:
        # LoadHeroSkillTemplate uses 1-indexed hero numbers (1-7)
        hero_number = hero_index + 1
        GLOBAL_CACHE.SkillBar.LoadHeroSkillTemplate(hero_number, BONDER_TEMPLATE)
        template_loaded = True
        Py4GW.Console.Log("Life Bonder", f"Template loaded on Hero {hero_number}", Py4GW.Console.MessageType.Info)
    except Exception as e:
        Py4GW.Console.Log("Life Bonder", f"Error loading template: {str(e)}", Py4GW.Console.MessageType.Error)


def run_bot():
    """Main bot logic - called when bot is started."""
    try:
        update_hero_flag()

        # Prioritize energy management - cast Blessed Signet first if needed
        # Only try to maintain bonds if we're not recovering energy
        if not use_blessed_signet():
            maintain_bonds()
    except Exception as e:
        Py4GW.Console.Log("Life Bonder", f"Error in run_bot: {str(e)}", Py4GW.Console.MessageType.Error)


def draw_ui():
    """Draw the bot configuration UI."""
    global bot_started, template_loaded, hero_index, flag_distance, bond_skills

    if PyImGui.begin("Life Bonder Bot", PyImGui.WindowFlags.AlwaysAutoResize):

        # Title
        PyImGui.text_colored("Life Bonder Hero Bot", CYAN)
        PyImGui.text("Maintains bonds on you using a hero.")
        PyImGui.separator()

        # Start/Stop Button
        if not bot_started:
            PyImGui.push_style_color(PyImGui.ImGuiCol.Button, (0.2, 0.6, 0.2, 1.0))
            PyImGui.push_style_color(PyImGui.ImGuiCol.ButtonHovered, (0.3, 0.7, 0.3, 1.0))
            PyImGui.push_style_color(PyImGui.ImGuiCol.ButtonActive, (0.1, 0.5, 0.1, 1.0))
            if PyImGui.button("Start Life Bonder"):
                bot_started = True
                Py4GW.Console.Log("Life Bonder", "Bot Started", Py4GW.Console.MessageType.Info)
            PyImGui.pop_style_color(3)
        else:
            PyImGui.push_style_color(PyImGui.ImGuiCol.Button, (0.6, 0.2, 0.2, 1.0))
            PyImGui.push_style_color(PyImGui.ImGuiCol.ButtonHovered, (0.7, 0.3, 0.3, 1.0))
            PyImGui.push_style_color(PyImGui.ImGuiCol.ButtonActive, (0.5, 0.1, 0.1, 1.0))
            if PyImGui.button("Stop Life Bonder"):
                bot_started = False
                Py4GW.Console.Log("Life Bonder", "Bot Stopped", Py4GW.Console.MessageType.Info)
            PyImGui.pop_style_color(3)

        PyImGui.same_line(0, 10)
        if bot_started:
            PyImGui.text_colored("RUNNING", GREEN)
        else:
            PyImGui.text_colored("STOPPED", RED)

        PyImGui.separator()

        # Hero Selection
        PyImGui.text("Hero Position:")
        hero_options = ["Hero 1", "Hero 2", "Hero 3", "Hero 4", "Hero 5", "Hero 6", "Hero 7"]
        new_hero_index = PyImGui.combo("##hero_select", hero_index, hero_options)
        if new_hero_index != hero_index:
            hero_index = new_hero_index
            template_loaded = False  # Need to reload template for new hero

        # Load Template Button
        if PyImGui.button("Load Template"):
            template_loaded = False
            if GLOBAL_CACHE.Map.IsOutpost():
                load_template()
            else:
                Py4GW.Console.Log("Life Bonder", "Must be in outpost to load template!", Py4GW.Console.MessageType.Warning)

        PyImGui.same_line(0, 10)
        if template_loaded:
            PyImGui.text_colored("Template Loaded", GREEN)
        else:
            PyImGui.text_colored("Template Not Loaded", ORANGE)

        PyImGui.separator()

        # Flagging Distance
        PyImGui.text("Flag Distance Behind:")
        flag_distance = PyImGui.slider_float("##flag_dist", flag_distance, 150.0, 600.0)

        PyImGui.separator()

        # Bond Status
        PyImGui.text_colored("Bond Status:", YELLOW)

        for i, bond in enumerate(bond_skills):
            is_active = check_bond_on_player(bond["name"])

            # Checkbox
            bond["enabled"] = PyImGui.checkbox(f"##{bond['name']}", bond["enabled"])
            PyImGui.same_line(0, 5)

            # Status indicator
            if is_active:
                PyImGui.text_colored(bond["display"], GREEN)
            else:
                PyImGui.text_colored(bond["display"], RED)

        PyImGui.separator()

        # Hero Info
        hero_id = get_hero_agent_id()
        if hero_id != 0:
            try:
                hero_name = GLOBAL_CACHE.Party.Heroes.GetNameByAgentID(hero_id)
                if hero_name:
                    PyImGui.text(f"Active Hero: {hero_name}")

                hero_energy = get_hero_energy_points(hero_id)
                max_energy = GLOBAL_CACHE.Agent.GetMaxEnergy(hero_id) or 0
                if hero_energy < 20:
                    PyImGui.text_colored(f"Hero Energy: {hero_energy}/{max_energy} (LOW!)", RED)
                elif hero_energy < 30:
                    PyImGui.text_colored(f"Hero Energy: {hero_energy}/{max_energy}", YELLOW)
                else:
                    PyImGui.text_colored(f"Hero Energy: {hero_energy}/{max_energy}", GREEN)

                if GLOBAL_CACHE.Agent.IsLiving(hero_id):
                    PyImGui.text_colored("Hero Status: Alive", GREEN)
                else:
                    PyImGui.text_colored("Hero Status: Dead", RED)
            except:
                pass
        else:
            PyImGui.text_colored("No hero found in party", ORANGE)

        PyImGui.end()


def main():
    """Main entry point - called every frame."""
    global bot_started, template_loaded

    # Always draw UI
    draw_ui()

    # Check if map is valid
    if not Routines.Checks.Map.MapValid():
        return

    # In outpost: try to load template if needed
    if GLOBAL_CACHE.Map.IsOutpost():
        if bot_started and not template_loaded:
            load_template()
        return

    # In explorable: run bot if started
    if GLOBAL_CACHE.Map.IsExplorable():
        if bot_started:
            run_bot()


if __name__ == "__main__":
    main()
