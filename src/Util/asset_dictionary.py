import os
import pygame.image
from Util.utilities import scale_image


class AssetDictionary:

    def __init__(self, current_dir):
        # Load sprites into a dictionary for easy reference
        self.asset_dict = {
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

        # Scale all the images in the asset dictionary
        for key in self.asset_dict:
            self.asset_dict[key] = scale_image(self.asset_dict[key])

        self.asset_dict.update({
            "triple-turtle": [self.get_asset("turtle-1"), self.get_asset("turtle-2"), self.get_asset("turtle-3")],
            "double-turtle": [self.get_asset("double-turtle-1"), self.get_asset("double-turtle-2"),
                              self.get_asset("double-turtle-3")],
            "triple-turtle-sink": [self.get_asset("turtle-1"), self.get_asset("turtle-sink-1"),
                                   self.get_asset("turtle-sink-2"), self.get_asset("submerged-turtle")],
            "double-turtle-sink": [self.get_asset("double-turtle-1"), self.get_asset("double-turtle-sink-1"),
                                   self.get_asset("double-turtle-sink-2"), self.get_asset("submerged-turtle")]
        })

    def get_asset(self, key):
        return self.asset_dict[key]
