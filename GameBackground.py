import pygame
import os

class GameBackground:
    def __init__(self, screen, image_path):
        self.screen = screen
        self.background = self._load_image(image_path)  # Načteme obrázek pozadí s ošetřením chybějícího souboru
        self.background = pygame.transform.scale(self.background, (600, 800))  # Změníme velikost pozadí na 600x800 px

    def _load_image(self, image_path):
        """Načte obrázek, nebo vrátí černé pozadí, pokud soubor neexistuje"""
        try:
            if os.path.exists(image_path):
                return pygame.image.load(image_path)
            else:
                print(f"Upozornění: Soubor {image_path} nebyl nalezen, používám černé pozadí.")
                # Vytvoříme černé pozadí
                surface = pygame.Surface((600, 800))
                surface.fill((0, 0, 0))
                return surface
        except Exception as e:
            print(f"Chyba při načítání obrázku {image_path}: {e}")
            # Vytvoříme černé pozadí
            surface = pygame.Surface((600, 800))
            surface.fill((0, 0, 0))
            return surface

    def display(self):
        self.screen.blit(self.background, (0, 0))  # Vykreslíme pozadí na obrazovku