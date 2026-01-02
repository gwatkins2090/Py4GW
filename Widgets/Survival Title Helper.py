import traceback
import math
import Py4GW

from Py4GWCoreLib import IniHandler, Timer, ThrottledTimer
from Py4GWCoreLib import GLOBAL_CACHE
from Py4GWCoreLib import RawAgentArray
from Py4GWCoreLib import PyImGui
from Py4GWCoreLib import ImGui
from Py4GWCoreLib import Routines
from Py4GWCoreLib import Keystroke
from Py4GWCoreLib import Key
from Py4GWCoreLib import ActionQueueManager
from Py4GWCoreLib import Effects

import os

module_name = "Survival Title Helper"

script_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = os.path.normpath(os.path.join(script_directory, ".."))
ini_file_location = os.path.join(root_directory, "Widgets/Config/Survival Title Helper.ini")

ini_handler = IniHandler(ini_file_location)
sync_timer = Timer()
sync_timer.Start()
sync_interval = 1000

class Global_Vars:
    def __init__(self):
        self.lvl1_10_threshold = 50           # lvl 1 - 10 threshold
        self.lvl11_20_threshold = 120         # lvl 11 - 20 threshold
        self.current_threhold = 50            # currrent treshold
        self.default_max_health_table = {
            1: 100,
            2: 120,
            3: 140,
            4: 160,
            5: 180,
            6: 200,
            7: 220,
            8: 240,
            9: 260,
            10: 280,
            11: 300,
            12: 320,
            13: 340,
            14: 360,
            15: 380,
            16: 400,
            17: 420,
            18: 440,
            19: 460,
            20: 480,    # Maybe this should be set to 550 +50 health rune, but pre-searing it's 480 (510 with health rune)
        }
        self.players_max_health_table:dict[int, float] = {}
        self.party_leader_name:dict[int, str] = {}
        self.is_party_leader = False
        self.reform_party = False
        self.party_names:dict[int, str] = {}
        self.last_outpost = 0

        self.low_life = False
        self.low_life_agent = 0
        self.log_low_health = True

        self.game_time = 200                  # Time between Updates
        self.game_timer = Timer()             # Timer for Time between Updates
        self.game_timer.Start()               # Starting the Timer for Time between Updates
        
        self.outpost_timer = ThrottledTimer(500)
        self.cache_timer = ThrottledTimer(200)

        self.travel_time = 4000               # Time between Updates
        self.travel_timer = Timer()           # Timer for Time between Updates
        self.travel_timer.Start()             # Starting the Timer for Time between Updates
        
        #extra control golbal cache variables added by apo
        self.player_agent_id = 0
        self.party_players = []
        self.plarty_leader_id = 0

        # Life Bonder Configuration
        self.life_bonder_enabled = False
        self.life_bonder_distance = 350.0       # Distance behind player to flag bonder
        self.life_bonder_hero_index = 0         # First hero (party position 0)
        self.life_bonder_template = "OwAS8YIPpE5B9Ie4QCJX/DC"
        self.life_bonder_template_loaded = False

        # Bond skill names and their slot positions in the template
        # Template: OwAS8YIPpE5B9Ie4QCJX/DC
        # Slots: 1-Balthazar's Spirit, 2-Life Attunement, 3-Life Bond, 4-Life Barrier,
        #        5-Vital Blessing, 6-Purifying Veil, 7-Protective Bond, 8-Blessed Signet
        self.bond_skills = [
            {"name": "Balthazars_Spirit", "slot": 1, "enabled": True},
            {"name": "Life_Attunement", "slot": 2, "enabled": True},
            {"name": "Life_Bond", "slot": 3, "enabled": True},
            {"name": "Life_Barrier", "slot": 4, "enabled": True},
            {"name": "Vital_Blessing", "slot": 5, "enabled": True},
            {"name": "Purifying_Veil", "slot": 6, "enabled": True},
            {"name": "Protective_Bond", "slot": 7, "enabled": True},
        ]
        self.blessed_signet_slot = 8            # Slot for energy management
        self.bond_cast_timer = ThrottledTimer(1500)  # Delay between bond casts
        self.flag_update_timer = ThrottledTimer(1000)  # Delay between flag updates
        self.blessed_signet_timer = ThrottledTimer(3000)  # Delay for blessed signet
        self.last_bonder_position = (0.0, 0.0)

    def reset_vars(self):
        if self.low_life:
            self.low_life = False
        if self.low_life_agent != 0:
            self.low_life_agent = 0
        if len(self.players_max_health_table) > 0:
            self.players_max_health_table = {}
        if self.log_low_health == False:
            self.log_low_health = True

        self.game_timer.Reset()
        self.outpost_timer.Reset()
        self.cache_timer.Reset()
        self.party_names = {}

        # Reset life bonder state
        self.life_bonder_template_loaded = False
        self.bond_cast_timer.Reset()
        self.flag_update_timer.Reset()
        self.blessed_signet_timer.Reset()
        self.last_bonder_position = (0.0, 0.0)
            
    def update_cache(self):
        if self.cache_timer.IsExpired():
            self.player_agent_id = GLOBAL_CACHE.Player.GetAgentID()
            self.party_players =  GLOBAL_CACHE.Party.GetPlayers()
            self.plarty_leader_id = GLOBAL_CACHE.Party.GetPartyLeaderID()
            if GLOBAL_CACHE.Party.IsPartyLeader():
                self.is_party_leader = True
            self.cache_timer.Reset()


