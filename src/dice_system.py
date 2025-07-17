"""
Dice rolling system for Dungeons & Daemons.
Provides D&D-style dice mechanics with beautiful visual output.
"""

import random
import re
from typing import List, Tuple, Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.columns import Columns
from ascii_art import Colors


class DiceResult:
    """Represents the result of a dice roll."""
    
    def __init__(self, rolls: List[int], dice_type: int, modifier: int = 0, description: str = ""):
        self.rolls = rolls
        self.dice_type = dice_type
        self.modifier = modifier
        self.description = description
        self.total = sum(rolls) + modifier
        self.roll_count = len(rolls)
    
    def __str__(self) -> str:
        """String representation of the dice result."""
        rolls_str = " + ".join(map(str, self.rolls))
        if self.modifier != 0:
            modifier_str = f" + {self.modifier}" if self.modifier > 0 else f" - {abs(self.modifier)}"
            return f"{rolls_str}{modifier_str} = {self.total}"
        return f"{rolls_str} = {self.total}"
    
    @property
    def is_critical_hit(self) -> bool:
        """Check if this was a critical hit (natural 20 on d20)."""
        return self.dice_type == 20 and self.roll_count == 1 and self.rolls[0] == 20
    
    @property
    def is_critical_fail(self) -> bool:
        """Check if this was a critical failure (natural 1 on d20)."""
        return self.dice_type == 20 and self.roll_count == 1 and self.rolls[0] == 1
    
    @property
    def is_max_roll(self) -> bool:
        """Check if all dice rolled maximum values."""
        return all(roll == self.dice_type for roll in self.rolls)
    
    @property
    def is_min_roll(self) -> bool:
        """Check if all dice rolled minimum values (1)."""
        return all(roll == 1 for roll in self.rolls)


