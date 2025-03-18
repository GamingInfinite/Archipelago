from worlds.AutoWorld import World
from worlds.bloonstd6.items import BloonsItems
from worlds.bloonstd6.locations import BloonsLocations
from worlds.bloonstd6.options import BloonsGameOptions


class BTD6World(World):
    game = "Bloons TD6"
    options_dataclass = BloonsGameOptions
    options: BloonsGameOptions

    bloonsItemData = BloonsItems
    bloonsMapData = BloonsLocations(options.active_maps.value)

    base_id = 1



    location_name_to_id = {name: code for name, code in enumerate(bloonsMapData.locations, base_id)}
    location_name_groups = bloonsMapData.location_groups