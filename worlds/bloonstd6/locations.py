from typing import Dict, List

from BaseClasses import Location
from worlds.bloonstd6.utils import Shared

maps = {
    "beginner": {
        "Tutorial",
        "InTheLoop",
        "MiddleOfTheRoad",
        "Tinkerton",
        "TreeStump",
        "TownCentre",
        "OneTwoTree",
        "Scrapyard",
        "TheCabin",
        "Resort",
        "Skates",
        "LotusIsland",
        "CandyFalls",
        "WinterPark",
        "Carved",
        "ParkPath",
        "AlpineRun",
        "FrozenOver",
        "Cubism",
        "FourCircles",
        "Hedge",
        "EndOfTheRoad",
        "Logs",
    },
    "intermediate": {
        "LuminousCove",
        "SulfurSprings",
        "WaterPark",
        "Polyphemus",
        "CoveredGarden",
        "Quarry",
        "QuietStreet",
        "BloonariusPrime",
        "Balance",
        "Encrypted",
        "Bazaar",
        "AdorasTemple",
        "SpringSpring",
        "KartsNDarts",
        "MoonLanding",
        "Haunted",
        "Downstream",
        "FiringRange",
        "Cracked",
        "Streambed",
        "Chutes",
        "Rake",
        "SpiceIslands",
    },
    "advanced": {
        "EnchantedGlade",
        "LastResort",
        "AncientPortal",
        "CastleRevenge",
        "DarkPath",
        "Erosion",
        "MidnightMansion",
        "SunkenColumns",
        "XFactor",
        "Mesa",
        "Geared",
        "Spillway",
        "Cargo",
        "PatsPond",
        "Peninsula",
        "HighFinance",
        "AnotherBrick",
        "OffTheCoast",
        "Cornfield",
        "Underground",
    },
    "expert": {
        "GlacialTrail",
        "DarkDungeons",
        "Sanctuary",
        "Ravine",
        "FloodedValley",
        "Infernal",
        "BloodyPuddles",
        "Workshop",
        "Quad",
        "DarkCastle",
        "MuddyPuddles",
        "#ouch",
    }
}

medals = [
    "Easy",
    "Medium",
    "Hard",
    "PrimaryOnly",
    "Deflation",
    "MilitaryOnly",
    "Reverse",
    "Apopalypse",
    "MagicOnly",
    "AlternateBloonsRounds",
    "DoubleMoabHealth",
    "HalfCash",
    "Impoppable",
    "Clicks"
]

mapDisplayNames = {
    "Tutorial": "Monkey Meadow",
    "InTheLoop": "In The Loop",
    "MiddleOfTheRoad": "Middle of The Road",
    "Tinkerton": "Tinkerton",
    "TreeStump": "Tree Stump",
    "TownCentre": "Town Center",
    "OneTwoTree": "One Two Tree",
    "Scrapyard": "Scrapyard",
    "TheCabin": "The Cabin",
    "Resort": "Resort",
    "Skates": "Skates",
    "LotusIsland": "Lotus Island",
    "CandyFalls": "Candy Falls",
    "WinterPark": "Winter Park",
    "Carved": "Carved",
    "ParkPath": "Park Path",
    "AlpineRun": "Alpine Run",
    "FrozenOver": "Frozen Over",
    "Cubism": "Cubism",
    "FourCircles": "Four Circles",
    "Hedge": "Hedge",
    "EndOfTheRoad": "End of The Road",
    "Logs": "Logs",
}
medalDisplayNames = [
    "Easy",
    "Medium",
    "Hard",
    "Primary Monkeys Only",
    "Deflation",
    "Military Monkeys Only",
    "Reverse",
    "Apopalypse",
    "Magic Monkeys Only",
    "Alternate Bloons Rounds",
    "Double HP Moabs",
    "Half Cash",
    "Impoppable",
    "Chimps"
]


class BloonsMedal(Location):
    game: str = "Bloons TD6"


class BloonsLocations:
    locations: List[str] = []
    location_groups = {
        "Medals": {},
        "Levels": {},
        "Heroes": {},
        "Knowledge": {}
    }

    def __init__(self, active_maps):
        for diff, map_list in maps:
            if diff in active_maps:
                for map in map_list:
                    for medal in medals:
                        check_name = f"{map}-{medal}"
                        self.locations.append(check_name)
                        self.location_groups.get("Medals")[check_name] = ""

        for i in range(149):
            self.locations.append(f"Level {i}")
            self.location_groups.get("Levels")[f"Level {i}"] = ""

        for hero in Shared.heroIDs:
            self.locations.append(f"{hero}")
            self.location_groups.get("Heroes")[f"{hero}"] = ""

        for name in Shared.knowledgeIDs:
            self.locations.append(f"{name}")
            self.location_groups.get("Knowledge")[f"{name}"] = ""
