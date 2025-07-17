"""
Character data for Dungeons & Daemons.
Contains races, classes, backgrounds, and their associated bonuses and abilities.
"""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class RacialTrait:
    """Represents a racial trait or ability."""
    name: str
    description: str
    mechanical_benefit: str = ""


@dataclass
class Race:
    """Represents a character race with stats and traits."""
    name: str
    description: str
    stat_bonuses: Dict[str, int]  # ability score increases
    traits: List[RacialTrait]
    languages: List[str]
    proficiencies: List[str] = None
    size: str = "Medium"
    speed: int = 30


@dataclass
class ClassFeature:
    """Represents a class feature or ability."""
    name: str
    level: int
    description: str
    mechanical_benefit: str = ""


@dataclass
class CharacterClass:
    """Represents a character class with features and proficiencies."""
    name: str
    description: str
    hit_die: int  # d6, d8, d10, d12
    primary_abilities: List[str]
    saving_throw_proficiencies: List[str]
    skill_proficiencies: List[str]  # Choose from these
    skill_choices: int  # How many skills to choose
    armor_proficiencies: List[str]
    weapon_proficiencies: List[str]
    starting_equipment: Dict[str, Any]
    features: List[ClassFeature]


@dataclass
class Background:
    """Represents a character background."""
    name: str
    description: str
    skill_proficiencies: List[str]
    languages: int  # Number of additional languages
    equipment: List[str]
    feature: str
    feature_description: str
    suggested_characteristics: List[str]


# RACES
RACES = {
    "Human": Race(
        name="Human",
        description="Versatile and ambitious, humans are the most common race in most D&D worlds.",
        stat_bonuses={"Strength": 1, "Dexterity": 1, "Constitution": 1, "Intelligence": 1, "Wisdom": 1, "Charisma": 1},
        traits=[
            RacialTrait("Versatile", "Humans gain +1 to all ability scores", "+1 to all stats"),
            RacialTrait("Extra Skill", "Humans gain one additional skill proficiency", "+1 skill choice"),
            RacialTrait("Extra Feat", "Humans gain a bonus feat at 1st level", "Choose a feat")
        ],
        languages=["Common", "One extra language of choice"],
        size="Medium",
        speed=30
    ),
    
    "Elf": Race(
        name="Elf",
        description="Graceful and long-lived, elves are masters of magic and archery.",
        stat_bonuses={"Dexterity": 2},
        traits=[
            RacialTrait("Darkvision", "See in dim light within 60 feet as if it were bright light", "60ft darkvision"),
            RacialTrait("Keen Senses", "Proficiency in Perception skill", "Perception proficiency"),
            RacialTrait("Fey Ancestry", "Advantage on saves against being charmed, immune to sleep magic", "Charm resistance"),
            RacialTrait("Trance", "Elves don't need to sleep, instead meditate for 4 hours", "4-hour rest")
        ],
        languages=["Common", "Elvish"],
        proficiencies=["Perception"],
        size="Medium",
        speed=30
    ),
    
    "Dwarf": Race(
        name="Dwarf",
        description="Hardy mountain folk known for their resilience and craftsmanship.",
        stat_bonuses={"Constitution": 2},
        traits=[
            RacialTrait("Darkvision", "See in dim light within 60 feet", "60ft darkvision"),
            RacialTrait("Dwarven Resilience", "Advantage on saves against poison, resistance to poison damage", "Poison resistance"),
            RacialTrait("Dwarven Combat Training", "Proficiency with certain weapons", "Weapon proficiencies"),
            RacialTrait("Stonecunning", "Add proficiency bonus to History checks related to stonework", "Stone expertise")
        ],
        languages=["Common", "Dwarvish"],
        proficiencies=["Battleaxe", "Handaxe", "Light hammer", "Warhammer"],
        size="Medium",
        speed=25
    ),
    
    "Halfling": Race(
        name="Halfling",
        description="Small and nimble folk known for their luck and courage.",
        stat_bonuses={"Dexterity": 2},
        traits=[
            RacialTrait("Lucky", "Reroll 1s on attack rolls, ability checks, and saving throws", "Reroll 1s"),
            RacialTrait("Brave", "Advantage on saving throws against being frightened", "Fear resistance"),
            RacialTrait("Halfling Nimbleness", "Move through space of creatures one size larger", "Move through enemies"),
            RacialTrait("Small Size", "Small size grants certain advantages", "Small size benefits")
        ],
        languages=["Common", "Halfling"],
        size="Small",
        speed=25
    ),
    
    "Dragonborn": Race(
        name="Dragonborn",
        description="Proud dragon-descended humanoids with elemental breath weapons.",
        stat_bonuses={"Strength": 2, "Charisma": 1},
        traits=[
            RacialTrait("Draconic Ancestry", "Choose a dragon type for resistance and breath weapon", "Damage resistance"),
            RacialTrait("Breath Weapon", "Exhale destructive energy based on ancestry", "AoE attack ability"),
            RacialTrait("Damage Resistance", "Resistance to damage type associated with ancestry", "Damage resistance")
        ],
        languages=["Common", "Draconic"],
        size="Medium",
        speed=30
    ),
    
    "Tiefling": Race(
        name="Tiefling",
        description="Humanoids with infernal heritage, bearing the mark of darker planes.",
        stat_bonuses={"Intelligence": 1, "Charisma": 2},
        traits=[
            RacialTrait("Darkvision", "See in dim light within 60 feet", "60ft darkvision"),
            RacialTrait("Hellish Resistance", "Resistance to fire damage", "Fire resistance"),
            RacialTrait("Infernal Legacy", "Know thaumaturgy cantrip, later learn hellish rebuke and darkness", "Innate spells")
        ],
        languages=["Common", "Infernal"],
        size="Medium",
        speed=30
    )
}

