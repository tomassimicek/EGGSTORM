import pygame

class Hen:
    def __init__(self, x, y):
        self.x = x  # Pozice slepice na ose X
        self.y = y  # Pozice slepice na ose Y

    def draw(self, screen):
        # Tato metoda je zde jen pro kompatibilitu, 
        # vlastní vykreslování probíhá přes GameGraphics
        pass