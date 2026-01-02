import traceback
import math
import Py4GW

from Py4GWCoreLib import IniHandler, Timer, ThrottledTimer
from Py4GWCoreLib import GLOBAL_CACHE
from Py4GWCoreLib import PyImGui
from Py4GWCoreLib import ImGui
from Py4GWCoreLib import Routines
from Py4GWCoreLib import Effects

import os

module_name = "Life Bonder"

script_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = os.path.normpath(os.path.join(script_directory, ".."))
ini_file_location = os.path.join(root_directory, "Widgets/Config/Life Bonder.ini")

ini_handler = IniHandler(ini_file_location)
sync_timer = Timer()
sync_timer.Start()
sync_interval = 1000


class LifeBonderVars:
    def __init__(self):
        # Core settings
        self.enabled = False
        self.hero_index = 0                      # First hero (party position 0)
        self.template = "OwAS8YIPpE5B9Ie4QCJX/DC"
        self.template_loaded = False

        # Flagging settings
        self.flagging_enabled = True
        self.flag_distance = 350.0               # Distance behind player to flag bonder

        # Bond skill configuration
        # Template: OwAS8YIPpE5B9Ie4QCJX/DC
        # Slots: 1-Balthazar's Spirit, 2-Life Attunement, 3-Life Bond, 4-Life Barrier,
        #        5-Vital Blessing, 6-Purifying Veil, 7-Protective Bond, 8-Blessed Signet
        self.bond_skills = [
            {"name": "Balthazars_Spirit", "slot": 1, "enabled": True, "display": "Balthazar's Spirit"},
            {"name": "Life_Attunement", "slot": 2, "enabled": True, "display": "Life Attunement"},
            {"name": "Life_Bond", "slot": 3, "enabled": True, "display": "Life Bond"},
            {"name": "Life_Barrier", "slot": 4, "enabled": True, "display": "Life Barrier"},
            {"name": "Vital_Blessing", "slot": 5, "enabled": True, "display": "Vital Blessing"},
            {"name": "Purifying_Veil", "slot": 6, "enabled": True, "display": "Purifying Veil"},
            {"name": "Protective_Bond", "slot": 7, "enabled": True, "display": "Protective Bond"},
        ]
        self.blessed_signet_slot = 8
        self.blessed_signet_enabled = True
        self.blessed_signet_threshold = 0.5      # Cast when energy below 50%

        # Timers
        self.bond_cast_timer = ThrottledTimer(1500)
        self.flag_update_timer = ThrottledTimer(1000)
        self.blessed_signet_timer = ThrottledTimer(3000)
        self.cache_timer = ThrottledTimer(200)

        # Cached values
        self.player_agent_id = 0
        self.hero_agent_id = 0
        self.last_flag_position = (0.0, 0.0)

    def reset(self):
        self.template_loaded = False
        self.bond_cast_timer.Reset()
        self.flag_update_timer.Reset()
        self.blessed_signet_timer.Reset()
        self.cache_timer.Reset()
        self.player_agent_id = 0
        self.hero_agent_id = 0
        self.last_flag_position = (0.0, 0.0)

    def update_cache(self):
        if self.cache_timer.IsExpired():
            self.player_agent_id = GLOBAL_CACHE.Player.GetAgentID()
            self.hero_agent_id = self._get_hero_agent_id()
            self.cache_timer.Reset()

    def _get_hero_agent_id(self):
        try:
            heroes = GLOBAL_CACHE.Party.GetHeroes()
            if len(heroes) > self.hero_index:
                return GLOBAL_CACHE.Party.Heroes.GetHeroAgentIDByPartyPosition(self.hero_index)
        except:
            pass
        return 0


bonder = LifeBonderVars()


# ============== CORE FUNCTIONS ==============

def calculate_position_behind_player(distance: float):
    """Calculate a position behind the player based on their facing direction."""
    try:
        player_x, player_y = GLOBAL_CACHE.Player.GetXY()
        player_angle = GLOBAL_CACHE.Agent.GetRotationAngle(bonder.player_agent_id)

        # Calculate position behind player (opposite of facing direction)
        behind_angle = player_angle + math.pi  # Add 180 degrees

        flag_x = player_x + distance * math.cos(behind_angle)
        flag_y = player_y + distance * math.sin(behind_angle)

        return (flag_x, flag_y)
    except:
        return (0.0, 0.0)


