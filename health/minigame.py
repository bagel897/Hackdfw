import arcade


class LightningBolt(arcade.Sprite):
    damage = 5

    def __init__(self):
        filename: str = "health/imgs/bolt.png"
        super().__init__(filename)
