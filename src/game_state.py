"""
Game state management for Dungeons & Daemons.
Handles character data, game state, and JSON persistence.
"""

import json
from typing import List, Optional, Dict, Any


class Character:
    """Represents the player character with all stats and inventory."""
    
    def __init__(self, name: str, hp: int = 100, max_hp: int = 100, inventory: Optional[List[str]] = None):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.inventory = inventory or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "inventory": self.inventory
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """Create character from dictionary."""
        return cls(
            name=data["name"],
            hp=data["hp"],
            max_hp=data["max_hp"],
            inventory=data.get("inventory", [])
        )


class GameState:
    """Manages the complete game state including player, story, and world state."""
    
    def __init__(self, player: Character, story_history: Optional[List[str]] = None, 
                 current_location: str = "Unknown", max_history_turns: int = 10):
        self.player = player
        self.story_history = story_history or []
        self.current_location = current_location
        self.max_history_turns = max_history_turns
    
    def save_to_json(self, file_path: str) -> None:
        """Save the entire game state to a JSON file."""
        game_data = {
            "player": self.player.to_dict(),
            "story_history": self.story_history,
            "current_location": self.current_location,
            "max_history_turns": self.max_history_turns
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(game_data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_json(cls, file_path: str) -> Optional['GameState']:
        """Load game state from JSON file. Returns None if file doesn't exist."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                game_data = json.load(f)
            
            player = Character.from_dict(game_data["player"])
            story_history = game_data.get("story_history", [])
            current_location = game_data.get("current_location", "Unknown")
            max_history_turns = game_data.get("max_history_turns", 10)
            
            return cls(player, story_history, current_location, max_history_turns)
            
        except FileNotFoundError:
            return None
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading save file: {e}")
            return None
    
    def add_to_history(self, user_action: str, ai_narrative: str) -> None:
        """Add a turn to the story history."""
        self.story_history.append(f"Player: {user_action}")
        self.story_history.append(f"DM: {ai_narrative}")
    
    def prune_history(self, max_turns: Optional[int] = None) -> None:
        """Keep only the most recent turns to prevent context from growing too large."""
        if max_turns is None:
            max_turns = self.max_history_turns
        
        if len(self.story_history) > max_turns * 2:  # Each turn is 2 entries (player + DM)
            self.story_history = self.story_history[-(max_turns * 2):]
    
    def get_history_text(self) -> str:
        """Get formatted history text for the AI prompt."""
        if not self.story_history:
            return "This is the beginning of your adventure."
        
        return "\n".join(self.story_history) 