def update_hero_flag():
    """Update the flag position for the life bonder hero."""
    if not bonder.enabled or not bonder.flagging_enabled:
        return

    if not bonder.flag_update_timer.IsExpired():
        return

    if bonder.hero_agent_id == 0:
        return

    # Calculate new position behind player
    new_pos = calculate_position_behind_player(bonder.flag_distance)
    if new_pos == (0.0, 0.0):
        return

    # Only update if position has changed significantly (more than 50 units)
    dx = new_pos[0] - bonder.last_flag_position[0]
    dy = new_pos[1] - bonder.last_flag_position[1]
    distance_moved = math.sqrt(dx*dx + dy*dy)

    if distance_moved > 50.0:
        GLOBAL_CACHE.Party.Heroes.FlagHero(bonder.hero_agent_id, new_pos[0], new_pos[1])
        bonder.last_flag_position = new_pos
        bonder.flag_update_timer.Reset()


def check_bond_on_player(skill_name: str) -> bool:
    """Check if a specific bond is active on the player."""
    try:
        skill_id = GLOBAL_CACHE.Skill.GetID(skill_name)
        if skill_id == 0:
            return True  # If skill not found, assume it's active
        return Effects.HasEffect(bonder.player_agent_id, skill_id)
    except:
        return True


def get_next_missing_bond():
    """Get the next bond that needs to be cast on the player."""
    for bond in bonder.bond_skills:
        if bond["enabled"] and not check_bond_on_player(bond["name"]):
            return bond
    return None


def cast_hero_skill(skill_slot: int, target_agent_id: int):
    """Have the life bonder hero cast a skill."""
    try:
        if bonder.hero_agent_id == 0:
            return False

        # HeroUseSkill(target_agent_id, skill_number, hero_number)
        # hero_number is 1-indexed (1 = first hero)
        hero_number = bonder.hero_index + 1
        GLOBAL_CACHE.SkillBar.HeroUseSkill(target_agent_id, skill_slot, hero_number)
        return True
    except Exception as e:
        Py4GW.Console.Log(module_name, f"Error casting hero skill: {str(e)}", Py4GW.Console.MessageType.Error)
        return False


def maintain_bonds():
    """Check and recast bonds that have expired."""
    if not bonder.enabled:
        return

    if not bonder.bond_cast_timer.IsExpired():
        return

    if bonder.hero_agent_id == 0:
        return

    # Check if hero is alive
    if not GLOBAL_CACHE.Agent.IsLiving(bonder.hero_agent_id):
        return

    # Find the next missing bond
    missing_bond = get_next_missing_bond()
    if missing_bond is not None:
        if cast_hero_skill(missing_bond["slot"], bonder.player_agent_id):
            Py4GW.Console.Log(module_name, f"Casting {missing_bond['display']} on player", Py4GW.Console.MessageType.Info)
            bonder.bond_cast_timer.Reset()


def use_blessed_signet():
    """Use Blessed Signet for energy management."""
    if not bonder.enabled or not bonder.blessed_signet_enabled:
        return

    if not bonder.blessed_signet_timer.IsExpired():
        return

    if bonder.hero_agent_id == 0:
        return

    if not GLOBAL_CACHE.Agent.IsLiving(bonder.hero_agent_id):
        return

    try:
        hero_energy = GLOBAL_CACHE.Agent.GetEnergy(bonder.hero_agent_id)
        if hero_energy is not None and hero_energy < bonder.blessed_signet_threshold:
            # Blessed Signet targets self
            if cast_hero_skill(bonder.blessed_signet_slot, bonder.hero_agent_id):
                bonder.blessed_signet_timer.Reset()
    except:
        pass


def load_template():
    """Load the life bonder skill template on the hero."""
    if bonder.template_loaded:
        return

    if not bonder.enabled:
        return

    try:
        GLOBAL_CACHE.SkillBar.LoadHeroSkillTemplate(bonder.hero_index, bonder.template)
        bonder.template_loaded = True
        Py4GW.Console.Log(module_name, f"Loaded life bonder template on hero {bonder.hero_index + 1}", Py4GW.Console.MessageType.Info)
    except Exception as e:
        Py4GW.Console.Log(module_name, f"Error loading template: {str(e)}", Py4GW.Console.MessageType.Error)


