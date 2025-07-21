import pygame

class MenuBackground:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load("images/menu_background.png")
        self.background_image = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))

    def draw(self):
        """Vykreslí pozadí menu"""
        self.screen.blit(self.background_image, (0, 0))

    def animate(self):
        """Volitelná metoda pro animaci pozadí menu"""
        # Zde můžete přidat animační efekty pro pozadí
        pass