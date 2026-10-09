from random import Random
from ursina import Entity, Vec3, color


class SpaceBackground(Entity):
    def __init__(self, star_count=350):
        super().__init__()

        rng = Random(42)

        star_colors = [
            color.rgb(255, 255, 255),
            color.rgb(180, 210, 255),
            color.rgb(160, 190, 255),
            color.rgb(255, 235, 200),
        ]

        for _ in range(star_count):
            x = rng.uniform(-300, 300)
            y = rng.uniform(-180, 180)
            z = rng.uniform(-100, 650)

            size = rng.uniform(0.15, 0.65)

            Entity(
                parent=self,
                model='sphere',
                position=Vec3(x, y, z),
                scale=size,
                color=rng.choice(star_colors),
                unlit=True,
            )