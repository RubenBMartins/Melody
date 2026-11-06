import pygame
from pathlib import Path

GAMEDIR = Path(__file__).parent.resolve()
ASSETSDIR = GAMEDIR / 'assets_ressources'

class Play(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.image.load(ASSETSDIR / "play1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()