# ============== CONFIGURATION ==============

class Config:
    def __init__(self):
        # Load settings from INI
        bonder.enabled = ini_handler.read_bool(module_name, "enabled", False)
        bonder.flagging_enabled = ini_handler.read_bool(module_name, "flagging_enabled", True)
        bonder.flag_distance = ini_handler.read_float(module_name, "flag_distance", 350.0)
        bonder.blessed_signet_enabled = ini_handler.read_bool(module_name, "blessed_signet_enabled", True)
        bonder.blessed_signet_threshold = ini_handler.read_float(module_name, "blessed_signet_threshold", 0.5)

        # Load bond enabled states
        for i, bond in enumerate(bonder.bond_skills):
            enabled = ini_handler.read_bool(module_name, f"bond_{i}_enabled", True)
            bonder.bond_skills[i]["enabled"] = enabled

    def save(self):
        if sync_timer.HasElapsed(sync_interval):
            ini_handler.write_key(module_name, "enabled", str(bonder.enabled))
            ini_handler.write_key(module_name, "flagging_enabled", str(bonder.flagging_enabled))
            ini_handler.write_key(module_name, "flag_distance", str(bonder.flag_distance))
            ini_handler.write_key(module_name, "blessed_signet_enabled", str(bonder.blessed_signet_enabled))
            ini_handler.write_key(module_name, "blessed_signet_threshold", str(bonder.blessed_signet_threshold))

            for i, bond in enumerate(bonder.bond_skills):
                ini_handler.write_key(module_name, f"bond_{i}_enabled", str(bond["enabled"]))

            sync_timer.Start()


config = Config()

# Window setup
window_module = ImGui.WindowModule(
    module_name,
    window_name=f"{module_name}##{module_name}",
    window_size=(300, 400),
    window_flags=PyImGui.WindowFlags.AlwaysAutoResize
)
window_x = ini_handler.read_int(module_name, "window_x", 100)
window_y = ini_handler.read_int(module_name, "window_y", 100)
window_module.window_pos = (window_x, window_y)


