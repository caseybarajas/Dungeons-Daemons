"""
Dungeons & Daemons - A terminal-based RPG with AI Dungeon Master
Main game loop and entry point with beautiful, professional interface.
"""

import os
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
from rich.columns import Columns
from rich.layout import Layout
from rich.console import Group

from game_state import GameState, Character
from ai_manager import AIManager
from settings import SettingsManager
from menu_system import MenuSystem, MenuChoice
from ascii_art import Colors, GAME_OVER_ART, get_health_indicator, get_location_prefix, get_item_type, SIMPLE_TITLE
from error_handler import ErrorHandler, ErrorType, safe_execute


class DungeonsAndDaemons:
    """Main game class for Dungeons & Daemons with beautiful interface."""
    
    def __init__(self):
        self.console = Console()
        self.settings_manager = SettingsManager()
        self.menu_system = MenuSystem(self.settings_manager)
        self.error_handler = ErrorHandler(self.console, self.settings_manager.settings.show_debug_info)
        self.ai_manager: Optional[AIManager] = None
        self.game_state: Optional[GameState] = None
    
    def initialize_ai_manager(self) -> bool:
        """Initialize the AI manager with automatic setup."""
        try:
            self.ai_manager = AIManager(
                model_name=self.settings_manager.settings.ai_model,
                temperature=self.settings_manager.settings.ai_temperature,
                ollama_host=self.settings_manager.settings.ollama_host,
                ollama_port=self.settings_manager.settings.ollama_port
            )
            return True
            
        except Exception as e:
            self.error_handler.handle_error(e, ErrorType.AI_CONNECTION, 
                                          "Initializing AI Manager")
            return False

    def load_existing_game(self) -> bool:
        """Load an existing game with improved feedback."""
        save_file = self.menu_system.show_load_menu()
        if not save_file:
            return False
        
        # Initialize AI if not already done
        if not self.ai_manager and not self.initialize_ai_manager():
            return False
        
        # Load the game state
        success, game_state = safe_execute(
            lambda: GameState.load_from_file(save_file),
            self.error_handler,
            ErrorType.SAVE_LOAD,
            f"Loading game from {save_file}"
        )
        
        if success and game_state:
            self.game_state = game_state
            
            # Update history length setting
            self.game_state.max_history_turns = self.settings_manager.settings.max_history_turns
            
            success_text = Text()
            success_text.append("Game loaded successfully! Continuing adventure...", style=Colors.SUCCESS)
            
            success_panel = Panel(
                Align.center(success_text),
                style=Colors.SUCCESS,
                border_style=Colors.SUCCESS,
                padding=(1, 2)
            )
            self.console.print(success_panel)
            
            # Clear screen before starting game
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.clear()
            
            return True
        
        return False

    def create_new_game(self) -> bool:
        """Create a new game with automatic AI setup."""
        # Show character creation
        character_name = self.menu_system.show_character_creation()
        if not character_name:
            return False
        
        # Initialize AI (this now handles all setup automatically)
        if not self.ai_manager and not self.initialize_ai_manager():
            return False
        
        # Create new character and game state
        player = Character(
            name=character_name, 
            hp=100, 
            max_hp=100, 
            inventory=["Old Sword", "Health Potion"]
        )
        
        self.game_state = GameState(
            player=player, 
            current_location="Village Square",
            max_history_turns=self.settings_manager.settings.max_history_turns
        )
        
        # Generate initial scenario with loading animation
        creating_text = Text()
        creating_text.append(f"Creating your adventure, {character_name}...", style=Colors.INFO)
        
        creating_panel = Panel(
            Align.center(creating_text),
            style=Colors.INFO,
            border_style=Colors.ACCENT,
            padding=(1, 2)
        )
        self.console.print(creating_panel)
        
        try:
            self.menu_system.animated_loading(2.0)
            
            # Clear screen after loading animation
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.clear()
            
            initial_prompt = (
                f"Start a new fantasy RPG adventure for {character_name}. "
                f"They begin in a village square with an old sword and health potion. "
                f"Create an engaging opening scenario that sets up the adventure."
            )
            
            response = self.ai_manager.get_ai_response(self.game_state, initial_prompt)
            self.update_game_state(response, f"Begin adventure as {character_name}")
            
            # Auto-save the initial state
            if self.settings_manager.settings.auto_save:
                safe_execute(
                    lambda: self.game_state.save_to_file(
                        self.settings_manager.get_save_path(f"{character_name}_save.json")
                    ),
                    self.error_handler,
                    ErrorType.SAVE_LOAD,
                    f"Auto-saving game for {character_name}"
                )
            
            return True
            
        except Exception as e:
            self.error_handler.handle_error(e, ErrorType.AI_RESPONSE, 
                                          f"Creating initial scenario for {character_name}")
            return False
    
    def display_game_state(self, narrative: str = None) -> None:
        """Display the current game state with clean UI and side-by-side character info/inventory panels."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        self.console.clear()
        self.console.print("\n")
        title_text = Text(SIMPLE_TITLE, style=Colors.TITLE)
        self.console.print(Align.center(title_text))
        self.console.print()
        if narrative:
            narrative_lines = narrative.split("\n")
            narrative_group = Group(*[Align.center(Text(line, style=Colors.NARRATIVE)) for line in narrative_lines])
            narrative_panel = Panel(
                narrative_group,
                title="Current Scene",
                title_align="center",
                style=Colors.INFO,
                border_style=Colors.ACCENT,
                padding=(2, 3),
                width=100
            )
            self.console.print(Align.center(narrative_panel))
            self.console.print()
        # Character Info (left)
        hp_ratio = self.game_state.player.hp / self.game_state.player.max_hp
        if hp_ratio > 0.7:
            hp_color = Colors.HEALTH_GOOD
        elif hp_ratio > 0.3:
            hp_color = Colors.HEALTH_OK
        else:
            hp_color = Colors.HEALTH_LOW
        health_indicator = get_health_indicator(self.game_state.player.hp, self.game_state.player.max_hp)
        location_prefix = get_location_prefix(self.game_state.current_location)
        char_info_lines = [
            Text("Hero:", style=Colors.STAT_LABEL) + Text(f" {self.game_state.player.name}", style=Colors.SELECTED),
            Text("Health:", style=Colors.STAT_LABEL) + Text(f" {health_indicator} {self.game_state.player.hp}/{self.game_state.player.max_hp}", style=hp_color),
            Text("Location:", style=Colors.STAT_LABEL) + Text(f" {location_prefix} {self.game_state.current_location}", style=Colors.STAT_VALUE)
        ]
        char_info_group = Group(*[Align.left(line) for line in char_info_lines])
        char_info_panel = Panel(
            char_info_group,
            title="Character Info",
            title_align="center",
            style=Colors.ACCENT,
            border_style=Colors.ACCENT,
            padding=(1, 2),
            width=38
        )
        # Inventory (right)
        if self.game_state.player.inventory:
            inventory_lines = [
                Text(f"{get_item_type(item)} {item}", style=Colors.STAT_VALUE) for item in self.game_state.player.inventory
            ]
        else:
            inventory_lines = [Text("[Empty]", style=Colors.MUTED)]
        inventory_group = Group(*[Align.left(line) for line in inventory_lines])
        inventory_panel = Panel(
            inventory_group,
            title="Inventory",
            title_align="center",
            style=Colors.ACCENT,
            border_style=Colors.ACCENT,
            padding=(1, 2),
            width=38
        )
        # Show side-by-side
        self.console.print(Align.center(Columns([char_info_panel, inventory_panel], align="center", expand=False)))
        self.console.print()
        # Debug info if enabled
        if self.settings_manager.settings.show_debug_info:
            debug_lines = [
                f"History: {len(self.game_state.story_history)} entries",
                f"AI Model: {self.settings_manager.settings.ai_model}"
            ]
            debug_group = Group(*[Align.center(Text(line, style=Colors.MUTED)) for line in debug_lines])
            debug_panel = Panel(
                debug_group,
                title="Debug Info",
                title_align="center",
                style=Colors.MUTED,
                border_style=Colors.MUTED,
                padding=(1, 2),
                width=80
            )
            self.console.print(Align.center(debug_panel))
            self.console.print()
    
    def check_game_over(self) -> bool:
        """Check if the game is over with beautiful game over screen and centered text."""
        if self.game_state.player.hp <= 0:
            self.console.clear()
            game_over_lines = [
                "G A M E   O V E R",
                "",
                f"{self.game_state.player.name} has fallen in the depths of adventure...",
                "",
                "Your legend will be remembered in the annals of history.",
                "",
                "Press Enter to return to menu"
            ]
            game_over_group = Group(*[Align.center(Text(line, style=Colors.ERROR if i < 3 else Colors.MUTED)) for i, line in enumerate(game_over_lines)])
            game_over_panel = Panel(
                game_over_group,
                style=Colors.ERROR,
                border_style=Colors.ERROR,
                padding=(2, 3),
                width=80
            )
            self.console.print(Align.center(game_over_panel))
            self.console.print()
            if Prompt.ask("", choices=[""], default="") == "":
                return True
        return False
    
    def get_user_input(self) -> Optional[str]:
        """Get user input with clean prompt and screen clearing."""
        try:
            action_prompt = Text()
            action_prompt.append("What do you do?", style=Colors.INFO)
            action_prompt.append(" (type 'menu' to return)", style=Colors.MUTED)
            
            user_input = Prompt.ask(action_prompt).strip()
            
            # Clear screen after input for clean look
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.clear()
            
            # Handle quit commands
            if user_input.lower() in ['quit', 'exit', 'q', 'menu']:
                return None
            
            if not user_input:
                return self.get_user_input()  # Try again if empty input
                
            return user_input
            
        except KeyboardInterrupt:
            return None
    
    def update_game_state(self, ai_response: dict, user_action: str) -> None:
        """Update game state based on AI response."""
        # Update HP
        if ai_response.get("hp_change", 0) != 0:
            self.game_state.player.hp += ai_response["hp_change"]
            self.game_state.player.hp = max(0, min(self.game_state.player.hp, self.game_state.player.max_hp))
        
        # Update location
        if ai_response.get("location"):
            self.game_state.current_location = ai_response["location"]
        
        # Update inventory
        items_added = ai_response.get("items_added", [])
        items_removed = ai_response.get("items_removed", [])
        
        for item in items_added:
            if item and item not in self.game_state.player.inventory:
                self.game_state.player.inventory.append(item)
        
        for item in items_removed:
            if item in self.game_state.player.inventory:
                self.game_state.player.inventory.remove(item)
        
        # Add to story history
        narrative = ai_response.get("narrative", "Nothing happens...")
        self.game_state.add_to_history(user_action, narrative)
        
        # Prune history based on settings
        self.game_state.prune_history(self.settings_manager.settings.max_history_turns)
    
    def run_game_loop(self) -> None:
        """Main game loop with beautiful interface."""
        if not self.game_state:
            return
        
        # Get initial narrative
        latest_narrative = "Your adventure continues..."
        if self.game_state.story_history:
            for entry in reversed(self.game_state.story_history):
                if entry.startswith("DM: "):
                    latest_narrative = entry[4:]  # Remove "DM: " prefix
                    break
        
        while True:
            # Display current state
            self.display_game_state(latest_narrative)
            
            # Check for game over
            if self.check_game_over():
                break
            
            # Get user input
            user_input = self.get_user_input()
            if user_input is None:  # Quit/menu command
                break
            
            # Show clean thinking message
            thinking_text = Text()
            thinking_text.append("The Oracle consults the cosmic tapestry...", style=Colors.INFO)
            
            thinking_panel = Panel(
                Align.center(thinking_text),
                style=Colors.INFO,
                border_style=Colors.ACCENT,
                padding=(1, 2)
            )
            self.console.print(thinking_panel)
            
            try:
                # Get AI response
                ai_response = self.ai_manager.get_ai_response(self.game_state, user_input)
                
                # Update game state
                self.update_game_state(ai_response, user_input)
                
                # Auto-save if enabled
                if self.settings_manager.settings.auto_save:
                    save_path = self.settings_manager.get_save_path(f"{self.game_state.player.name}_save.json")
                    self.game_state.save_to_json(save_path)
                
                # Update narrative for next iteration
                latest_narrative = ai_response.get("narrative", "The Oracle remains mysteriously silent...")
                
            except Exception as e:
                error_message = f"Error processing action: {e}"
                if self.settings_manager.settings.show_debug_info:
                    error_panel = Panel(
                        error_message,
                        style=Colors.ERROR,
                        border_style=Colors.ERROR
                    )
                    self.console.print(error_panel)
                else:
                    mystical_error = Panel(
                        "The mystical energies flicker momentarily...",
                        style=Colors.WARNING,
                        border_style=Colors.WARNING
                    )
                    self.console.print(mystical_error)
                
                latest_narrative = "The cosmic forces seem momentarily disrupted..."
    
    def run(self) -> None:
        """Main entry point with beautiful interface."""
        try:
            # Main menu loop
            while True:
                choice = self.menu_system.show_main_menu()
                
                if choice == MenuChoice.NEW_GAME:
                    if self.create_new_game():
                        self.run_game_loop()
                
                elif choice == MenuChoice.LOAD_GAME:
                    if self.load_existing_game():
                        self.run_game_loop()
                
                elif choice == MenuChoice.SETTINGS:
                    self.menu_system.show_settings_menu()
                
                elif choice == MenuChoice.ABOUT:
                    self.menu_system.show_about()
                
                elif choice == MenuChoice.QUIT:
                    if self.menu_system.confirm_quit():
                        self.menu_system.show_farewell()
                        break
                
        except KeyboardInterrupt:
            interrupt_panel = Panel(
                "Game interrupted. Progress saved.",
                style=Colors.WARNING,
                border_style=Colors.WARNING
            )
            self.console.print(interrupt_panel)
        except Exception as e:
            if self.settings_manager.settings.show_debug_info:
                error_panel = Panel(
                    f"Unexpected error: {e}",
                    style=Colors.ERROR,
                    border_style=Colors.ERROR
                )
                self.console.print(error_panel)
            else:
                mystical_error = Panel(
                    "An unexpected disturbance in the magical realm occurred.",
                    style=Colors.ERROR,
                    border_style=Colors.ERROR
                )
                self.console.print(mystical_error)
        finally:
            # Final save if we have an active game
            if self.game_state and self.settings_manager.settings.auto_save:
                try:
                    save_path = self.settings_manager.get_save_path(f"{self.game_state.player.name}_save.json")
                    self.game_state.save_to_json(save_path)
                except Exception:
                    pass


def main():
    """Main function to start the game."""
    game = DungeonsAndDaemons()
    game.run()


if __name__ == "__main__":
    main() 