class DiceRoller:
    """D&D-style dice rolling system with beautiful output."""
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.dice_faces = {
            4: [str(i) for i in range(1, 5)],
            6: [str(i) for i in range(1, 7)],
            8: [str(i) for i in range(1, 9)],
            10: [str(i) for i in range(1, 11)],
            12: [str(i) for i in range(1, 13)],
            20: [str(i) for i in range(1, 21)]
        }
    
    def roll_dice(self, count: int, sides: int, modifier: int = 0, description: str = "") -> DiceResult:
        """Roll dice and return results."""
        if count <= 0 or sides <= 0:
            raise ValueError("Count and sides must be positive integers")
        
        rolls = [random.randint(1, sides) for _ in range(count)]
        return DiceResult(rolls, sides, modifier, description)
    
    def parse_dice_notation(self, notation: str) -> Tuple[int, int, int]:
        """Parse dice notation like '3d6+2' or '1d20-1'."""
        # Clean up the notation
        notation = notation.replace(" ", "").lower()
        
        # Pattern: optional count, 'd', sides, optional modifier
        pattern = r'(?:(\d+))?d(\d+)(?:([+-])(\d+))?'
        match = re.match(pattern, notation)
        
        if not match:
            raise ValueError(f"Invalid dice notation: {notation}")
        
        count = int(match.group(1)) if match.group(1) else 1
        sides = int(match.group(2))
        
        modifier = 0
        if match.group(3) and match.group(4):
            modifier_value = int(match.group(4))
            modifier = modifier_value if match.group(3) == '+' else -modifier_value
        
        return count, sides, modifier
    
    def roll_from_notation(self, notation: str, description: str = "") -> DiceResult:
        """Roll dice from standard notation (e.g., '3d6+2')."""
        count, sides, modifier = self.parse_dice_notation(notation)
        return self.roll_dice(count, sides, modifier, description)
    
    def display_roll_result(self, result: DiceResult, show_animation: bool = True) -> None:
        """Display dice roll result with beautiful formatting."""
        if show_animation:
            self._show_rolling_animation(result.roll_count, result.dice_type)
        
        # Create dice visual representation
        dice_visuals = []
        for i, roll in enumerate(result.rolls):
            dice_visual = self._get_dice_visual(roll, result.dice_type)
            dice_visuals.append(dice_visual)
        
        # Determine color based on result
        if result.is_critical_hit:
            style = Colors.SUCCESS
            border_style = Colors.SUCCESS
            title = "CRITICAL HIT!"
        elif result.is_critical_fail:
            style = Colors.ERROR
            border_style = Colors.ERROR
            title = "CRITICAL FAILURE!"
        elif result.is_max_roll:
            style = Colors.SELECTED
            border_style = Colors.ACCENT
            title = "MAXIMUM ROLL!"
        elif result.is_min_roll:
            style = Colors.WARNING
            border_style = Colors.WARNING
            title = "MINIMUM ROLL"
        else:
            style = Colors.INFO
            border_style = Colors.ACCENT
            title = f"Dice Roll ({result.roll_count}d{result.dice_type})"
        
        # Create the display content
        content_lines = []
        
        # Show dice visuals
        if len(dice_visuals) <= 6:  # Show all dice if 6 or fewer
            dice_row = "   ".join(dice_visuals)
            content_lines.append(Text(dice_row, style=Colors.ACCENT, justify="center"))
        else:  # Show count if more than 6
            content_lines.append(Text(f"Rolled {len(dice_visuals)} dice", style=Colors.INFO, justify="center"))
        
        content_lines.append(Text(""))  # Empty line
        
        # Show individual rolls
        if result.roll_count <= 10:  # Show individual rolls if 10 or fewer
            rolls_text = " + ".join(str(roll) for roll in result.rolls)
            content_lines.append(Text(f"Rolls: {rolls_text}", style=Colors.STAT_VALUE, justify="center"))
        else:
            content_lines.append(Text(f"Individual rolls: {result.rolls}", style=Colors.STAT_VALUE, justify="center"))
        
        # Show modifier if any
        if result.modifier != 0:
            modifier_text = f"Modifier: {result.modifier:+d}"
            content_lines.append(Text(modifier_text, style=Colors.INFO, justify="center"))
        
        content_lines.append(Text(""))  # Empty line
        
        # Show total
        total_text = Text()
        total_text.append("TOTAL: ", style=Colors.STAT_LABEL)
        total_text.append(str(result.total), style=Colors.SELECTED)
        content_lines.append(total_text.copy())
        
        # Show description if provided
        if result.description:
            content_lines.append(Text(""))
            content_lines.append(Text(result.description, style=Colors.MUTED, justify="center"))
        
        # Create the panel
        from rich.console import Group
        content_group = Group(*[Align.center(line) for line in content_lines])
        
        result_panel = Panel(
            content_group,
            title=title,
            title_align="center",
            style=style,
            border_style=border_style,
            padding=(1, 2),
            width=min(80, max(40, len(str(result)) + 20))
        )
        
        self.console.print(Align.center(result_panel))
    
    def _get_dice_visual(self, value: int, sides: int) -> str:
        """Get visual representation of a dice face."""
        if sides in self.dice_faces and value <= len(self.dice_faces[sides]):
            return self.dice_faces[sides][value - 1]
        else:
            return str(value)
    
    def _show_rolling_animation(self, count: int, sides: int) -> None:
        """Show a brief rolling animation."""
        import time
        
        rolling_text = Text()
        rolling_text.append("Rolling ", style=Colors.INFO)
        rolling_text.append(f"{count}d{sides}", style=Colors.ACCENT)
        rolling_text.append("...", style=Colors.INFO)
        
        rolling_panel = Panel(
            Align.center(rolling_text),
            style=Colors.INFO,
            border_style=Colors.ACCENT,
            padding=(0, 2)
        )
        
        self.console.print(Align.center(rolling_panel))
        time.sleep(0.8)  # Brief pause for drama
        
        # Clear the rolling message
        import os
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        self.console.clear()
    
    def roll_stats(self, method: str = "4d6_drop_lowest") -> Dict[str, int]:
        """Roll D&D ability scores using various methods."""
        stats = {}
        stat_names = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        
        for stat in stat_names:
            if method == "4d6_drop_lowest":
                # Roll 4d6, drop the lowest
                rolls = [random.randint(1, 6) for _ in range(4)]
                rolls.sort(reverse=True)
                stats[stat] = sum(rolls[:3])  # Take the highest 3
            elif method == "3d6":
                # Standard 3d6
                stats[stat] = sum(random.randint(1, 6) for _ in range(3))
            elif method == "point_buy":
                # Point buy system (all start at 8, player allocates 27 points)
                stats[stat] = 8  # Will be customized later
            elif method == "array":
                # Standard array: 15, 14, 13, 12, 10, 8
                pass  # Will be assigned later
        
        if method == "array":
            # Assign standard array values
            array_values = [15, 14, 13, 12, 10, 8]
            for i, stat in enumerate(stat_names):
                stats[stat] = array_values[i]
        
        return stats
    
    def display_stat_roll(self, stat_name: str, rolls: List[int], final_value: int) -> None:
        """Display the result of rolling a single stat."""
        # Show the rolling process
        dice_visuals = [self._get_dice_visual(roll, 6) for roll in rolls]
        
        content_lines = []
        content_lines.append(Text(f"Rolling {stat_name}:", style=Colors.STAT_LABEL, justify="center"))
        content_lines.append(Text(""))
        
        # Show dice
        dice_row = "   ".join(dice_visuals)
        content_lines.append(Text(dice_row, style=Colors.ACCENT, justify="center"))
        content_lines.append(Text(""))
        
        # Show calculation (if 4d6 drop lowest)
        if len(rolls) == 4:
            sorted_rolls = sorted(rolls, reverse=True)
            kept_rolls = sorted_rolls[:3]
            dropped_roll = sorted_rolls[3]
            
            calc_text = " + ".join(str(roll) for roll in kept_rolls)
            content_lines.append(Text(f"Keep highest 3: {calc_text}", style=Colors.INFO, justify="center"))
            content_lines.append(Text(f"(Dropped: {dropped_roll})", style=Colors.MUTED, justify="center"))
        else:
            calc_text = " + ".join(str(roll) for roll in rolls)
            content_lines.append(Text(f"Total: {calc_text}", style=Colors.INFO, justify="center"))
        
        content_lines.append(Text(""))
        
        # Show final value with appropriate color
        if final_value >= 16:
            value_style = Colors.SUCCESS
        elif final_value >= 14:
            value_style = Colors.SELECTED
        elif final_value >= 12:
            value_style = Colors.INFO
        elif final_value >= 10:
            value_style = Colors.WARNING
        else:
            value_style = Colors.ERROR
        
        final_text = Text()
        final_text.append(f"{stat_name}: ", style=Colors.STAT_LABEL)
        final_text.append(str(final_value), style=value_style)
        content_lines.append(final_text.copy())
        
        # Create panel
        from rich.console import Group
        content_group = Group(*[Align.center(line) for line in content_lines])
        
        stat_panel = Panel(
            content_group,
            title=f"{stat_name} Roll",
            title_align="center",
            style=Colors.ACCENT,
            border_style=Colors.ACCENT,
            padding=(1, 2),
            width=50
        )
        
        self.console.print(Align.center(stat_panel))
    
    def get_modifier(self, ability_score: int) -> int:
        """Calculate D&D ability modifier from score."""
        return (ability_score - 10) // 2
    
    def format_modifier(self, modifier: int) -> str:
        """Format modifier with proper +/- sign."""
        if modifier >= 0:
            return f"+{modifier}"
        else:
            return str(modifier)


