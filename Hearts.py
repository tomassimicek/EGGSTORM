import pygame

class Hearts:
    def __init__(self, screen, initial_lives=3):
        self.screen = screen
        self.max_lives = initial_lives
        self.current_lives = initial_lives
        # Změněná cesta k obrázku heart.png ve složce "images"
        self.heart_image = pygame.image.load("images/heart_pixel.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))

    def draw(self):
        # Vykreslení srdíček na obrazovce - zarovnáno na stejnou výšku jako text Level a Score (20px od horního okraje)
        for i in range(self.current_lives):
            x = 10 + i * 40  # Vodorovné rozložení srdíček s mezerou 10px
            y = 20  # Stejná výška jako text Level a Score
            self.screen.blit(self.heart_image, (x, y))

    def lose_life(self):
        # Odebrání života
        if self.current_lives > 0:
            self.current_lives -= 1

    def reset(self):
        # Obnovení všech životů
        self.current_lives = self.max_lives

    def is_game_over(self):
        # Kontrola, zda jsou všechny životy pryč
        return self.current_lives <= 0