from math import sin, cos, radians
from ursina import Entity, Vec3, color, held_keys, time, clamp


class Aircraft(Entity):
    """Simple arcade aircraft. Heading 0 points along positive Z."""

    def __init__(self):
        super().__init__(position=(0, 3, 0))
        self.speed = 9.0
        self.heading = 0.0
        self.pitch = 0.0
        self._build_model()

    def _build_model(self):
        # Colores principales
        body = color.hex('#778899')
        #body = color.red
        cockpit = color.hex('#1478B4')
        wing_details = color.hex('#E34C4C')
        
        #cockpit = color.rgb(18, 52, 88)        # Azul oscuro
        #wing_details = color.rgb(227, 76, 76)  # Rojo

        # Fuselaje principal
        Entity(
            parent=self,
            model='cube',
            color=body,
            scale=(0.7, 0.35, 2.6)
        )

        # Cabina
        Entity(
            parent=self,
            model='cube',
            color=cockpit,
            scale=(0.42, 0.2, 0.8),
            position=(0, 0.23, 0.45)
        )

        # Alas principales
        Entity(
            parent=self,
            model='cube',
            color=body,
            scale=(3.1, 0.12, 0.65),
            position=(0, 0, -0.2)
        )

        # Estabilizador horizontal
        Entity(
            parent=self,
            model='cube',
            color=body,
            scale=(1.3, 0.12, 0.4),
            position=(0, 0.05, -1.05)
        )

        # Estabilizador vertical
        Entity(
            parent=self,
            model='cube',
            color=body,
            scale=(0.13, 0.85, 0.45),
            position=(0, 0.42, -1.05)
        )

        # Motor trasero
        Entity(
            parent=self,
            model='cube',
            color=color.orange,
            scale=(0.35, 0.12, 0.1),
            position=(0, 0, -1.35)
        )

        # Detalles rojos en las puntas de las alas
        Entity(
            parent=self,
            model='cube',
            color=wing_details,
            scale=(0.35, 0.13, 0.68),
            position=(-1.35, 0, -0.2)
        )

        Entity(
            parent=self,
            model='cube',
            color=wing_details,
            scale=(0.35, 0.13, 0.68),
            position=(1.35, 0, -0.2)
        )
        
    def update(self):
        dt = min(time.dt, .05)
        yaw_input = held_keys['right arrow'] - held_keys['left arrow']
        vertical_input = held_keys['up arrow'] - held_keys['down arrow']
        self.heading += yaw_input * 75 * dt
        self.pitch = clamp(self.pitch + vertical_input * 55 * dt, -35, 35)
        self.rotation_y = self.heading
        self.rotation_x = -self.pitch
        heading_rad = radians(self.heading)
        pitch_rad = radians(self.pitch)
        direction = Vec3(sin(heading_rad) * cos(pitch_rad), sin(pitch_rad), cos(heading_rad) * cos(pitch_rad))
        self.position += direction * self.speed * dt
        self.y = clamp(self.y, 1.5, 40)
