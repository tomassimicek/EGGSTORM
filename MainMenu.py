import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        # Font for title
        self.title_font = pygame.font.SysFont("Arial", 100)  # Larger font size for title
        # Font for buttons
        self.button_font = pygame.font.SysFont("Arial", 36)  # Smaller font size for buttons

        # Šířka a výška tlačítek
        button_width = 180
        button_height = 50
        button_margin = 20  # Mezera mezi tlačítky
        
        # Výpočet X pozice pro zarovnání tlačítek od středu
        total_width = (button_width * 2) + button_margin
        start_x = (self.screen.get_width() - total_width) // 2
        
        # Vytvoření tlačítek
        self.level1_button = pygame.Rect(start_x, 200, button_width, button_height)
        self.level2_button = pygame.Rect(start_x + button_width + button_margin, 200, button_width, button_height)
        self.controls_button = pygame.Rect(start_x + (total_width - button_width) // 2, 275, button_width, button_height)  # Controls button - posunuto o 15px dolů
        self.quit_button = pygame.Rect(start_x + (total_width - button_width) // 2, 355, button_width, button_height)   # Quit button - posunuto o 15px dolů
        # Načtení pozadí menu
        self.background_image = pygame.image.load("images/pozadi menu.png")  # Set your background image path here
        self.background = pygame.transform.scale(self.background_image, (600, 800))  # Scale the background to fit the screen

    def display(self):
        self.screen.blit(self.background, (0, 0))  # Display background image, now scaled to fit the screen

        # Title Text - Game title with larger font size, moved up
        title_text = self.title_font.render("", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen.get_width() // 2 - title_text.get_width() // 2, 50))  # Title y = 50

        mouse_pos = pygame.mouse.get_pos()  # Get mouse position to detect hovering

        # Tlačítko Level 1 - efekt při najetí myší
        if self.level1_button.collidepoint(mouse_pos):
            # Zesvětlená zelená při najetí
            pygame.draw.rect(self.screen, (100, 255, 100), self.level1_button)
        else:
            # Základní zelená
            pygame.draw.rect(self.screen, (50, 200, 0), self.level1_button)
            
        # Tlačítko Level 2 - efekt při najetí myší
        if self.level2_button.collidepoint(mouse_pos):
            # Zesvětlená zelená při najetí
            pygame.draw.rect(self.screen, (100, 255, 100), self.level2_button)
        else:
            # Základní zelená
            pygame.draw.rect(self.screen, (50, 200, 0), self.level2_button)

        # Tlačítko Controls - efekt při najetí myší s hranatými rohy
        if self.controls_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (100, 150, 255), self.controls_button)  # Light Blue when hovered
        else:
            pygame.draw.rect(self.screen, (0, 51, 102), self.controls_button)  # Darker Blue

        # Quit Button Hover Effect with square corners
        if self.quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (255, 120, 120), self.quit_button)  # Light Red when hovered
        else:
            pygame.draw.rect(self.screen, (204, 0, 0), self.quit_button)  # Dark Red by default

        # Texty tlačítek
        level1_text = self.button_font.render("Level 1", True, (255, 255, 255))
        level2_text = self.button_font.render("Level 2", True, (255, 255, 255))
        controls_text = self.button_font.render("Controls", True, (255, 255, 255))
        quit_text = self.button_font.render("Quit", True, (255, 255, 255))

        # Vycentrování textu na tlačítkách
        self.screen.blit(level1_text, (self.level1_button.x + (self.level1_button.width - level1_text.get_width()) // 2, 
                                     self.level1_button.y + (self.level1_button.height - level1_text.get_height()) // 2))
        self.screen.blit(level2_text, (self.level2_button.x + (self.level2_button.width - level2_text.get_width()) // 2, 
                                     self.level2_button.y + (self.level2_button.height - level2_text.get_height()) // 2))
        self.screen.blit(controls_text, (self.controls_button.x + (self.controls_button.width - controls_text.get_width()) // 2, 
                                       self.controls_button.y + (self.controls_button.height - controls_text.get_height()) // 2))
        self.screen.blit(quit_text, (self.quit_button.x + (self.quit_button.width - quit_text.get_width()) // 2, 
                                   self.quit_button.y + (self.quit_button.height - quit_text.get_height()) // 2))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.level1_button.collidepoint(mouse_pos):
                return 'start'  # Kliknuto na Level 1 - spustí první level
            if self.level2_button.collidepoint(mouse_pos):
                return 'start_level2'  # Kliknuto na Level 2 - spustí druhý level
            if self.controls_button.collidepoint(mouse_pos):
                return 'controls'  # Kliknuto na Controls
            if self.quit_button.collidepoint(mouse_pos):
                return 'quit'  # Kliknuto na Quit
        return None

    def display_controls(self):
        # Vytvoření průhledného černého překryvu
        overlay = pygame.Surface((600, 800), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))  # Černá barva s vyšší neprůhledností
        
        # Nadpis ovládání
        controls_font = pygame.font.SysFont("Arial", 50)
        controls_title = controls_font.render("Game Controls", True, (255, 255, 255))
        title_rect = controls_title.get_rect(center=(self.screen.get_width() // 2, 100))
        
        # Text ovládání
        text_font = pygame.font.SysFont("Arial", 30)
        controls_text = [
            "Left Arrow: Move wolf left",
            "Right Arrow: Move wolf right",
            "P: Pause game",
            "Catch as many white and golden eggs as possible!"
        ]
        
        # Vytvoření tlačítka zpět
        back_font = pygame.font.SysFont("Arial", 30)
        back_text = back_font.render("Back", True, (255, 255, 255))
        back_button = pygame.Rect(200, 600, 200, 50)
        
        # Vyčištění fronty událostí před vstupem do smyčky
        pygame.event.clear()
        
        # Hlavní smyčka pro zobrazení ovládání
        waiting = True
        while waiting and pygame.get_init():
            # Zpracování událostí jako první věc v každém snímku
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Levé tlačítko myši
                    if back_button.collidepoint(event.pos):
                        return None  # Okamžitý návrat při kliknutí
            
            # Vykreslení pozadí a obsahu
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(controls_title, title_rect)
            
            # Vykreslení textu ovládání
            for i, text in enumerate(controls_text):
                text_surface = text_font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 250 + i * 50))
                self.screen.blit(text_surface, text_rect)
            
            # Získání pozice myši pro efekt při najetí
            mouse_pos = pygame.mouse.get_pos()
            
            # Vykreslení tlačítka zpět s efektem při najetí myší
            if back_button.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (255, 100, 100), back_button)  # Světlejší červená při najetí
            else:
                pygame.draw.rect(self.screen, (204, 0, 0), back_button)  # Původní tmavě červená
            
            # Vykreslení textu tlačítka
            back_text_rect = back_text.get_rect(center=back_button.center)
            self.screen.blit(back_text, back_text_rect)
            
            # Aktualizace obrazovky
            pygame.display.flip()
            
            # Krátké zpoždění pro snížení vytížení CPU
            pygame.time.delay(30)

        return None