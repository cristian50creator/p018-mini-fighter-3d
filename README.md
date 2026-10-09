# Mini Fighter 3D 🚀

**Mini Fighter 3D** is a small 3D arcade flight game built with **Python** and the **Ursina Engine** as a Code in Place project.

Pilot a fighter-style spacecraft through a sequence of checkpoints in a star-filled environment. Follow the wireframe course, steer through the highlighted ring, and complete the mission as quickly as you can.

## Gameplay

The game starts at a menu, with the spacecraft stationary until you select **START MISSION** (or press **Enter**). Once the mission begins, the spacecraft moves forward automatically. Steer and adjust your altitude to fly through all **8 checkpoints** in order.

- **Space environment:** a dark background and procedurally positioned stars.
- **3D spacecraft:** a simple fighter model assembled from geometric shapes.
- **Checkpoint course:** wireframe tunnel guides and colored rings. The active checkpoint is highlighted in bright lime; upcoming checkpoints are blue.
- **Chase camera:** follows the spacecraft from behind.
- **Flight HUD:** displays checkpoints completed, elapsed time, altitude, and a control reminder.
- **Mission complete screen:** shows your finishing time and a **PLAY AGAIN** button.

> The ring glow is approximated with overlapping outlines, rather than a post-processing bloom effect. The flight model is arcade-style, not a realistic physics simulator.

## Controls

| Key / action | Function |
| --- | --- |
| **← / →** | Turn left / right |
| **↑ / ↓** | Climb / dive |
| **Enter** | Start from the main menu |
| **R** | Restart during or after a mission |
| **START MISSION** | Begin the flight |
| **PLAY AGAIN** | Restart after completing the course |

The spacecraft moves forward automatically during gameplay.

## Requirements

- Python **3.12** (development version)
- [Ursina Engine](https://www.ursinaengine.org/) **8.3.0** (development version)
- A desktop environment capable of running Ursina / Panda3D

## Installation and running

Clone the repository and open the project folder:

```bash
git clone https://github.com/YOUR_USERNAME/p018-mini-fighter-3d.git
cd p018-mini-fighter-3d
```

Create and activate a virtual environment:

**Windows (PowerShell)**

```powershell
py -3.12 -m venv env
.\env\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv env
source env/bin/activate
```

Install the game engine:

```bash
python -m pip install ursina==8.3.0
```

Start the game:

```bash
python main.py
```

If the repository includes a `requirements.txt` file, you can use `python -m pip install -r requirements.txt` instead of installing Ursina directly.

## Project structure

```text
p018-mini-fighter-3d/
├── main.py               # Creates the Ursina application and window
├── game.py               # Game states, camera, UI, timer, and restart logic
├── aircraft.py           # Spacecraft model and movement controls
├── checkpoints.py        # Checkpoint positions, rings, and course detection
├── space_background.py   # Procedurally generated star field
└── README.md             # Project documentation
```

## How it works

The spacecraft starts at a fixed position and travels forward while the arrow keys change its heading and pitch. Each checkpoint is positioned on a plane perpendicular to the course's forward Z axis. A checkpoint is counted when the spacecraft reaches its Z position and is within the ring's radius in the X–Y plane.

The game has three states:

1. **Menu:** the spacecraft is stationary and the start controls are shown.
2. **Playing:** movement, checkpoint tracking, and the timer are active.
3. **Completed:** the spacecraft stops and the final time is displayed.

## Built with

- **Python** — game logic and controls
- **Ursina Engine** — 3D rendering, entities, input, and interface
- **Panda3D** — rendering framework used by Ursina

## Possible future improvements

- Extend the course beyond eight checkpoints.
- Improve the appearance of glowing rings and the spacecraft.
- Add sound effects, music, and additional missions.
- Add difficulty levels or a best-time record.

## Project status

**Playable prototype.** The current version includes a main menu, an eight-checkpoint course, a flight HUD, a star field, and a completion screen.

---

*Created as a Python learning project for Code in Place.*

