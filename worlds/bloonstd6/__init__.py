import math
from BaseClasses import Item, Region
from worlds.AutoWorld import World

from typing import Any, ClassVar, Dict, List, Type
from Options import PerGameCommonOptions
from worlds.generic.Rules import set_rule

from .Options import BloonsTD6Options, Difficulty
from .Locations import BTD6Medal, BloonsLocations
from .Items import (
    BTD6FillerItem,
    BTD6KnowledgeUnlock,
    BTD6MapUnlock,
    BTD6MedalItem,
    BTD6MonkeyUnlock,
    BloonsItems,
)


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

        map = self.bloonsItemData.items.get(f"{name}-MUnlock")
        monkey = self.bloonsItemData.items.get(f"{name}-TUnlock")
        knowledge = self.bloonsItemData.items.get(f"{name}-KUnlock")
        if map:
            return BTD6MapUnlock(f"{name}-MUnlock", map, self.player)
        elif knowledge:
            return BTD6KnowledgeUnlock(f"{name}-KUnlock", map, self.player)
        return BTD6MonkeyUnlock(f"{name}-TUnlock", monkey, self.player)
        # Remember to add Monkey Money later for future Hero Checks.

    def create_items(self) -> None:
        map_keys = self.included_maps.copy()
        all_map_keys: List[str] = map_keys.copy()
        all_map_keys.extend(self.starting_maps.copy())

        total_items = len(self.multiworld.get_unfilled_locations(self.player))

        for name in map_keys:
            self.multiworld.itempool.append(self.create_item(name))
            total_items -= 1

        for _ in range(len(all_map_keys) * self.options.rando_difficulty.value):
            self.multiworld.itempool.append(self.create_item(BloonsItems.MEDAL_NAME))
            total_items -= 1

        for monkey in self.remaining_monkeys:
            self.multiworld.itempool.append(self.create_item(monkey))
            total_items -= 1

        for knowledge in BloonsItems.knowledgeIDs:
            self.multiworld.itempool.append(self.create_item(f"{knowledge}-KUnlock"))
            total_items -= 1

    def create_regions(self) -> None:
        # Define all main regions
        menu_region = Region("Menu", self.player, self.multiworld)
        map_select_region = Region("Map Select", self.player, self.multiworld)
        xp_region = Region("XP Progression", self.player, self.multiworld)
        knowledge_region = Region("Knowledge Tree", self.player, self.multiworld)

        #Add all the main regions to the multiworld
        self.multiworld.regions += [
            menu_region,
            map_select_region,
            xp_region,
            knowledge_region,
        ]

        #Connect the regions to Menu (Menu is the only required region in Archipelago)
        menu_region.connect(map_select_region)
        menu_region.connect(xp_region)
        menu_region.connect(knowledge_region)

        all_maps_copy = self.starting_maps.copy()
        incl_maps_copy = self.included_maps.copy()

        self.random.shuffle(incl_maps_copy)
        all_maps_copy.extend(incl_maps_copy)

        #Locations and regions for maps
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
                        + "-AlternateBloonRounds": self.bloonsMapData.locations[
                            name + "-AlternateBloonRounds"
                        ],
                    },
                    BTD6Medal,
                )

        #Locations for Level ups
        for i in range(self.options.max_level.value - 1):
            name: str = f"Level {i+2}"
            xp_region.add_locations({name: self.bloonsMapData.locations[name]})

        #Knowledge Specific Regions and Locations

        primary_region = Region("Primary Knowledge", self.player, self.multiworld)
        military_region = Region("Military Knowledge", self.player, self.multiworld)
        magic_region = Region("Magic Knowledge", self.player, self.multiworld)
        support_region = Region("Support Knowledge", self.player, self.multiworld)
        heroes_region = Region("Hero Knowledge", self.player, self.multiworld)
        powers_region = Region("Powers Region", self.player, self.multiworld)

        self.multiworld.regions += [primary_region, military_region, magic_region, support_region, heroes_region, powers_region]
        knowledge_region.connect(primary_region)
        knowledge_region.connect(military_region)
        knowledge_region.connect(magic_region)
        knowledge_region.connect(support_region)
        knowledge_region.connect(heroes_region)
        knowledge_region.connect(powers_region)

        knowledge_regions: List[Region] = []
        for i in range(len(BloonsItems.knowledgeIDs)):
            region = Region(BloonsItems.knowledgeIDs[i], self.player, self.multiworld)
            region.add_locations(BloonsItems.knowledgeIDs[i])
            knowledge_regions.append(region)
        


        self.multiworld.regions += knowledge_regions

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
