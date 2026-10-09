from ursina import Entity, Text, Button, Vec3, color, camera, time, held_keys, lerp, Sky, window
from aircraft import Aircraft
from checkpoints import CheckpointCourse
from math import radians, sin, cos
from space_background import SpaceBackground

class FlightGame(Entity):
    def __init__(self):
        super().__init__()
        #Sky(color=color.rgb(95, 158, 208))
        camera.clip_plane_far = 1000
        self.aircraft = Aircraft()
        self.course = CheckpointCourse()
        self.space_background = SpaceBackground()
        self.state = 'menu'
        self.aircraft.enabled = False
        self.elapsed = 0.0
        self.completed = False
        '''
        Entity(
            model='plane',
            scale=(450, 1, 450),
            color=color.rgb(80, 130, 92),
            double_sided=True
        )
        '''
        #self.hud = Text(position=(-.85, .45), scale=1.2, color=color.white)
        self.hud_panel = Entity(
            parent=camera.ui,
            model='quad',
            position=(-0.60, 0.405, 0.01),
            scale=(0.52, 0.17),
            color=color.hex('#081120'),
            #unlit=True,
            enabled=False
        )
        #self.message = Text(text='', origin=(0, 0), scale=2, color=color.yellow)

        self.hud = Text(
            parent=camera.ui,
            text='',
            position=(-0.84, 0.465, -0.01),
            scale=0.85,
            color=color.white,
            enabled=False
        )

        # Pantalla de inicio sobre el escenario 3D
        self.menu_panel = Entity(
            parent=camera.ui,
            model='quad',
            position=(0, 0.05, 0.01),
            scale=(0.72, 0.48),
            color=color.hex('#0C192D'),
            unlit=True
        )

        self.menu_title = Text(
            parent=camera.ui,
            text='MINI FIGHTER 3D',
            origin=(0, 0),
            position=(0, 0.21),
            scale=2,
            color=color.azure
        )

        self.menu_controls = Text(
            parent=camera.ui,
            text='ARROW LEFT / RIGHT: TURN\n'
                'ARROW UP / DOWN: CLIMB / DIVE\n'
                'R: RESTART',
            origin=(0, 0),
            position=(0, 0.04),
            scale=0.9,
            color=color.white
        )

        self.start_button = Button(
            parent=camera.ui,
            text='START MISSION',
            position=(0, -0.11, -0.02),
            scale=(0.30, 0.07),
            color=color.hex('#2387AF'),
            highlight_color=color.hex('#37AFD7'),
            text_color=color.white,
            on_click=self.start_game
        )

        # Pantalla final, inicialmente oculta
        self.finish_panel = Entity(
            parent=camera.ui,
            model='quad',
            position=(0, 0, 0.01),
            scale=(0.7, 0.35),
            color=color.hex('#0C192D'),
            unlit=True,
            enabled=False
        )

        self.finish_text = Text(
            parent=camera.ui,
            text='',
            origin=(0, 0),
            position=(0, 0.05, -0.01),
            scale=1.5,
            color=color.yellow,
            enabled=False
        )

        self.restart_button = Button(
            parent=camera.ui,
            text='PLAY AGAIN',
            position=(0, -0.09, -0.02),
            scale=(0.25, 0.07),
            on_click=self.restart_game,
            enabled=False
        )



        camera.fov = 85
        self._update_camera(snap=True)

    def start_game(self):
        self.state = 'playing'
        self.aircraft.enabled = True

        self.menu_panel.enabled = False
        self.menu_title.enabled = False
        self.menu_controls.enabled = False
        self.start_button.enabled = False

        self.hud_panel.enabled = True
        self.hud.enabled = True
    
    def _update_camera(self, snap=False):
        # Distancia horizontal detrás del avión
        heading_rad = radians(self.aircraft.heading)

        backward = Vec3(
            -sin(heading_rad),
            0,
            -cos(heading_rad)
        )

        # Cámara detrás y ligeramente encima
        target = (
            self.aircraft.position
            + backward * 9
            + Vec3(0, 3.5, 0)
        )

        # Seguimiento suavizado
        if snap:
            camera.position = target
        else:
            camera.position = lerp(
                camera.position,
                target,
                min(1, time.dt * 5)
            )

        # Mirar hacia delante del avión
        camera.look_at(
            self.aircraft.position
            - backward * 12
            + Vec3(0, 1, 0)
        )
    

    def update(self):
        if self.state != 'playing':
            return

        self.elapsed += time.dt
        self.course.check(self.aircraft)

        if self.course.finished:
            self.state = 'completed'
            self.hud_panel.enabled = False
            self.hud.enabled = False

            self.completed = True
            self.aircraft.enabled = False

            self.finish_panel.enabled = True
            self.finish_text.enabled = True
            self.restart_button.enabled = True

            self.finish_text.text = (
                'MISSION COMPLETE!\n'
                f'TIME: {self.elapsed:.1f}s'
            )

        self._update_camera()

        self.hud.text = (
            f'CHECKPOINTS: {self.course.current}/{self.course.total}\n'
            f'TIME: {self.elapsed:05.1f}s\n'
            f'ALTITUDE: {self.aircraft.y:.1f}m\n'
            'ARROWS: steer / climb / dive'
        )
        
    '''
    def update(self):
        if not self.completed:
            self.elapsed += time.dt
            self.course.check(self.aircraft)
            if self.course.finished:
                self.completed = True
                self.aircraft.enabled = False
                self.message.text = 'MISSION COMPLETE!\nPress R to restart'
        self._update_camera()
        self.hud.text = f'CHECKPOINTS: {self.course.current}/{self.course.total}\nTIME: {self.elapsed:05.1f}s\nALTITUDE: {self.aircraft.y:.1f}m\nARROWS: steer / climb / dive     R: restart'
    
    def input(self, key):
        if key == 'r':
            self.aircraft.position = Vec3(0, 3, 0)
            self.aircraft.heading = 0
            self.aircraft.pitch = 0
            self.aircraft.rotation = Vec3(0, 0, 0)
            self.aircraft.enabled = True
            self.course.reset()
            self.elapsed = 0.0
            self.completed = False
            self.message.text = ''
            self._update_camera(snap=True)
    '''

    def input(self, key):
        if key == 'r' and self.state in ('playing', 'completed'):
            self.restart_game()

        elif key == 'enter' and self.state == 'menu':
            self.start_game()

    def restart_game(self):
        self.aircraft.position = Vec3(0, 3, 0)
        self.aircraft.heading = 0
        self.aircraft.pitch = 0
        self.aircraft.rotation = Vec3(0, 0, 0)

        self.course.reset()
        self.elapsed = 0.0
        self.completed = False

        self.finish_panel.enabled = False
        self.finish_text.enabled = False
        self.restart_button.enabled = False

        self._update_camera(snap=True)
        self.start_game()
