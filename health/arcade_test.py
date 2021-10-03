"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import math
from time import sleep
from typing import List

import arcade
import arcade.gui

from health import backend
from health.backend import STATUS

FONT = "Papyrus"
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Vitality Trainer"
FOOD_FILE = "health/data/food.csv"
ACTIONS_FILE = "health/data/ActionEvents.csv"
DAILY_FILE = "health/data/DailyBrief.csv"
LAYER_NAME_FOOD = "food"
LAYER_NAME_PLAYER = "player"
LAYER_NAME_HEALTHBAR = "bar"
LAYER_NAME_TEXT = "text"
LAYER_NAME_STATUS = "status"

START = 0
STOP = math.pi
CENTER_X: int = int(SCREEN_WIDTH / 2)
CENTER_Y: int = int(SCREEN_HEIGHT / 2)
INDENT_X: int = 400
INDENT_Y: int = 0
BALLOON_START: int = 400
STATUS_Y: int = 900
OFFSET_STATUS_X: int = 200


def position_sprites(sprites: List[arcade.Sprite]):
    results = arcade.SpriteList()
    if len(sprites) > 1:
        spacing = int(INDENT_X * 2 / (len(sprites) - 1))
        positions = list(range(int(CENTER_X - INDENT_X), int(CENTER_X + INDENT_X + spacing),
                               spacing))
    else:
        positions = [CENTER_X]
    for i, sprite in enumerate(sprites):
        sprite.center_x = positions[i]
        sprite.center_y = CENTER_Y + INDENT_Y
        results.append(sprite)
    return results


class Intro(arcade.View):
    def __init__(self, window):
        super().__init__(window)

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.RED, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame(self.window)
        game_view.setup()
        self.window.show_view(game_view)


class MyGame(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """
    foodlist: List[backend.food]
    manager: arcade.gui.UIManager
    player: backend.player
    scene: arcade.Scene
    FOOD_PLACED: bool = False
    BAR_PLACED: bool = False
    gameBackend: backend.Backend
    healthSprite: arcade.Sprite
    healthBar: backend.healthBar
    SETUP: bool
    TEXT_PLACED: bool = False

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        arcade.set_background_color(arcade.color.WHITE)
        self.gameBackend = backend.Backend(FOOD_FILE, ACTIONS_FILE, DAILY_FILE)
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.player = self.gameBackend.get_player()
        self.scene = arcade.scene.Scene()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.scene.add_sprite_list(LAYER_NAME_PLAYER, sprite_list=self.player_list)
        self.healthBar = backend.healthBar(self.player)
        self.getBar()
        self.generate_text()

        # If you have sprite lists, you should create them here,
        # and set them to None

    def get_events(self):
        if self.FOOD_PLACED:
            self.scene.remove_sprite_list_by_name(LAYER_NAME_FOOD)
            self.scene.remove_sprite_list_by_name(LAYER_NAME_STATUS)
        items = self.gameBackend.get_events()
        foodlist = items[0]
        dayStatus = items[1]
        dayStatus.center_x = CENTER_X + OFFSET_STATUS_X
        dayStatus.center_y = STATUS_Y
        self.scene.add_sprite_list_after(LAYER_NAME_FOOD, LAYER_NAME_PLAYER,
                                         sprite_list=position_sprites(
                                             foodlist))
        self.scene.add_sprite(LAYER_NAME_STATUS, dayStatus)
        self.FOOD_PLACED = True

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

    def getBar(self):
        if self.BAR_PLACED:
            self.scene.remove_sprite_list_by_name(LAYER_NAME_HEALTHBAR)
        self.healthBar.get_image()
        self.healthSprite = self.healthBar.sprite
        self.healthSprite.center_x = (self.healthSprite.width / 2) + 20
        self.healthSprite.center_y = self.healthSprite.height / 2 + 27
        self.scene.add_sprite(LAYER_NAME_HEALTHBAR, self.healthSprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        self.manager.draw()
        self.scene.draw()
        # Call draw() on all your sprite lists below

    def generate_text(self):
        if self.TEXT_PLACED:
            self.scene.remove_sprite_list_by_name(LAYER_NAME_TEXT)
        text = arcade.text_pillow.create_text_sprite(self.gameBackend.get_motivation_text(),
                                                     self.healthSprite.center_x - 45,
                                                     self.healthSprite.center_y - 20,
                                                     color=arcade.color.WHITE,
                                                     font_size=20, width=INDENT_X,
                                                     font_name=FONT)
        text2 = arcade.text_pillow.create_text_sprite(self.gameBackend.get_day_text(),
                                                      SCREEN_WIDTH - INDENT_X,
                                                      40,
                                                      color=arcade.color.RED,
                                                      font_size=20, width=INDENT_X,
                                                      font_name=FONT)

        self.scene.add_sprite(LAYER_NAME_TEXT, text)
        self.scene.add_sprite(LAYER_NAME_TEXT, text2)
        self.TEXT_PLACED = True

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.event_handler(True)

    def event_handler(self, DAILY):
        event = self.gameBackend.event()
        if event is STATUS.DAILY and DAILY:
            new_view = DailyView(self.gameBackend, self)
            self.window.show_view(new_view)
        elif event is STATUS.WON:
            minigame = MiniGame(self.gameBackend, self.window, self)
            self.window.show_view(minigame)
        elif event is STATUS.SELECT:
            self.get_events()
            self.getBar()
            self.generate_text()
        elif event is STATUS.LOSS:
            gameover = GameOver(self)
            self.window.show_view(gameover)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        self.player.center_y = y
        self.player.center_x = x

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if self.FOOD_PLACED:
            food_collisions = self.player.collides_with_list(
                self.scene.get_sprite_list(LAYER_NAME_FOOD))
            if len(food_collisions) >= 1:
                self.gameBackend.process(food_collisions[0])
                if len(food_collisions) > 1:
                    print("Multiple collision")
        self.event_handler(True)
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """

        pass

    def release_all(self):
        self.change_y = 0
        self.change_x = 0
        self.window.set_mouse_visible(False)


class DailyView(arcade.View):
    def __init__(self, backend: backend.Backend, gameView: MyGame):
        super().__init__()
        self.backend = backend
        self.game_view = gameView
        self.messages = arcade.SpriteList()
        day = self.backend.getDay()
        day.center_x = SCREEN_WIDTH / 2
        day.center_y = SCREEN_HEIGHT / 2
        self.messages.append(day)

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        self.messages.draw()
        # arcade.draw_text(self.backend.get_day_text(), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        #                 arcade.color.RED, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 600,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.game_view.release_all()
        self.backend.daily()
        self.window.show_view(self.game_view)


class GameOver(arcade.View):
    def __init__(self, GameView):
        super().__init__()
        self.GameView = GameView

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to exit", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        exit()


class MiniGame(arcade.View):
    def __init__(self, backend, window, GameView):
        super().__init__(window)
        self.GameView = GameView

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Minigame Placeholder", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        next_view = GameEnd(self)
        self.window.show_view(next_view)


class GameEnd(arcade.View):
    def __init__(self, GameView):
        super().__init__()
        self.GameView = GameView

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("YOU WON!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to exit", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        exit()


def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, vsync=True, fullscreen=True)
    game = Intro(window)
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
