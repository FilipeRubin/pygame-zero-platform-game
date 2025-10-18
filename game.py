import time
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

import pgzrun
import random

WIDTH = 512
HEIGHT = 448

mouse_pos = (0, 0)

current_scene = None
music_on: bool = True

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
    
    def create_player(self):
        for y in range(len(self.tileset_array)):
            for x in range(len(self.tileset_array[y])):
                if self.tileset_array[y][x] == 3:
                    return Character(self, ((x * 32) + 16, (y * 32) + 16))
        return None
    
    def create_enemies(self):
        result = []
        for y in range(len(self.tileset_array)):
            for x in range(len(self.tileset_array[y])):
                if self.tileset_array[y][x] == 2:
                    result.append(Enemy(((x * 32) + 16, (y * 32) + 8)))
        return result
    
    def create_item(self):
        for y in range(len(self.tileset_array)):
            for x in range(len(self.tileset_array[y])):
                if self.tileset_array[y][x] == 4:
                    return Item(((x * 32) + 16, (y * 32) + 16))
        return None
    
    def has_tile_at_position(self, pos):
        index_x: int = int(pos[0] / 32.0)
        index_y: int = int(pos[1] / 32.0)
        
        if index_x < 0 or index_y < 0 or index_y >= len(self.tileset_array) or index_x >= len(self.tileset_array[index_y]):
            return False
        
        return True if (self.tileset_array[index_y][index_x] == 1) else False

class Enemy:
    def __init__(self, pos):
        self.actor = Actor('enemy')
        self.actor.pos = pos
    
    def draw(self):
        self.actor.draw()

class Lives:
    def __init__(self, pos):
        self.actor = Actor('heart')
        self.actor.pos = pos
        self.amount = 3
    
    def draw(self):
        initial_x = self.actor.x
        self.actor.x -= 16
        for i in range(self.amount):
            self.actor.x += 16
            self.actor.draw()
        self.actor.x = initial_x
    
    def hurt(self):
        if self.amount > 0:
            self.amount -= 1

class Item:
    def __init__(self, pos):
        self.actor = Actor('item')
        self.actor.pos = pos
        self.sprite_animation_length = 15
        self.sprite_animation_frames_passed = 0
    
    def draw(self):
        self.sprite_animation_frames_passed += 1
        if self.sprite_animation_frames_passed >= self.sprite_animation_length:
            if self.actor.image == 'item':
                self.actor.image = 'item2'
            elif self.actor.image == 'item2':
                self.actor.image = 'item'
            self.sprite_animation_frames_passed = 0
        self.actor.draw()

