"""
Menu system for Dungeons & Daemons.
Redesigned for beautiful, elegant interface with natural flow.
"""

import os
import time
from typing import Optional, List, Callable, Dict, Any
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.align import Align
from rich.columns import Columns
from rich.layout import Layout
from rich.padding import Padding
from rich.console import Group

from ascii_art import TITLE_ART, CHARACTER_ART, Colors, get_random_loading_message, SIMPLE_TITLE
from settings import SettingsManager
from dice_system import DiceRoller


class MenuChoice(Enum):
    """Menu choices enumeration."""
    NEW_GAME = "new"
    LOAD_GAME = "load"
    SETTINGS = "settings"
    ABOUT = "about"
    QUIT = "quit"


class MenuSystem:
    """Handles all menu interactions with beautiful, professional interface."""
    
    def __init__(self, settings_manager: SettingsManager):
        self.console = Console()
        self.settings_manager = settings_manager
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen properly."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        self.console.clear()
    
    def show_title(self):
        """Display the clean game title."""
        # Add some spacing at the top for better visual balance
        self.console.print("\n" * 2)

        # Use Rich Group and Align to center each line
        title_lines = Group(
            Align.center(Text("DUNGEONS & DAEMONS", style=Colors.TITLE)),
            Align.center(Text("An AI-Powered Adventure Awaits", style=Colors.TITLE))
        )
        title_panel = Panel(
            title_lines,
            style=Colors.TITLE,
            border_style=Colors.ACCENT,
            padding=(2, 4),
            width=65
        )
        self.console.print(Align.center(title_panel))
        self.console.print()
    
    def animated_loading(self, duration: float = 2.0):
        """Show an elegant animated loading sequence."""
        messages = [
            "Awakening the ancient spirits...",
            "Consulting the mystical archives...",
            "The Oracle prepares your destiny...",
            "Magic flows through the realm...",
            "Your adventure begins now!"
        ]
        
        for i, message in enumerate(messages):
            loading_panel = Panel(
                Text(message, justify="center", style=Colors.INFO),
                style=Colors.ACCENT,
                border_style=Colors.ACCENT,
                padding=(0, 2)
            )
            self.console.print(Align.center(loading_panel))
            time.sleep(duration / len(messages))
            if i < len(messages) - 1:
                self.console.clear()
                # Re-show title for context
                title_text = Text(SIMPLE_TITLE, style=Colors.TITLE)
                self.console.print(Align.center(title_text))
                self.console.print()
    
    def show_main_menu(self) -> MenuChoice:
        """Display the clean main menu with all text centered."""
        while True:
            self.clear_screen()
            self.show_title()
            menu_options = [
                ("1", "[New]", "New Adventure", "Begin your legendary quest"),
                ("2", "[Load]", "Continue Journey", "Resume your saved game"),
                ("3", "[Config]", "Settings", "Configure your experience"),
                ("4", "[Info]", "About", "Learn about this realm"),
                ("5", "[Exit]", "Exit", "Leave this world")
            ]
            menu_table = Table.grid(padding=(0, 2))
            menu_table.add_column(justify="center", width=6)
            menu_table.add_column(justify="center", width=10)
            menu_table.add_column(justify="center", width=18)
            menu_table.add_column(justify="center", width=30)
            for num, prefix, title, desc in menu_options:
                menu_table.add_row(
                    Align.center(Text(f"[{num}]", style=Colors.SELECTED)),
                    Align.center(Text(prefix, style=Colors.ACCENT)),
                    Align.center(Text(title, style=Colors.MENU_OPTION)),
                    Align.center(Text(desc, style=Colors.MUTED))
                )
            menu_panel = Panel(
                menu_table,
                title="Main Menu",
                title_align="center",
                style=Colors.ACCENT,
                border_style=Colors.ACCENT,
                padding=(2, 3),
                width=75
            )
            self.console.print(Align.center(menu_panel))
            self.console.print("\n")
            prompt_text = Text()
            prompt_text.append("Choose your path", style=Colors.INFO)
            prompt_text.append(" (1-5)", style=Colors.MUTED)
            try:
                choice = Prompt.ask(
                    prompt_text,
                    choices=["1", "2", "3", "4", "5"],
                    default="1",
                    show_choices=False
                )
                
                # Clear screen after menu input
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                self.console.clear()
                
                choice_map = {
                    "1": MenuChoice.NEW_GAME,
                    "2": MenuChoice.LOAD_GAME,
                    "3": MenuChoice.SETTINGS,
                    "4": MenuChoice.ABOUT,
                    "5": MenuChoice.QUIT
                }
                return choice_map[choice]
            except KeyboardInterrupt:
                return MenuChoice.QUIT
    
    def show_character_creation(self) -> Optional[Dict[str, Any]]:
        """Handle comprehensive D&D character creation with dice rolling."""
        from character_data import (
            get_race_choices, get_class_choices, get_background_choices,
            RACES, CLASSES, BACKGROUNDS,
            apply_racial_bonuses, get_racial_proficiencies,
            get_class_proficiencies, get_background_proficiencies,
            calculate_starting_hp, calculate_armor_class
        )
        
        roller = DiceRoller(self.console)
        character_data = {}
        
        # Step 1: Character Name
        character_data["name"] = self._get_character_name()
        if not character_data["name"]:
            return None
        
        # Step 2: Choose Ability Score Method
        stat_method = self._choose_stat_method()
        if not stat_method:
            return None
        
        # Step 3: Roll/Assign Ability Scores
        base_stats = self._roll_ability_scores(roller, stat_method)
        if not base_stats:
            return None
        
        # Step 4: Choose Race
        character_data["race"] = self._choose_race()
        if not character_data["race"]:
            return None
        
        # Step 5: Apply Racial Bonuses
        final_stats = apply_racial_bonuses(base_stats, character_data["race"])
        character_data.update({
            "strength": final_stats["Strength"],
            "dexterity": final_stats["Dexterity"],
            "constitution": final_stats["Constitution"],
            "intelligence": final_stats["Intelligence"],
            "wisdom": final_stats["Wisdom"],
            "charisma": final_stats["Charisma"]
        })
        
        # Step 6: Choose Class
        character_data["character_class"] = self._choose_class()
        if not character_data["character_class"]:
            return None
        
        # Step 7: Choose Background
        character_data["background"] = self._choose_background()
        if not character_data["background"]:
            return None
        
        # Step 8: Finalize Character Details
        character_data.update(self._finalize_character(character_data, roller))
        
        # Step 9: Show Final Character Sheet
        if not self._show_final_character_sheet(character_data):
            return None
        
        return character_data
    
    def _get_character_name(self) -> Optional[str]:
        """Get character name from player."""
        while True:
            self.clear_screen()
            self.console.print("\n" * 2)
            title_text = Text("DUNGEONS & DAEMONS", style=Colors.TITLE)
            self.console.print(Align.center(title_text))
            self.console.print()
            
            char_lines = [
                "CHARACTER CREATION",
                "",
                "Step 1: Choose Your Hero's Name",
                "",
                "What name shall be whispered in taverns",
                "and carved upon monuments?"
            ]
            char_group = Group(*[Align.center(Text(line, style=Colors.ACCENT)) for line in char_lines])
            char_panel = Panel(
                char_group,
                title="Creating Your Legend",
                title_align="center",
                style=Colors.ACCENT,
                border_style=Colors.ACCENT,
                padding=(2, 4),
                width=80
            )
            self.console.print(Align.center(char_panel))
            self.console.print()
            
            name_prompt = Text()
            name_prompt.append("Enter your hero's name", style=Colors.INFO)
            name_prompt.append(" (or 'back' to return)", style=Colors.MUTED)
            
            name = Prompt.ask(name_prompt, default="").strip()
            
            if name.lower() == 'back':
                return None
            
            if name and len(name) <= 20 and name.replace(" ", "").replace("'", "").isalpha():
                return name
            
            # Show error
            self.console.print()
            error_panel = Panel(
                Align.center(Text("Name must be 1-20 characters and contain only letters", style=Colors.ERROR)),
                style=Colors.ERROR,
                border_style=Colors.ERROR,
                width=60
            )
            self.console.print(Align.center(error_panel))
            time.sleep(2)
    
    def _choose_stat_method(self) -> Optional[str]:
        """Choose method for determining ability scores."""
        while True:
            self.clear_screen()
            self.console.print("\n" * 2)
            title_text = Text("DUNGEONS & DAEMONS", style=Colors.TITLE)
            self.console.print(Align.center(title_text))
            self.console.print()
            
            method_lines = [
                "ABILITY SCORE GENERATION",
                "",
                "Step 2: Choose Your Stat Rolling Method",
                "",
                "How shall the fates determine your abilities?"
            ]
            method_group = Group(*[Align.center(Text(line, style=Colors.ACCENT)) for line in method_lines])
            method_panel = Panel(
                method_group,
                title="Rolling the Dice of Destiny",
                title_align="center",
                style=Colors.ACCENT,
                border_style=Colors.ACCENT,
                padding=(2, 4),
                width=80
            )
            self.console.print(Align.center(method_panel))
            self.console.print()
            
            # Show options
            methods_table = Table.grid(padding=(0, 2))
            methods_table.add_column(justify="center", width=6)
            methods_table.add_column(justify="left", width=25)
            methods_table.add_column(justify="left", width=35)
            
            methods = [
                ("1", "4d6 Drop Lowest", "Roll 4d6, drop lowest (Heroic)"),
                ("2", "3d6 Straight", "Roll 3d6 for each stat (Classic)"),
                ("3", "Standard Array", "Use preset array: 15,14,13,12,10,8"),
                ("4", "Point Buy", "Allocate 27 points (Balanced)")
            ]
            
            for num, name, desc in methods:
                methods_table.add_row(
                    Text(f"[{num}]", style=Colors.SELECTED),
                    Text(name, style=Colors.INFO),
                    Text(desc, style=Colors.MUTED)
                )
            
            methods_panel = Panel(
                methods_table,
                title="Available Methods",
                title_align="center",
                style=Colors.INFO,
                border_style=Colors.INFO,
                padding=(1, 2),
                width=80
            )
            self.console.print(Align.center(methods_panel))
            self.console.print()
            
            choice_prompt = Text()
            choice_prompt.append("Choose method", style=Colors.INFO)
            choice_prompt.append(" (1-4, or 'back')", style=Colors.MUTED)
            
            choice = Prompt.ask(choice_prompt, choices=["1", "2", "3", "4", "back"], default="1")
            
            if choice == "back":
                return None
            
            method_map = {
                "1": "4d6_drop_lowest",
                "2": "3d6",
                "3": "array",
                "4": "point_buy"
            }
            
            return method_map[choice]
    
    def _roll_ability_scores(self, roller: DiceRoller, method: str) -> Optional[Dict[str, int]]:
        """Roll ability scores using chosen method."""
        import time
        
        if method == "array":
            return self._assign_standard_array()
        elif method == "point_buy":
            return self._point_buy_system()
        else:
            return self._roll_stats_with_dice(roller, method)
    
    def _roll_stats_with_dice(self, roller: DiceRoller, method: str) -> Optional[Dict[str, int]]:
        """Roll stats with dice animation."""
        import time
        stats = {}
        stat_names = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        
        for stat_name in stat_names:
            self.clear_screen()
            self.console.print("\n" * 2)
            title_text = Text("ROLLING YOUR DESTINY", style=Colors.TITLE)
            self.console.print(Align.center(title_text))
            self.console.print()
            
            # Roll the dice
            if method == "4d6_drop_lowest":
                rolls = [roller.roll_dice(1, 6).rolls[0] for _ in range(4)]
                sorted_rolls = sorted(rolls, reverse=True)
                final_value = sum(sorted_rolls[:3])
                roller.display_stat_roll(stat_name, rolls, final_value)
            else:  # 3d6
                rolls = [roller.roll_dice(1, 6).rolls[0] for _ in range(3)]
                final_value = sum(rolls)
                roller.display_stat_roll(stat_name, rolls, final_value)
            
            stats[stat_name] = final_value
            
            self.console.print()
            continue_prompt = Text()
            continue_prompt.append("Press Enter to continue...", style=Colors.MUTED)
            Prompt.ask(continue_prompt, default="")
        
        return stats
    
    def _assign_standard_array(self) -> Optional[Dict[str, int]]:
        """Let player assign standard array values."""
        # This would be a more complex interface - for now, auto-assign
        return {
            "Strength": 15,
            "Dexterity": 14,
            "Constitution": 13,
            "Intelligence": 12,
            "Wisdom": 10,
            "Charisma": 8
        }
    
    def _point_buy_system(self) -> Optional[Dict[str, int]]:
        """Point buy system - simplified for now."""
        return {
            "Strength": 13,
            "Dexterity": 14,
            "Constitution": 13,
            "Intelligence": 12,
            "Wisdom": 12,
            "Charisma": 10
        }
    
    def _choose_race(self) -> Optional[str]:
        """Choose character race."""
        from character_data import RACES, get_race_choices
        
        while True:
            self.clear_screen()
            self.console.print("\n" * 2)
            title_text = Text("DUNGEONS & DAEMONS", style=Colors.TITLE)
            self.console.print(Align.center(title_text))
            self.console.print()
            
            race_lines = [
                "CHOOSE YOUR HERITAGE",
                "",
                "Step 4: Select Your Character's Race",
                "",
                "From what lineage do you descend?"
            ]
            race_group = Group(*[Align.center(Text(line, style=Colors.ACCENT)) for line in race_lines])
            race_panel = Panel(
                race_group,
                title="Bloodlines and Ancestry",
                title_align="center",
                style=Colors.ACCENT,
                border_style=Colors.ACCENT,
                padding=(2, 4),
                width=70
            )
            self.console.print(Align.center(race_panel))
            self.console.print()
            
            # Show race options
            races_table = Table.grid(padding=(0, 2))
            races_table.add_column(justify="center", width=6)
            races_table.add_column(justify="left", width=15)
            races_table.add_column(justify="left", width=45)
            
            race_choices = get_race_choices()
            for i, race_name in enumerate(race_choices, 1):
                race = RACES[race_name]
                races_table.add_row(
                    Text(f"[{i}]", style=Colors.SELECTED),
                    Text(race_name, style=Colors.INFO),
                    Text(race.description[:50] + "...", style=Colors.MUTED)
                )
            
            races_panel = Panel(
                races_table,
                title="Available Races",
                title_align="center",
                style=Colors.INFO,
                border_style=Colors.INFO,
                padding=(1, 2),
                width=80
            )
            self.console.print(Align.center(races_panel))
            self.console.print()
            
            choice_prompt = Text()
            choice_prompt.append("Choose race", style=Colors.INFO)
            choice_prompt.append(f" (1-{len(race_choices)}, or 'back')", style=Colors.MUTED)
            
            valid_choices = [str(i) for i in range(1, len(race_choices) + 1)] + ["back"]
            choice = Prompt.ask(choice_prompt, choices=valid_choices, default="1")
            
            if choice == "back":
                return None
            
            return race_choices[int(choice) - 1]
    
    def _choose_class(self) -> Optional[str]:
        """Choose character class."""
        from character_data import CLASSES, get_class_choices
        
        while True:
            self.clear_screen()
            self.console.print("\n" * 2)
            title_text = Text("DUNGEONS & DAEMONS", style=Colors.TITLE)
            self.console.print(Align.center(title_text))
            self.console.print()
            
            class_lines = [
                "CHOOSE YOUR PATH",
                "",
                "Step 6: Select Your Character's Class",
                "",
                "What calling speaks to your soul?"
            ]
            class_group = Group(*[Align.center(Text(line, style=Colors.ACCENT)) for line in class_lines])
            class_panel = Panel(
                class_group,
                title="Paths of Power",
                title_align="center",
                style=Colors.ACCENT,
                border_style=Colors.ACCENT,
                padding=(2, 4),
                width=70
            )
            self.console.print(Align.center(class_panel))
            self.console.print()
            
            # Show class options
            classes_table = Table.grid(padding=(0, 2))
            classes_table.add_column(justify="center", width=6)
            classes_table.add_column(justify="left", width=15)
            classes_table.add_column(justify="left", width=45)
            
            class_choices = get_class_choices()
            for i, class_name in enumerate(class_choices, 1):
                char_class = CLASSES[class_name]
                classes_table.add_row(
                    Text(f"[{i}]", style=Colors.SELECTED),
                    Text(class_name, style=Colors.INFO),
                    Text(char_class.description[:50] + "...", style=Colors.MUTED)
                )
            
            classes_panel = Panel(
                classes_table,
                title="Available Classes",
                title_align="center",
                style=Colors.INFO,
                border_style=Colors.INFO,
                padding=(1, 2),
                width=80
            )
            self.console.print(Align.center(classes_panel))
            self.console.print()
            
            choice_prompt = Text()
            choice_prompt.append("Choose class", style=Colors.INFO)
            choice_prompt.append(f" (1-{len(class_choices)}, or 'back')", style=Colors.MUTED)
            
            valid_choices = [str(i) for i in range(1, len(class_choices) + 1)] + ["back"]
            choice = Prompt.ask(choice_prompt, choices=valid_choices, default="1")
            
            if choice == "back":
                return None
            
            return class_choices[int(choice) - 1]
    
    def _choose_background(self) -> Optional[str]:
        """Choose character background."""
        from character_data import BACKGROUNDS, get_background_choices
        
        while True:
            self.clear_screen()
            self.console.print("\n" * 2)
            title_text = Text("DUNGEONS & DAEMONS", style=Colors.TITLE)
            self.console.print(Align.center(title_text))
            self.console.print()
            
            bg_lines = [
                "YOUR PAST SHAPES YOU",
                "",
                "Step 7: Select Your Background",
                "",
                "What did you do before adventure called?"
            ]
            bg_group = Group(*[Align.center(Text(line, style=Colors.ACCENT)) for line in bg_lines])
            bg_panel = Panel(
                bg_group,
                title="Life Before Adventure",
                title_align="center",
                style=Colors.ACCENT,
                border_style=Colors.ACCENT,
                padding=(2, 4),
                width=70
            )
            self.console.print(Align.center(bg_panel))
            self.console.print()
            
            # Show background options
            bg_table = Table.grid(padding=(0, 2))
            bg_table.add_column(justify="center", width=6)
            bg_table.add_column(justify="left", width=15)
            bg_table.add_column(justify="left", width=45)
            
            bg_choices = get_background_choices()
            for i, bg_name in enumerate(bg_choices, 1):
                background = BACKGROUNDS[bg_name]
                bg_table.add_row(
                    Text(f"[{i}]", style=Colors.SELECTED),
                    Text(bg_name, style=Colors.INFO),
                    Text(background.description[:50] + "...", style=Colors.MUTED)
                )
            
            bg_panel = Panel(
                bg_table,
                title="Available Backgrounds",
                title_align="center",
                style=Colors.INFO,
                border_style=Colors.INFO,
                padding=(1, 2),
                width=80
            )
            self.console.print(Align.center(bg_panel))
            self.console.print()
            
            choice_prompt = Text()
            choice_prompt.append("Choose background", style=Colors.INFO)
            choice_prompt.append(f" (1-{len(bg_choices)}, or 'back')", style=Colors.MUTED)
            
            valid_choices = [str(i) for i in range(1, len(bg_choices) + 1)] + ["back"]
            choice = Prompt.ask(choice_prompt, choices=valid_choices, default="1")
            
            if choice == "back":
                return None
            
            return bg_choices[int(choice) - 1]
    
    def _finalize_character(self, character_data: Dict[str, Any], roller: DiceRoller) -> Dict[str, Any]:
        """Finalize character with calculated stats and equipment."""
        from character_data import (
            CLASSES, RACES, BACKGROUNDS,
            get_class_proficiencies, get_background_proficiencies,
            calculate_starting_hp, calculate_armor_class
        )
        
        # Calculate derived stats
        con_modifier = (character_data["constitution"] - 10) // 2
        dex_modifier = (character_data["dexterity"] - 10) // 2
        
        # Hit points
        char_class = CLASSES[character_data["character_class"]]
        max_hp = char_class.hit_die + con_modifier
        
        # Armor class (base calculation)
        armor_class = 10 + dex_modifier
        
        # Get proficiencies
        class_profs = get_class_proficiencies(character_data["character_class"])
        bg_profs = get_background_proficiencies(character_data["background"])
        
        # Equipment based on class and background
        race = RACES[character_data["race"]]
        background = BACKGROUNDS[character_data["background"]]
        
        inventory = ["Backpack", "Bedroll", "Rations (5 days)"]
        inventory.extend(background.equipment[:3])  # Add some background equipment
        
        equipment = {
            "armor": "Leather Armor",
            "weapon": "Longsword" if character_data["character_class"] == "Fighter" else "Dagger",
            "shield": "Shield" if character_data["character_class"] in ["Fighter", "Cleric"] else None,
            "tools": []
        }
        
        return {
            "level": 1,
            "hp": max_hp,
            "max_hp": max_hp,
            "armor_class": armor_class + 1,  # +1 for leather armor
            "proficiency_bonus": 2,
            "skill_proficiencies": class_profs.get("skills", [])[:2] + bg_profs.get("skills", []),
            "saving_throw_proficiencies": class_profs.get("saving_throws", []),
            "inventory": inventory,
            "equipment": equipment,
            "experience_points": 0,
            "gold_pieces": 100,
            "alignment": "Neutral Good"
        }
    
    def _show_final_character_sheet(self, character_data: Dict[str, Any]) -> bool:
        """Show final character sheet for confirmation."""
        self.clear_screen()
        self.console.print("\n" * 2)
        title_text = Text("YOUR HERO AWAITS", style=Colors.TITLE)
        self.console.print(Align.center(title_text))
        self.console.print()
        
        # Character summary
        summary_lines = [
            f"Name: {character_data['name']}",
            f"Race: {character_data['race']} | Class: {character_data['character_class']}",
            f"Background: {character_data['background']} | Level: {character_data['level']}",
            "",
            f"STR: {character_data['strength']} | DEX: {character_data['dexterity']} | CON: {character_data['constitution']}",
            f"INT: {character_data['intelligence']} | WIS: {character_data['wisdom']} | CHA: {character_data['charisma']}",
            "",
            f"HP: {character_data['hp']}/{character_data['max_hp']} | AC: {character_data['armor_class']}",
            f"Gold: {character_data['gold_pieces']} GP"
        ]
        
        summary_group = Group(*[Align.center(Text(line, style=Colors.INFO)) for line in summary_lines])
        summary_panel = Panel(
            summary_group,
            title="Your Complete Character",
            title_align="center",
            style=Colors.SUCCESS,
            border_style=Colors.SUCCESS,
            padding=(2, 4),
            width=80
        )
        self.console.print(Align.center(summary_panel))
        self.console.print()
        
        confirm_prompt = Text()
        confirm_prompt.append("Begin your legendary adventure?", style=Colors.INFO)
        
        return Confirm.ask(confirm_prompt, default=True)
    
    def show_load_menu(self) -> Optional[str]:
        """Show clean load game menu with centered text."""
        self.clear_screen()
        self.console.print("\n" * 2)
        title_text = Text(SIMPLE_TITLE, style=Colors.TITLE)
        self.console.print(Align.center(title_text))
        self.console.print()
        saves_dir = self.settings_manager.settings.save_directory
        save_files = []
        if os.path.exists(saves_dir):
            for file in os.listdir(saves_dir):
                if file.endswith('.json'):
                    full_path = os.path.join(saves_dir, file)
                    try:
                        mtime = os.path.getmtime(full_path)
                        save_files.append((file, full_path, mtime))
                    except OSError:
                        continue
            save_files.sort(key=lambda x: x[2], reverse=True)
        if not save_files:
            no_saves_lines = [
                "No saved adventures found.",
                "Start a new quest to begin your legend!"
            ]
            no_saves_group = Group(*[Align.center(Text(line, style=Colors.WARNING)) for line in no_saves_lines])
            no_saves_panel = Panel(
                no_saves_group,
                title="Saved Adventures",
                title_align="center",
                style=Colors.WARNING,
                border_style=Colors.WARNING,
                padding=(3, 5),
                width=65
            )
            self.console.print(Align.center(no_saves_panel))
            self.console.print()
            Prompt.ask("\nPress Enter to return to menu...")
            return None
        save_table = Table(show_header=True, header_style=Colors.MENU_TITLE)
        save_table.add_column("Slot", justify="center", width=6)
        save_table.add_column("Adventure", justify="center", width=25)
        save_table.add_column("Last Played", justify="center", width=20)
        for i, (filename, filepath, mtime) in enumerate(save_files[:10], 1):
            display_name = filename.replace('_save.json', '').replace('_', ' ').title()
            modified_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
            save_table.add_row(
                Align.center(Text(f"[{i}]", style=Colors.SELECTED)),
                Align.center(Text(display_name, style=Colors.INFO)),
                Align.center(Text(modified_time, style=Colors.MUTED))
            )
        saves_panel = Panel(
            save_table,
            title="Saved Adventures",
            title_align="center",
            style=Colors.ACCENT,
            border_style=Colors.ACCENT,
            padding=(2, 3),
            width=75
        )
        self.console.print(Align.center(saves_panel))
        self.console.print()
        load_prompt = Text()
        load_prompt.append("Select adventure slot", style=Colors.INFO)
        load_prompt.append(" (or 'back' to return)", style=Colors.MUTED)
        try:
            choice = Prompt.ask(load_prompt, default="back")
            if choice.lower() == 'back':
                return None
            slot_num = int(choice)
            if 1 <= slot_num <= len(save_files):
                return save_files[slot_num - 1][1]
            else:
                error_panel = Panel(
                    Align.center(Text("Invalid slot number! Please try again.", style=Colors.ERROR)),
                    style=Colors.ERROR,
                    border_style=Colors.ERROR
                )
                self.console.print(error_panel)
                time.sleep(1)
                return self.show_load_menu()
        except (ValueError, KeyboardInterrupt):
            return None
    
    def show_settings_menu(self):
        """Show clean settings menu with centered text."""
        while True:
            self.clear_screen()
            self.console.print("\n" * 2)
            title_text = Text(SIMPLE_TITLE, style=Colors.TITLE)
            self.console.print(Align.center(title_text))
            self.console.print()
            settings_lines = [
                f"AI Model: {self.settings_manager.settings.ai_model}",
                f"Temperature: {self.settings_manager.settings.ai_temperature}",
                f"Save Directory: {self.settings_manager.settings.save_directory}",
                f"Max History: {self.settings_manager.settings.max_history_turns} turns",
                f"Auto Save: {'[Enabled]' if self.settings_manager.settings.auto_save else '[Disabled]'}",
                f"Debug Mode: {'[Enabled]' if self.settings_manager.settings.show_debug_info else '[Disabled]'}",
                f"Animation Speed: {self.settings_manager.settings.animation_speed}s",
                f"Ollama: {self.settings_manager.settings.ollama_host}:{self.settings_manager.settings.ollama_port}"
            ]
            settings_group = Group(*[Align.center(Text(line, style=Colors.INFO)) for line in settings_lines])
            settings_panel = Panel(
                settings_group,
                title="Current Settings",
                title_align="center",
                style=Colors.INFO,
                border_style=Colors.INFO,
                padding=(2, 4),
                width=75
            )
            self.console.print(Align.center(settings_panel))
            self.console.print()
            options_table = Table.grid(padding=(0, 2))
            options_table.add_column(justify="center", width=6)
            options_table.add_column(justify="center", width=25)
            options = [
                ("1", "Change AI Model"),
                ("2", "Adjust Temperature"),
                ("3", "Set Save Directory"),
                ("4", "Configure History Length"),
                ("5", "Toggle Auto Save"),
                ("6", "Toggle Debug Mode"),
                ("7", "Back to Main Menu")
            ]
            for num, option in options:
                options_table.add_row(
                    Align.center(Text(f"[{num}]", style=Colors.SELECTED)),
                    Align.center(Text(option, style=Colors.MENU_OPTION))
                )
            options_panel = Panel(
                options_table,
                title="Configuration Options",
                title_align="center",
                style=Colors.ACCENT,
                border_style=Colors.ACCENT,
                padding=(2, 3),
                width=60
            )
            self.console.print(Align.center(options_panel))
            self.console.print()
            try:
                choice_prompt = Text()
                choice_prompt.append("Select option", style=Colors.INFO)
                choice = Prompt.ask(
                    choice_prompt,
                    choices=["1", "2", "3", "4", "5", "6", "7"],
                    default="7",
                    show_choices=False
                )
                if choice == "1":
                    self._change_ai_model()
                elif choice == "2":
                    self._change_ai_temperature()
                elif choice == "3":
                    self._change_save_directory()
                elif choice == "4":
                    self._change_max_history_turns()
                elif choice == "5":
                    self._toggle_auto_save()
                elif choice == "6":
                    self._toggle_debug_mode()
                elif choice == "7":
                    break
            except KeyboardInterrupt:
                break
    
    def _change_ai_model(self):
        """Change AI model with beautiful interface."""
        available_models = self.settings_manager.get_available_models()
        current_model = self.settings_manager.settings.ai_model
        
        self.console.print()
        
        models_table = Table(show_header=True, header_style=Colors.MENU_TITLE)
        models_table.add_column("Slot", style=Colors.SELECTED, justify="center", width=6)
        models_table.add_column("Model", style=Colors.INFO, width=20)
        models_table.add_column("Status", style=Colors.ACCENT, width=10)
        
        for i, model in enumerate(available_models, 1):
            status = "Current" if model == current_model else "Available"
            models_table.add_row(f"[{i}]", model, status)
        
        models_panel = Panel(
            models_table,
            title=Text("Available AI Models", style=Colors.MENU_TITLE),
            style=Colors.INFO,
            border_style=Colors.INFO
        )
        self.console.print(models_panel)
        
        try:
            model_prompt = Text()
            model_prompt.append("Select model number", style=Colors.INFO)
            
            choice = Prompt.ask(
                model_prompt,
                default=str(available_models.index(current_model) + 1) if current_model in available_models else "1"
            )
            
            model_index = int(choice) - 1
            if 0 <= model_index < len(available_models):
                new_model = available_models[model_index]
                self.settings_manager.update_setting("ai_model", new_model)
                
                success_panel = Panel(
                    f"AI model changed to: {new_model}",
                    style=Colors.SUCCESS,
                    border_style=Colors.SUCCESS
                )
                self.console.print(success_panel)
            else:
                error_panel = Panel(
                    "Invalid model selection!",
                    style=Colors.ERROR,
                    border_style=Colors.ERROR
                )
                self.console.print(error_panel)
                
        except ValueError:
            error_panel = Panel(
                "Invalid input! Please enter a number.",
                style=Colors.ERROR,
                border_style=Colors.ERROR
            )
            self.console.print(error_panel)
        
        time.sleep(2)
    
    def _change_ai_temperature(self):
        """Change AI temperature with validation."""
        current_temp = self.settings_manager.settings.ai_temperature
        
        temp_info = f"""
Current temperature: {current_temp}

Temperature Guide:
• 0.0-0.3: Very focused and deterministic
• 0.4-0.7: Balanced creativity and consistency  
• 0.8-1.0: More creative and varied responses
• 1.1-2.0: Highly creative but less predictable
"""
        
        info_panel = Panel(
            temp_info.strip(),
            title=Text("AI Temperature Settings", style=Colors.MENU_TITLE),
            style=Colors.INFO,
            border_style=Colors.INFO
        )
        self.console.print(info_panel)
        
        try:
            temp_prompt = Text()
            temp_prompt.append("Enter temperature (0.0-2.0)", style=Colors.INFO)
            
            new_temp = FloatPrompt.ask(temp_prompt, default=current_temp)
            
            if 0.0 <= new_temp <= 2.0:
                self.settings_manager.update_setting("ai_temperature", new_temp)
                success_panel = Panel(
                    f"AI temperature changed to: {new_temp}",
                    style=Colors.SUCCESS,
                    border_style=Colors.SUCCESS
                )
                self.console.print(success_panel)
            else:
                error_panel = Panel(
                    "Temperature must be between 0.0 and 2.0!",
                    style=Colors.ERROR,
                    border_style=Colors.ERROR
                )
                self.console.print(error_panel)
                
        except ValueError:
            error_panel = Panel(
                "Invalid temperature value!",
                style=Colors.ERROR,
                border_style=Colors.ERROR
            )
            self.console.print(error_panel)
        
        time.sleep(2)
    
    def _change_save_directory(self):
        """Change save directory."""
        current_dir = self.settings_manager.settings.save_directory
        
        try:
            dir_prompt = Text()
            dir_prompt.append("Enter save directory path", style=Colors.INFO)
            
            new_dir = Prompt.ask(dir_prompt, default=current_dir)
            
            # Clear screen after input
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.clear()
            
            if os.path.exists(new_dir) or new_dir == current_dir:
                self.settings_manager.update_setting("save_directory", new_dir)
                success_panel = Panel(
                    f"Save directory changed to: {new_dir}",
                    style=Colors.SUCCESS,
                    border_style=Colors.SUCCESS
                )
                self.console.print(success_panel)
            else:
                error_panel = Panel(
                    f"Directory '{new_dir}' does not exist or is not writable.",
                    style=Colors.ERROR,
                    border_style=Colors.ERROR
                )
                self.console.print(error_panel)
        except OSError as e:
            error_panel = Panel(
                f"Could not create directory: {e}",
                style=Colors.ERROR,
                border_style=Colors.ERROR
            )
            self.console.print(error_panel)
        
        time.sleep(2)
    
    def _change_max_history_turns(self):
        """Change the maximum number of turns for history."""
        current_turns = self.settings_manager.settings.max_history_turns
        
        turns_info = f"""
Current history length: {current_turns} turns

History Length Guide:
• 10 turns: Short, focused sessions
• 50 turns: Balanced, good for exploration
• 100 turns: Long, detailed sessions
• 200 turns: Very detailed, but slower
"""
        
        info_panel = Panel(
            turns_info.strip(),
            title=Text("History Length Settings", style=Colors.MENU_TITLE),
            style=Colors.INFO,
            border_style=Colors.INFO
        )
        self.console.print(info_panel)
        
        try:
            turns_prompt = Text()
            turns_prompt.append("Enter history length (10-200)", style=Colors.INFO)
            
            new_turns = IntPrompt.ask(turns_prompt, default=current_turns)
            
            if 10 <= new_turns <= 200:
                self.settings_manager.update_setting("max_history_turns", new_turns)
                success_panel = Panel(
                    f"History length changed to: {new_turns} turns",
                    style=Colors.SUCCESS,
                    border_style=Colors.SUCCESS
                )
                self.console.print(success_panel)
            else:
                error_panel = Panel(
                    "History length must be between 10 and 200!",
                    style=Colors.ERROR,
                    border_style=Colors.ERROR
                )
                self.console.print(error_panel)
                
        except ValueError:
            error_panel = Panel(
                "Invalid history length value!",
                style=Colors.ERROR,
                border_style=Colors.ERROR
            )
            self.console.print(error_panel)
        
        time.sleep(2)
    
    def _toggle_auto_save(self):
        """Toggle auto-save setting."""
        current_setting = self.settings_manager.settings.auto_save
        new_setting = not current_setting
        
        self.settings_manager.update_setting("auto_save", new_setting)
        status = "enabled" if new_setting else "disabled"
        
        status_panel = Panel(
            f"Auto-save {status}",
            style=Colors.SUCCESS,
            border_style=Colors.SUCCESS
        )
        self.console.print(status_panel)
        time.sleep(1)
    
    def _toggle_debug_mode(self):
        """Toggle debug mode."""
        current_setting = self.settings_manager.settings.show_debug_info
        new_setting = not current_setting
        
        self.settings_manager.update_setting("show_debug_info", new_setting)
        status = "enabled" if new_setting else "disabled"
        
        status_panel = Panel(
            f"Debug mode {status}",
            style=Colors.SUCCESS,
            border_style=Colors.SUCCESS
        )
        self.console.print(status_panel)
        time.sleep(1)
    
    def _reset_settings(self):
        """Reset settings to defaults."""
        reset_prompt = Text()
        reset_prompt.append("Reset all settings to defaults?", style=Colors.WARNING)
        
        if Confirm.ask(reset_prompt, default=False):
            self.settings_manager.reset_to_defaults()
            success_panel = Panel(
                "Settings reset to defaults",
                style=Colors.SUCCESS,
                border_style=Colors.SUCCESS
            )
            self.console.print(success_panel)
            time.sleep(2)
    
    def show_about(self):
        """Show clean about screen with centered text."""
        self.clear_screen()
        self.console.print("\n" * 2)
        title_text = Text(SIMPLE_TITLE, style=Colors.TITLE)
        self.console.print(Align.center(title_text))
        self.console.print()
        about_lines = [
            "Welcome to the realm of infinite possibilities!",
            "",
            "FEATURES:",
            "• AI-Powered storytelling with local LLM integration",
            "• Dynamic world generation and character progression",
            "• Rich terminal interface with clean visuals",
            "• Multiple save slots and automatic progress saving",
            "• Configurable AI behavior and game settings",
            "",
            "HOW TO PLAY:",
            "• Create your hero and embark on epic quests",
            "• Type any action you wish to perform",
            "• The AI Dungeon Master responds to your choices",
            "• Your adventure is automatically saved as you play",
            "",
            "TECHNOLOGY:",
            "• Python 3.8+ with Rich library for terminal UI",
            "• Ollama for local AI model integration",
            "• LangChain for intelligent conversation management",
            "• JSON-based save system for reliable progress storage",
            "",
            "REQUIREMENTS:",
            "• Ollama installed and running on your system",
            "• Compatible LLM model (llama3, mistral, etc.)",
            "• Python dependencies from requirements.txt",
            "",
            "Your destiny awaits, brave adventurer!"
        ]
        about_group = Group(*[Align.center(Text(line, style=Colors.INFO if i == 0 else Colors.MUTED)) for i, line in enumerate(about_lines)])
        about_panel = Panel(
            about_group,
            title="About Dungeons & Daemons",
            title_align="center",
            style=Colors.INFO,
            border_style=Colors.INFO,
            padding=(2, 4),
            width=85
        )
        self.console.print(Align.center(about_panel))
        self.console.print()
        return_prompt = Text()
        return_prompt.append("Press Enter to return to menu...", style=Colors.MUTED)
        Prompt.ask(return_prompt, default="")

    def confirm_quit(self) -> bool:
        """Elegant quit confirmation."""
        quit_prompt = Text()
        quit_prompt.append("Are you sure you want to leave this magical realm?", style=Colors.WARNING)
        
        return Confirm.ask(quit_prompt, default=False)
    
    def show_farewell(self):
        """Show clean farewell message with centered text."""
        self.clear_screen()
        self.console.print("\n" * 3)
        farewell_lines = [
            "Until we meet again, brave adventurer!",
            "",
            "May your journeys beyond this realm be filled with",
            "wonder, courage, and endless possibilities.",
            "",
            "The gates of Dungeons & Daemons remain open,",
            "ready for your return whenever adventure calls.",
            "",
            "Farewell, and may legends be told of your deeds!"
        ]
        farewell_group = Group(*[Align.center(Text(line, style=Colors.ACCENT)) for line in farewell_lines])
        farewell_panel = Panel(
            farewell_group,
            title="Farewell, Hero!",
            title_align="center",
            style=Colors.ACCENT,
            border_style=Colors.ACCENT,
            padding=(3, 5),
            width=70
        )
        self.console.print(Align.center(farewell_panel))
        self.console.print("\n" * 2)
        time.sleep(2) 