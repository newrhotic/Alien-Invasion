import sys
import pygame as pyg

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    #Overall class to manage game assets and behaviour

    def __init__(self):
        #Initialise the game and create its resources
        pyg.init()
        self.settings = Settings()
        self.screen = pyg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pyg.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pyg.sprite.Group()
        self.aliens =pyg.sprite.Group()

        self._create_fleet()

        #Set background colour
        self.bg_color = self.settings.bg_color
    
    def run_game(self):
        #Start the main loop for the game
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()       
    
    def _check_events(self):
    #Reponds to keypresses and mouse events
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    sys.exit()
                elif event.type == pyg.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pyg.KEYUP:
                    self._check_keyup_events(event) 

    def _check_keydown_events(self, event):
        #Respond to key presses
        if event.key == pyg.K_RIGHT:
            #Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pyg.K_LEFT:
            #Move the ship to the left
            self.ship.moving_left = True
        elif event.key == pyg.K_ESCAPE:
            sys.exit()
        elif event.key == pyg.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        #Respond to key reeleases
        if event.key == pyg.K_RIGHT:
            #Stop moving the ship
            self.ship.moving_right = False
        elif event.key == pyg.K_LEFT:
            #Stop moving the ship
            self.ship.moving_left = False

    def _fire_bullet(self):
        #Create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
    #Get rid of bullets and get rid of bullets
            self.bullets.update()       

            #Get rid of bullets that have disappeared  
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

    def _update_aliens(self):
        #Check if the fleet is at an edge, then update the positions of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()

    def _update_screen(self):
    #Update images on the screen and flip to the new screen
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

            # #Make the most recently drawn screen visible
            pyg.display.flip()

    def _create_fleet(self):
        #create the fleet of aliens
        #Create an alien and find the number of aliens in a row
        #Spacing between each alien is equal to one alien width

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create full fleet os aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
                

    def _create_alien(self, alien_number, row_number):
        #Create alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        #Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        #Drop the entire fleet and chenge the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
            self.settings.fleet_drop_speed *= -1

if __name__ == "__main__":
    #Make instance and run the game
    ai = AlienInvasion()
    ai.run_game()