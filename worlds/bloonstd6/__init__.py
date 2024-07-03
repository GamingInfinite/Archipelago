import math
from BaseClasses import Item, Region
from Utils import visualize_regions
from worlds.AutoWorld import World

from typing import Any, ClassVar, Dict, List, Type
from Options import PerGameCommonOptions
from worlds.generic.Rules import set_rule

from .Options import BloonsTD6Options, Difficulty
from .Locations import BTD6Knowledge, BTD6Map, BTD6Medal, BloonsLocations
from .Items import (
    BTD6FillerItem,
    BTD6KnowledgeUnlock,
    BTD6MapUnlock,
    BTD6MedalItem,
    BTD6MonkeyUnlock,
    BloonsItems,
)
from .Utils import Shared


class BTD6World(World):
    """
    Bloons TD6 is a tower defense game about Monkeys trying to defend themselves against the Balloon onslaught.
    Play a random assortment of maps to collect medals until you can complete the goal map.
    """

    # World Options
    game = "Bloons TD6"
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = BloonsTD6Options
    options: BloonsTD6Options

    bloonsMapData = BloonsLocations()
    bloonsItemData = BloonsItems()

    item_name_to_id = {name: code for name, code in bloonsItemData.items.items()}
    location_name_to_id = {name: code for name, code in bloonsMapData.locations.items()}

    def generate_early(self) -> None:
        ## Initialize per-player instances of variables:
        self.starting_maps: List[str] = []
        self.included_maps: List[str] = []

        self.starting_monkeys: List[str] = []
        self.remaining_monkeys: List[str] = []

        ## Handle selection of maps for locations
        available_maps: List[str] = self.bloonsMapData.get_maps(
            self.options.min_map_diff.value, self.options.max_map_diff.value
        )
        self.random.shuffle(available_maps)

        # Select Victory Map
        self.victory_map_name = available_maps.pop()

        # Select and initialize starting maps
        for _ in range(self.options.starting_map_count.value):
            self.starting_maps.append(available_maps.pop())

        for map in self.starting_maps:
            self.multiworld.push_precollected(self.create_item(map))

        # Select unlockable maps for item checks
        for _ in range(self.options.total_maps.value):
            if len(available_maps) == 0:
                break
            self.included_maps.append(available_maps.pop())

        ## Handle start of game initialization for monkey towers
        available_towers: List[str] = self.bloonsItemData.monkeyIDs.copy()

        # Sets starting monkey to Dart Monkey or randomizes it based on options
        if not self.options.starting_monkey.value:
            self.starting_monkeys.append(available_towers.pop(0))
            self.random.shuffle(available_towers)
        else:
            self.random.shuffle(available_towers)
            self.starting_monkeys.append(available_towers.pop())

        # Adds additional starting monkeys based on options
        for _ in range(self.options.num_start_monkey.value - 1):
            self.starting_monkeys.append(available_towers.pop())

        for monkey in self.starting_monkeys:
            self.multiworld.push_precollected(self.create_item(monkey))

        # Put the rest of the monkeys into storage for item generation
        self.remaining_monkeys.extend(available_towers)

    def create_item(self, name: str) -> Item:
        if name == self.bloonsItemData.MEDAL_NAME:
            return BTD6MedalItem(name, self.bloonsItemData.MEDAL_CODE, self.player)

        if name == self.bloonsItemData.MONEY_NAME:
            return BTD6FillerItem(name, self.bloonsItemData.MONEY_CODE, self.player)

        map = self.bloonsItemData.items.get(f"{name}-MUnlock")
        monkey = self.bloonsItemData.items.get(f"{name}-TUnlock")
        knowledge = self.bloonsItemData.items.get(f"{name}-KUnlock")
        if map:
            return BTD6MapUnlock(f"{name}-MUnlock", map, self.player)
        if knowledge:
            return BTD6KnowledgeUnlock(f"{name}-KUnlock", knowledge, self.player)
        return BTD6MonkeyUnlock(f"{name}-TUnlock", monkey, self.player)
        # Remember to add Monkey Money later for future Hero Checks.

    def create_items(self) -> None:
        map_keys = self.included_maps.copy()
        all_map_keys: List[str] = map_keys.copy()
        all_map_keys.extend(self.starting_maps.copy())

        item_count = 0

        for name in map_keys:
            self.multiworld.itempool.append(self.create_item(name))
            item_count += 1

        for _ in range(len(all_map_keys) * self.options.rando_difficulty.value):
            self.multiworld.itempool.append(self.create_item(BloonsItems.MEDAL_NAME))
            item_count += 1

        for monkey in self.remaining_monkeys:
            self.multiworld.itempool.append(self.create_item(monkey))
            item_count += 1

        for knowledge in Shared.knowledgeIDs:
            self.multiworld.itempool.append(self.create_item(knowledge))
            item_count += 1

        filler_items = len(self.multiworld.get_unfilled_locations(self.player)) - item_count
        for _ in range(filler_items):
            self.multiworld.itempool.append(self.create_item(BloonsItems.MONEY_NAME))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        map_select_region = Region("Map Select", self.player, self.multiworld)
        xp_region = Region("XP Progression", self.player, self.multiworld)
        knowledge_region = Region("Knowledge Tree", self.player, self.multiworld)
        self.multiworld.regions += [
            menu_region,
            map_select_region,
            xp_region,
            knowledge_region,
        ]
        menu_region.connect(map_select_region)
        menu_region.connect(xp_region)
        menu_region.connect(knowledge_region)

        all_maps_copy = self.starting_maps.copy()
        incl_maps_copy = self.included_maps.copy()

        self.random.shuffle(incl_maps_copy)
        all_maps_copy.extend(incl_maps_copy)

        # region Map Locations
        for i in range(len(all_maps_copy)):
            name: str
            name = all_maps_copy[i]

            region = Region(name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
            map_select_region.connect(
                region,
                name,
                lambda state, place=name + "-MUnlock": state.has(place, self.player),
            )
            region.add_locations(
                {
                    name + "-Unlock": self.bloonsMapData.locations[name + "-Unlock"],
                },
                BTD6Map,
            )

            # Handle Mode Based Checks
            region.add_locations(
                {
                    name + "-Easy": self.bloonsMapData.locations[name + "-Easy"],
                    name + "-Medium": self.bloonsMapData.locations[name + "-Medium"],
                    name + "-Hard": self.bloonsMapData.locations[name + "-Hard"],
                    name
                    + "-Impoppable": self.bloonsMapData.locations[name + "-Impoppable"],
                },
                BTD6Medal,
            )
            if self.options.rando_difficulty.value >= Difficulty.option_Advanced:
                region.add_locations(
                    {name + "-Clicks": self.bloonsMapData.locations[name + "-Clicks"]},
                    BTD6Medal,
                )
            if self.options.rando_difficulty.value == Difficulty.option_Expert:
                region.add_locations(
                    {
                        name
                        + "-PrimaryOnly": self.bloonsMapData.locations[
                            name + "-PrimaryOnly"
                        ],
                        name
                        + "-Deflation": self.bloonsMapData.locations[
                            name + "-Deflation"
                        ],
                        name
                        + "-MilitaryOnly": self.bloonsMapData.locations[
                            name + "-MilitaryOnly"
                        ],
                        name
                        + "-Apopalypse": self.bloonsMapData.locations[
                            name + "-Apopalypse"
                        ],
                        name
                        + "-Reverse": self.bloonsMapData.locations[name + "-Reverse"],
                        name
                        + "-MagicOnly": self.bloonsMapData.locations[
                            name + "-MagicOnly"
                        ],
                        name
                        + "-DoubleMoabHealth": self.bloonsMapData.locations[
                            name + "-DoubleMoabHealth"
                        ],
                        name
                        + "-HalfCash": self.bloonsMapData.locations[name + "-HalfCash"],
                        name
                        + "-AlternateBloonsRounds": self.bloonsMapData.locations[
                            name + "-AlternateBloonsRounds"
                        ],
                    },
                    BTD6Medal,
                )
        # endregion

        # region Level Locations
        for i in range(self.options.max_level.value - 1):
            name: str = f"Level {i+2}"
            xp_region.add_locations({name: self.bloonsMapData.locations[name]})
        # endregion

        # Knowledge Specific Regions and Locations
        # region Create K Categories
        primary_region = Region("Primary Knowledge", self.player, self.multiworld)
        military_region = Region("Military Knowledge", self.player, self.multiworld)
        magic_region = Region("Magic Knowledge", self.player, self.multiworld)
        support_region = Region("Support Knowledge", self.player, self.multiworld)
        heroes_region = Region("Hero Knowledge", self.player, self.multiworld)
        powers_region = Region("Powers Region", self.player, self.multiworld)

        self.multiworld.regions += [
            primary_region,
            military_region,
            magic_region,
            support_region,
            heroes_region,
            powers_region,
        ]

        knowledge_region.connect(primary_region)
        knowledge_region.connect(military_region)
        knowledge_region.connect(magic_region)
        knowledge_region.connect(support_region)
        knowledge_region.connect(heroes_region)
        knowledge_region.connect(powers_region)
        # endregion

        # region Create K Locations for Logic
        knowledge_regions: List[Region] = []
        for name in Shared.knowledgeIDs:
            region = Region(name, self.player, self.multiworld)
            region.add_locations(
                {
                    name + "-Tree": self.bloonsMapData.locations[f"{name}-Tree"],
                },
                BTD6Knowledge,
            )
            knowledge_regions.append(region)
        # endregion

        self.multiworld.regions += knowledge_regions

        def knowledge_connection(parent_region: Region | int, knowledge_id: int):
            if type(parent_region) is int:
                region = knowledge_regions[parent_region]
                region.connect(
                    knowledge_regions[knowledge_id],
                    rule=lambda state, place=Shared.knowledgeIDs[
                        knowledge_id
                    ] + "-KUnlock": state.has(place, self.player),
                )
            else:
                region: Region = parent_region
                region.connect(
                    knowledge_regions[knowledge_id],
                    rule=lambda state, place=Shared.knowledgeIDs[
                        knowledge_id
                    ] + "-KUnlock": state.has(place, self.player),
                )

        # region K. Tree Logic
        # region Primary
        # Primary Layer 1
        knowledge_connection(primary_region, 0)  # Fast Tack Attacks
        knowledge_connection(primary_region, 1)  # Increased Lifespan
        knowledge_connection(primary_region, 2)  # Extra Dart Pops
        # Primary Layer 2
        knowledge_connection(0, 4)  # Hard Tacks
        knowledge_connection(4, 3)  # Poppy Blades
        knowledge_connection(0, 5)
        knowledge_connection(1, 6)
        knowledge_connection(1, 7)
        knowledge_connection(2, 8)
        # Primary Layer 3
        knowledge_connection(3, 9)
        knowledge_connection(4, 10)
        knowledge_connection(5, 11)
        knowledge_connection(6, 12)
        knowledge_connection(7, 13)
        knowledge_connection(13, 16)
        knowledge_connection(8, 14)
        knowledge_connection(8, 15)
        # Primary Layer 4
        knowledge_connection(10, 17)
        knowledge_connection(11, 18)
        knowledge_connection(13, 19)
        knowledge_connection(14, 20)
        # region Mega Mauler
        knowledge_connection(18, 21)
        knowledge_connection(19, 21)
        # endregion
        # Primary Layer 5
        knowledge_connection(17, 22)
        knowledge_connection(17, 23)
        knowledge_connection(18, 24)
        knowledge_connection(12, 25)
        knowledge_connection(19, 26)
        knowledge_connection(26, 28)
        knowledge_connection(20, 27)
        # Primary Layer 6
        knowledge_connection(24, 29)
        knowledge_connection(27, 30)
        # region More Cash
        knowledge_connection(29, 31)
        knowledge_connection(30, 31)
        # endregion
        # endregion
        # region Military
        # Military Layer 1
        knowledge_connection(military_region, 32)
        knowledge_connection(military_region, 33)
        knowledge_connection(military_region, 34)
        knowledge_connection(military_region, 35)
        # Military Layer 2
        knowledge_connection(32, 36)
        knowledge_connection(33, 37)
        knowledge_connection(34, 38)
        # Military Layer 3
        knowledge_connection(military_region, 39)
        knowledge_connection(32, 40)
        knowledge_connection(36, 41)
        knowledge_connection(37, 42)
        knowledge_connection(33, 43)
        knowledge_connection(38, 44)
        knowledge_connection(35, 45)
        # Military Layer 4
        knowledge_connection(40, 46)
        knowledge_connection(41, 47)
        knowledge_connection(42, 48)
        knowledge_connection(39, 49)
        knowledge_connection(45, 50)
        # Military Layer 5
        # region Flanking Maneuvers
        knowledge_connection(46, 56)
        knowledge_connection(47, 56)
        # endregion
        knowledge_connection(48, 52)
        knowledge_connection(52, 55)
        knowledge_connection(43, 51)
        knowledge_connection(49, 54)
        knowledge_connection(44, 53)
        # Military Layer 6
        knowledge_connection(56, 57)
        knowledge_connection(47, 58)
        knowledge_connection(51, 59)
        # region Advanced Logistics
        knowledge_connection(59, 60)
        knowledge_connection(52, 60)
        # endregion
        # Military Layer 7
        # region Big Bloon Sabotage
        knowledge_connection(57, 61)
        knowledge_connection(53, 61)
        # endregion
        # endregion
        # region Magic
        # Magic Layer 1
        knowledge_connection(magic_region, 62)
        knowledge_connection(magic_region, 64)
        knowledge_connection(magic_region, 63)
        # Magic Layer 2
        knowledge_connection(62, 65)
        knowledge_connection(62, 66)
        knowledge_connection(64, 67)
        knowledge_connection(63, 68)
        knowledge_connection(68, 69)
        # Magic Layer 3
        knowledge_connection(65, 70)
        knowledge_connection(66, 71)
        knowledge_connection(67, 72)
        knowledge_connection(68, 73)
        # region Flame Jet
        knowledge_connection(67, 78)
        knowledge_connection(63, 78)
        # endregion
        # Magic Layer 4
        knowledge_connection(71, 74)
        knowledge_connection(72, 77)
        knowledge_connection(73, 76)
        knowledge_connection(78, 75)
        # Magic Layer 5
        knowledge_connection(77, 81)
        knowledge_connection(74, 80)
        knowledge_connection(70, 79)
        # Magic Layer 6
        # region Tiny Tornadoes
        knowledge_connection(79, 83)
        knowledge_connection(81, 83)
        # endregion
        knowledge_connection(75, 82)
        # endregion
        # region Support
        # Support Layer 1
        knowledge_connection(support_region, 84)
        knowledge_connection(support_region, 85)
        # Support Layer 2
        knowledge_connection(84, 86)
        knowledge_connection(84, 87)
        knowledge_connection(85, 88)
        # Support Layer 3
        knowledge_connection(86, 90)
        knowledge_connection(87, 91)
        knowledge_connection(85, 92)
        knowledge_connection(support_region, 89)
        # Support Layer 4
        knowledge_connection(90, 94)
        knowledge_connection(91, 95)
        knowledge_connection(92, 97)
        knowledge_connection(88, 93)
        knowledge_connection(89, 96)
        # Support Layer 5
        knowledge_connection(94, 98)
        knowledge_connection(95, 103)
        knowledge_connection(97, 102)
        knowledge_connection(93, 99)
        knowledge_connection(96, 100)
        knowledge_connection(96, 101)
        # Support Layer 6
        knowledge_connection(98, 104)
        knowledge_connection(100, 105)
        # endregion
        # region Heroes
        # Heroes Layer 1
        knowledge_connection(heroes_region, 106)
        knowledge_connection(heroes_region, 107)
        knowledge_connection(heroes_region, 108)
        # Heroes Layer 2
        knowledge_connection(106, 109)
        knowledge_connection(107, 110)
        # Heroes Layer 3
        knowledge_connection(109, 111)
        knowledge_connection(110, 112)
        knowledge_connection(108, 113)
        # Heroes Layer 4
        # region Hero Favors
        knowledge_connection(111, 114)
        knowledge_connection(112, 114)
        # endregion
        # Heroes Layer 5
        knowledge_connection(114, 115)
        knowledge_connection(113, 116)
        # Heroes Layer 6
        knowledge_connection(115, 117)
        knowledge_connection(116, 118)
        # endregion
        # region Powers
        # Powers Layer 1
        knowledge_connection(powers_region, 119)
        knowledge_connection(powers_region, 120)
        knowledge_connection(powers_region, 121)
        # Powers Layer 2
        knowledge_connection(119, 122)
        knowledge_connection(120, 123)
        knowledge_connection(121, 124)
        # Powers Layer 3
        knowledge_connection(122, 125)
        knowledge_connection(123, 126)
        # region Powerful Monkey Storm
        knowledge_connection(124, 132)
        knowledge_connection(126, 132)
        # endregion
        # Powers Layer 4
        knowledge_connection(125, 129)
        knowledge_connection(126, 127)
        knowledge_connection(132, 128)
        # Powers Layer 5
        knowledge_connection(128, 130)
        knowledge_connection(128, 131)
        # Powers Layer 6
        knowledge_connection(130, 133)
        # endregion
        # endregion

        # visualize_regions(
        #     self.multiworld.get_region("Menu", self.player),
        #     "output/regionmap.puml",
        # )

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            BloonsItems.MEDAL_NAME,
            self.player,
            int(
                round(
                    (len(self.starting_maps) + len(self.included_maps))
                    * self.options.rando_difficulty.value
                    * (self.options.medalreq.value / 100)
                )
            ),
        )

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "victoryLocation": self.victory_map_name,
            "medalsNeeded": int(
                round(
                    (len(self.starting_maps) + len(self.included_maps))
                    * self.options.rando_difficulty.value
                    * (self.options.medalreq.value / 100)
                )
            ),
            "xpCurve": bool(self.options.xp_curve.value),
            "staticXPReq": int(self.options.static_req.value),
            "maxLevel": int(self.options.max_level.value),
            "difficulty": int(self.options.rando_difficulty.value),
        }
