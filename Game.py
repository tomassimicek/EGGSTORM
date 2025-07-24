import pygame
from GameLogic import GameLogic
from GameGraphics import GameGraphics
from GameBackground import GameBackground
from MainMenu import MainMenu
from Hearts import Hearts

class Game:
    def __init__(self, screen, level=1):
        self.screen = screen
        self.level = level
        
        self.hearts = Hearts(screen)
        self.game_logic = GameLogic(self.hearts)
        self.game_logic.level = level
        
        background_images = {
            1: "images/pozadi_hry.png",
            2: "images/pozadi_hry_lvl2.png"
        }
        background_image = background_images.get(level, background_images[1])
        self.game_background = GameBackground(screen, background_image)
        
        self.game_logic.reset_game()
        
        self.game_graphics = GameGraphics(screen)
        self.game_graphics.convert_images()
        self.font = pygame.font.SysFont("Arial", 50)
        self.main_menu = MainMenu(screen)
        self.paused = False

    def game_loop(self):
        return self.run_game()
        
    def run_game(self):
        self.game_logic.reset_game()
        running = True
        clock = pygame.time.Clock()
        fps_font = pygame.font.SysFont("Arial", 20)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 'quit'
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.game_logic.move_wolf('left')
                    elif event.key == pygame.K_RIGHT:
                        self.game_logic.move_wolf('right')
            
            game_state = self.game_logic.update()
            
            if game_state == 'game_over':
                result = self.display_game_over()
                if result == 'menu':
                    return 'menu'
                elif result == 'quit':
                    return 'quit'
            elif game_state == 'level_complete':
                result = self.display_win()
                if result == 'continue':
                    return 'continue'
                elif result == 'menu':
                    return 'menu'
                elif result == 'quit':
                    return 'quit'
            
            self.game_background.display()
            self.game_graphics.draw_wolf(self.game_logic.wolf)
            self.game_graphics.draw_hens(self.game_logic.hens)
            self.game_graphics.draw_eggs(self.game_logic.eggs)
            self.game_graphics.draw_score(self.game_logic.score)
            self.game_graphics.draw_level(self.game_logic.level)
            self.hearts.draw()
            
            # Zobrazení FPS odstraněno podle požadavku uživatele
            
            pygame.display.flip()
            clock.tick(60)
        
        return 'quit'

    def run_game(self):
        self.game_logic.reset_game()
        running = True
        clock = pygame.time.Clock()
        fps_font = pygame.font.SysFont("Arial", 20)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused

            if not self.paused:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.game_logic.move_wolf("left")
                if keys[pygame.K_RIGHT]:
                    self.game_logic.move_wolf("right")

                self.game_background.display()
                self.game_graphics.draw_wolf(self.game_logic.wolf)
                self.game_graphics.draw_hens(self.game_logic.hens)
                self.game_graphics.draw_eggs(self.game_logic.eggs)
                self.game_graphics.draw_score(self.game_logic.score)
                self.game_graphics.draw_level(self.game_logic.level)
                self.hearts.draw()

                self.game_logic.generate_eggs(is_paused=self.paused)
                result = self.game_logic.update()

                if result == 'you_won':
                    current_score = self.game_logic.score
                    self.game_background.display()
                    self.game_graphics.draw_wolf(self.game_logic.wolf)
                    self.game_graphics.draw_hens(self.game_logic.hens)
                    self.game_graphics.draw_eggs(self.game_logic.eggs)
                    self.game_graphics.draw_score(current_score)
                    self.game_graphics.draw_level(self.game_logic.level)
                    self.hearts.draw()
                    pygame.display.flip()
                    
                    menu_result = self.display_game_result(True)
                    if menu_result == 'restart':
                        return 'restart'
                    elif menu_result == 'continue':
                        if self.game_logic.level < 2:
                            self.game_logic.level += 1
                            self.game_logic.hens = self.game_logic._generate_hens()
                            self.game_logic.score = 0
                            self.game_logic.hearts.reset()
                            return 'continue'
                    
                    return menu_result
                    
                elif self.hearts.is_game_over():
                    menu_result = self.display_game_result(False)
                    if menu_result == 'restart':
                        return 'restart'
                    return menu_result

                pygame.display.flip()
                clock.tick(60)
            else:
                pause_result = self.display_paused()
                if pause_result == 'continue':
                    self.paused = False
                elif pause_result == 'exit':
                    running = False
                elif pause_result == 'menu':
                    self.game_logic = GameLogic(self.hearts)
                    self.game_graphics = GameGraphics(self.screen)
                    return 'menu'

    def display_game_over(self):
        # Vytvoření průhledného překryvu
        overlay = pygame.Surface((600, 800), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 64))  # Snížená průhlednost
        self.screen.blit(overlay, (0, 0))

        game_over_font = pygame.font.SysFont("Arial", 70)
        game_over_text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(self.screen.get_width() / 2, 200))
        self.screen.blit(game_over_text, text_rect)

        exit_font = pygame.font.SysFont("Arial", 40)
        exit_text = exit_font.render("Exit", True, (255, 255, 255))
        exit_button = pygame.Rect(200, 400, 200, 50)
        exit_button_color = (204, 0, 0)
        pygame.draw.rect(self.screen, exit_button_color, exit_button)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        self.screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            mouse_pos = pygame.mouse.get_pos()

            if exit_button.collidepoint(mouse_pos):
                exit_button_color = (255, 120, 120)
            else:
                exit_button_color = (204, 0, 0)

            self.screen.blit(overlay, (0, 0))
            self.screen.blit(game_over_text, text_rect)
            pygame.draw.rect(self.screen, exit_button_color, exit_button)
            self.screen.blit(exit_text, exit_text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'exit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        return 'exit'

        pygame.quit()
        return 'exit'

    def display_win(self):
        self.screen.fill((0, 0, 0))
        win_font = pygame.font.SysFont("Arial", 70)
        win_text = win_font.render("YOU WON!", True, (0, 255, 0))
        text_rect = win_text.get_rect(center=(self.screen.get_width() / 2, 200))
        self.screen.blit(win_text, text_rect)

        exit_font = pygame.font.SysFont("Arial", 40)
        exit_text = exit_font.render("Exit", True, (255, 255, 255))
        exit_button = pygame.Rect(200, 400, 200, 50)
        exit_button_color = (100, 100, 100)
        pygame.draw.rect(self.screen, exit_button_color, exit_button)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        self.screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'exit'
                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if exit_button.collidepoint(mouse_pos):
                        exit_button_color = (150, 150, 150)
                    else:
                        exit_button_color = (100, 100, 100)

                    self.screen.fill((0, 0, 0))
                    self.screen.blit(win_text, text_rect)
                    pygame.draw.rect(self.screen, exit_button_color, exit_button)
                    self.screen.blit(exit_text, exit_text_rect)
                    pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        return 'exit'
        pygame.quit()
        return 'exit'

    def display_paused(self):
        overlay = pygame.Surface((600, 800))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        pause_font = pygame.font.SysFont("Arial", 70)
        pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(self.screen.get_width() / 2, 200))
        self.screen.blit(pause_text, text_rect)

        continue_font = pygame.font.SysFont("Arial", 40)
        continue_text = continue_font.render("Continue", True, (255, 255, 255))
        continue_button = pygame.Rect(200, 400, 200, 50)
        pygame.draw.rect(self.screen, (100, 100, 100), continue_button)
        continue_text_rect = continue_text.get_rect(center=continue_button.center)
        self.screen.blit(continue_text, continue_text_rect)

        exit_font = pygame.font.SysFont("Arial", 40)
        exit_text = exit_font.render("Exit", True, (255, 255, 255))
        exit_button = pygame.Rect(200, 500, 200, 50)
        pygame.draw.rect(self.screen, (100, 100, 100), exit_button)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        self.screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'exit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return 'continue'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if continue_button.collidepoint(mouse_pos):
                        return 'continue'
                    if exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        return 'exit'
        pygame.quit()
        return 'exit'

    def display_game_result(self, is_win):
        # Černé pozadí
        self.screen.fill((0, 0, 0))

        # Nadpis
        font_title = pygame.font.SysFont("Arial", 72, bold=True)
        title_text = font_title.render("YOU WON!" if is_win else "GAME OVER!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(300, 200))
        self.screen.blit(title_text, title_rect)

        # Zobrazení levelu (posunuto níže)
        font_score = pygame.font.SysFont("Arial", 48)
        level_text = font_score.render(f"Level: {self.game_logic.level}", True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(300, 300))  # Posunuto z 250 na 300
        self.screen.blit(level_text, level_rect)
        
        # Zobrazení skóre (posunuto níže pod level)
        score_text = font_score.render(f"Score: {self.game_logic.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(300, 360))  # Posunuto z 300 na 360
        self.screen.blit(score_text, score_rect)

        # Vytvoření tlačítka
        font_button = pygame.font.SysFont("Arial", 36)
        menu_text = font_button.render("Exit to Menu", True, (255, 255, 255))

        # Nastavení pozice tlačítka
        menu_rect = pygame.Rect(150, 400, 300, 50)  # Moved up to where restart button was

        # Barva tlačítka
        menu_color = (204, 0, 0)  # Červená
        
        # Čekání na akci uživatele
        waiting = True
        while waiting:
            mouse_pos = pygame.mouse.get_pos()

            # Reset barvy tlačítka
            menu_color = (204, 0, 0)  # Výchozí červená
            
            # Změna barvy při najetí myší
            if menu_rect.collidepoint(mouse_pos):
                menu_color = (255, 120, 120)  # Světlejší červená
                
            # Pro tlačítko Next Level již není potřeba žádný kód

            # Překreslení obrazovky s aktuálními barvami
            self.screen.fill((0, 0, 0))  # Černé pozadí
            self.screen.blit(title_text, title_rect)
            self.screen.blit(level_text, level_rect)
            self.screen.blit(score_text, score_rect)

            # Vykreslení tlačítka
            pygame.draw.rect(self.screen, menu_color, menu_rect)

            # Vykreslení textu tlačítka
            self.screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Kliknutí na tlačítko Menu
                    if menu_rect.collidepoint(mouse_pos):
                        self.game_logic = GameLogic(self.hearts)
                        self.game_graphics = GameGraphics(self.screen)
                        return 'menu'  # Vrátí 'menu' pro návrat do hlavního menu

        return 'quit'

    def display_paused(self):
        # Nejprve vykreslit aktuální herní obrazovku
        self.screen.fill((255, 255, 255))  # Bílé pozadí
        self.game_background.display()
        self.game_graphics.draw_wolf(self.game_logic.wolf)
        self.game_graphics.draw_hens(self.game_logic.hens)
        self.game_graphics.draw_eggs(self.game_logic.eggs)
        self.game_graphics.draw_score(self.game_logic.score)
        self.game_graphics.draw_level(self.game_logic.level)
        self.hearts.draw()

        # Vytvoření průhledného překryvu
        overlay = pygame.Surface((600, 800), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Nejtmavší zatímnění
        self.screen.blit(overlay, (0, 0))

        # Nadpis
        font_title = pygame.font.SysFont("Arial", 72, bold=True)
        title_text = font_title.render("PAUSED", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(300, 200))
        self.screen.blit(title_text, title_rect)

        # Vytvoření tlačítek
        font_button = pygame.font.SysFont("Arial", 36)
        continue_text = font_button.render("Continue", True, (255, 255, 255))
        menu_text = font_button.render("Exit to Menu", True, (255, 255, 255))

        continue_rect = pygame.Rect(150, 400, 300, 50)
        menu_rect = pygame.Rect(150, 470, 300, 50)

        continue_color = (0, 102, 204)  # Tmavě modrá
        menu_color = (204, 0, 0)  # Tmavě červená

        pygame.draw.rect(self.screen, continue_color, continue_rect)
        pygame.draw.rect(self.screen, menu_color, menu_rect)

        self.screen.blit(continue_text, continue_text.get_rect(center=continue_rect.center))
        self.screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))

        pygame.display.flip()

        # Čekání na akci uživatele
        waiting = True
        while waiting:
            mouse_pos = pygame.mouse.get_pos()

            # Změna barvy tlačítka Continue při najetí
            if continue_rect.collidepoint(mouse_pos):
                continue_color = (100, 150, 255)  # Světlejší modrá
            else:
                continue_color = (0, 102, 204)  # Původní modrá

            # Změna barvy tlačítka Menu při najetí
            if menu_rect.collidepoint(mouse_pos):
                menu_color = (255, 120, 120)  # Světlejší červená
            else:
                menu_color = (204, 0, 0)  # Původní červená

            # Překreslení obrazovky s aktuálními barvami
            self.screen.fill((255, 255, 255))  # Bílé pozadí
            self.game_background.display()
            self.game_graphics.draw_wolf(self.game_logic.wolf)
            self.game_graphics.draw_hens(self.game_logic.hens)
            self.game_graphics.draw_eggs(self.game_logic.eggs)
            self.game_graphics.draw_score(self.game_logic.score)
            self.game_graphics.draw_level(self.game_logic.level)
            self.hearts.draw()

            self.screen.blit(overlay, (0, 0))
            self.screen.blit(title_text, title_rect)

            pygame.draw.rect(self.screen, continue_color, continue_rect)
            pygame.draw.rect(self.screen, menu_color, menu_rect)

            self.screen.blit(continue_text, continue_text.get_rect(center=continue_rect.center))
            self.screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if continue_rect.collidepoint(mouse_pos):
                        return 'continue'
                    if menu_rect.collidepoint(mouse_pos):
                        # Reset hry před návratem do menu
                        self.game_logic = GameLogic(self.hearts)
                        self.game_graphics = GameGraphics(self.screen)
                        return 'menu'

        return 'exit'

    def display_you_won(self):
        # Vytvoření průhledného překryvu
        overlay = pygame.Surface((600, 800), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Nadpis
        font_title = pygame.font.SysFont("Arial", 72, bold=True)
        title_text = font_title.render("YOU WON!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(300, 200))
        self.screen.blit(title_text, title_rect)

        # Vytvoření tlačítek
        font_button = pygame.font.SysFont("Arial", 36)
        restart_text = font_button.render("Restart", True, (255, 255, 255))
        menu_text = font_button.render("Exit to Menu", True, (255, 255, 255))

        restart_rect = pygame.Rect(150, 400, 300, 50)
        menu_rect = pygame.Rect(150, 470, 300, 50)

        pygame.draw.rect(self.screen, (0, 102, 204), restart_rect, border_radius=10)
        pygame.draw.rect(self.screen, (204, 0, 0), menu_rect, border_radius=10)

        self.screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))
        self.screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))

        pygame.display.flip()

        # Čekání na akci uživatele
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mouse_pos):
                        # Restart hry
                        return 'restart'
                    if menu_rect.collidepoint(mouse_pos):
                        # Explicitní reset hry před návratem do menu
                        return 'menu'

        return 'quit'


