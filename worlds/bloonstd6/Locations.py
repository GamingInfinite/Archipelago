from typing import Dict, List, NamedTuple, Optional
from BaseClasses import Location, Region
from .Utils import Utils


class MapData(NamedTuple):
    code: Optional[int]


class BTD6Medal(Location):
    game: str = "Bloons TD6"

    def __init__(
        self,
        player: int,
        name: str = "",
        code: int | None = None,
        parent: Region | None = None,
    ):
        super().__init__(player, name, code, parent)


class BTD6Level(Location):
    game: str = "Bloons TD6"


class BloonsLocations:
    locations = {}

    map_names_by_difficulty: Dict[str, List[str]] = {
        "beginner": [
            "Tutorial",
            "InTheLoop",
            "MiddleOfTheRoad",
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
        ],
        "intermediate": [
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
        ],
        "advanced": [
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
        ],
        "expert": [
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
        ],
    }

    def __init__(self) -> None:
        index = 70 + Utils.BaseOffset

        for diff in self.map_names_by_difficulty:
            for name in diff:
                self.locations[f"{name}-Easy"] = index
                self.locations[f"{name}-PrimaryOnly"] = index + 1
                self.locations[f"{name}-Deflation"] = index + 2
                self.locations[f"{name}-Medium"] = index + 3
                self.locations[f"{name}-MilitaryOnly"] = index + 4
                self.locations[f"{name}-Apopalypse"] = index + 5
                self.locations[f"{name}-Reverse"] = index + 6
                self.locations[f"{name}-Hard"] = index + 7
                self.locations[f"{name}-MagicOnly"] = index + 8
                self.locations[f"{name}-DoubleMoabHealth"] = index + 9
                self.locations[f"{name}-HalfCash"] = index + 10
                self.locations[f"{name}-AlternateBloonRounds"] = index + 11
                self.locations[f"{name}-Impoppable"] = index + 12
                self.locations[f"{name}-Clicks"] = index + 13
                self.locations[f"{name}-Unlock"] = index + 14
                index += 15

    def get_maps(self, minDiff, maxDiff) -> List[str]:
        """List all Map IDs within the difficulties that can be played."""
        filtered_list: List[str] = []

        index = 0

        for diff, list in self.map_names_by_difficulty.items():
            if index > minDiff and index < maxDiff:
                continue
            filtered_list.extend(list)
            index += 1

        return filtered_list

    def get_map_code(self, name):
        return self.locations[name + "-Unlock"]
