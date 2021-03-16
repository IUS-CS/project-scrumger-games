import os
import pygame.image
from Util.utilities import scale_image

current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class AssetDictionary:

    # Load assets into a static dictionary for easy reference
    asset_dict = {
        "frog": pygame.image.load(os.path.join(current_dir, "Assets", "frog.png")),
        "frog_jumping": pygame.image.load(os.path.join(current_dir, "Assets", "frog_jumping.png")),
        "car1": pygame.image.load(os.path.join(current_dir, "Assets", "car-1.png")),
        "car2": pygame.image.load(os.path.join(current_dir, "Assets", "car-2.png")),
        "car3": pygame.image.load(os.path.join(current_dir, "Assets", "car-3.png")),
        "car4": pygame.image.load(os.path.join(current_dir, "Assets", "car-4.png")),
        "log-long": pygame.image.load(os.path.join(current_dir, "Assets", "log-long.png")),
        "log-medium": pygame.image.load(os.path.join(current_dir, "Assets", "log-medium.png")),
        "log-short": pygame.image.load(os.path.join(current_dir, "Assets", "log-short.png")),
        "logo": pygame.image.load(os.path.join(current_dir, "Assets", "logo.png")),
        "semi-truck": pygame.image.load(os.path.join(current_dir, "Assets", "semi-truck.png")),
        "turtle-1": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-1.png")),
        "turtle-2": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-2.png")),
        "turtle-3": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-3.png")),
        "double-turtle-1": pygame.image.load(os.path.join(current_dir, "Assets", "double-turtle-1.png")),
        "double-turtle-2": pygame.image.load(os.path.join(current_dir, "Assets", "double-turtle-2.png")),
        "double-turtle-3": pygame.image.load(os.path.join(current_dir, "Assets", "double-turtle-3.png")),
        "double-turtle-sink-1": pygame.image.load(os.path.join(current_dir, "Assets", "double-turtle-sink-1.png")),
        "double-turtle-sink-2": pygame.image.load(os.path.join(current_dir, "Assets", "double-turtle-sink-2.png")),
        "turtle-sink-1": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-sink-1.png")),
        "turtle-sink-2": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-sink-2.png")),
        "submerged-turtle": pygame.image.load(os.path.join(current_dir, "Assets", "blank-triple-turtle.png")),
        "win-frog": pygame.image.load(os.path.join(current_dir, "Assets", "win-frog.png")),
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
        return cls.asset_dict[key]