def run_game(self):
    running = True
    clock = pygame.time.Clock()
    frame_count = 0

    debug_collision_count = 0  # Počítadlo kolizí pro ladění
    while running:
        # FPS výpis odstraněn

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused

        if not self.paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.game_logic.move_wolf("left")
            if keys[pygame.K_RIGHT]:
                self.game_logic.move_wolf("right")

            self.screen.fill((255, 255, 255))  # Bílé pozadí
            self.game_background.display()
            self.game_graphics.draw_wolf(self.game_logic.wolf)
            self.game_graphics.draw_hens(self.game_logic.hens)
            self.game_graphics.draw_eggs(self.game_logic.eggs)
            self.game_graphics.draw_score(self.game_logic.score)
            # FPS se netiskne do terminálu
            # Vykreslení srdíček
            self.hearts.draw()

            result = self.game_logic.update()

            # Kontrola stavu životů
            if self.hearts.is_game_over():
                game_over_result = self.display_game_over()
                if game_over_result == 'restart':
                    # Vrátíme 'restart' pro restartování aktuálního levelu
                    return 'restart'
                elif game_over_result == 'menu':
                    return 'menu'
            elif result == 'you_won':
                win_result = self.display_win()
                if win_result == 'restart':
                    self.__init__(self.screen)
                    self.run_game()
                elif win_result == 'exit':
                    return 'menu'

            pygame.display.update()
            clock.tick(60)
        else:
            self.display_paused()


def display_game_over(self):
    game_over_font = pygame.font.SysFont("Arial", 70)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))