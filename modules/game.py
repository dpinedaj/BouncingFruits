import pygame
import json
import random
import os
from .utils import load_image

class Game:

    def __init__(self, network, Player, Canvas, width, height, title):
        self.players = {}
        self.all_sprites = pygame.sprite.Group()

        self.PlayerClass = Player
        self.net = network
        self.width = width
        self.height = height
        self.fruits_path = os.path.join(os.path.abspath(".") , "assets", "fruits")
        self.images = [os.path.join(self.fruits_path, p) for p in os.listdir(self.fruits_path)]
        self.image_ind = int(self.net.id) % len(self.images)
        self.player_image = load_image(self.images[self.image_ind])
        self.player = self.PlayerClass(random.randint(50,450),
                    random.randint(50, 450), 
                    image = self.player_image)
        self.canvas = Canvas(self.width, self.height, title)
        
        self.run_game = True
        self.events = True

    

    def send_data(self, exit_game=False):
        """
        Send position to server
        :return: None
        """
        if exit_game:
            data = json.dumps({"exit": self.net.id})
        else:
            data = json.dumps({self.net.id: [str(self.player.rect.x), str(self.player.rect.y)]})
        reply = self.net.send(data)
        return reply

    def position_players(self):
        json_data = self.send_data()
        if not json_data:
            return
        data = json.loads(json_data) 
        data.pop(self.net.id)
        
        self.canvas.draw_background()
        self.player.draw(self.canvas.get_canvas())
        for key in data.keys():
            arr = [int(i) for i in data[key]]
            if key in self.players:
                player = self.players[key]
                player.rect.x, player.rect.y = arr
            else:
                image_ind = int(key) % len(self.images)
                player = self.PlayerClass(*arr, image=load_image(self.images[image_ind]))
                self.players[key] = player
                self.all_sprites.add(player)

            self.player.handle_collisions(player)
            player.draw(self.canvas.get_canvas())
            
        self.canvas.update()
        
    
    def close_player(self):
        self.send_data(exit_game=True)
        self.run_game = False
        self.events = False

    def run(self):
        clock = pygame.time.Clock()
        try:
            while self.run_game:
                clock.tick(60)

                for event in pygame.event.get():
                    if event.type in (pygame.QUIT, pygame.K_ESCAPE):
                        self.close_player()

                if self.events:
                    self.player.handle_keys(self.width, self.height)
                    # Send Network Stuff
                    self.position_players()
        except KeyboardInterrupt:
            self.close_player()
        pygame.quit()


        


