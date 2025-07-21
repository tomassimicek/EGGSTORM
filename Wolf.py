import pygame


class Wolf:
    def __init__(self, screen_width, screen_height):
        # Umístění vlka úplě dole uprostřed
        self.screen_width = screen_width  # Uložení šířky obrazovky
        self.screen_height = screen_height  # Uložení výšky obrazovky
        self.x = (screen_width - 80) // 2  # Polovina šířky vlka
        self.y = screen_height - 130  # Spodní část obrazovky
        self.direction = "right"  # Počáteční směr vlka je doprava
        self.speed = 15  # Rychlost pohybu vlka pro užšího vlka

        # Nahrání obrázků vlka - používáme pixelové verze, které jsou k dispozici ve složce images
        self.wolf_image_left = pygame.image.load("images/l_wolf_pixel.png")
        self.wolf_image_right = pygame.image.load("images/r_wolf_pixel.png")

        # Měřítko a velikost obrázků
        wolf_scale = 0.2  # Měřítko pro ještě menšího vlka
        wolf_width = int(self.wolf_image_left.get_width() * wolf_scale)
        wolf_height = int(self.wolf_image_left.get_height() * wolf_scale)

        # Zmenšení obrázků
        self.wolf_image_left = pygame.transform.scale(self.wolf_image_left, (wolf_width, wolf_height))
        self.wolf_image_right = pygame.transform.scale(self.wolf_image_right, (wolf_width, wolf_height))

        # Uložení rozměrů pro kolize
        self.wolf_width = wolf_width
        self.wolf_height = wolf_height

    def draw(self, screen):
        # Vyber správný obrázek vlka podle směru
        if self.direction == "left":
            wolf_image = self.wolf_image_left
        else:
            wolf_image = self.wolf_image_right

        # Vykresli vlka na obrazovku na aktuální pozici
        screen.blit(wolf_image, (self.x, self.y))

    def move(self, direction):
        """Pohyb vlka s přesným omezením v herním poli.

        Args:
            direction (str): Směr pohybu - 'left' nebo 'right'
        """
        # Přesné omezení na šířku 600 pixelů
        game_width = 600
        move_speed = 5  # Snížení rychlosti pohybu

        if direction == "left":
            # Pohyb doleva s přesným omezením
            self.x = max(0, self.x - move_speed)
            self.direction = "left"

        elif direction == "right":
            # Pohyb doprava s přesným omezením
            self.x = min(580 - self.wolf_width, self.x + move_speed)
            self.direction = "right"

    def check_collision(self, egg):
        # Přesná kontrola kolize mezi vlkem a vajíčkem
        # Oblast kolize v závislosti na aktuálním směru
        if self.direction == "left":
            wolf_rect = pygame.Rect(self.x + 10, self.y + self.wolf_height * 2 // 3, self.wolf_width - 20,
                                    self.wolf_height // 3)
        else:
            wolf_rect = pygame.Rect(self.x, self.y + self.wolf_height * 2 // 3, self.wolf_width - 10,
                                    self.wolf_height // 3)

        egg_rect = pygame.Rect(egg.x + 5, egg.y + 5, 20, 20)  # Zmenšená oblast vajíčka

        # Kontrola kolize
        intersection = wolf_rect.clip(egg_rect)

        # Výpočet překryvu
        overlap_area = intersection.width * intersection.height
        max_possible_overlap = min(egg_rect.width * egg_rect.height, wolf_rect.width * wolf_rect.height)
        overlap_percentage = (overlap_area / max_possible_overlap) * 100

        return (
                overlap_percentage > 50 and  # Alespoň 50% překryv
                egg.y >= self.y + self.wolf_height * 2 // 3 and  # Vajíčko v dolní třetině vlka
                intersection.width > 5  # Horizontální překryv
        )
        # 3. Výrazný překryv
        is_vertical_collision = egg.y >= self.y + 50
        is_horizontal_collision = (egg.x >= self.x + 5) and (egg.x <= self.x + 55)
        is_significant_overlap = intersection.width * intersection.height > 50

        return is_vertical_collision and is_horizontal_collision and is_significant_overlap