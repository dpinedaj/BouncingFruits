from entities import Player, Canvas
from modules import Game, Network

if __name__ == "__main__":
    g = Game(Network("localhost", 15000), Player,
             Canvas,
             500, 500, "game")
    g.run()
