import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont("Arial", 100)
        self.button_font = pygame.font.SysFont("Arial", 36)

        button_width = 180
        button_height = 50
        button_margin = 20
        
        total_width = (button_width * 2) + button_margin
        start_x = (self.screen.get_width() - total_width) // 2
        
        self.level1_button = pygame.Rect(start_x, 200, button_width, button_height)
        self.level2_button = pygame.Rect(start_x + button_width + button_margin, 200, button_width, button_height)
        self.controls_button = pygame.Rect(start_x + (total_width - button_width) // 2, 275, button_width, button_height)
        self.quit_button = pygame.Rect(start_x + (total_width - button_width) // 2, 355, button_width, button_height)
        
        self.background_image = pygame.image.load("images/pozadi_menu.png")
        self.background = pygame.transform.scale(self.background_image, (600, 800))

    def display(self):
        self.screen.blit(self.background, (0, 0))

        title_text = self.title_font.render("", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen.get_width() // 2 - title_text.get_width() // 2, 50))

        mouse_pos = pygame.mouse.get_pos()

        if self.level1_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (100, 255, 100), self.level1_button)
        else:
            pygame.draw.rect(self.screen, (50, 200, 0), self.level1_button)
            
        if self.level2_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (100, 255, 100), self.level2_button)
        else:
            pygame.draw.rect(self.screen, (50, 200, 0), self.level2_button)

        if self.controls_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (255, 200, 100), self.controls_button, border_radius=0)
        else:
            pygame.draw.rect(self.screen, (255, 165, 0), self.controls_button, border_radius=0)

        if self.quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (255, 100, 100), self.quit_button, border_radius=0)
        else:
            pygame.draw.rect(self.screen, (200, 0, 0), self.quit_button, border_radius=0)

        level1_text = self.button_font.render("Level 1", True, (255, 255, 255))
        level2_text = self.button_font.render("Level 2", True, (255, 255, 255))
        controls_text = self.button_font.render("Controls", True, (255, 255, 255))
        quit_text = self.button_font.render("Quit", True, (255, 255, 255))

        self.screen.blit(level1_text, (self.level1_button.centerx - level1_text.get_width() // 2, 
                                     self.level1_button.centery - level1_text.get_height() // 2))
        
        self.screen.blit(level2_text, (self.level2_button.centerx - level2_text.get_width() // 2, 
                                     self.level2_button.centery - level2_text.get_height() // 2))
        
        self.screen.blit(controls_text, (self.controls_button.centerx - controls_text.get_width() // 2, 
                                       self.controls_button.centery - controls_text.get_height() // 2))
        
        self.screen.blit(quit_text, (self.quit_button.centerx - quit_text.get_width() // 2, 
                                   self.quit_button.centery - quit_text.get_height() // 2))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.level1_button.collidepoint(mouse_pos):
                return 'start'  
            if self.level2_button.collidepoint(mouse_pos):
                return 'start_level2'
            if self.controls_button.collidepoint(mouse_pos):
                return 'controls'
            if self.quit_button.collidepoint(mouse_pos):
                return 'quit'
        return None

    def display_controls(self):
        overlay = pygame.Surface((600, 800), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        
        controls_font = pygame.font.SysFont("Arial", 50)
        controls_title = controls_font.render("Game Controls", True, (255, 255, 255))
        title_rect = controls_title.get_rect(center=(self.screen.get_width() // 2, 100))
        
        text_font = pygame.font.SysFont("Arial", 30)
        controls_text = [
            "Left Arrow: Move wolf left",
            "Right Arrow: Move wolf right",
            "P: Pause game",
            "Catch as many white and golden eggs as possible!"
        ]
        
        back_font = pygame.font.SysFont("Arial", 30)
        back_text = back_font.render("Back", True, (255, 255, 255))
        back_button = pygame.Rect(200, 600, 200, 50)
        
        pygame.event.clear()
        
        waiting = True
        while waiting and pygame.get_init():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        return None
            
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(overlay, (0, 0))
            
            self.screen.blit(controls_title, title_rect)
            
            for i, text in enumerate(controls_text):
                text_surface = text_font.render(text, True, (255, 255, 255))
                self.screen.blit(text_surface, (100, 200 + i * 50))
            
            pygame.draw.rect(self.screen, (255, 0, 0), back_button, border_radius=0)
            back_text_rect = back_text.get_rect(center=back_button.center)
            self.screen.blit(back_text, back_text_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            if back_button.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (255, 100, 100), back_button, border_radius=0)
            else:
                pygame.draw.rect(self.screen, (200, 0, 0), back_button, border_radius=0)
            
            self.screen.blit(back_text, back_text_rect)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            
            pygame.time.delay(30)

        return None