global_vars = Global_Vars()

def update_max_health():
    global global_vars, agent_array
    #players = Party.GetPlayers()
    for player in global_vars.party_players:
        agent_id = GLOBAL_CACHE.Party.Players.GetAgentIDByLoginNumber(player.login_number)
        agent = agent_array.get_agent(agent_id)
        
        agent_max_health = agent.living_agent.max_hp #Agent.GetMaxHealth(agent_id)
        current_health = agent.living_agent.hp #Agent.GetHealth(agent_id)

        if 0.0 < current_health <= 1 and agent_max_health > 0.0:
            #if global_vars.players_max_health_table.get(agent_id, Player.GetAgentID()) != agent_max_health:
            if global_vars.players_max_health_table.get(agent_id, global_vars.player_agent_id) != agent_max_health:
                global_vars.players_max_health_table[agent_id] = agent_max_health

def update_party_names():
    global global_vars
    #players = Party.GetPlayers()
    for player in global_vars.party_players:
        agent_id = GLOBAL_CACHE.Party.Players.GetAgentIDByLoginNumber(player.login_number)
        name = GLOBAL_CACHE.Agent.GetName(agent_id) #agent_array.get_name(agent_id)
        if name != "":
            #if agent_id == Party.GetPartyLeaderID():
            if agent_id == global_vars.plarty_leader_id:
                #if global_vars.party_leader_name.get(agent_id, Player.GetAgentID()) != name:
                if global_vars.party_leader_name.get(agent_id, global_vars.player_agent_id) != name:
                    global_vars.party_leader_name[agent_id] = name
                    #Py4GW.Console.Log(module_name, f"Set Party Leader: {name}", Py4GW.Console.MessageType.Info)
            else:
                #if global_vars.party_names.get(agent_id, Player.GetAgentID()) != name:
                if global_vars.party_names.get(agent_id, global_vars.player_agent_id) != name:
                    global_vars.party_names[agent_id] = name
                    #Py4GW.Console.Log(module_name, f"Added Player: {name} to Party", Py4GW.Console.MessageType.Info)

def get_max_health(agent_id:int):
    global global_vars
    level = GLOBAL_CACHE.Agent.GetLevel(agent_id)
    default = global_vars.default_max_health_table.get(level, 1)
    max_health = global_vars.players_max_health_table.get(agent_id, default)
    return max_health

def get_threshold(agent_id:int):
    global global_vars
    level = GLOBAL_CACHE.Agent.GetLevel(agent_id)
    if 1 <= level <= 10:
        global_vars.current_threhold = global_vars.lvl1_10_threshold

    elif 11 <= level <= 20:
        global_vars.current_threhold = global_vars.lvl11_20_threshold
    
    health_treshold = 1 / (get_max_health(agent_id) / global_vars.current_threhold)
    return health_treshold


def reformparty():
    global global_vars
    if not len(global_vars.party_players) > 1:
        for agent_id in global_vars.party_names:
            name = global_vars.party_names.get(agent_id, "")
            GLOBAL_CACHE.Party.Players.InvitePlayer(name)
        global_vars.reform_party = False

def acceptparty():
    global global_vars
    party_leader_name = ""
    if not len(global_vars.party_players) > 1:
        for agent_id in global_vars.party_leader_name:
            party_leader_name = global_vars.party_leader_name.get(agent_id, "")
            GLOBAL_CACHE.Party.Players.InvitePlayer(party_leader_name)
            global_vars.reform_party = False

