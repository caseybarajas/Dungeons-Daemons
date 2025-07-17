"""
Settings and configuration management for Dungeons & Daemons.
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class GameSettings:
    """Game configuration settings."""
    # AI Settings
    ai_model: str = "llama3"
    ai_temperature: float = 0.7
    
    # Game Settings
    save_directory: str = "saves"
    max_history_turns: int = 10
    auto_save: bool = True
    
    # Display Settings
    show_debug_info: bool = False
    animation_speed: float = 0.05
    
    # Advanced Settings
    ollama_host: str = "localhost"
    ollama_port: int = 11434

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameSettings':
        """Create settings from dictionary, filtering unknown fields."""
        # Get only the fields that exist in GameSettings
        valid_fields = {field.name for field in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)


class SettingsManager:
    """Manages loading, saving, and updating game settings."""
    
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = settings_file
        self.settings = self.load_settings()
        
        # Ensure save directory exists
        os.makedirs(self.settings.save_directory, exist_ok=True)
    
    def load_settings(self) -> GameSettings:
        """Load settings from file or create defaults."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check if we're loading an old format and provide feedback
                valid_fields = {field.name for field in GameSettings.__dataclass_fields__.values()}
                unknown_fields = set(data.keys()) - valid_fields
                if unknown_fields:
                    print(f"Settings file contains unknown fields: {', '.join(unknown_fields)}")
                    print("These will be ignored and reset to defaults.")
                
                return GameSettings.from_dict(data)
        except (json.JSONDecodeError, KeyError, FileNotFoundError, TypeError) as e:
            print(f"Could not load settings: {e}")
            print("Using default settings.")
        
        return GameSettings()
    
    def save_settings(self) -> bool:
        """Save current settings to file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False
    
    def get_save_path(self, filename: str = "savegame.json") -> str:
        """Get the full path for a save file."""
        return os.path.join(self.settings.save_directory, filename)
    
    def get_available_models(self) -> list:
        """Get list of available Ollama models."""
        try:
            import subprocess
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                models = []
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                return models
            
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Return default models if ollama command fails
        return ["llama3", "mistral", "codellama", "llama2"]
    
    def validate_model(self, model_name: str) -> bool:
        """Check if a model is available."""
        return model_name in self.get_available_models()
    
    def update_setting(self, key: str, value: Any) -> bool:
        """Update a specific setting."""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            return self.save_settings()
        return False
    
    def reset_to_defaults(self) -> bool:
        """Reset all settings to defaults."""
        self.settings = GameSettings()
        return self.save_settings()
    
    def get_settings_summary(self) -> str:
        """Get a formatted summary of current settings."""
        return f"""
Current Settings:
═══════════════════════════════════════════════════════
AI Model: {self.settings.ai_model}
Temperature: {self.settings.ai_temperature}
Save Directory: {self.settings.save_directory}
Max History: {self.settings.max_history_turns} turns
Auto Save: {'Enabled' if self.settings.auto_save else 'Disabled'}
Debug Mode: {'Enabled' if self.settings.show_debug_info else 'Disabled'}
Animation Speed: {self.settings.animation_speed}s
Ollama Host: {self.settings.ollama_host}:{self.settings.ollama_port}
═══════════════════════════════════════════════════════
""" 