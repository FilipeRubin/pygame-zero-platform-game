import pgzrun
import random

WIDTH = 512
HEIGHT = 448

class Character:
    def __init__(self):
        self.actor = Actor('character')
        self.speed = 5.0
    
    def draw(self):
        self.actor.draw()
    
    def update(self, input):
        if input.left:
            self.actor.x -= self.speed
        if input.right:
            self.actor.x += self.speed
        if input.up:
            self.actor.y -= self.speed
        if input.down:
            self.actor.y += self.speed
    
class Tile:
    def __init__(self, pos):
        self.actor = Actor('tile')
        self.actor.pos = pos
    
    def draw(self):
        self.actor.draw()

def create_tiles_from_tileset(tileset):
    result = []
    for y in range(len(tileset)):
        for x in range(len(tileset[y])):
            if tileset[y][x] == 1:
                result.append(Tile(((x * 32) + 16, (y * 32) + 16)))
    return result

background = Actor('background')
character = Character()

tileset = [
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
]
tiles = create_tiles_from_tileset(tileset)

def draw():
    background.draw()
    for tile in tiles:
        tile.draw()
    character.draw()

def update():
    character.update(keyboard)

pgzrun.go()