# ============== LIFE BONDER FUNCTIONS ==============

def get_life_bonder_hero_agent_id():
    """Get the agent ID of the life bonder hero (first hero in party)."""
    global global_vars
    try:
        heroes = GLOBAL_CACHE.Party.GetHeroes()
        if len(heroes) > global_vars.life_bonder_hero_index:
            return GLOBAL_CACHE.Party.Heroes.GetHeroAgentIDByPartyPosition(global_vars.life_bonder_hero_index)
    except:
        pass
    return 0

def calculate_position_behind_player(distance: float):
    """Calculate a position behind the player based on their facing direction."""
    global global_vars
    try:
        player_x, player_y = GLOBAL_CACHE.Player.GetXY()
        player_angle = GLOBAL_CACHE.Agent.GetRotationAngle(global_vars.player_agent_id)

        # Calculate position behind player (opposite of facing direction)
        behind_angle = player_angle + math.pi  # Add 180 degrees

        flag_x = player_x + distance * math.cos(behind_angle)
        flag_y = player_y + distance * math.sin(behind_angle)

        return (flag_x, flag_y)
    except:
        return (0.0, 0.0)

def update_life_bonder_flag():
    """Update the flag position for the life bonder hero to keep them behind the group."""
    global global_vars

    if not global_vars.life_bonder_enabled:
        return

    if not global_vars.flag_update_timer.IsExpired():
        return

    hero_agent_id = get_life_bonder_hero_agent_id()
    if hero_agent_id == 0:
        return

    # Calculate new position behind player
    new_pos = calculate_position_behind_player(global_vars.life_bonder_distance)
    if new_pos == (0.0, 0.0):
        return

    # Only update if position has changed significantly (more than 50 units)
    dx = new_pos[0] - global_vars.last_bonder_position[0]
    dy = new_pos[1] - global_vars.last_bonder_position[1]
    distance_moved = math.sqrt(dx*dx + dy*dy)

    if distance_moved > 50.0:
        GLOBAL_CACHE.Party.Heroes.FlagHero(hero_agent_id, new_pos[0], new_pos[1])
        global_vars.last_bonder_position = new_pos
        global_vars.flag_update_timer.Reset()

def check_bond_on_player(skill_name: str) -> bool:
    """Check if a specific bond is active on the player."""
    global global_vars
    try:
        skill_id = GLOBAL_CACHE.Skill.GetID(skill_name)
        if skill_id == 0:
            return True  # If skill not found, assume it's active to avoid errors
        return Effects.HasEffect(global_vars.player_agent_id, skill_id)
    except:
        return True  # Assume active on error

def get_next_missing_bond():
    """Get the next bond that needs to be cast on the player."""
    global global_vars
    for bond in global_vars.bond_skills:
        if bond["enabled"] and not check_bond_on_player(bond["name"]):
            return bond
    return None

def cast_hero_skill_on_player(skill_slot: int, hero_number: int = 1):
    """Have the life bonder hero cast a skill on the player."""
    global global_vars
    try:
        player_agent_id = global_vars.player_agent_id
        if player_agent_id == 0:
            return False

        # HeroUseSkill(target_agent_id, skill_number, hero_number)
        # hero_number is 1-indexed (1 = first hero)
        GLOBAL_CACHE.SkillBar.HeroUseSkill(player_agent_id, skill_slot, hero_number)
        return True
    except Exception as e:
        Py4GW.Console.Log(module_name, f"Error casting hero skill: {str(e)}", Py4GW.Console.MessageType.Error)
        return False

def maintain_bonds():
    """Check and recast bonds that have expired."""
    global global_vars

    if not global_vars.life_bonder_enabled:
        return

    if not global_vars.bond_cast_timer.IsExpired():
        return

    # Get the hero agent ID
    hero_agent_id = get_life_bonder_hero_agent_id()
    if hero_agent_id == 0:
        return

    # Check if hero is alive
    if not GLOBAL_CACHE.Agent.IsLiving(hero_agent_id):
        return

    # Find the next missing bond
    missing_bond = get_next_missing_bond()
    if missing_bond is not None:
        # Cast the missing bond
        hero_number = global_vars.life_bonder_hero_index + 1  # Convert to 1-indexed
        if cast_hero_skill_on_player(missing_bond["slot"], hero_number):
            Py4GW.Console.Log(module_name, f"Casting {missing_bond['name']} on player", Py4GW.Console.MessageType.Info)
            global_vars.bond_cast_timer.Reset()
        return

