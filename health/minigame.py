import arcade

MOVE_SCALE = 50


class LightningBolt(arcade.Sprite):
    damage = 5

    def __init__(self):
        filename: str = "health/imgs/bolt.png"
        super().__init__(filename)


class MiniGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.change_x = 0
        self.change_y = 0

    def on_update(self, delta_time: float):
        self.player.change_y = self.change_y * delta_time * MOVE_SCALE
        self.player.change_x = self.change_x * delta_time * MOVE_SCALE

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self.change_y = self.player.getSpeed()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.change_y = -self.player.getSpeed()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.change_x = -self.player.getSpeed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.change_x = self.player.getSpeed()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.change_x = 0
