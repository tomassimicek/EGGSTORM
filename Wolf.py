import pygame


class Wolf:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = (screen_width - 80) // 2
        self.y = screen_height - 130
        self.direction = "right"
        self.speed = 15

        self.wolf_image_left = pygame.image.load("images/l_wolf_pixel.png")
        self.wolf_image_right = pygame.image.load("images/r_wolf_pixel.png")

        wolf_scale = 0.2
        wolf_width = int(self.wolf_image_left.get_width() * wolf_scale)
        wolf_height = int(self.wolf_image_left.get_height() * wolf_scale)

        self.wolf_image_left = pygame.transform.scale(self.wolf_image_left, (wolf_width, wolf_height))
        self.wolf_image_right = pygame.transform.scale(self.wolf_image_right, (wolf_width, wolf_height))

        self.wolf_width = wolf_width
        self.wolf_height = wolf_height

    def draw(self, screen):
        if self.direction == "left":
            wolf_image = self.wolf_image_left
        else:
            wolf_image = self.wolf_image_right

        screen.blit(wolf_image, (self.x, self.y))

    def move(self, direction):
        """Pohyb vlka s přesným omezením v herním poli.

        Args:
            direction (str): Směr pohybu - 'left' nebo 'right'
        """
        game_width = 600
        move_speed = 5

        if direction == "left":
            self.x = max(0, self.x - move_speed)
            self.direction = "left"
        elif direction == "right":
            self.x = min(580 - self.wolf_width, self.x + move_speed)
            self.direction = "right"

    def check_collision(self, egg):
        if self.direction == "left":
            wolf_rect = pygame.Rect(self.x + 10, self.y + self.wolf_height * 2 // 3, self.wolf_width - 20,
                                    self.wolf_height // 3)
        else:
            wolf_rect = pygame.Rect(self.x, self.y + self.wolf_height * 2 // 3, self.wolf_width - 10,
                                    self.wolf_height // 3)

        egg_rect = pygame.Rect(egg.x + 5, egg.y + 5, 20, 20)

        intersection = wolf_rect.clip(egg_rect)
        overlap_area = intersection.width * intersection.height
        max_possible_overlap = min(egg_rect.width * egg_rect.height, wolf_rect.width * wolf_rect.height)
        overlap_percentage = (overlap_area / max_possible_overlap) * 100

        return (
            overlap_percentage > 50 and
            egg.y >= self.y + self.wolf_height * 2 // 3 and
            intersection.width > 5
        )