def use_blessed_signet():
    """Use Blessed Signet for energy management when hero energy is low."""
    global global_vars

    if not global_vars.life_bonder_enabled:
        return

    if not global_vars.blessed_signet_timer.IsExpired():
        return

    hero_agent_id = get_life_bonder_hero_agent_id()
    if hero_agent_id == 0:
        return

    # Check if hero is alive
    if not GLOBAL_CACHE.Agent.IsLiving(hero_agent_id):
        return

    # Check hero energy (cast Blessed Signet when below 50% energy)
    try:
        hero_energy = GLOBAL_CACHE.Agent.GetEnergy(hero_agent_id)
        if hero_energy is not None and hero_energy < 0.5:
            hero_number = global_vars.life_bonder_hero_index + 1
            # Blessed Signet is self-targeted (target_agent_id = 0 or hero's own ID)
            GLOBAL_CACHE.SkillBar.HeroUseSkill(hero_agent_id, global_vars.blessed_signet_slot, hero_number)
            global_vars.blessed_signet_timer.Reset()
    except:
        pass

def load_life_bonder_template():
    """Load the life bonder skill template on the hero."""
    global global_vars

    if global_vars.life_bonder_template_loaded:
        return

    if not global_vars.life_bonder_enabled:
        return

    try:
        hero_index = global_vars.life_bonder_hero_index
        GLOBAL_CACHE.SkillBar.LoadHeroSkillTemplate(hero_index, global_vars.life_bonder_template)
        global_vars.life_bonder_template_loaded = True
        Py4GW.Console.Log(module_name, f"Loaded life bonder template on hero {hero_index + 1}", Py4GW.Console.MessageType.Info)
    except Exception as e:
        Py4GW.Console.Log(module_name, f"Error loading template: {str(e)}", Py4GW.Console.MessageType.Error)

def run_life_bonder():
    """Main function to run life bonder functionality."""
    global global_vars

    if not global_vars.life_bonder_enabled:
        return

    # Update hero flag position
    update_life_bonder_flag()

    # Maintain bonds on player
    maintain_bonds()

    # Use Blessed Signet for energy
    use_blessed_signet()

# ============== END LIFE BONDER FUNCTIONS ==============

class Config:
    global ini_handler, module_name, sync_timer, sync_interval, global_vars
    def __init__(self):
        """Read configuration values from INI file"""
        self.lvl1_10 = ini_handler.read_int(module_name, "lvl1_10", global_vars.lvl1_10_threshold)
        if global_vars.lvl1_10_threshold != self.lvl1_10:
            global_vars.lvl1_10_threshold = self.lvl1_10
        self.lvl11_20 = ini_handler.read_int(module_name, "lvl11_20", global_vars.lvl11_20_threshold)
        if global_vars.lvl11_20_threshold != self.lvl11_20:
            global_vars.lvl11_20_threshold = self.lvl11_20

        # Life Bonder configuration
        self.life_bonder_enabled = ini_handler.read_bool(module_name, "life_bonder_enabled", False)
        global_vars.life_bonder_enabled = self.life_bonder_enabled
        self.life_bonder_distance = ini_handler.read_float(module_name, "life_bonder_distance", 350.0)
        global_vars.life_bonder_distance = self.life_bonder_distance

        # Load bond enabled states
        for i, bond in enumerate(global_vars.bond_skills):
            enabled = ini_handler.read_bool(module_name, f"bond_{i}_enabled", True)
            global_vars.bond_skills[i]["enabled"] = enabled

    def save(self):
        """Save the current configuration to the INI file."""
        if sync_timer.HasElapsed(sync_interval):
            ini_handler.write_key(module_name, "lvl1_10", str(self.lvl1_10))
            ini_handler.write_key(module_name, "lvl11_20", str(self.lvl11_20))

            # Save life bonder settings
            ini_handler.write_key(module_name, "life_bonder_enabled", str(self.life_bonder_enabled))
            ini_handler.write_key(module_name, "life_bonder_distance", str(self.life_bonder_distance))

            # Save bond enabled states
            for i, bond in enumerate(global_vars.bond_skills):
                ini_handler.write_key(module_name, f"bond_{i}_enabled", str(bond["enabled"]))

            sync_timer.Start()

