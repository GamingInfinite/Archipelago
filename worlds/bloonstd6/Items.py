from typing import Optional
from BaseClasses import Item, ItemClassification
from .Utils import Utils


class BTD6MedalItem(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, player: int):
        super().__init__(
            name,
            ItemClassification.progression_skip_balancing,
            BloonsItems.MEDAL_CODE,
            player,
        )


class BTD6MapUnlock(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.progression, code, player)


class BTD6LevelItem(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, player: int):
        super().__init__(
            name,
            ItemClassification.useful,
            BloonsItems.level_rewards.index(name) + BloonsItems.item_offset,
            player,
        )


class BTD6FillerItem(Item):
    game: str = "Bloons TD6"

    def __init__(self, name: str, code: Optional[int], player: int):
        super().__init__(name, ItemClassification.filler, code, player)


class BloonsItems:
    MEDAL_NAME: str = "Medal"
    MEDAL_CODE: int = 0

    KNOWLEDGE_NAME: str = "Monkey Knowledge"
    KNOWLEDGE_CODE: int = 1

    item_offset = 2 + Utils.BASE_OFFSET

    level_rewards = [
        "Boomerang Monkey",
        "Bomb Shooter",
        "Tack Shooter",
        "Ice Monkey",
        "Glue Gunner",
        "Sniper Monkey",
        "Monkey Sub",
        "Monkey Buccaneer",
        "Monkey Ace",
        "Mortar Monkey",
        "Gwendolin",
        "Wizard Monkey",
        "Super Monkey",
        "Ninja Monkey",
        "Alchemist",
        "Druid",
        "Striker Jones",
        "Banana Farm",
        "Spike Factory",
        "Monkey Village",
        "Engineer Monkey",
        "Obyn Greenfoot",
    ]
