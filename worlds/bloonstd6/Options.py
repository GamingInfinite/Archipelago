from Options import Choice, Toggle, Range,PerGameCommonOptions
from dataclasses import dataclass

class StartingMaps(Range):
    """The number of maps that will be automatically unlocked at the start."""
    range_start = 1
    range_end = 6
    default = 3
    display_name = "Starting Map Count"

class TotalMaps(Range):
    """The number of maps to be included.  This determines the number of \"Medal\" Items that are in the game"""
    range_start = 15
    range_end = 40

class Difficulty(Choice):
    """
    The difficulty of the randomizer.

    Basic: The Easy, Medium, Hard, and Impoppable Medals are all checks.
    Advanced: The Easy, Medium, Hard, Impoppable, and Chimps Medals are all checks.
    Expert: All Medals are checks.
    """
    display_name = "Difficulty"
    option_Basic = 4
    option_Advanced = 5
    option_Expert = 14
    default = 0

class StartingMonkey(Choice):
    """Do you want a random starting monkey or the vanilla Dart Monkey (Not Implemented)"""
    display_name = "Starting Monkey"
    option_Vanilla = False
    option_Random = True
    default = False

@dataclass
class BloonsTD6Options(PerGameCommonOptions):
    starting_map_count: StartingMaps
    map_difficulty: Difficulty
    starting_monkey: StartingMonkey