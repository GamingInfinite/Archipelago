from typing import Dict, NamedTuple, Optional
from BaseClasses import Location

class MapData(NamedTuple):
    code: Optional[int]

class BTD6Medal(Location):
    game: str = "Bloons TD6"

class BTD6Level(Location):
    game: str = "Bloons TD6"

class BloonsLocations:
    locations = {}

    map_names_by_difficulty: Dict[str, list] = {
        "beginner": ["Monkey Meadow", "In The Loop", "Middle of the Road", "Tree Stump", "Town Center", "One Two Tree",
                     "Scrapyard", "The Cabin", "Resort", "Skates", "Lotus Island", "Candy Falls",
                     "Winter Park", "Carved", "Park Path", "Alpine Run", "Frozen Over", "Cubism",
                     "Four Circles", "Hedge", "End of the Road", "Logs"],
        "intermediate": ["Water Park", "Polyphemus", "Covered Garden", "Quarry", "Quiet Street", "Bloonarius Prime",
                         "Balance", "Encrypted", "Bazaar", "Adora's Temple", "Spring Spring", "KartsNDarts",
                         "Moon Landing", "Haunted", "Downstream", "Firing Range", "Cracked", "Streambed",
                         "Chutes", "Rake", "Spice Islands"],
        "advanced": ["Dark Path", "Erosion", "Midnight Mansion", "Sunken Columns", "X Factor", "Mesa",
                     "Geared", "Spillway", "Cargo", "Pat's Pond", "Peninsula", "High Finance",
                     "Another Brick", "Off the Coast", "Cornfield", "Underground"],
        "expert": ["Glacial Trail", "Dark Dungeons", "Sanctuary", "Ravine", "Flooded Valley", "Infernal",
                   "Bloody Puddles", "Workshop", "Quad", "Dark Castle", "Muddy Puddles", "#Ouch"]
    }

    levels_by_reward = ["Boomerang Monkey", "Bomb Shooter", "Tack Shooter", "Ice Monkey", "Glue Gunner",
                        "Sniper Monkey", "Monkey Sub", "Monkey Buccaneer", "Monkey Ace", "Mortar Monkey",
                        "Gwendolin", 
                        "Wizard Monkey", "Super Monkey", "Ninja Monkey", "Alchemist", "Druid",
                        "Striker Jones",
                        "Banana Farm", "Spike Factory", "Monkey Village", "Engineer Monkey",
                        "Obyn Greenfoot"]
    
    def __init__(self) -> None:
        index = 0

        for diff in self.map_names_by_difficulty:
            for name in diff:
                self.locations[f"{name}-0"] = index
                self.locations[f"{name}-0"] = index
                index += 1
        
        for reward in self.levels_by_reward:
            self.locations[reward] = index
            index += 1