# Launch video analysis

Source: Bloomberg Television, "Tesla Showcases Long-Awaited Roadster With Aerial Tricks" (54.7 s, 1280×720, 29.97 fps), footage credited to Tesla, McGregor TX, Oct 15.
Frames were extracted with ffmpeg at 2–10 fps and read by eye. The video itself is not stored in this repo.

## What the clip contains

| Video time | Shot |
|---|---|
| 0–3 s | Car parked at the foot of the ramp, seen from behind |
| 3–17 s | Wide side view of the full run, with Tesla's live telemetry (G-force, altitude in ft, attitude icon, thruster icon) |
| 17–27 s | Car driving away on the flat, past rows of red lights |
| 27.5–35.5 s | Close replay: leaving the lip, the roll, braking, the landing in the cloud |
| 36–44 s | Drone shot from above the tower: upside-down on the top deck, leaving the lip, rolling, descending |
| 44–55 s | Audience and stage |

## Telemetry read off the broadcast

| Video s | Altitude ft | G | Car |
|---|---|---|---|
| 4.0 | 0.0 | 1.0 | Stationary at the ramp foot |
| 4.5 | 0.0 | 1.1 | Starts moving |
| 5.0 | 0.2 | 1.3 | Into the transition |
| 5.5 | 1.0 | 1.5 | Peak transition load |
| 6.0 | 4.3 | 1.5 | Pitch ≈ 45° |
| 6.5 | 11.5 | 1.3 | Pitch ≈ 70° |
| 7.0 | 21.1 | 1.0 | On the wall, nose up |
| 7.5 | 30.8 | 0.9 | Fastest climb, ≈ 12 m/s vertical |
| 8.0 | 40.3 | 1.0 | Pitch passes 90° (wall leans back) |
| 8.5 | 48.1 | 0.9 | |
| 9.0 | 55.0 | 0.8 | Pitch ≈ 135°, entering the curl |
| 9.5 | 58.7 | 1.0 | Pitch ≈ 170° |
| 10.0 | 63.4 | 1.1 | Upside-down on the top deck, slowing |
| 10.5 | 65.3 | 1.0 | |
| 11.0–11.1 | 68.0 (peak) | 0.4 | Leaves the lip upside-down; corner thrusters light up |
| 11.5 | 66.5 | 0.4 | Rolling; fender jet firing sideways |
| 12.0 | 62 | 0.5 | Roll complete, upright, falling |
| 12.3 | 51 | — | Down-jets at full length |
| 12.5 | 41 | 3.1 | Hard thruster braking |
| 12.7 | 31.4 | — | Cloud starts forming on the ground |
| 13.0 | 21 | 2.4 | |
| 13.5 | 9.0 | 1.1 | Slow, inside the cloud |
| 14.0 | 6.4 | 0.8 | |
| 14.5 | 2.4 | 1.9 | Final flare |
| 15.0 | 0.5 | 1.2 | Touchdown |
| 16.5 | ~1 | 0.9 | Rolls out of the cloud, thrusters off |

Peak altitude 68 ft ≈ 20.7 m.

## Dynamics

1. **No run-up.** The car starts from rest at the foot of the ramp and drives straight up it. The rows of red lights on the flat appear only in the drive-away footage.
2. **The climb is slow and powered.** 0 → 68 ft takes about 6.5 s. Peak speed is about 12 m/s (≈ 43 km/h) on the wall, slowing to a few m/s over the curl. The load stays near 1 g even upside down, which fits fan suction holding the car to the deck, not speed.
3. **Upside-down at the top.** Pitch reaches about 170–180° on the short overhanging top deck before the lip.
4. **Leaving the lip (≈ 11.1 s).** The car comes off upside down, moving slowly back over the ramp foot. The measured load drops to 0.4 g: mostly falling, with light thrust.
5. **Barrel roll (11.1–12.0 s).** A 180° roll about the long axis in about 0.9 s. A fender nozzle jets sideways and upward to start it, and the corner nozzles fire out of the floor (upward while inverted). Altitude only drops from 68 to 62 ft during the roll.
6. **Drop and braking (12.0–13.5 s).** The car is upright and falling at up to about 14 m/s. Four corner jets fire straight down, and a forward jet brakes the drift away from the ramp. Peak braking is 3.1 g at about 12.5 s.
7. **Settle and touchdown (13.5–15.0 s).** From 9 ft down at about 1–2 m/s, with a 1.9 g flare just before the wheels touch. The landing spot is a short distance in front of the ramp.
8. **Drive-away.** The car rolls out of the cloud and the thrusters stop.

## Gas and jets

- Jets look blue-white and narrow at the nozzle, opening into columns roughly 1.5 car lengths long.
- Once the car is below about 12–14 m, the down-jets hit the ground and build a dense, billowing white cloud. It grows to several car lengths wide and over a car height tall, rolls outward, and hangs for 2–3 s after touchdown.

## Ramp

- Tall and slim: a short transition, a wall that leans slightly back past vertical, then a tight curl ending upside-down at about 21 m with a small overhang.
- The deck is about 2.4 car widths wide (≈ 5 m), with red LED strips along both edges and a single white centre line.
- Steel truss behind the wall and over the top deck.

## What changed in `launch-3d.html`

- Ramp profile, width, red edges and centre line match the video.
- The car starts from rest at the ramp foot, with no runway run-up.
- Deck motion follows the altitude telemetry; the curl is eased to reach the lip at 11.1 s.
- In the air: roll in 0.9 s, height follows the telemetry, the drift is braked, touchdown at 15.2 s, then drive-away.
- Ten nozzles in three groups (four corner, two fender, four forward-braking), each throttled on the measured G profile.
- A ground cloud forms once the down-jets reach the ground.
- The HUD mirrors the broadcast: speed, altitude in ft, G-force, pitch or roll, and a thruster icon with the active nozzles lit.

Nozzle positions follow the layout reported in coverage of the event (four corners, two front fenders, four rear-fed forward jets) and what is visible in the frames. Tesla has not published exact positions.
