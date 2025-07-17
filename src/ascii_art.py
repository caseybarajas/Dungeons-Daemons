"""
ASCII Art and visual elements for Dungeons & Daemons.
Professional design with clean, aligned typography.
"""

# Clean main title with professional design
TITLE_ART = r"""

{:^55}

{:^55}

""".format(
    "DUNGEONS & DAEMONS",
    "An AI-Powered Adventure Awaits"
)

# Clean simple title for smaller spaces
SIMPLE_TITLE = "D U N G E O N S   &   D A E M O N S"

# Character creation with clean design
CHARACTER_ART = r"""

        Create Your Hero

     [ Sword ] [ Shield ]
      Choose your destiny

"""

# Professional game over screen
GAME_OVER_ART = r"""

                     G A M E   O V E R

              Your legend comes to an end...

           Press Enter to return to main menu

"""

# Clean loading messages
LOADING_FRAMES = [
    "Awakening the ancient spirits...",
    "Consulting the mystical archives...",
    "The Oracle prepares your destiny...",
    "Magic flows through the realm...",
    "Your adventure begins now!"
]

# Health status indicators with text symbols
HEALTH_INDICATORS = {
    "critical": "[X]",
    "low": "[!]", 
    "medium": "[~]",
    "good": "[+]",
    "full": "[*]"
}

# Location prefixes for clean display
LOCATION_PREFIXES = {
    "village": "[Village]",
    "town": "[Town]",
    "forest": "[Forest]",
    "dungeon": "[Dungeon]",
    "cave": "[Cave]",
    "mountain": "[Mountain]",
    "desert": "[Desert]",
    "swamp": "[Swamp]",
    "tavern": "[Tavern]",
    "inn": "[Inn]",
    "shop": "[Shop]",
    "castle": "[Castle]",
    "tower": "[Tower]",
    "ruins": "[Ruins]",
    "temple": "[Temple]",
    "library": "[Library]",
    "default": "[Location]"
}

# Item type indicators for clean display
ITEM_TYPES = {
    "sword": "[Weapon]",
    "blade": "[Weapon]",
    "shield": "[Armor]",
    "potion": "[Consumable]",
    "elixir": "[Consumable]",
    "gold": "[Currency]",
    "coin": "[Currency]",
    "key": "[Key Item]",
    "scroll": "[Scroll]",
    "bow": "[Weapon]",
    "armor": "[Armor]",
    "helm": "[Armor]",
    "ring": "[Accessory]",
    "gem": "[Valuable]",
    "crystal": "[Magical]",
    "book": "[Readable]",
    "tome": "[Readable]",
    "staff": "[Weapon]",
    "wand": "[Weapon]",
    "dagger": "[Weapon]",
    "default": "[Item]"
}

# Professional color scheme
class Colors:
    # Primary colors
    TITLE = "bold bright_magenta"
    ACCENT = "bright_cyan"
    SUCCESS = "bright_green"
    WARNING = "bright_yellow"
    ERROR = "bright_red"
    INFO = "bright_blue"
    
    # UI colors
    MENU_TITLE = "bold bright_white"
    MENU_OPTION = "bright_cyan"
    SELECTED = "bold bright_yellow"
    MUTED = "dim bright_black"
    
    # Game colors
    HEALTH_GOOD = "bright_green"
    HEALTH_OK = "yellow"
    HEALTH_LOW = "bright_red"
    NARRATIVE = "bright_white"
    STAT_LABEL = "bright_blue"
    STAT_VALUE = "bright_white"

def get_health_indicator(hp: int, max_hp: int) -> str:
    """Get health indicator symbol based on HP percentage."""
    if hp <= 0:
        return HEALTH_INDICATORS["critical"]
    
    ratio = hp / max_hp
    if ratio >= 1.0:
        return HEALTH_INDICATORS["full"]
    elif ratio >= 0.75:
        return HEALTH_INDICATORS["good"] 
    elif ratio >= 0.5:
        return HEALTH_INDICATORS["medium"]
    elif ratio >= 0.25:
        return HEALTH_INDICATORS["low"]
    else:
        return HEALTH_INDICATORS["critical"]

def get_location_prefix(location: str) -> str:
    """Get location type prefix for display."""
    location_lower = location.lower()
    for key, prefix in LOCATION_PREFIXES.items():
        if key in location_lower:
            return prefix
    return LOCATION_PREFIXES["default"]

def get_item_type(item: str) -> str:
    """Get item type indicator for display."""
    item_lower = item.lower()
    for key, item_type in ITEM_TYPES.items():
        if key in item_lower:
            return item_type
    return ITEM_TYPES["default"]

def get_random_loading_message():
    """Get a random loading message."""
    import random
    return random.choice(LOADING_FRAMES)

# Professional borders and frames
def create_fancy_border(width: int = 60) -> tuple[str, str, str]:
    """Create fancy border components."""
    top = "╭" + "─" * (width - 2) + "╮"
    middle = "│" + " " * (width - 2) + "│"
    bottom = "╰" + "─" * (width - 2) + "╯"
    return top, middle, bottom

def create_double_border(width: int = 60) -> tuple[str, str, str]:
    """Create double-line border components."""
    top = "╔" + "═" * (width - 2) + "╗"
    middle = "║" + " " * (width - 2) + "║"
    bottom = "╚" + "═" * (width - 2) + "╝"
    return top, middle, bottom 