widget_config = Config()

agent_array = RawAgentArray()

config_module = ImGui.WindowModule(f"{module_name} Config", window_name=f"{module_name} Config##{module_name}", window_size=(100, 100), window_flags=PyImGui.WindowFlags.AlwaysAutoResize)
window_x = ini_handler.read_int(module_name + " Config", "config_x", 100)
window_y = ini_handler.read_int(module_name + " Config", "config_y", 100)

config_module.window_pos = (window_x, window_y)

def configure():
    global widget_config, config_module, ini_handler, global_vars
    try:
        if not Routines.Checks.Map.MapValid():
            global_vars.reset_vars()
            return
        
        if config_module.first_run:
            PyImGui.set_next_window_size(config_module.window_size[0], config_module.window_size[1])
            PyImGui.set_next_window_pos(config_module.window_pos[0], config_module.window_pos[1])
            config_module.first_run = False

        end_pos = config_module.window_pos
        if PyImGui.begin(config_module.window_name, config_module.window_flags):
            # new_collapsed = PyImGui.is_window_collapsed()

            agent_level = GLOBAL_CACHE.Agent.GetLevel(global_vars.player_agent_id)
            PyImGui.text_wrapped(f"         {module_name}:")
            PyImGui.text_wrapped("if any of your player party members")
            PyImGui.text_wrapped("          goes below threshold:")
            if 1 <= agent_level <= 10:
                PyImGui.text_colored(f"lvl: 1-10 = {global_vars.lvl1_10_threshold}", (0.143, 0.724, 0.017, 1.000))
            else:
                PyImGui.text_wrapped(f"lvl: 1-10 = {global_vars.lvl1_10_threshold}")
            PyImGui.same_line(100, -1.0)
            PyImGui.text_wrapped("or")
            PyImGui.same_line(120, -1.0)
            if 11 <= agent_level <= 20:
                PyImGui.text_colored(f"lvl: 11-20 = {global_vars.lvl11_20_threshold}", (0.143, 0.724, 0.017, 1.000))
            else:
                PyImGui.text_wrapped(f"lvl: 11-20 = {global_vars.lvl11_20_threshold}")

            PyImGui.text_wrapped("    it'll Map Travel to last Outpost,")
            PyImGui.text_wrapped("    you can set the threshold below.")
            PyImGui.text_wrapped("                 If in a Party,")
            PyImGui.text_wrapped("  It'll also reform your player party")
            PyImGui.text_wrapped("            once in the Outpost")
            PyImGui.text_wrapped("    Current character lvl threshold")
            PyImGui.text_wrapped("        is highlighted with")
            PyImGui.same_line(157, -1.0)
            PyImGui.text_colored("green", (0.143, 0.724, 0.017, 1.000))
            if 1 <= agent_level <= 10:
                PyImGui.text_colored("                  Level 1 - 10:", (0.143, 0.724, 0.017, 1.000))
            else:
                PyImGui.text_wrapped("                  Level 1 - 10:")
            widget_config.lvl1_10 = PyImGui.slider_int("1", widget_config.lvl1_10, 0, 330)
            PyImGui.text_wrapped("                       0 - 330")
            if global_vars.lvl1_10_threshold != widget_config.lvl1_10:
                global_vars.lvl1_10_threshold = widget_config.lvl1_10
            if 11 <= agent_level <= 20:
                PyImGui.text_colored("                  Level 11 - 20:", (0.143, 0.724, 0.017, 1.000))
            else:
                PyImGui.text_wrapped("                  Level 11 - 20:")
            widget_config.lvl11_20 = PyImGui.slider_int("20", widget_config.lvl11_20, 0, 550)
            PyImGui.text_wrapped("                       0 - 550")
            if global_vars.lvl11_20_threshold != widget_config.lvl11_20:
                global_vars.lvl11_20_threshold = widget_config.lvl11_20

            # ============== LIFE BONDER UI ==============
            PyImGui.separator()
            PyImGui.text_colored("Life Bonder Hero", (0.4, 0.8, 1.0, 1.0))

            # Enable/Disable checkbox
            widget_config.life_bonder_enabled = PyImGui.checkbox("Enable Life Bonder", widget_config.life_bonder_enabled)
            if global_vars.life_bonder_enabled != widget_config.life_bonder_enabled:
                global_vars.life_bonder_enabled = widget_config.life_bonder_enabled
                if widget_config.life_bonder_enabled:
                    global_vars.life_bonder_template_loaded = False  # Reset to reload template

            if widget_config.life_bonder_enabled:
                PyImGui.text_wrapped("Hero 1 will maintain bonds on you")
                PyImGui.text_wrapped("and stay behind to avoid aggro.")

                # Distance slider
                widget_config.life_bonder_distance = PyImGui.slider_float("Distance Behind##bonder", widget_config.life_bonder_distance, 200.0, 600.0)
                if global_vars.life_bonder_distance != widget_config.life_bonder_distance:
                    global_vars.life_bonder_distance = widget_config.life_bonder_distance

                # Load Template button
                if PyImGui.button("Load Bonder Template##loadtemplate"):
                    global_vars.life_bonder_template_loaded = False
                    load_life_bonder_template()

                # Show bond status
                PyImGui.separator()
                PyImGui.text("Bond Status:")
                for i, bond in enumerate(global_vars.bond_skills):
                    # Get friendly name (replace underscores with spaces)
                    friendly_name = bond["name"].replace("_", " ").replace("Balthazars", "Balthazar's")

                    # Check if bond is active
                    is_active = check_bond_on_player(bond["name"])

                    # Checkbox for enabling/disabling this bond
                    bond["enabled"] = PyImGui.checkbox(f"##{bond['name']}", bond["enabled"])
                    PyImGui.same_line(0, 5)

                    # Show status colored text
                    if is_active:
                        PyImGui.text_colored(f"{friendly_name}", (0.0, 1.0, 0.0, 1.0))  # Green
                    else:
                        PyImGui.text_colored(f"{friendly_name}", (1.0, 0.3, 0.3, 1.0))  # Red

                # Show hero energy if available
                hero_agent_id = get_life_bonder_hero_agent_id()
                if hero_agent_id != 0:
                    try:
                        hero_energy = GLOBAL_CACHE.Agent.GetEnergy(hero_agent_id)
                        if hero_energy is not None:
                            energy_pct = int(hero_energy * 100)
                            if energy_pct < 30:
                                PyImGui.text_colored(f"Hero Energy: {energy_pct}%", (1.0, 0.3, 0.3, 1.0))
                            elif energy_pct < 60:
                                PyImGui.text_colored(f"Hero Energy: {energy_pct}%", (1.0, 1.0, 0.0, 1.0))
                            else:
                                PyImGui.text_colored(f"Hero Energy: {energy_pct}%", (0.0, 1.0, 0.0, 1.0))
                    except:
                        pass

            # ============== END LIFE BONDER UI ==============

            widget_config.save()
            end_pos = PyImGui.get_window_pos()

        PyImGui.end()

        if end_pos[0] != config_module.window_pos[0] or end_pos[1] != config_module.window_pos[1]:
            config_module.window_pos = (int(end_pos[0]), int(end_pos[1]))
            ini_handler.write_key(module_name + " Config", "config_x", str(int(end_pos[0])))
            ini_handler.write_key(module_name + " Config", "config_y", str(int(end_pos[1])))

    except ImportError as e:
        Py4GW.Console.Log(module_name, f"ImportError encountered: {str(e)}", Py4GW.Console.MessageType.Error)
        Py4GW.Console.Log(module_name, f"Stack trace: {traceback.format_exc()}", Py4GW.Console.MessageType.Error)
    except ValueError as e:
        Py4GW.Console.Log(module_name, f"ValueError encountered: {str(e)}", Py4GW.Console.MessageType.Error)
        Py4GW.Console.Log(module_name, f"Stack trace: {traceback.format_exc()}", Py4GW.Console.MessageType.Error)
    except TypeError as e:
        Py4GW.Console.Log(module_name, f"TypeError encountered: {str(e)}", Py4GW.Console.MessageType.Error)
        Py4GW.Console.Log(module_name, f"Stack trace: {traceback.format_exc()}", Py4GW.Console.MessageType.Error)
    except Exception as e:
        Py4GW.Console.Log(module_name, f"Unexpected error encountered: {str(e)}", Py4GW.Console.MessageType.Error)
        Py4GW.Console.Log(module_name, f"Stack trace: {traceback.format_exc()}", Py4GW.Console.MessageType.Error)
    finally:
        pass
    

