"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import math
from typing import List

import arcade
import arcade.gui

import health.backend
from health import backend

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1024
SCREEN_TITLE = "Vitality Trainer"
FOOD_FILE = "health/data/food.csv"
LAYER_NAME_FOOD = "food"
LAYER_NAME_PLAYER = "player"
PLAYER_MOVEMENT_SPEED = 5
START = 0
STOP = math.pi
CENTER_X = SCREEN_WIDTH / 2
CENTER_Y = SCREEN_HEIGHT / 2
RADIUS = 200


def position_sprites(sprites: List[arcade.Sprite], scene: arcade.Scene):
    degrees = [STOP / len(sprites) * x + START for x in range(0, len(sprites))]
    for i, sprite in enumerate(sprites):
        sprite.center_x = CENTER_X + math.cos(degrees[i]) * RADIUS
        sprite.center_y = CENTER_Y + math.sin(degrees[i]) * RADIUS
        scene.add_sprite(LAYER_NAME_FOOD, sprite)


backend = backend.Backend(FOOD_FILE)


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """
    foodlist: List[health.backend.food]

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.physics_engine = None

        # If you have sprite lists, you should create them here,
        # and set them to None

    def get_food(self):
        self.foodlist = backend.get_food()

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.player = backend.player
        self.scene = arcade.scene.Scene()
        self.get_food()
        position_sprites(self.foodlist, self.scene)
        self.reset_player()
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, [])
        self.on_click_open(None)

    def reset_player(self):
        self.player.center_y = SCREEN_HEIGHT / 2
        self.player.center_x = SCREEN_WIDTH / 2

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        self.scene.draw()
        self.manager.draw()
        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        self.physics_engine.update()
        food_collisions = self.player.collides_with_list(self.scene.get_sprite_list(LAYER_NAME_FOOD))
        for food in food_collisions:
            self.reset_player()
            self.player.eatFood(food)
        if self.player.happiness < 0:
            self.game_over()
        self.get_food()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """

        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """

        pass

    def on_click_open(self, event):
        messagebox = arcade.gui.UIMessageBox(width=300, height=200, message_text="Hello There Vin")
        self.manager.add(messagebox)

    def game_over(self):
        messagebox = arcade.gui.UIMessageBox(width=300, height=200, message_text="You Lost")
        self.manager.add(messagebox)
        self.setup()

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
