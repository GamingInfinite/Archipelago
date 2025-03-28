from Options import Choice, OptionSet, Toggle, Range, PerGameCommonOptions
from dataclasses import dataclass


class StartingMaps(Range):
    """The number of maps that will be automatically unlocked at the start."""

    range_start = 1
    range_end = 6
    default = 3
    display_name = "Starting Map Count"


class TotalMaps(Range):
    """
    The number of maps to be included (not including starting maps).
    This determines the number of \"Medal\" Items that are in the game in relation to your Randomizer Difficulty.
    """

    range_start = 15
    range_end = 69
    default = 15
    display_name = "Total Map Count"


class MinMapDiff(Range):
    """
    The Minimum Map Difficulty for selected maps (including starting and goal map)

    0 = Beginner
    1 = Intermediate
    2 = Advanced
    3 = Expert
    """

    range_start = 0
    range_end = 3
    default = 0
    display_name = "Minimum Map Difficulty"


class MaxMapDiff(Range):
    """
    The Maximum Map Difficulty for selected maps (including starting and goal map)

    0 = Beginner
    1 = Intermediate
    2 = Advanced
    3 = Expert
    """

    range_start = 0
    range_end = 3
    default = 3
    display_name = "Maximum Map Difficulty"


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
    default = 4


class MedalSelect(OptionSet):
    display_name = "Custom Medals"
    default = []
    valid_keys = [
        "Easy",
        "PrimaryOnly",
        "Deflation",
        "Medium",
        "MilitaryOnly",
        "Apopalypse",
        "Reverse",
        "Hard",
        "MagicOnly",
        "DoubleMoabHealth",
        "HalfCash",
        "AlternateBloonsRounds",
        "Impoppable",
        "Chimps",
    ]


class MedalRequirementPercentage(Range):
    """
    The Percentage of the Total Medals required for you to access the Goal Map

    For my own sanity and the randomizers this is hard bottomed at 50% so it can't be cheesed
    """

    display_name = "Medal Requirement Percentage"
    range_start = 50
    range_end = 100
    default = 50


class StartingMonkeys(Toggle):
    """
    Would you like to randomize all starting monkeys or include the Dart Monkey in the starting monkeys.

    True/On: All Starting Monkeys will be random.
    False/Off: The first starting monkey no matter how many you include will always be the vanilla Dart Monkey.
    """

    display_name = "Random Starting Monkeys"


class StartingMonkeyAmount(Range):
    """
    How many starting Monkeys would you like?
    """

    range_start = 1
    range_end = 3
    default = 1
    display_name = "Starting Monkey Amount"


class XPCurve(Toggle):
    """
    Off: Static
    On: Curved

    Static: A Configurable Amount of XP is Required to Level Up EACH time.
    Curved: Uses the default XP Curve from BTD6
    """

    display_name = "XP Curve"


class StaticXPRequirement(Range):
    """
    Min Req. 500 XP
    Max Req. 10,000 XP
    """

    display_name = "Static XP Requirement"
    range_start = 500
    range_end = 10000
    default = 1000


class MaxLevel(Range):
    """
    What do you want to be the maximum level of the randomizer.

    Levels start at 1, and you're required to go to at least 24
    """

    display_name = "Maximum Level"
    range_start = 24
    range_end = 150
    default = 24


@dataclass
class BloonsTD6Options(PerGameCommonOptions):
    starting_map_count: StartingMaps
    total_maps: TotalMaps
    min_map_diff: MinMapDiff
    max_map_diff: MaxMapDiff
    rando_difficulty: Difficulty
    custom_medal_inclusion: MedalSelect
    medalreq: MedalRequirementPercentage
    starting_monkey: StartingMonkeys
    num_start_monkey: StartingMonkeyAmount
    xp_curve: XPCurve
    static_req: StaticXPRequirement
    max_level: MaxLevel
