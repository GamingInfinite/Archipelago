from typing import Dict, List, Optional
from BaseClasses import Item, ItemClassification
from worlds.bloonstd6.Locations import BloonsLocations
from .Utils import Shared


class BTD6MedalItem(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(
            name,
            ItemClassification.progression_skip_balancing,
            code,
            player,
        )


class BTD6MapUnlock(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)


class BTD6MonkeyUnlock(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)

class BTD6HeroUnlock(Item):
    game: str = "Bloons TD6"
    
    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)

class BTD6KnowledgeUnlock(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)


class BTD6FillerItem(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.filler, code, player)


class BloonsItems:
    MEDAL_NAME: str = "Medal"
    MEDAL_CODE: int = 1

    MONEY_NAME: str = "Monkey Money"
    MONEY_CODE: int = 2

    item_offset = 3

    items: Dict[str, int] = {}
    auto_item_groups: Dict[str, set] = {}

    monkeyIDs: List[str] = [
        "DartMonkey",
        "BoomerangMonkey",
        "BombShooter",
        "TackShooter",
        "IceMonkey",
        "GlueGunner",
        "SniperMonkey",
        "MonkeySub",
        "MonkeyBuccaneer",
        "MonkeyAce",
        "HeliPilot",
        "MortarMonkey",
        "DartlingGunner",
        "WizardMonkey",
        "SuperMonkey",
        "NinjaMonkey",
        "Alchemist",
        "Druid",
        "Mermonkey",
        "BananaFarm",
        "SpikeFactory",
        "MonkeyVillage",
        "EngineerMonkey",
        "BeastHandler",
    ]

    def __init__(self) -> None:
        mapdata = BloonsLocations()
        maplist = mapdata.get_maps()

        self.items[self.MEDAL_NAME] = self.MEDAL_CODE
        self.items[self.MONEY_NAME] = self.MONEY_CODE

        index = self.item_offset
        for name in maplist:
            self.items[f"{name}-MUnlock"] = index
            index += 1
        for name in self.monkeyIDs:
            self.items[f"{name}-TUnlock"] = index
            index += 1
        for name in Shared.heroIDs:
            self.items[f"{name}-HUnlock"] = index
            index += 1
        for name in Shared.knowledgeIDs:
            self.items[f"{name}-KUnlock"] = index
            index += 1

        self.auto_item_groups["maps"] = set(
            name for names in self.items.keys() if names.endswith("-MUnlock")
        )
        self.auto_item_groups["towers"] = set(
            name for names in self.items.keys() if names.endswith("-TUnlock")
        )
        self.auto_item_groups["knowledge"] = set(
            name for names in self.items.keys() if names.endswith("-KUnlock")
        )
