import random
import sys
import os
import io
import pygame
import eyed3
from pathlib import Path
from pygame._sdl2 import Window
GAMEDIR = Path(__file__).parent.resolve() # Resolve is to clean up the path
ASSETSDIR = GAMEDIR / 'assets_ressources'
MUSDIR = GAMEDIR / 'temp_musdir'
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
# Start windowed, then maximize cleanly
screen = pygame.display.set_mode((1920, 1040), pygame.RESIZABLE)
Window.from_display_module().maximize()
pygame.display.set_caption('Melody')
clock = pygame.time.Clock()
font = pygame.font.Font(None,36)
gameover_start_time = None
song = -1
# Tracks if window is selected (prevents Alt-Tab spam)
window_focused = True
extensions = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}
listmus = [
    fichier for fichier in MUSDIR.rglob("*")
    if fichier.is_file() and fichier.suffix.lower() in extensions
]
# Safely load your assets
try:
    placeholder = pygame.image.load(ASSETSDIR/'placeholder.png')
    appicon = pygame.image.load(ASSETSDIR/'applogo.png')
    pygame.display.set_icon(appicon)
except pygame.error as e:
    print(f"Erreur de chargement d'image: {e}")
game_state = "MENU"
running = True
while running:
    # -------------------------------------------------------------
    # 1. THE SINGLE CENTRAL EVENT LOOP (All inputs handled here)
    # -------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and window_focused:
            if event.key in (pygame.K_5, pygame.K_KP5):
                song = (song + 1) % len(listmus)
                pygame.mixer.music.load(str(listmus[song]))
                audiofile = eyed3.load(str(listmus[song]))
                if audiofile.tag and audiofile.tag.images:
                    curimage = audiofile.tag.images[0]
                    image_stream = io.BytesIO(curimage.image_data)
                    appicon = pygame.image.load(image_stream, namehint="cover.jpg")
                    if appicon.get_height() > appicon.get_width():
                        ratio = 256 / appicon.get_width()
                        appicon = pygame.transform.smoothscale(appicon,(256,appicon.get_height()*ratio))
                    elif appicon.get_height() < appicon.get_width():
                        ratio = 256 / appicon.get_height()
                        appicon = pygame.transform.smoothscale(appicon,(appicon.get_width()*ratio,256))
                    else:
                        appicon = pygame.transform.smoothscale(appicon,(256,256))
                else:
                    appicon = pygame.image.load(ASSETSDIR/"NoIcon.png")
                    ratio = 256 / appicon.get_height()
                    appicon = pygame.transform.smoothscale(appicon,(appicon.get_width()*ratio,256))
                pygame.mixer.music.play(0)
                pygame.display.set_caption('Melody : ' + listmus[song].stem)
        elif game_state == "MENU":
            pass
        elif game_state == "GAME":
            pass
        elif game_state == "GAMEOVER":
            pass
        elif game_state == "SETTINGS":
            pass
    # -------------------------------------------------------------
    # 2. RENDERING AND DRAWING SECTION
    # -------------------------------------------------------------
    if game_state == "MENU":
        screen.blit(placeholder, (0,0))
        logo_rect = appicon.get_rect(centerx=screen.get_width() // 2, y=50)
        if appicon.get_width() == appicon.get_height():
            screen.blit(appicon, logo_rect)
        else:
            screen.blit(appicon,(screen.get_width()//2-128,50),((appicon.get_width()//2)-128,(appicon.get_height()//2)-128,256,256))
    elif game_state == "GAME":
        pass
    elif game_state == "GAMEOVER":
        pass
    elif game_state == "SETTINGS":
        pass
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()