import os
import pygame.image
from Util.utilities import scale_image


class AssetDictionary:

    asset_dict = {}

    def __init__(self, current_dir):
        # Load sprites into a dictionary for easy reference
        self.asset_dict = {
            "frog": pygame.image.load(os.path.join(current_dir, "Assets", "frog.png")),
            "frog_jumping": pygame.image.load(os.path.join(current_dir, "Assets", "car-1.png")),
            "car1": pygame.image.load(os.path.join(current_dir, "Assets", "car-1.png")),
            "car2": pygame.image.load(os.path.join(current_dir, "Assets", "car-2.png")),
            "car3": pygame.image.load(os.path.join(current_dir, "Assets", "car-3.png")),
            "car4": pygame.image.load(os.path.join(current_dir, "Assets", "car-4.png")),
            "log-long": pygame.image.load(os.path.join(current_dir, "Assets", "log-long.png")),
            "log-short": pygame.image.load(os.path.join(current_dir, "Assets", "log-short.png")),
            "logo": pygame.image.load(os.path.join(current_dir, "Assets", "logo.png")),
            "semi-truck": pygame.image.load(os.path.join(current_dir, "Assets", "semi-truck.png")),
            "turtle-1": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-1.png")),
            "turtle-2": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-2.png")),
            "turtle-3": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-3.png")),
            "turtle-sink-1": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-sink-1.png")),
            "turtle-sink-2": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-sink-2.png")),
        }

        # Scale all the images in the asset dictionary
        for key in self.asset_dict:
            self.asset_dict[key] = scale_image(self.asset_dict[key])

    def get_asset(self, key):
        return self.asset_dict[key]
