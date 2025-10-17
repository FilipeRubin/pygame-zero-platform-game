import pgzrun
import random

WIDTH = 512
HEIGHT = 448

mouse_pos = (0, 0)

current_scene = None

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
        pass
    
    def draw(self):
        screen.clear()
    
    def update(self, dt):
        pass
    
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