# CLASSES
CLASSES = {
    "Fighter": CharacterClass(
        name="Fighter",
        description="Masters of martial combat, skilled with weapons and armor.",
        hit_die=10,
        primary_abilities=["Strength", "Dexterity"],
        saving_throw_proficiencies=["Strength", "Constitution"],
        skill_proficiencies=["Acrobatics", "Animal Handling", "Athletics", "History", "Insight", "Intimidation", "Perception", "Survival"],
        skill_choices=2,
        armor_proficiencies=["All armor", "Shields"],
        weapon_proficiencies=["Simple weapons", "Martial weapons"],
        starting_equipment={
            "armor": "Chain mail or leather armor",
            "weapons": ["Martial weapon and shield", "Two handaxes or simple weapon"],
            "equipment": ["Light crossbow and 20 bolts", "Dungeoneer's pack or Explorer's pack"]
        },
        features=[
            ClassFeature("Fighting Style", 1, "Choose a fighting style", "Combat bonus"),
            ClassFeature("Second Wind", 1, "Regain hit points as bonus action", "Self-healing"),
            ClassFeature("Action Surge", 2, "Take additional action on turn", "Extra action")
        ]
    ),
    
    "Wizard": CharacterClass(
        name="Wizard",
        description="Masters of arcane magic through study and preparation.",
        hit_die=6,
        primary_abilities=["Intelligence"],
        saving_throw_proficiencies=["Intelligence", "Wisdom"],
        skill_proficiencies=["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion"],
        skill_choices=2,
        armor_proficiencies=["None"],
        weapon_proficiencies=["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
        starting_equipment={
            "weapons": ["Quarterstaff or dagger"],
            "equipment": ["Component pouch or arcane focus", "Scholar's pack", "Spellbook", "Two cantrips"]
        },
        features=[
            ClassFeature("Spellcasting", 1, "Cast wizard spells using Intelligence", "Magic"),
            ClassFeature("Arcane Recovery", 1, "Recover spell slots on short rest", "Spell recovery"),
            ClassFeature("Arcane Tradition", 2, "Choose magical school specialization", "Specialization")
        ]
    ),
    
    "Rogue": CharacterClass(
        name="Rogue",
        description="Skilled in stealth, trickery, and precision strikes.",
        hit_die=8,
        primary_abilities=["Dexterity"],
        saving_throw_proficiencies=["Dexterity", "Intelligence"],
        skill_proficiencies=["Acrobatics", "Athletics", "Deception", "Insight", "Intimidation", "Investigation", 
                           "Perception", "Performance", "Persuasion", "Sleight of Hand", "Stealth"],
        skill_choices=4,
        armor_proficiencies=["Light armor"],
        weapon_proficiencies=["Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
        starting_equipment={
            "armor": "Leather armor",
            "weapons": ["Rapier or shortsword", "Shortbow and quiver of 20 arrows"],
            "equipment": ["Burglar's pack", "Thieves' tools"]
        },
        features=[
            ClassFeature("Expertise", 1, "Double proficiency bonus for two skills", "Skill mastery"),
            ClassFeature("Sneak Attack", 1, "Deal extra damage with advantage or flanking", "Extra damage"),
            ClassFeature("Thieves' Cant", 1, "Secret language of rogues", "Secret communication")
        ]
    ),
    
    "Cleric": CharacterClass(
        name="Cleric",
        description="Divine spellcasters wielding the power of their deity.",
        hit_die=8,
        primary_abilities=["Wisdom"],
        saving_throw_proficiencies=["Wisdom", "Charisma"],
        skill_proficiencies=["History", "Insight", "Medicine", "Persuasion", "Religion"],
        skill_choices=2,
        armor_proficiencies=["Light armor", "Medium armor", "Shields"],
        weapon_proficiencies=["Simple weapons"],
        starting_equipment={
            "armor": "Scale mail or leather armor",
            "weapons": ["Mace or warhammer", "Shield"],
            "equipment": ["Light crossbow and 20 bolts", "Priest's pack", "Holy symbol"]
        },
        features=[
            ClassFeature("Spellcasting", 1, "Cast cleric spells using Wisdom", "Divine magic"),
            ClassFeature("Divine Domain", 1, "Choose domain for additional spells and abilities", "Specialization"),
            ClassFeature("Channel Divinity", 2, "Use divine energy for various effects", "Divine power")
        ]
    ),
    
    "Ranger": CharacterClass(
        name="Ranger",
        description="Warriors of the wilderness, skilled in tracking and survival.",
        hit_die=10,
        primary_abilities=["Dexterity", "Wisdom"],
        saving_throw_proficiencies=["Strength", "Dexterity"],
        skill_proficiencies=["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"],
        skill_choices=3,
        armor_proficiencies=["Light armor", "Medium armor", "Shields"],
        weapon_proficiencies=["Simple weapons", "Martial weapons"],
        starting_equipment={
            "armor": "Scale mail or leather armor",
            "weapons": ["Two shortswords or two simple weapons", "Longbow and quiver of 20 arrows"],
            "equipment": ["Dungeoneer's pack or Explorer's pack"]
        },
        features=[
            ClassFeature("Favored Enemy", 1, "Advantage on tracking and knowledge of chosen enemy type", "Enemy expertise"),
            ClassFeature("Natural Explorer", 1, "Benefits in chosen terrain type", "Terrain mastery"),
            ClassFeature("Fighting Style", 2, "Choose a fighting style", "Combat bonus")
        ]
    ),
    
    "Barbarian": CharacterClass(
        name="Barbarian",
        description="Fierce warriors who fight with primal fury and instinct.",
        hit_die=12,
        primary_abilities=["Strength"],
        saving_throw_proficiencies=["Strength", "Constitution"],
        skill_proficiencies=["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"],
        skill_choices=2,
        armor_proficiencies=["Light armor", "Medium armor", "Shields"],
        weapon_proficiencies=["Simple weapons", "Martial weapons"],
        starting_equipment={
            "armor": "No armor (rely on high Constitution)",
            "weapons": ["Greataxe or any martial weapon", "Two handaxes or simple weapon"],
            "equipment": ["Explorer's pack", "Four javelins"]
        },
        features=[
            ClassFeature("Rage", 1, "Enter fury for damage bonus and resistance", "Combat enhancement"),
            ClassFeature("Unarmored Defense", 1, "AC = 10 + Dex + Con when not wearing armor", "Natural armor"),
            ClassFeature("Reckless Attack", 2, "Gain advantage but grant advantage to enemies", "Risk/reward combat")
        ]
    )
}

# BACKGROUNDS
BACKGROUNDS = {
    "Acolyte": Background(
        name="Acolyte",
        description="You have spent your life in service to a temple or religious order.",
        skill_proficiencies=["Insight", "Religion"],
        languages=2,
        equipment=["Holy symbol", "Prayer book", "Incense", "Vestments", "Common clothes", "Belt pouch with 15 gp"],
        feature="Shelter of the Faithful",
        feature_description="You can find refuge in temples and receive healing and assistance from clergy.",
        suggested_characteristics=["Devoted", "Faithful", "Contemplative", "Righteous"]
    ),
    
    "Criminal": Background(
        name="Criminal",
        description="You are an experienced criminal with connections to the underworld.",
        skill_proficiencies=["Deception", "Stealth"],
        languages=0,
        equipment=["Crowbar", "Dark clothes with hood", "Gaming set", "Belt pouch with 15 gp"],
        feature="Criminal Contact",
        feature_description="You have contacts in the criminal underworld who can provide information and services.",
        suggested_characteristics=["Sneaky", "Opportunistic", "Street-smart", "Pragmatic"]
    ),
    
    "Folk Hero": Background(
        name="Folk Hero",
        description="You come from humble origins but are destined for greater things.",
        skill_proficiencies=["Animal Handling", "Survival"],
        languages=0,
        equipment=["Artisan's tools", "Shovel", "Smith's tools", "Common clothes", "Belt pouch with 10 gp"],
        feature="Rustic Hospitality",
        feature_description="Common folk will provide you with food, shelter, and assistance.",
        suggested_characteristics=["Humble", "Determined", "Protective", "Down-to-earth"]
    ),
    
    "Noble": Background(
        name="Noble",
        description="You were born into privilege and understand wealth, power, and privilege.",
        skill_proficiencies=["History", "Persuasion"],
        languages=1,
        equipment=["Fine clothes", "Signet ring", "Scroll of pedigree", "Purse with 25 gp"],
        feature="Position of Privilege",
        feature_description="You are welcome in high society and can secure audiences with nobles.",
        suggested_characteristics=["Proud", "Cultured", "Entitled", "Diplomatic"]
    ),
    
    "Hermit": Background(
        name="Hermit",
        description="You lived in seclusion, learning profound truths about the world.",
        skill_proficiencies=["Medicine", "Religion"],
        languages=1,
        equipment=["Herbalism kit", "Scroll of spiritual writings", "Winter blanket", "Common clothes", "Belt pouch with 5 gp"],
        feature="Discovery",
        feature_description="You learned a unique and powerful secret during your seclusion.",
        suggested_characteristics=["Wise", "Reclusive", "Philosophical", "Patient"]
    ),
    
    "Soldier": Background(
        name="Soldier",
        description="You have experience as a professional warrior in an organized military.",
        skill_proficiencies=["Athletics", "Intimidation"],
        languages=0,
        equipment=["Rank insignia", "Trophy from fallen enemy", "Playing cards", "Common clothes", "Belt pouch with 10 gp"],
        feature="Military Rank",
        feature_description="You have rank and can invoke authority over soldiers of lower rank.",
        suggested_characteristics=["Disciplined", "Loyal", "Tactical", "Honor-bound"]
    )
}


def get_race_choices() -> List[str]:
    """Get list of available race names."""
    return list(RACES.keys())


def get_class_choices() -> List[str]:
    """Get list of available class names."""
    return list(CLASSES.keys())


def get_background_choices() -> List[str]:
    """Get list of available background names."""
    return list(BACKGROUNDS.keys())


def apply_racial_bonuses(stats: Dict[str, int], race_name: str) -> Dict[str, int]:
    """Apply racial stat bonuses to base stats."""
    if race_name not in RACES:
        return stats
    
    race = RACES[race_name]
    modified_stats = stats.copy()
    
    for stat, bonus in race.stat_bonuses.items():
        modified_stats[stat] += bonus
    
    return modified_stats


def get_racial_proficiencies(race_name: str) -> List[str]:
    """Get racial proficiencies for a race."""
    if race_name not in RACES:
        return []
    
    return RACES[race_name].proficiencies or []


def get_class_proficiencies(class_name: str) -> Dict[str, List[str]]:
    """Get class proficiencies (skills, saves, equipment)."""
    if class_name not in CLASSES:
        return {}
    
    char_class = CLASSES[class_name]
    return {
        "saving_throws": char_class.saving_throw_proficiencies,
        "skills": char_class.skill_proficiencies,
        "armor": char_class.armor_proficiencies,
        "weapons": char_class.weapon_proficiencies
    }


def get_background_proficiencies(background_name: str) -> Dict[str, Any]:
    """Get background proficiencies and equipment."""
    if background_name not in BACKGROUNDS:
        return {}
    
    background = BACKGROUNDS[background_name]
    return {
        "skills": background.skill_proficiencies,
        "languages": background.languages,
        "equipment": background.equipment,
        "feature": background.feature,
        "feature_description": background.feature_description
    }


def calculate_starting_hp(character_class: str, constitution_modifier: int) -> int:
    """Calculate starting hit points based on class and CON modifier."""
    if character_class not in CLASSES:
        return 8  # Default
    
    hit_die = CLASSES[character_class].hit_die
    return hit_die + constitution_modifier


def calculate_armor_class(dexterity_modifier: int, armor_type: str = "none") -> int:
    """Calculate armor class based on DEX and armor."""
    base_ac = 10 + dexterity_modifier
    
    armor_bonuses = {
        "none": 0,
        "leather": 1,  # 11 + Dex
        "studded_leather": 2,  # 12 + Dex
        "chain_shirt": 3,  # 13 + Dex (max 2)
        "scale_mail": 4,  # 14 + Dex (max 2)
        "chain_mail": 6,  # 16, no Dex
        "plate": 8   # 18, no Dex
    }
    
    if armor_type in armor_bonuses:
        if armor_type in ["chain_mail", "plate"]:
            return 10 + armor_bonuses[armor_type]  # No dex bonus
        elif armor_type in ["chain_shirt", "scale_mail"]:
            return 10 + armor_bonuses[armor_type] + min(dexterity_modifier, 2)  # Max +2 dex
        else:
            return 10 + armor_bonuses[armor_type] + dexterity_modifier  # Full dex bonus
    
    return base_ac 