class Character:
    def __init__(self, tileset, pos):
        self.actor = Actor('character')
        self.actor.pos = pos
        self.starting_pos = pos
        self.speed = 2.0
        self.gravity = 0.5
        self.jump_force = 10.0
        self.y_vel = 0.0
        self.tileset = tileset
        self.is_on_floor = False
        self.is_on_ceiling = False
    
    def draw(self):
        self.actor.draw()
    
    def update(self):
        if self.is_on_floor:
            self.y_vel = 0.0
            if keyboard.z:
                self.y_vel = -self.jump_force
        else:
            if self.is_on_ceiling:
                self.y_vel = 0.0
            self.y_vel += self.gravity
        
        vel = [0.0, self.y_vel]
        if keyboard.left:
            vel[0] -= self.speed
        if keyboard.right:
            vel[0] += self.speed
        
        self.apply_movement(vel)
    
    def respawn(self):
        self.actor.pos = self.starting_pos
        self.y_vel = 0.0
        self.is_on_ceiling = False
        self.is_on_floor = False
    
    def apply_movement(self, vel):
        self.apply_vertical_collision(vel)
        self.apply_horizontal_collision(vel)
    
    def apply_vertical_collision(self, vel):
        side = 0
        
        if vel[1] > 0.0:
            side = 1
        elif vel[1] < 0.0:
            side = -1
        
        p1 = self.actor.bottomleft if side == 1 else self.actor.topleft
        p2 = self.actor.bottomright if side == 1 else self.actor.topright
        p1 = (p1[0] + 1, p1[1])
        p2 = (p2[0] - 1, p2[1])
        t1 = self.tileset.has_tile_at_position(p1)
        t2 = self.tileset.has_tile_at_position(p2)
        
        if not t1 and not t2:
            self.actor.y += vel[1]
            self.is_on_floor = False
            self.is_on_ceiling = False
        elif side == 1:
            self.actor.midbottom = (self.actor.midbottom[0], self.actor.midbottom[1] - (self.actor.midbottom[1] % 32))
            self.is_on_floor = True
        elif side == -1:
            side_y = self.actor.top
            self.actor.midbottom = (self.actor.midbottom[0], self.actor.midbottom[1] - (self.actor.midbottom[1] % 32) - (side_y - self.actor.midbottom[1]) + 1)
            self.is_on_ceiling = True
        
    def apply_horizontal_collision(self, vel):
        side = 0
        
        if vel[0] > 0.0:
            side = 1
        elif vel[0] < 0.0:
            side = -1
        
        p1 = self.actor.topright if side == 1 else self.actor.topleft
        p2 = self.actor.bottomright if side == 1 else self.actor.bottomleft
        p1 = (p1[0], p1[1] + 1)
        p2 = (p2[0], p2[1] - 1)
        t1 = self.tileset.has_tile_at_position(p1)
        t2 = self.tileset.has_tile_at_position(p2)
        
        if not t1 and not t2:
            self.actor.x += vel[0]
        elif side == 1:
            side_x = self.actor.right
            self.actor.midbottom = (self.actor.center[0] - (self.actor.center[0] % 32) + 32 - (side_x - self.actor.center[0]), self.actor.midbottom[1])
        elif side == -1:
            side_x = self.actor.left
            self.actor.midbottom = (self.actor.center[0] - (self.actor.center[0] % 32) - 1 - (side_x - self.actor.center[0]), self.actor.midbottom[1])

class MainMenuButton:
    def __init__(self, text, pos, on_pressed):
        x, y = pos
        self.text = text
        self.pos = pos
        self.rect = Rect((x - 40, y - 14), (80, 28))
        self.on_pressed = on_pressed
    
    def draw(self, color, owidth=0):
        screen.draw.text(self.text, center=self.pos, color=color, ocolor='black', owidth=owidth, fontsize=32)

class GameScene:
    def __init__(self):
        tileset_array = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.tileset = TileSet(tileset_array)
        self.enemies = self.tileset.create_enemies()
        self.character = self.tileset.create_player()
        self.item = self.tileset.create_item()
        self.lives = Lives((16, 16))
    
    def draw(self):
        screen.clear()
        self.tileset.draw()
        self.character.draw()
        self.lives.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.item.draw()
    
    def update(self, dt):
        self.character.update()
        for enemy in self.enemies:
            if self.character.actor.colliderect(enemy.actor):
                self.lives.hurt()
                if self.lives.amount > 0:
                    self.character.respawn()
                else:
                    global current_scene
                    current_scene = LossScene()
                break
        if self.character.actor.colliderect(self.item.actor):
            current_scene = VictoryScene()
    
    def on_key_down(self, key):
        pass

def on_play_pressed():
    global current_scene
    current_scene = GameScene()

def on_music_pressed():
    global music_on
    music_on = not music_on

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
        self.buttons[1].text = 'Music on' if music_on else 'Music off'
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

class VictoryScene:
    def __init__(self):
        self.background = Actor('background-victory')
    
    def draw(self):
        self.background.draw()
        screen.draw.text('Congratulations!\nYou are now free from the monsters!\n\nPress Enter to continue...', center=(WIDTH/2, HEIGHT/2), color='white', fontsize=30, align='center')
    
    def update(self, dt):
        pass
    
    def on_key_down(self, key):
        if key == keys.RETURN:
            global current_scene
            current_scene = MainMenuScene()

class LossScene:
    def __init__(self):
        self.background = Actor('background-loss')
    
    def draw(self):
        self.background.draw()
        screen.draw.text('You did well, but the enemies did better.\nGood luck next time!\n\nPress Enter to continue...', center=(WIDTH/2, HEIGHT/2), color='white', fontsize=30, align='center')
    
    def update(self, dt):
        pass
    
    def on_key_down(self, key):
        if key == keys.RETURN:
            global current_scene
            current_scene = MainMenuScene()

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