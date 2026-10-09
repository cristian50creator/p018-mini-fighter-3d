from ursina import Ursina, window, application
from game import FlightGame

app = Ursina()

window.title = 'Mini Fighter 3D - Flight Challenge'
window.borderless = False
window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False
window.exit_button.visible = False
#window.color = color.rgb(22, 40, 62)

application.base.setBackgroundColor(
    22 / 255,
    40 / 255,
    62 / 255,
    1
)

flight_game = FlightGame()

app.run()