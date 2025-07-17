# Dungeons & Daemons

A terminal-based RPG powered by AI! Experience dynamic storytelling with a local Large Language Model acting as your Dungeon Master.

## Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running
3. A compatible LLM model (llama3, mistral, etc.)

### Installation

1. **Install Ollama** (if not already installed):
   ```bash
   # On macOS
   brew install ollama
   
   # On Linux/Windows, download from https://ollama.ai
   ```

2. **Pull a compatible model**:
   ```bash
   ollama pull llama3
   # or
   ollama pull mistral
   ```

3. **Start Ollama service**:
   ```bash
   ollama serve
   ```

4. **Install game dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game**:
   ```bash
   python main.py
   ```

## How to Play

### First Time Setup
- Run the game and enter your character's name
- The AI will create your starting scenario

### Gameplay
- **Actions**: Type what you want to do (e.g., "explore the forest", "attack the goblin", "drink health potion")
- **Inventory**: Your items are tracked automatically
- **Health**: Monitor your HP - if it reaches 0, the game ends
- **Save System**: Progress is saved automatically after every turn

### Commands
- `quit`, `exit`, or `q` - Exit the game
- Any other text - Perform that action in the game

## File Structure

```
├── src/                    # Source code directory
│   ├── main.py            # Main game loop and entry point
│   ├── menu_system.py     # Menu navigation and UI
│   ├── game_state.py      # Character and game state management
│   ├── ai_manager.py      # AI/LLM communication handler
│   ├── prompts.py         # AI prompt templates
│   ├── settings.py        # Configuration management
│   ├── ascii_art.py       # Visual elements and ASCII art
│   └── error_handler.py   # Error handling and user feedback
├── saves/                 # Save game directory (created automatically)
├── assets/                # Game assets and resources
├── requirements.txt       # Python dependencies
├── settings.json          # Game configuration (created automatically)
└── README.md              # This documentation
```

## Configuration

### Changing AI Model
Edit the model name in `ai_manager.py`:
```python
self.model = "llama3"  # Change to your preferred model
```

### Settings File
The game creates a `settings.json` file automatically with these options:
```json
{
    "ai_model": "llama3",
    "ai_temperature": 0.7,
    "save_directory": "./saves",
    "max_history_turns": 10,
    "auto_save": true,
    "show_debug_info": false,
    "animation_speed": 1.0,
    "ollama_host": "localhost",
    "ollama_port": 11434
}
```

## Troubleshooting

### Common Issues

1. **"Connection refused" error**:
   - Make sure Ollama is running: `ollama serve`
   - Check if the service is on the correct port (11434)

2. **Model not found**:
   - Pull the model first: `ollama pull llama3`
   - Verify available models: `ollama list`

3. **Save file issues**:
   - Check file permissions in the saves directory
   - Verify the saves directory exists and is writable

4. **Performance issues**:
   - Try a smaller model (e.g., `mistral` instead of `llama3`)
   - Reduce `ai_temperature` in settings for faster responses
   - Lower `max_history_turns` to reduce context size

### Requirements
- Python 3.8 or higher
- Ollama installed and running
- At least 4GB RAM (8GB recommended for larger models)
- Terminal that supports ANSI colors and Unicode characters

## Contributing

Feel free to submit issues and enhancement requests! This is a hobby project designed to showcase AI-powered gaming experiences.

## License

This project is open source and available under the MIT License.

---

**Ready to embark on your adventure? Run `python main.py` and let the adventure begin!** 