import csv
from typing import List

import arcade
from PIL import Image

MOVE_SCALE = 200
GRAVITY = (0, -1500)
ENEMY_SCALE = 200
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Vitality Trainer"
DAMPING = 0.4
ENEMY_FILE = "health/data/enemies.csv"
ACTIONS_FILE = "health/data/ActionEvents.csv"
DAILY_FILE = "health/data/DailyBrief.csv"
FOOD_FILE = "health/data/food.csv"
LAYER_NAME_ENEMIES = "enemies"
LAYER_NAME_PLAYER = "player"
PLAYER_JUMP_IMPULSE = 1800


class enemy(arcade.Sprite):
    name: str
    image_file: str
    start_x: int
    start_y: int
    move_x: int
    move_y: int
    secs: int
    rendered: bool = False

    def __init__(self, line: List[str]):
        self.name = line[0]
        self.image_file = line[1]
        self.start_x = int(line[2])
        self.start_y = int(line[3])
        self.move_x = int(line[4])
        self.move_y = int(line[5])
        self.secs = int(line[6])
        filename = f"health/imgs/{self.image_file}"
        scale = ENEMY_SCALE / Image.open(filename).size[0]
        super().__init__(filename, scale=scale)


def read_enemy(filename: str) -> List[enemy]:
    results = []
    with open(filename) as file:
        rows = csv.reader(file)
        for row in rows:
            if not row:
                break
            results.append(enemy(row))
    return results


class LightningBolt(arcade.Sprite):
    damage = 5

    def __init__(self):
        filename: str = "health/imgs/bolt.png"
        super().__init__(filename)


class MiniGame(arcade.View):
    def __init__(self, backend, window, GameView, GameOver, GameEnd):
        super().__init__()
        self.backend = backend
        self.enemies_list = read_enemy(ENEMY_FILE)
        self.change_y = 0
        self.GameView = GameView
        self.GameEnd = GameEnd
        self.GameOver = GameOver
        self.health = int(backend.player.health + backend.player.motivation / 2) - 4
        self.player = self.backend.player
        arcade.set_background_color(arcade.color.WHITE)
        self.scene = arcade.Scene()
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player)
        self.walls = arcade.SpriteList()
        for x in range(0, SCREEN_WIDTH, 400):
            floor = arcade.Sprite("health/imgs/floor.jpg")
            floor.center_x = x + 200
            floor.center_y = 160
            self.walls.append(floor)
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = 320
        self.physics = arcade.PymunkPhysicsEngine(damping=DAMPING, gravity=GRAVITY)
        self.physics.add_sprite(self.player, collision_type="player")
        self.physics.add_sprite_list(self.walls, collision_type="walls",
                                     body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.current_time = 0
        self.last_time = 0
        self.enemies = arcade.SpriteList()

    def render_enemies(self):
        timeDelta = self.current_time - self.last_time
        self.last_time = self.current_time
        for enemy in self.enemies:
            enemy.change_x = enemy.change_x
            enemy.change_y = enemy.change_y
        completed = True
        for enemy in self.enemies_list:
            if not enemy.rendered:
                completed = False
                if self.current_time > enemy.secs:
                    enemy.center_x = enemy.start_x + (
                            self.current_time - enemy.secs) * enemy.move_x
                    enemy.center_y = enemy.start_y + (
                            self.current_time - enemy.secs) * enemy.move_y
                    enemy.rendered = True
                    enemy.change_x = enemy.move_x
                    enemy.change_y = enemy.move_y
                    self.enemies.append(enemy)
        if completed:
            self.game_end()

    def on_update(self, delta_time: float):
        self.player.change_y = self.change_y * delta_time
        self.current_time += delta_time
        collisions = self.player.collides_with_list(self.enemies)
        for collision in collisions:
            self.health -= 1
            if self.health < 1:
                self.game_over()
            self.enemies.remove(collision)
        self.render_enemies()
        self.physics.step(delta_time=delta_time)
        self.enemies.update()

    def on_draw(self):
        arcade.start_render()
        self.scene.draw()
        self.enemies.draw()
        self.walls.draw()
        arcade.draw_text(f"Health: {self.health}", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100,
                         arcade.color.RED, font_size=20, anchor_x="right")

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
secs
        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """

        if key == arcade.key.UP:
            # find out if player is standing on ground
            if self.physics.is_on_ground(self.player):
                # She is! Go ahead and jump
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics.apply_impulse(self.player, impulse)
        if key == arcade.key.ESCAPE:
            exit()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self.change_y = 0

    def game_end(self):
        next_screen = self.GameEnd(self)
        self.window.show_view(next_screen)

    def game_over(self):
        next_screen = self.GameOver(self)
        self.window.show_view(next_screen)


def test():
    from health.arcade_test import GameEnd, GameOver
    from health.backend import Backend
    backend = Backend(FOOD_FILE, ACTIONS_FILE, DAILY_FILE)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, vsync=True, fullscreen=True)
    game = MiniGame(backend, window, None, GameOver, GameEnd)
    window.show_view(game)
    arcade.run()


if __name__ == '__main__':
    test()
