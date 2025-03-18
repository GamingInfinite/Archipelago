from dataclasses import dataclass

from Options import PerGameCommonOptions, OptionSet
from .locations import medals, maps

class ActiveMedals(OptionSet):
    """
    Choose Which Medals You Would Like to Be Included
    """
    display_name = "Active Medals"
    default = ["Easy", "Medium", "Hard"]
    valid_keys = frozenset(medals)

class ActiveMapDiffs(OptionSet):
    """
    Choose Which Map Difficulties Are Active
    """
    display_name = "Active Map Diffs"
    default = ["Beginner", "Intermediate", "Advanced", "Expert"]
    valid_keys = frozenset(maps.keys())

@dataclass
class BloonsGameOptions(PerGameCommonOptions):
    active_medals: ActiveMedals
    active_maps: ActiveMapDiffs