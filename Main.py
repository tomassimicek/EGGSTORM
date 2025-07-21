import pygame
from Game import Game
from MainMenu import MainMenu


def main():
    pygame.init()
    pygame.font.init()  # Inicializace fontů
    screen = None
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("EGGSTORM")

    running = True
    current_level = 1
    # Vytvoření instance menu jednou na začátku
    menu = MainMenu(screen)
    
    # Hlavní herní smyčka
    while running and screen is not None:
            menu_running = True
            menu_result = None
            
            # Obnovení zobrazení menu
            menu.display()
            pygame.display.flip()
            
            # Vnitřní smyčka pro menu
            while menu_running and running:
                # Zpracování událostí
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        menu_running = False
                        break
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        menu_result = menu.handle_events(event)
                        
                        if menu_result == 'start':
                            current_level = 1
                            menu_running = False
                            break
                            
                        elif menu_result == 'start_level2':
                            current_level = 2
                            menu_running = False
                            break
                            
                        elif menu_result == 'quit':
                            running = False
                            menu_running = False
                            break
                            
                        elif menu_result == 'controls':
                            # Zobrazení ovládání - tato metoda sama o sobě čeká na stisk tlačítka zpět
                            menu.display_controls()
                            # Po návratu zobrazení menu
                            menu.display()
                            pygame.display.flip()
                
                # Pokud uživatel zavřel okno, ukončíme
                if not running:
                    break
                
                # Vykreslení menu
                menu.display()
                pygame.display.flip()
                
                # Malé zpoždění pro snížení vytížení CPU
                pygame.time.delay(30)
            
            # Pokud uživatel zavřel okno, ukončíme
            if not running:
                break
                
            # Spuštění hry s vybraným levelem
            # Vytvoření nové instance hry s aktuálním levelem
            game = Game(screen, current_level)
            result = game.game_loop()
            
            if result == 'quit':
                running = False
            elif result == 'menu':
                current_level = 1  # Návrat do hlavního menu
            elif result == 'continue':
                # Přechod na další level
                if current_level < 2:  # Máme jen 2 levely
                    current_level += 1
                    # Pokračujeme ve vnější smyčce s novým levelem
                    continue
                else:
                    current_level = 1  # Po druhém levelu jdeme znovu na první
            elif result == 'restart':
                # Při restartu začínáme znovu od aktuálního levelu
                # Pokračujeme ve vnější smyčce se stejným levelem
                continue
                    
    # Ukončení Pygame
    if pygame.get_init():
        pygame.quit()


if __name__ == "__main__":
    main()