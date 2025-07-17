"""
Menu system for Dungeons & Daemons.
Redesigned for beautiful, elegant interface with natural flow.
"""

import os
import time
from typing import Optional, List, Callable
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
    
    def show_character_creation(self) -> Optional[str]:
        """Handle character creation with clean interface and centered panel content."""
        self.clear_screen()
        self.console.print("\n" * 2)
        title_text = Text(SIMPLE_TITLE, style=Colors.TITLE)
        self.console.print(Align.center(title_text))
        self.console.print()
        # Split the art and text into lines and center each line
        char_lines = [
            "Create Your Hero",
            "",
            "[ Sword ] [ Shield ]",
            "Choose your destiny"
        ]
        char_group = Group(*[Align.center(Text(line, style=Colors.ACCENT)) for line in char_lines])
        char_panel = Panel(
            char_group,
            title="Character Creation",
            title_align="center",
            style=Colors.ACCENT,
            border_style=Colors.ACCENT,
            padding=(2, 4),
            width=55
        )
        self.console.print(Align.center(char_panel))
        self.console.print("\n")
        # Clean prompt for name
        while True:
            name_prompt = Text()
            name_prompt.append("What is your hero's name?", style=Colors.INFO)
            
            name = Prompt.ask(
                name_prompt,
                default="Adventurer"
            ).strip()
            
            # Clear screen after input
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.clear()
            
            if name and len(name) <= 20 and name.replace(" ", "").isalpha():
                break
            
            # Redisplay the character creation screen
            self.console.print("\n" * 2)
            title_text = Text(SIMPLE_TITLE, style=Colors.TITLE)
            self.console.print(Align.center(title_text))
            self.console.print()
            char_lines = [
                "Create Your Hero",
                "",
                "[ Sword ] [ Shield ]",
                "Choose your destiny"
            ]
            char_group = Group(*[Align.center(Text(line, style=Colors.ACCENT)) for line in char_lines])
            char_panel = Panel(
                char_group,
                title="Character Creation",
                title_align="center",
                style=Colors.ACCENT,
                border_style=Colors.ACCENT,
                padding=(2, 4),
                width=55
            )
            self.console.print(Align.center(char_panel))
            self.console.print("\n")
            
            error_panel = Panel(
                Align.center(Text("Please enter a valid name (letters only, 1-20 characters)", style=Colors.ERROR)),
                style=Colors.ERROR,
                border_style=Colors.ERROR,
                width=60
            )
            self.console.print(Align.center(error_panel))
        # Clean confirmation
        self.console.print()
        welcome_text = Text()
        welcome_text.append("Welcome, ", style=Colors.SUCCESS)
        welcome_text.append(name, style=Colors.SELECTED)
        welcome_text.append("! Your legend awaits...", style=Colors.SUCCESS)
        welcome_panel = Panel(
            Align.center(welcome_text),
            style=Colors.SUCCESS,
            border_style=Colors.SUCCESS,
            padding=(1, 2),
            width=60
        )
        self.console.print(Align.center(welcome_panel))
        self.console.print()
        confirm_prompt = Text()
        confirm_prompt.append("Begin this adventure?", style=Colors.INFO)
        
        result = Confirm.ask(confirm_prompt, default=True)
        
        # Clear screen after confirmation
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        self.console.clear()
        
        if result:
            return name
        return None
    
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

🌡️ Temperature Guide:
• 0.0-0.3: Very focused and deterministic
• 0.4-0.7: Balanced creativity and consistency  
• 0.8-1.0: More creative and varied responses
• 1.1-2.0: Highly creative but less predictable
"""
        
        info_panel = Panel(
            temp_info.strip(),
            title=Text("🌡️ AI Temperature Settings", style=Colors.MENU_TITLE),
            style=Colors.INFO,
            border_style=Colors.INFO
        )
        self.console.print(info_panel)
        
        try:
            temp_prompt = Text()
            temp_prompt.append("🌡️ ", style=Colors.ACCENT)
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

🔄 History Length Guide:
• 10 turns: Short, focused sessions
• 50 turns: Balanced, good for exploration
• 100 turns: Long, detailed sessions
• 200 turns: Very detailed, but slower
"""
        
        info_panel = Panel(
            turns_info.strip(),
            title=Text("🔄 History Length Settings", style=Colors.MENU_TITLE),
            style=Colors.INFO,
            border_style=Colors.INFO
        )
        self.console.print(info_panel)
        
        try:
            turns_prompt = Text()
            turns_prompt.append("🔄 ", style=Colors.ACCENT)
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
        reset_prompt.append("🔄 ", style=Colors.WARNING)
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