def configure():
    """Draw the configuration UI."""
    global config, window_module

    try:
        if not Routines.Checks.Map.MapValid():
            bonder.reset()
            return

        if window_module.first_run:
            PyImGui.set_next_window_size(window_module.window_size[0], window_module.window_size[1])
            PyImGui.set_next_window_pos(window_module.window_pos[0], window_module.window_pos[1])
            window_module.first_run = False

        end_pos = window_module.window_pos

        if PyImGui.begin(window_module.window_name, window_module.window_flags):
            # Title
            PyImGui.text_colored("Life Bonder Hero Bot", (0.4, 0.8, 1.0, 1.0))
            PyImGui.separator()

            # Enable/Disable
            bonder.enabled = PyImGui.checkbox("Enable Bot", bonder.enabled)
            if bonder.enabled and not bonder.template_loaded:
                bonder.template_loaded = False  # Will trigger reload

            PyImGui.separator()

            # Hero Selection
            PyImGui.text("Hero Position:")
            PyImGui.same_line(0, 10)
            hero_options = ["Hero 1", "Hero 2", "Hero 3", "Hero 4", "Hero 5", "Hero 6", "Hero 7"]
            bonder.hero_index = PyImGui.combo("##hero_select", bonder.hero_index, hero_options)

            # Load Template button
            if PyImGui.button("Load Template##load"):
                bonder.template_loaded = False
                if GLOBAL_CACHE.Map.IsOutpost():
                    load_template()

            PyImGui.same_line(0, 10)
            if bonder.template_loaded:
                PyImGui.text_colored("Template Loaded", (0.0, 1.0, 0.0, 1.0))
            else:
                PyImGui.text_colored("Not Loaded", (1.0, 0.5, 0.0, 1.0))

            PyImGui.separator()

            # Flagging Section
            PyImGui.text_colored("Hero Flagging", (0.8, 0.8, 0.2, 1.0))
            bonder.flagging_enabled = PyImGui.checkbox("Enable Flagging", bonder.flagging_enabled)

            if bonder.flagging_enabled:
                bonder.flag_distance = PyImGui.slider_float("Distance Behind##flag", bonder.flag_distance, 150.0, 600.0)
                PyImGui.text_wrapped("Hero will stay behind you to avoid aggro.")

            PyImGui.separator()

            # Bond Status
            PyImGui.text_colored("Bond Status", (0.8, 0.8, 0.2, 1.0))

            for i, bond in enumerate(bonder.bond_skills):
                is_active = check_bond_on_player(bond["name"])

                # Checkbox
                bond["enabled"] = PyImGui.checkbox(f"##{bond['name']}", bond["enabled"])
                PyImGui.same_line(0, 5)

                # Status indicator
                if is_active:
                    PyImGui.text_colored(bond["display"], (0.0, 1.0, 0.0, 1.0))
                else:
                    PyImGui.text_colored(bond["display"], (1.0, 0.3, 0.3, 1.0))

            PyImGui.separator()

            # Blessed Signet Section
            PyImGui.text_colored("Energy Management", (0.8, 0.8, 0.2, 1.0))
            bonder.blessed_signet_enabled = PyImGui.checkbox("Use Blessed Signet", bonder.blessed_signet_enabled)

            if bonder.blessed_signet_enabled:
                threshold_pct = int(bonder.blessed_signet_threshold * 100)
                threshold_pct = PyImGui.slider_int("Energy Threshold %##signet", threshold_pct, 20, 80)
                bonder.blessed_signet_threshold = threshold_pct / 100.0

            # Hero Info
            PyImGui.separator()
            if bonder.hero_agent_id != 0:
                try:
                    hero_name = GLOBAL_CACHE.Party.Heroes.GetNameByAgentID(bonder.hero_agent_id)
                    if hero_name:
                        PyImGui.text(f"Active Hero: {hero_name}")

                    hero_energy = GLOBAL_CACHE.Agent.GetEnergy(bonder.hero_agent_id)
                    if hero_energy is not None:
                        energy_pct = int(hero_energy * 100)
                        if energy_pct < 30:
                            PyImGui.text_colored(f"Hero Energy: {energy_pct}%", (1.0, 0.3, 0.3, 1.0))
                        elif energy_pct < 60:
                            PyImGui.text_colored(f"Hero Energy: {energy_pct}%", (1.0, 1.0, 0.0, 1.0))
                        else:
                            PyImGui.text_colored(f"Hero Energy: {energy_pct}%", (0.0, 1.0, 0.0, 1.0))

                    if GLOBAL_CACHE.Agent.IsLiving(bonder.hero_agent_id):
                        PyImGui.text_colored("Hero Status: Alive", (0.0, 1.0, 0.0, 1.0))
                    else:
                        PyImGui.text_colored("Hero Status: Dead", (1.0, 0.0, 0.0, 1.0))
                except:
                    pass
            else:
                PyImGui.text_colored("No hero found in party", (1.0, 0.5, 0.0, 1.0))

            config.save()
            end_pos = PyImGui.get_window_pos()

        PyImGui.end()

        # Save window position
        if end_pos[0] != window_module.window_pos[0] or end_pos[1] != window_module.window_pos[1]:
            window_module.window_pos = (int(end_pos[0]), int(end_pos[1]))
            ini_handler.write_key(module_name, "window_x", str(int(end_pos[0])))
            ini_handler.write_key(module_name, "window_y", str(int(end_pos[1])))

    except Exception as e:
        Py4GW.Console.Log(module_name, f"Error in configure: {str(e)}", Py4GW.Console.MessageType.Error)
        Py4GW.Console.Log(module_name, f"Stack trace: {traceback.format_exc()}", Py4GW.Console.MessageType.Error)


def main():
    """Main bot loop."""
    try:
        if not Routines.Checks.Map.MapValid():
            bonder.reset()
            return

        bonder.update_cache()

        if not bonder.enabled:
            return

        # In outpost: load template
        if GLOBAL_CACHE.Map.IsOutpost():
            load_template()
            return

        # In explorable: run bot
        if GLOBAL_CACHE.Map.IsExplorable():
            update_hero_flag()
            maintain_bonds()
            use_blessed_signet()

    except Exception as e:
        Py4GW.Console.Log(module_name, f"Error in main: {str(e)}", Py4GW.Console.MessageType.Error)
        Py4GW.Console.Log(module_name, f"Stack trace: {traceback.format_exc()}", Py4GW.Console.MessageType.Error)


if __name__ == "__main__":
    main()
