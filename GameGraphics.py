import pygame


class GameGraphics:
    def __init__(self, screen):
        # Inicializace fontů
        if not pygame.font.get_init():
            pygame.font.init()

        # Nahrání obrázků
        self.wolf_image_left = pygame.image.load("images/l_wolf_pixel.png")
        self.wolf_image_right = pygame.image.load("images/r_wolf_pixel.png")

        # Obrázky vajíček
        self.white_egg = pygame.image.load("images/egg__white.png")
        self.black_egg = pygame.image.load("images/egg__black.png")
        self.golden_egg = pygame.image.load("images/egg__gold.png")

        # Obrázek slepice
        self.hen_image = pygame.image.load("images/hen_pixel.png")

        # Zmenšení obrázků
        self.wolf_image_left = pygame.transform.scale(self.wolf_image_left, (85, 125))
        self.wolf_image_right = pygame.transform.scale(self.wolf_image_right, (85, 125))
        self.white_egg = pygame.transform.scale(self.white_egg, (22, 22))
        self.black_egg = pygame.transform.scale(self.black_egg, (22, 22))
        self.golden_egg = pygame.transform.scale(self.golden_egg, (22, 22))

        self.screen = screen

        # Pixel font pro hru
        self.pixel_font = pygame.font.SysFont('Courier', 24, bold=True)
        self.pixel_font_small = pygame.font.SysFont('Courier', 16, bold=True)

        # Nastavení pixelového stylu pro tlačítka
        def create_pixelated_text(text, font, color=(255, 255, 255)):
            text_surface = font.render(text, True, color)
            # Zmenšení a zvětšení pro pixelový efekt
            scaled_surface = pygame.transform.scale(text_surface,
                                                    (text_surface.get_width() * 2, text_surface.get_height() * 2))
            scaled_surface = pygame.transform.scale(scaled_surface,
                                                    (text_surface.get_width(), text_surface.get_height()))
            return scaled_surface

        self.create_pixelated_text = create_pixelated_text

        self.hen_image = pygame.transform.scale(self.hen_image, (80, 80))

    def convert_images(self):
        # Explicitní inicializace displeje
        if not pygame.display.get_init():
            pygame.display.init()
            pygame.display.set_mode((600, 800))
        # Odstranění alfa kanálu pro odstraňování rámečku
        self.white_egg = self.white_egg.convert_alpha()
        self.black_egg = self.black_egg.convert_alpha()
        self.golden_egg = self.golden_egg.convert_alpha()

    def draw_wolf(self, wolf):
        # Vykreslení vlka podle směru
        if wolf.direction == "left":
            self.screen.blit(self.wolf_image_left, (wolf.x, wolf.y))
        else:
            self.screen.blit(self.wolf_image_right, (wolf.x, wolf.y))

        # Odebrání vizualizace kolizní oblasti vlka

    def draw_eggs(self, eggs):
        for egg in eggs:
            if egg.type == "white":
                self.screen.blit(self.white_egg, (egg.x, egg.y))
            elif egg.type == "black":
                self.screen.blit(self.black_egg, (egg.x, egg.y))
            elif egg.type == "golden":
                self.screen.blit(self.golden_egg, (egg.x, egg.y))



    def draw_hens(self, hens):
        for hen in hens:
            self.screen.blit(self.hen_image, (hen.x, hen.y))

    def draw_score(self, score):
        font = pygame.font.SysFont("Arial", 36)
        # Zobrazovat jen nezáporné skóre
        display_score = max(0, score)
        score_text = font.render(f"Score: {display_score}", True, (255, 255, 255))
        screen_width = self.screen.get_width()
        text_width = score_text.get_width()
        self.screen.blit(score_text, (screen_width - text_width - 20, 20))

    def draw_level(self, level):
        font = pygame.font.SysFont("Arial", 32, bold=True)
        level_text = font.render(f"LEVEL {level}", True, (255, 255, 255))
        screen_width = self.screen.get_width()
        text_width = level_text.get_width()
        self.screen.blit(level_text, ((screen_width - text_width) // 2, 20))