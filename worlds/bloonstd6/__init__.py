from worlds.AutoWorld import World

from typing import ClassVar, Type
from Options import PerGameCommonOptions

from .Options import BloonsTD6Options
from .Locations import BloonsLocations

class BTD6World(World):
    """Bloons TD6 is a tower defense game about Monkeys trying to defend themselves against the Balloon onslaught.  
    Play a random assortment of maps to collect medals until you can complete the goal map."""

    #World Options
    game = "Bloons TD6"
    options_dataclass: ClassVar[Type[PerGameCommonOptions]]
    options: BloonsTD6Options

    bloonsData = BloonsLocations()

    location_name_to_id = {name: code for name, code in bloonsData.locations}

    

    def create_regions(self) -> None:
        return super().create_regions()