# Convenience functions for common dice rolls
def d4(count: int = 1, modifier: int = 0) -> DiceResult:
    """Roll d4(s)."""
    roller = DiceRoller()
    return roller.roll_dice(count, 4, modifier)

def d6(count: int = 1, modifier: int = 0) -> DiceResult:
    """Roll d6(s)."""
    roller = DiceRoller()
    return roller.roll_dice(count, 6, modifier)

def d8(count: int = 1, modifier: int = 0) -> DiceResult:
    """Roll d8(s)."""
    roller = DiceRoller()
    return roller.roll_dice(count, 8, modifier)

def d10(count: int = 1, modifier: int = 0) -> DiceResult:
    """Roll d10(s)."""
    roller = DiceRoller()
    return roller.roll_dice(count, 10, modifier)

def d12(count: int = 1, modifier: int = 0) -> DiceResult:
    """Roll d12(s)."""
    roller = DiceRoller()
    return roller.roll_dice(count, 12, modifier)

def d20(count: int = 1, modifier: int = 0) -> DiceResult:
    """Roll d20(s)."""
    roller = DiceRoller()
    return roller.roll_dice(count, 20, modifier)

def d100() -> DiceResult:
    """Roll percentile dice (d100)."""
    roller = DiceRoller()
    return roller.roll_dice(1, 100, 0, "Percentile Roll") 