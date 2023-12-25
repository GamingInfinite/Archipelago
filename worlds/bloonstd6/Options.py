from Options import Choice, Toggle, Range,PerGameCommonOptions
from dataclasses import dataclass

class StartingMaps(Range):
    """The number of maps that will be automatically unlocked at the start."""
    range_start = 1
    range_end = 6
    default = 3
    display_name = "Starting Map Count"

class Difficulty(Choice):
    """The difficulty you must beat maps on to get checks"""
    display_name = "Difficulty"
    option_Easy = 0
    option_Medium = 1
    option_Hard = 2
    option_Impoppable = 3
    option_CHIMPS = 4
    default = 2

@dataclass
class BloonsTD6Options(PerGameCommonOptions):
    starting_map_count: StartingMaps
    map_difficulty: Difficulty