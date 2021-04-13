import os
import pygame.image
from Util.utilities import scale_image

current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class AssetDictionary:
    """A static class used for easily accessing the game's assets from any file in the project. Assets are stored
    as a Python dictionary. When an asset is needed, it should be accessed by the static `get_asset()` method."""

    # Load assets into a static dictionary for easy reference
    asset_dict = {
        "frog": pygame.image.load(os.path.join(current_dir, "Assets/Images", "frog.png")),
        "frog_jumping": pygame.image.load(os.path.join(current_dir, "Assets/Images", "frog_jumping.png")),
        "car1": pygame.image.load(os.path.join(current_dir, "Assets/Images", "car-1.png")),
        "car2": pygame.image.load(os.path.join(current_dir, "Assets/Images", "car-2.png")),
        "car3": pygame.image.load(os.path.join(current_dir, "Assets/Images", "car-3.png")),
        "car4": pygame.image.load(os.path.join(current_dir, "Assets/Images", "car-4.png")),
        "log-long": pygame.image.load(os.path.join(current_dir, "Assets/Images", "log-long.png")),
        "log-medium": pygame.image.load(os.path.join(current_dir, "Assets/Images", "log-medium.png")),
        "log-short": pygame.image.load(os.path.join(current_dir, "Assets/Images", "log-short.png")),
        "logo": pygame.image.load(os.path.join(current_dir, "Assets/Images", "logo.png")),
        "semi-truck": pygame.image.load(os.path.join(current_dir, "Assets/Images", "semi-truck.png")),
        "turtle-1": pygame.image.load(os.path.join(current_dir, "Assets/Images", "turtle-1.png")),
        "turtle-2": pygame.image.load(os.path.join(current_dir, "Assets/Images", "turtle-2.png")),
        "turtle-3": pygame.image.load(os.path.join(current_dir, "Assets/Images", "turtle-3.png")),
        "double-turtle-1": pygame.image.load(os.path.join(current_dir, "Assets/Images", "double-turtle-1.png")),
        "double-turtle-2": pygame.image.load(os.path.join(current_dir, "Assets/Images", "double-turtle-2.png")),
        "double-turtle-3": pygame.image.load(os.path.join(current_dir, "Assets/Images", "double-turtle-3.png")),
        "double-turtle-sink-1": pygame.image.load(os.path.join(current_dir, "Assets/Images", "double-turtle-sink-1.png")),
        "double-turtle-sink-2": pygame.image.load(os.path.join(current_dir, "Assets/Images", "double-turtle-sink-2.png")),
        "turtle-sink-1": pygame.image.load(os.path.join(current_dir, "Assets/Images", "turtle-sink-1.png")),
        "turtle-sink-2": pygame.image.load(os.path.join(current_dir, "Assets/Images", "turtle-sink-2.png")),
        "submerged-turtle": pygame.image.load(os.path.join(current_dir, "Assets/Images", "blank-triple-turtle.png")),
        "win-frog": pygame.image.load(os.path.join(current_dir, "Assets/Images", "win-frog.png")),
    }

    for key in asset_dict:
        asset_dict[key] = scale_image(asset_dict[key])

    asset_dict.update({
        "triple-turtle": [asset_dict["turtle-1"], asset_dict["turtle-2"], asset_dict["turtle-3"]],
        "double-turtle": [asset_dict["double-turtle-1"], asset_dict["double-turtle-2"],
                          asset_dict["double-turtle-3"]],
        "triple-turtle-sink": [asset_dict["turtle-1"], asset_dict["turtle-sink-1"],
                               asset_dict["turtle-sink-2"], asset_dict["submerged-turtle"]],
        "double-turtle-sink": [asset_dict["double-turtle-1"], asset_dict["double-turtle-sink-1"],
                               asset_dict["double-turtle-sink-2"], asset_dict["submerged-turtle"]],
        "player": [asset_dict["frog"], asset_dict["frog_jumping"]]
    })

    def __init__(self):
        return

    @classmethod
    def get_asset(cls, key):
        """Returns the asset requested by the dictionary key passed to the method."""
        return cls.asset_dict[key]
