import pygame
import random
from Wolf import Wolf
from Hen import Hen
from Egg import Egg
from Hearts import Hearts

class Level2:
    def __init__(self, screen, hearts=None):
        self.screen = screen
        self.hearts = hearts if hearts else Hearts(screen)
        
        # Konfigurace pro druhý level
        self.wolf = Wolf(300, 700)
        
        # Tři slepice v druhém levelu - zarovnány na mraky v pozadí
        self.hens = [
            Hen(20, 100),    # Levá slepice - více doleva na mrak
            Hen(280, 150),   # Prostřední slepice - více doleva, aby byla na mraku
            Hen(380, 100)    # Pravá slepice - více doleva, aby byla na mraku
        ]
        
        # Prázdný seznam vajec
        self.eggs = []
        
        # Skóre začíná na 0
        self.score = 0
        
        # Nastavení obtížnosti pro druhý level
        self.egg_drop_frequency = 0.02     # Vyšší frekvence házení vajec
    
    def update(self):
        # Pohyb vlka
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.wolf.move_left()
        if keys[pygame.K_RIGHT]:
            self.wolf.move_right()
        
        # Házení vajec slepicemi
        for hen in self.hens:
            if random.random() < self.egg_drop_frequency:
                new_egg = hen.drop_egg()
                if new_egg:
                    self.eggs.append(new_egg)
        
        # Aktualizace vajec
        for egg in self.eggs[:]:
            egg.fall()
            
            # Kontrola kolize vajec s vlkem
            if self.wolf.catch_egg(egg):
                self.eggs.remove(egg)
                self.score += 1
            
            # Odebrání vajec mimo obrazovku
            if egg.y > 800:
                self.eggs.remove(egg)
                self.hearts.decrease()
        
        # Kontrola herního stavu
        if self.hearts.current_hearts <= 0:
            return 'game_over'
        
        # Postup do dalšího levelu nebo výhra
        if self.score >= 25:
            return 'you_won'
        
        return None