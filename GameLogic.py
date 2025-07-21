import random
import time
from Egg import Egg
from Hen import Hen
from Wolf import Wolf


class GameLogic:
    def __init__(self, hearts=None):
        self.score = 0
        self.hearts = hearts
        self.level = 1
        self.wolf = Wolf(600, 800)  # Počáteční pozice vlka ve středu obrazovky
        self.hens = self._generate_hens()
        self.eggs = []
        self.egg_spawn_interval = 120  # Delší interval generování vajíček (2000 ms při 60 FPS)
        self.egg_spawn_counter = 0  # Počítač snímků pro generování
        self.fall_speed = 3  # Rychlejší pád vajíček
        self.white_eggs_collected = 0  # Počet chytitých bílých vajíček

    def _generate_hens(self):
        # Dynamické generování slepic podle levelu
        hen_positions = {
            1: [(120, 100), (410, 100)],  # Pozice pro Level 1 (pravá slepice posunuta o 10 doleva)
            # Pro Level 2: upravené pozice podle posledního požadavku
            2: [
                (70, 100),    # Původně 80, nyní o 10 doleva
                (270, 100),   # Prostřední slepice beze změny
                (460, 100)    # Pravá slepice beze změny
            ]
        }
        return [Hen(x, y) for x, y in hen_positions.get(self.level, hen_positions[1])]

    def advance_level(self):
        if self.level < 2:  # Máme jen 2 levely
            self.level += 1
            self.hens = self._generate_hens()
            self.egg_spawn_interval = 120
            self.fall_speed = 3
            self.score = 0
            return True
        return False

    def update_score(self, egg_type):
        if egg_type == "white":
            self.score += 1  # Bílé vajíčko přidává 1 bod
            self.white_eggs_collected += 1  # Počítej jen bílá vajíčka
        elif egg_type == "black":
            if self.hearts:
                self.hearts.lose_life()  # Odeber život
            return 'black_egg'  # Specifický návrat pro černé vajíčko
        elif egg_type == "golden":
            self.score += 3  # Zlaté vajíčko přidává 3 body

    def reset_game(self):
        # Resetování všech herních parametrů
        self.score = 0
        # Zachováme aktuální level, abychom neresetovali level na 1
        # self.level zůstává beze změny
        
        self.wolf = Wolf(600, 800)  # Obnovení vlka na výchozí pozici
        self.hens = self._generate_hens()  # Dynamické generování slepic podle aktuálního levelu
        self.eggs = []  # Vyprázdnění seznamu vajíček
        self.egg_spawn_interval = 120  # Obnovení intervalu generování vajíček
        self.egg_spawn_counter = 0  # Reset počítače snímků
        self.fall_speed = 3  # Obnovení rychlosti pádu
        self.white_eggs_collected = 0  # Reset počtu sběraných bílých vajíček

        # Resetování životů, pokud jsou použity
        if self.hearts:
            self.hearts.reset()

        if self.score < 0:
            return 'game_over'  # Pokud skóre klesne pod 0, hra končí
        if self.level == 1 and self.score >= 10:  # První level - 10 bodů
            return 'you_won'
        if self.level == 2 and self.score >= 25:  # Druhý level - 25 bodů
            return 'you_won'
        return None

    def move_wolf(self, direction):
        """Pohyb vlka s přesným omezením v herním poli.

        Args:
            direction (str): Směr pohybu - 'left' nebo 'right'
        """
        game_width = 600  # Šířka herní obrazovky
        wolf_width = 40  # Šířka vlka
        move_speed = 5  # Snížení rychlosti pohybu

        if direction == "left":
            # Pohyb doleva s přesným omezením
            self.wolf.x = max(0, self.wolf.x - move_speed)
            self.wolf.direction = "left"
        elif direction == "right":
            # Pohyb doprava s přesným omezením
            self.wolf.x = min(580 - wolf_width, self.wolf.x + move_speed)
            self.wolf.direction = "right"

    def generate_eggs(self, is_paused=False):
        # Pokud hra není pozastavena
        if not is_paused:
            # Zvýšení počítače snímků
            self.egg_spawn_counter += 1

            # Kontrola, zda je čas na generování vajíček
            if self.egg_spawn_counter >= self.egg_spawn_interval:
                for hen in self.hens:
                    egg_type = random.choices(["black", "white", "golden"], weights=[65, 30, 5])[0]
                    # Generování vajíček přímo od slepice
                    self.eggs.append(Egg(hen.x + 30, hen.y + 80, egg_type))
                # Reset počítače snímků
                self.egg_spawn_counter = 0

    def move_eggs(self):
        for egg in self.eggs:
            egg.fall(self.fall_speed)  # Posouváme vajíčka směrem dolů

    def check_collisions(self):
        wolf_rect = {
            'x': self.wolf.x,
            'y': self.wolf.y,
            'width': 85,  # Aktuální šířka vlka
            'height': 125  # Aktuální výška vlka
        }

        for egg in self.eggs.copy():  # Kopie pro bezpečnou iteraci
            egg_rect = {
                'x': egg.x + 2,  # Malý posun pro přesnější zachycení
                'y': egg.y + 2,
                'width': 18,  # Přesná šířka vajíčka
                'height': 18  # Přesná výška vajíčka
            }

            # Kontrola překrytí obdélníků
            if not (
                    egg_rect['x'] + egg_rect['width'] < wolf_rect['x'] or
                    egg_rect['x'] > wolf_rect['x'] + wolf_rect['width'] or
                    egg_rect['y'] + egg_rect['height'] < wolf_rect['y'] or
                    egg_rect['y'] > wolf_rect['y'] + wolf_rect['height']
            ):
                self.eggs.remove(egg)  # Odstraň chytlé vajíčko
                result = self.update_score(egg.type)  # Přičte body podle typu vajíčka
                if result == 'game_over':
                    return 'game_over'
                elif result == 'you_won':
                    return 'you_won'
                elif result == 'black_egg':
                    if self.hearts and self.hearts.is_game_over():
                        return 'game_over'
        return None

    def update(self):
        self.generate_eggs()  # Generování vajíček
        self.move_eggs()  # Posouváme vajíčka směrem dolů
        result = self.check_collisions()  # Kontrola kolizí s vlkem

        # Kontrola, zda hráč vyhrál podle aktuálního levelu
        if (self.level == 1 and self.score >= 10) or (self.level == 2 and self.score >= 25):
            return 'you_won'
            
        return result