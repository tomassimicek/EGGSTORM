import pygame

class Egg:
    def __init__(self, x, y, egg_type):
        self.x = x  # Počáteční pozice vajíčka na ose X
        self.y = y  # Počáteční pozice vajíčka na ose Y
        self.type = egg_type  # Typ vajíčka (bílé, černé, zlaté)

    def fall(self, fall_speed):
        self.y += fall_speed  # Pomalu padající vajíčko (zvolíme rychlost pádu)

    def draw(self, screen):
        # Tato metoda je zde jen pro kompatibilitu, 
        # vlastní vykreslování probíhá přes GameGraphics
        pass

        # Zmenseni obrazku
        self.white_egg = pygame.transform.scale(self.white_egg, (30, 30))
        self.black_egg = pygame.transform.scale(self.black_egg, (30, 30))
        self.golden_egg = pygame.transform.scale(self.golden_egg, (30, 30))

    def fall(self, speed):
        # Pohyb vajicka smerem dolu
        self.y += speed

    def draw(self, screen):
        # Vykresleni spravneho obrazku vajicka
        if self.type == "white":
            screen.blit(self.white_egg, (self.x, self.y))
        elif self.type == "black":
            screen.blit(self.black_egg, (self.x, self.y))
        elif self.type == "golden":
            screen.blit(self.golden_egg, (self.x, self.y))
