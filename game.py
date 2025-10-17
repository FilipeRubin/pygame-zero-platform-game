import pgzrun
import random

WIDTH = 512
HEIGHT = 448

mouse_pos = (0, 0)

current_scene = None

class Tile:
    def __init__(self, pos):
        self.actor = Actor('tile')
        self.actor.pos = pos
    
    def draw(self):
        self.actor.draw()

class TileSet:
    def __init__(self, tileset_array):
        self.tileset_array = tileset_array
        self.tiles = self.create_tiles()
    
    def draw(self):
        for tile in self.tiles:
            tile.draw()
    
    def create_tiles(self):
        result = []
        for y in range(len(self.tileset_array)):
            for x in range(len(self.tileset_array[y])):
                if self.tileset_array[y][x] == 1:
                    result.append(Tile(((x * 32) + 16, (y * 32) + 16)))
        return result
    
    def has_tile_at_position(self, pos):
        index_x: int = int(pos[0] / 32.0)
        index_y: int = int(pos[1] / 32.0)
        
        if index_x < 0 or index_y < 0 or index_y >= len(self.tileset_array) or index_x >= len(self.tileset_array[index_y]):
            return False
        
        return True if (self.tileset_array[index_y][index_x] != 0) else False

class Character:
    def __init__(self, tileset):
        self.actor = Actor('character')
        self.speed = 5.0
        self.tileset = tileset
    
    def draw(self):
        self.actor.draw()
    
    def update(self):
        vel = [0.0, 0.0]
        if keyboard.left:
            vel[0] -= self.speed
        if keyboard.right:
            vel[0] += self.speed
        if keyboard.up:
            vel[1] -= self.speed
        if keyboard.down:
            vel[1] += self.speed
        
        self.apply_movement(vel)
    
    def apply_movement(self, vel):
        if not self.tileset.has_tile_at_position((self.actor.x + vel[0], self.actor.y + vel[1])):
            self.actor.x += vel[0]
            self.actor.y += vel[1]

class MainMenuButton:
    def __init__(self, text, pos, on_pressed):
        x, y = pos
        self.text = text
        self.pos = pos
        self.rect = Rect((x - 40, y - 14), (80, 28))
        self.on_pressed = on_pressed
    
    def draw(self, color, owidth=0):
        screen.draw.text(self.text, center=self.pos, color=color, ocolor='black', owidth=owidth, fontsize=32)
        screen.draw.rect(self.rect, 'green')

class GameScene:
    def __init__(self):
        tileset_array = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        self.tileset = TileSet(tileset_array)
        self.character = Character(self.tileset)
    
    def draw(self):
        screen.clear()
        self.tileset.draw()
        self.character.draw()
    
    def update(self, dt):
        self.character.update()
    
    def on_key_down(self, key):
        pass

def on_play_pressed():
    global current_scene
    current_scene = GameScene()

def on_music_pressed():
    print('music!')

def on_quit_pressed():
    quit()

class MainMenuScene:
    def __init__(self):
        self.background = Actor('background')
        self.buttons = [
            MainMenuButton('Play', (256, 196), on_play_pressed),
            MainMenuButton('Music', (256, 224), on_music_pressed),
            MainMenuButton('Quit', (256, 252), on_quit_pressed)
        ]
        self.selected_button_index = 0
        self.last_mouse_pos = mouse_pos
    
    def draw(self):
        self.background.draw()
        for i in range(len(self.buttons)):
            if i == self.selected_button_index:
                self.buttons[i].draw('orange', 1)
            else:
                self.buttons[i].draw('white')
    
    def update(self, dt):
        if self.last_mouse_pos != mouse_pos:
            for i in range(len(self.buttons)):
                if self.buttons[i].rect.collidepoint(mouse_pos):
                    self.selected_button_index = i
                    break
        self.last_mouse_pos = mouse_pos
    
    def on_key_down(self, key):
        if key == keys.UP:
            self.selected_button_index -= 1
            if self.selected_button_index < 0:
                self.selected_button_index = len(self.buttons) - 1
        elif key == keys.DOWN:
            self.selected_button_index += 1
            if self.selected_button_index >= len(self.buttons):
                self.selected_button_index = 0
        elif key == keys.RETURN:
            self.buttons[self.selected_button_index].on_pressed()

current_scene = MainMenuScene()

def draw():
    current_scene.draw()

def update(dt):
    current_scene.update(dt)

def on_key_down(key):
    current_scene.on_key_down(key)

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

pgzrun.go()