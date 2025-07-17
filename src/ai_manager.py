"""
AI Manager for Dungeons & Daemons.
Handles all communication with the local LLM through Ollama and LangChain.
"""

import json
import subprocess
import time
import os
from typing import Dict, Any, Optional
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from game_state import GameState
from prompts import SYSTEM_PROMPT, GAME_PROMPT_TEMPLATE


class AIManager:
    """Manages AI interactions with automatic setup and fallback modes."""
    
    def __init__(self, model_name: str = "llama3", temperature: float = 0.7, 
                 ollama_host: str = "localhost", ollama_port: int = 11434):
        """Initialize AI Manager with automatic setup."""
        self.model_name = model_name
        self.temperature = temperature
        self.ollama_host = ollama_host
        self.ollama_port = ollama_port
        self.llm = None
        self.chain = None
        self.fallback_mode = False
        
        try:
            print("Setting up AI Dungeon Master...")
            
            # Auto-setup Ollama
            if self._setup_ollama():
                self._initialize_ai()
                print("AI Dungeon Master ready!")
            else:
                print("AI setup failed - using fallback story mode")
                self.fallback_mode = True
                
        except Exception as e:
            print(f"AI initialization failed: {e}")
            print("Using fallback story mode")
            self.fallback_mode = True
    
    def _setup_ollama(self) -> bool:
        """Automatically setup Ollama and models."""
        try:
            # Check if Ollama is installed
            if not self._check_ollama_installed():
                print("Ollama not found. Please install Ollama from https://ollama.ai")
                return False
            
            # Start Ollama if not running
            if not self._check_ollama_running():
                print("Starting Ollama service...")
                if not self._start_ollama():
                    print("Failed to start Ollama")
                    return False
                
                # Wait for Ollama to start
                time.sleep(3)
            
            # Check for available models
            if not self._check_models_available():
                print(f"Downloading AI model ({self.model_name})...")
                if not self._download_model():
                    print("Failed to download model")
                    return False
            
            return True
            
        except Exception as e:
            print(f"Ollama setup failed: {e}")
            return False
    
    def _check_ollama_installed(self) -> bool:
        """Check if Ollama is installed."""
        try:
            subprocess.run(["ollama", "--version"], 
                         capture_output=True, check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _check_ollama_running(self) -> bool:
        """Check if Ollama service is running."""
        try:
            import requests
            response = requests.get(f"http://{self.ollama_host}:{self.ollama_port}/api/tags", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def _start_ollama(self) -> bool:
        """Start Ollama service."""
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(["ollama", "serve"], 
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:  # Unix/Linux/Mac
                subprocess.Popen(["ollama", "serve"], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            print(f"Failed to start Ollama: {e}")
            return False
    
    def _check_models_available(self) -> bool:
        """Check if any models are available."""
        try:
            result = subprocess.run(["ollama", "list"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                # Skip header line, check if any models exist
                return len(lines) > 1 and any(self.model_name in line for line in lines[1:])
            return False
        except:
            return False
    
    def _download_model(self) -> bool:
        """Download the required model."""
        try:
            print(f"This may take a few minutes for first-time setup...")
            result = subprocess.run(["ollama", "pull", self.model_name], 
                                  capture_output=True, text=True, timeout=300)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print("Model download timed out")
            return False
        except Exception as e:
            print(f"Model download failed: {e}")
            return False
    
    def _initialize_ai(self):
        """Initialize the AI chain."""
        base_url = f"http://{self.ollama_host}:{self.ollama_port}"
        
        self.llm = OllamaLLM(
            model=self.model_name,
            format="json",
            temperature=self.temperature,
            base_url=base_url,
        )
        
        # Create the chat prompt template
        prompt = PromptTemplate(
            template=SYSTEM_PROMPT + "\n\n" + GAME_PROMPT_TEMPLATE,
            input_variables=["player_name", "current_hp", "max_hp", "current_location", 
                           "inventory", "story_history", "user_input"]
        )
        
        # Create the chain
        self.chain = (
            prompt 
            | self.llm
            | StrOutputParser()
        )
    
    def get_ai_response(self, game_state: GameState, user_input: str) -> Dict[str, Any]:
        """Get AI response with fallback mode support."""
        if self.fallback_mode:
            return self._get_fallback_response(game_state, user_input)
        
        try:
            # Prepare the context
            context = {
                "player_name": game_state.player.name,
                "current_hp": game_state.player.hp,
                "max_hp": game_state.player.max_hp,
                "current_location": game_state.current_location,
                "inventory": ", ".join(game_state.player.inventory) if game_state.player.inventory else "Empty",
                "story_history": game_state.get_history_text(),
                "user_input": user_input
            }
            
            # Get response from AI
            response = self.chain.invoke(context)
            
            # Parse JSON response
            try:
                if isinstance(response, str):
                    parsed_response = json.loads(response)
                else:
                    parsed_response = response
                
                # Ensure all required keys exist
                required_keys = ["narrative", "location", "hp_change", "items_added", "items_removed"]
                for key in required_keys:
                    if key not in parsed_response:
                        parsed_response[key] = self._get_default_value(key)
                
                return parsed_response
                
            except json.JSONDecodeError as e:
                print("AI response parsing failed - switching to fallback mode")
                self.fallback_mode = True
                return self._get_fallback_response(game_state, user_input)
                
        except Exception as e:
            print("AI connection lost - switching to fallback mode")
            self.fallback_mode = True
            return self._get_fallback_response(game_state, user_input)
    
    def _get_fallback_response(self, game_state: GameState, user_input: str) -> Dict[str, Any]:
        """Generate fallback responses when AI isn't available."""
        action = user_input.lower().strip()
        
        # Simple pattern matching for common actions
        if any(word in action for word in ["attack", "fight", "hit", "strike"]):
            return {
                "narrative": f"{game_state.player.name} swings their weapon! You deal damage to your opponent.",
                "location": game_state.current_location,
                "hp_change": -5,  # Take some damage in return
                "items_added": [],
                "items_removed": []
            }
        
        elif any(word in action for word in ["heal", "potion", "drink", "use potion"]):
            if "Health Potion" in game_state.player.inventory:
                return {
                    "narrative": f"{game_state.player.name} drinks a health potion and feels much better!",
                    "location": game_state.current_location,
                    "hp_change": 20,
                    "items_added": [],
                    "items_removed": ["Health Potion"]
                }
            else:
                return {
                    "narrative": "You search your belongings but find no healing items.",
                    "location": game_state.current_location,
                    "hp_change": 0,
                    "items_added": [],
                    "items_removed": []
                }
        
        elif any(word in action for word in ["explore", "look", "search", "examine"]):
            return {
                "narrative": f"You explore the {game_state.current_location} carefully. The area seems peaceful for now, but you sense adventure awaits.",
                "location": game_state.current_location,
                "hp_change": 0,
                "items_added": [],
                "items_removed": []
            }
        
        elif any(word in action for word in ["north", "south", "east", "west", "go", "move", "travel"]):
            new_locations = ["Forest Path", "Mountain Trail", "Village Square", "Ancient Ruins", "Mystic Cave"]
            import random
            new_location = random.choice([loc for loc in new_locations if loc != game_state.current_location])
            return {
                "narrative": f"You travel onward and arrive at the {new_location}. The journey was uneventful but you feel ready for whatever comes next.",
                "location": new_location,
                "hp_change": 0,
                "items_added": [],
                "items_removed": []
            }
        
        else:
            return {
                "narrative": f"You attempt to {action}. The world around you responds in mysterious ways, and your adventure continues.",
                "location": game_state.current_location,
                "hp_change": 0,
                "items_added": [],
                "items_removed": []
            }
    
    def _get_default_value(self, key: str) -> Any:
        """Get default value for missing keys."""
        defaults = {
            "narrative": "The adventure continues...",
            "location": "Unknown",
            "hp_change": 0,
            "items_added": [],
            "items_removed": []
        }
        return defaults.get(key, "")
    
    def test_connection(self) -> bool:
        """Test the connection to Ollama."""
        if self.fallback_mode:
            return True  # Fallback mode always works
            
        try:
            test_response = self.llm.invoke("Hello")
            if test_response:
                print("Ollama connection successful")
                return True
            else:
                print("No response from Ollama")
                return False
        except Exception as e:
            print(f"AI connection test failed: {e}")
            return False 