# main Function
def main():
    global global_vars, agent_array
    try:

        if not Routines.Checks.Map.MapValid():
            global_vars.reset_vars()
            return
        
        if not global_vars.game_timer.HasElapsed(global_vars.game_time):
            return
        global_vars.game_timer.Reset()
        
        global_vars.update_cache()
        
        if not Routines.Checks.Map.MapValid():
            global_vars.reset_vars()
            return
        
        if GLOBAL_CACHE.Map.IsOutpost():
            if not global_vars.outpost_timer.IsExpired():
                return

            global_vars.outpost_timer.Reset()
            map_id = GLOBAL_CACHE.Map.GetMapID()
            if global_vars.last_outpost != map_id:
                global_vars.last_outpost = map_id
                #Py4GW.Console.Log(module_name, f"Last Outpost: {Map.GetMapName(global_vars.last_outpost)}({Map.GetMapID()})", Py4GW.Console.MessageType.Info)

            # Load life bonder template in outpost
            if global_vars.life_bonder_enabled:
                load_life_bonder_template()

            #reform party
            if global_vars.reform_party:
                if global_vars.is_party_leader:
                    reformparty()
                else:
                    acceptparty()
            return

        elif GLOBAL_CACHE.Map.IsExplorable():
            # Run life bonder (flagging + bond maintenance)
            run_life_bonder()

            update_max_health()
            update_party_names()
            if global_vars.low_life:
                global_vars.low_life = False
            #players = Party.GetPlayers()
            for player in global_vars.party_players:
                agent_id = GLOBAL_CACHE.Party.Players.GetAgentIDByLoginNumber(player.login_number)
                agent = agent_array.get_agent(agent_id)
                #if 0.0 < Agent.GetHealth(agent_id) < 1.0:
                if 0.0 < agent.living_agent.hp < 1.0:
                    health = agent.living_agent.hp #Agent.GetHealth(agent_id)
                    max_health = get_max_health(agent_id)
                    if health <= get_threshold(agent_id):
                        if global_vars.log_low_health:
                            global_vars.log_low_health = False
                            Py4GW.Console.Log(module_name, f"Player: {GLOBAL_CACHE.Agent.GetName(agent_id)} ({agent_id}) have low health: {round(health * max_health)}", Py4GW.Console.MessageType.Info)
                        global_vars.low_life = True
                        global_vars.low_life_agent = agent_id

            if global_vars.low_life:
                if global_vars.travel_timer.HasElapsed(global_vars.travel_time):
                    if len(global_vars.party_players) > 1:
                        global_vars.reform_party = True

                    GLOBAL_CACHE.Map.Travel(global_vars.last_outpost)

                    ActionQueueManager().AddAction("ACTION", Keystroke.PressAndRelease, Key.Y.value)
                    ActionQueueManager().AddAction("ACTION", Keystroke.PressAndRelease, Key.Y.value)
