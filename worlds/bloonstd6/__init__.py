from BaseClasses import Item, Region
from worlds.AutoWorld import World

from typing import Any, ClassVar, Dict, List, Type
from Options import PerGameCommonOptions

from .Options import BloonsTD6Options, Difficulty
from .Locations import BTD6Medal, BloonsLocations
from .Items import (
    BTD6FillerItem,
    BTD6LevelItem,
    BTD6MapUnlock,
    BTD6MedalItem,
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

    victory_map_name: str = ""
    starting_maps: List[str] = []
    included_maps: List[str] = []

    def generate_early(self) -> None:
        starting_map_count = self.options.starting_map_count.value
        total_map_count = self.options.total_maps.value

        print(starting_map_count)
        print(total_map_count)
        available_maps: List[str] = self.bloonsMapData.get_maps(
            self.options.min_map_diff.value, self.options.max_map_diff.value
        )

        self.random.shuffle(available_maps)
        self.victory_map_name = available_maps.pop()
        for _ in range(starting_map_count):
            self.starting_maps.append(available_maps.pop())

        for _ in range(total_map_count):
            if len(available_maps) == 0:
                break
            self.included_maps.append(available_maps.pop())

        for map in self.starting_maps:
            self.multiworld.push_precollected(self.create_item(map))

    def create_item(self, name: str) -> Item:
        if name == self.bloonsItemData.MEDAL_NAME:
            return BTD6MedalItem(name, self.bloonsItemData.MEDAL_CODE, self.player)

        # if name in BloonsItems.level_rewards:
        #     return BTD6LevelItem(name, self.player)

        if name == self.bloonsItemData.KNOWLEDGE_NAME:
            return BTD6FillerItem(name, self.bloonsItemData.KNOWLEDGE_CODE, self.player)

        map = self.bloonsItemData.items.get(f"{name}-Unlock")
        return BTD6MapUnlock(f"{name}-Unlock", map, self.player)
        # Remember to add Monkey Money later for future Hero Checks.

    def create_items(self) -> None:
        map_keys = self.included_maps.copy()

        for name in map_keys:
            self.multiworld.itempool.append(self.create_item(name))

        for _ in range(len(map_keys) * self.options.rando_difficulty.value):
            self.multiworld.itempool.append(self.create_item(BloonsItems.MEDAL_NAME))

        for _ in range(self.options.max_level):
            self.multiworld.itempool.append(
                self.create_item(BloonsItems.KNOWLEDGE_NAME)
            )

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        map_select_region = Region("Map Select", self.player, self.multiworld)
        xp_region = Region("XP Progression", self.player, self.multiworld)
        self.multiworld.regions += [menu_region, map_select_region, xp_region]
        menu_region.connect(map_select_region)
        menu_region.connect(xp_region)

        all_maps_copy = self.starting_maps.copy()
        incl_maps_copy = self.included_maps.copy()

        self.random.shuffle(incl_maps_copy)
        all_maps_copy.extend(incl_maps_copy)

        for i in range(len(all_maps_copy)):
            name: str
            name = all_maps_copy[i]

            region = Region(name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
            map_select_region.connect(
                region,
                name,
                lambda state, place=name + "-Unlock": state.has(place, self.player),
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

        for i in range(self.options.max_level.value):
            name: str = f"Level {i+1}"
            xp_region.add_locations({name: self.bloonsMapData.locations[name]})

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            BloonsItems.MEDAL_NAME,
            self.player,
            (len(self.starting_maps) + len(self.included_maps))
            * self.options.rando_difficulty.value
            * (self.options.medalreq.value / 100),
        )

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "victoryLocation": self.victory_map_name,
            "medalsNeeded": (len(self.starting_maps) + len(self.included_maps))
            * self.options.rando_difficulty.value
            * (self.options.medalreq.value / 100),
        }
