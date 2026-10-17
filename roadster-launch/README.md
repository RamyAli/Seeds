# Tesla Roadster launch — simulation

**Simulation:** open [`simulation.html`](simulation.html) in a browser. The car launches down the runway, climbs the ramp, leaves the lip upside-down, brakes to a stop in mid-air on thrusters, flips upright, hovers and lands. Controls: play/pause (space), restart, speed (1× / 0.5× / 0.25×), follow camera, timeline scrubber.

Step 1: drawings of the stage set-up, based on the reference photos.

![Stage, isometric](stage-isometric.png)

![Stage wireframe](stage-wireframe.png)

- `stage-wireframe.svg`: side elevation and plan view, drawn to scale (1 m grid)
- `stage-isometric.svg`: isometric line illustration of the same stage (3D model projected in `build_isometric.py`)
- `build_wireframe.py`: generates the SVG; change the numbers here and run `python3 build_wireframe.py` again

All dimensions are estimates from the photos. Approach runway length, the exact ramp curve and the thruster details are still open.
