"""
Game state management for Dungeons & Daemons.
Handles character data, game state, and JSON persistence.
"""

import json
from typing import List, Optional, Dict, Any


class Character:
    """Represents the player character with full D&D-style stats and abilities."""
    
    def __init__(self, name: str, hp: int = 100, max_hp: int = 100, inventory: Optional[List[str]] = None,
                 # D&D Stats
                 strength: int = 10, dexterity: int = 10, constitution: int = 10,
                 intelligence: int = 10, wisdom: int = 10, charisma: int = 10,
                 # Character Details
                 race: str = "Human", character_class: str = "Fighter", level: int = 1,
                 background: str = "Folk Hero", alignment: str = "Neutral Good",
                 # Derived Stats
                 armor_class: int = 10, proficiency_bonus: int = 2,
                 # Skills and Proficiencies
                 skill_proficiencies: Optional[List[str]] = None,
                 saving_throw_proficiencies: Optional[List[str]] = None,
                 # Equipment
                 equipment: Optional[Dict[str, Any]] = None,
                 # Experience and Money
                 experience_points: int = 0, gold_pieces: int = 0):
        
        # Basic Info
        self.name = name
        self.race = race
        self.character_class = character_class
        self.level = level
        self.background = background
        self.alignment = alignment
        
        # Stats
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        
        # Health (recalculate based on constitution if using defaults)
        if hp == 100 and max_hp == 100:  # Default values, calculate from CON
            con_modifier = self.get_ability_modifier(constitution)
            base_hp = 8 + con_modifier  # Fighter starting HP
            self.max_hp = max(1, base_hp)
            self.hp = self.max_hp
        else:
            self.hp = hp
            self.max_hp = max_hp
        
        # Combat Stats
        self.armor_class = armor_class
        self.proficiency_bonus = proficiency_bonus
        
        # Skills and Proficiencies
        self.skill_proficiencies = skill_proficiencies or []
        self.saving_throw_proficiencies = saving_throw_proficiencies or ["Strength", "Constitution"]
        
        # Inventory and Equipment
        self.inventory = inventory or ["Backpack", "Bedroll", "Rations (5 days)"]
        self.equipment = equipment or {
            "armor": "Leather Armor",
            "weapon": "Longsword",
            "shield": "Shield",
            "tools": []
        }
        
        # Progression
        self.experience_points = experience_points
        self.gold_pieces = gold_pieces
    
    def get_ability_modifier(self, ability_score: int) -> int:
        """Calculate D&D ability modifier from score."""
        return (ability_score - 10) // 2
    
    def get_modifier_string(self, ability_score: int) -> str:
        """Get formatted modifier string with +/- sign."""
        modifier = self.get_ability_modifier(ability_score)
        return f"+{modifier}" if modifier >= 0 else str(modifier)
    
    def get_stat_modifiers(self) -> Dict[str, int]:
        """Get all ability modifiers."""
        return {
            "Strength": self.get_ability_modifier(self.strength),
            "Dexterity": self.get_ability_modifier(self.dexterity),
            "Constitution": self.get_ability_modifier(self.constitution),
            "Intelligence": self.get_ability_modifier(self.intelligence),
            "Wisdom": self.get_ability_modifier(self.wisdom),
            "Charisma": self.get_ability_modifier(self.charisma)
        }
    
    def get_saving_throw_modifier(self, ability: str) -> int:
        """Get saving throw modifier for an ability."""
        base_modifier = self.get_stat_modifiers()[ability]
        if ability in self.saving_throw_proficiencies:
            return base_modifier + self.proficiency_bonus
        return base_modifier
    
    def get_skill_modifier(self, skill: str) -> int:
        """Get skill modifier. Skills map to abilities."""
        skill_to_ability = {
            "Acrobatics": "Dexterity", "Animal Handling": "Wisdom", "Arcana": "Intelligence",
            "Athletics": "Strength", "Deception": "Charisma", "History": "Intelligence",
            "Insight": "Wisdom", "Intimidation": "Charisma", "Investigation": "Intelligence",
            "Medicine": "Wisdom", "Nature": "Intelligence", "Perception": "Wisdom",
            "Performance": "Charisma", "Persuasion": "Charisma", "Religion": "Intelligence",
            "Sleight of Hand": "Dexterity", "Stealth": "Dexterity", "Survival": "Wisdom"
        }
        
        ability = skill_to_ability.get(skill, "Strength")
        base_modifier = self.get_stat_modifiers()[ability]
        
        if skill in self.skill_proficiencies:
            return base_modifier + self.proficiency_bonus
        return base_modifier
    
    def level_up(self):
        """Handle level up mechanics."""
        self.level += 1
        
        # Update proficiency bonus
        self.proficiency_bonus = 2 + ((self.level - 1) // 4)
        
        # Add hit points (simplified - normally you'd roll hit dice)
        con_modifier = self.get_ability_modifier(self.constitution)
        hp_gain = max(1, 5 + con_modifier)  # Average of d8 + CON mod
        self.max_hp += hp_gain
        self.hp += hp_gain
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary for JSON serialization."""
        return {
            # Basic Info
            "name": self.name,
            "race": self.race,
            "character_class": self.character_class,
            "level": self.level,
            "background": self.background,
            "alignment": self.alignment,
            
            # Stats
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma": self.charisma,
            
            # Health and Combat
            "hp": self.hp,
            "max_hp": self.max_hp,
            "armor_class": self.armor_class,
            "proficiency_bonus": self.proficiency_bonus,
            
            # Skills and Proficiencies
            "skill_proficiencies": self.skill_proficiencies,
            "saving_throw_proficiencies": self.saving_throw_proficiencies,
            
            # Inventory and Equipment
            "inventory": self.inventory,
            "equipment": self.equipment,
            
            # Progression
            "experience_points": self.experience_points,
            "gold_pieces": self.gold_pieces
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """Create character from dictionary."""
        return cls(
            # Basic Info
            name=data["name"],
            race=data.get("race", "Human"),
            character_class=data.get("character_class", "Fighter"),
            level=data.get("level", 1),
            background=data.get("background", "Folk Hero"),
            alignment=data.get("alignment", "Neutral Good"),
            
            # Stats
            strength=data.get("strength", 10),
            dexterity=data.get("dexterity", 10),
            constitution=data.get("constitution", 10),
            intelligence=data.get("intelligence", 10),
            wisdom=data.get("wisdom", 10),
            charisma=data.get("charisma", 10),
            
            # Health and Combat
            hp=data["hp"],
            max_hp=data["max_hp"],
            armor_class=data.get("armor_class", 10),
            proficiency_bonus=data.get("proficiency_bonus", 2),
            
            # Skills and Proficiencies
            skill_proficiencies=data.get("skill_proficiencies", []),
            saving_throw_proficiencies=data.get("saving_throw_proficiencies", []),
            
            # Inventory and Equipment
            inventory=data.get("inventory", []),
            equipment=data.get("equipment", {}),
            
            # Progression
            experience_points=data.get("experience_points", 0),
            gold_pieces=data.get("gold_pieces", 0)
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
        import os
        
        # Ensure the directory exists
        save_dir = os.path.dirname(file_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        
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