#                        Keystroke.PressAndRelease(Key.Y.value)
                    Py4GW.Console.Log(module_name, f"Traveling to: {GLOBAL_CACHE.Map.GetMapName(global_vars.last_outpost)}({global_vars.last_outpost})", Py4GW.Console.MessageType.Info)
                    global_vars.low_life = False
                    global_vars.travel_timer.Start()

                global_vars.game_timer.Start()
            return

    except ImportError as e:
        Py4GW.Console.Log(module_name, f"ImportError encountered: {str(e)}", Py4GW.Console.MessageType.Error)
        Py4GW.Console.Log(module_name, f"Stack trace: {traceback.format_exc()}", Py4GW.Console.MessageType.Error)
    except ValueError as e:
        Py4GW.Console.Log(module_name, f"ValueError encountered: {str(e)}", Py4GW.Console.MessageType.Error)
        Py4GW.Console.Log(module_name, f"Stack trace: {traceback.format_exc()}", Py4GW.Console.MessageType.Error)
    except TypeError as e:
        Py4GW.Console.Log(module_name, f"TypeError encountered: {str(e)}", Py4GW.Console.MessageType.Error)
        Py4GW.Console.Log(module_name, f"Stack trace: {traceback.format_exc()}", Py4GW.Console.MessageType.Error)
    except Exception as e:
        Py4GW.Console.Log(module_name, f"Unexpected error encountered: {str(e)}", Py4GW.Console.MessageType.Error)
        Py4GW.Console.Log(module_name, f"Stack trace: {traceback.format_exc()}", Py4GW.Console.MessageType.Error)
    finally:
        pass

if __name__ == "__main__":
    main()