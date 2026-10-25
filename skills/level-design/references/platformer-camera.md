# Platformer Camera (2D and 3D)

## Contents
1. The camera is level design
2. Keren's vocabulary
3. 2D defaults
4. Celeste's room camera
5. Per-region camera spec
6. Vertical sections: climbs, descents, kill planes
7. Camera paper checks
8. 3D cameras
9. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Numbers for jumps and drops are in `platformer-metrics.md`; looking up and down as a general design axis is in `verticality.md`.

---

## 1. The camera is level design

What the player can see decides whether a jump is fair, a hazard readable or a secret findable. Keren's three camera challenges are attention (what is important), interaction (what the player needs to see) and comfort (no jarring motion; eye–inner-ear conflict causes discomfort "even in 2D") (Keren, *Scroll Back*, GDC 2015). Original Rayman's lesson, in his words: "Camera system is an integral part of game design." Koizumi: "Thinking about the camera is game design, too." Specify the camera per region in the level document, not as a global engine setting.

## 2. Keren's vocabulary

| Technique | What it does | Use when |
|---|---|---|
| camera-window | "Push camera position as the player hits the window edge" | stable framing; size the window to the jump |
| position-snapping | constantly drifts back to centre the player | small windows, slow games |
| platform-snapping | "Camera snaps to the player only as it lands on a platform" | platformers: jumps don't move the camera vertically |
| lerp / physics smoothing | eases toward the target | everywhere; watch for lag at speed |
| dual-forward-focus | direction change switches focus "to enable wide forward view", with a threshold before switching | levels with frequent back-and-forth |
| static-forward-focus | fixed lead in one direction | auto-runners, one-way scrollers |
| projected-focus | leads by velocity | horizontal speed only; fails vertically |
| target-focus | stick input shifts the view | let players look ahead or down |
| cue-focus / attractors | world objects pull the camera | bosses, doors, secrets, threats |
| region-based-anchors / region-focus | regions set their own anchor and focus | rooms, arenas, set pieces |
| speedup push / pull zones | camera accelerates in stages | avoid 0-to-full-speed jolts |
| zoom-to-fit | widens to include targets | multiplayer, arenas |
| camera-path / cinematic path | camera follows an authored path | foreshadowing, reveals |
| edge-snapping | "Set a hard edge for camera positioning" | level bounds, kill planes |
| auto-scroll | camera moves on its own | chase and tempo sequences |

## 3. 2D defaults

- **Window about one jump tall.** Rastan Saga's "camera-window is as high as a standard jump, so jumps don't cause vertical camera motion"; Rayman's is "just over the height of Rayman's jump", with platform-snapping. Default: window height = full-jump apex + ~1 tile [convention].
- **Platform-snap vertically** (Super Mario World snaps when Mario lands). The frame moves up or down only when the player commits to a new floor.
- **Dual forward focus with hysteresis**: SMW keeps the old anchor until Mario passes a threshold, which suits frequent left-right motion. A narrow lead to the left (Rastan's castles) leaves "a very narrow lookahead margin".
- **Forward lead about 25% of screen width** (Defender's focus point; Bonanza Bros. moves its forward-focus switch at about double the player's speed so the camera "only moves when the player moves").
- **Speed-up zones**: SMB adds "a virtual point, around 25% off-center, where the camera speeds up to catch up", avoiding a jump from 0 to full scroll speed.
- **Region anchors**: DKC gave level designers per-region camera tools; runner regions "require a wide forward view at the expense of seeing what's behind."
- **Attractors with two rings** (Insanely Twisted Shadow Planet): outside the outer ring the player rules; between rings the camera blends toward the cue; inside the inner ring it frames the cue only. Detractors push the camera away and can hide secrets.
- **Cautions**: lerp lets fast characters reach the screen edge, "keeping incoming enemies hidden till the last minute"; camera windows give "very little view of what's coming forward or up ahead"; projected focus "may not work well in platforms, especially vertically, where jumps and especially landing don't extrapolate well."

## 4. Celeste's room camera

From the released `Player.cs`:

- The target is the player centred in a 320×180 view plus a per-room offset, **clamped to the room's bounds**: the room is the frame.
- Smoothing is an exponential lerp that closes about 99% of the gap per second.
- Rooms can add anchors and lock modes with maximum offsets.
- **The camera never scrolls below a kill plane**: it snaps above killboxes. The bottom of the frame therefore means "below here is death", read from framing alone.
- Some states lead the view: the red-bubble dash leads 48 px in its direction, flight leads by 0.2 × velocity.
- Combined with per-screen respawn, the player always sees the whole challenge and its exit before committing.

## 5. Per-region camera spec

Write one line per camera region next to the map (coordinates in tiles, `(col,row)` origin top-left):

```
CAM R3 cols 40–80: window w=4t h=apex+1t; platform-snap; dual-forward 25% lead, 2t hysteresis;
  speedup-push at 25% off-centre; lock-bottom = kill plane row 22;
  attractor boss door (78,10) r_out=10t r_in=4t; exit: ease to R4 anchor over 0.5 s
```

- Required fields: region extent, window or lock, vertical behaviour, forward focus, bottom edge rule, attractors and detractors, transition into the next region.
- Mark regions that change behaviour (auto-scroll, cinematic path, zoom) and every place a forced pan takes control; keep control during pans unless the pan is a deliberate pause.
- Name the camera's job per region in one word (follow, frame, reveal, chase, hide) [convention].

## 6. Vertical sections: climbs, descents, kill planes

- **Climbs**: lead the view upward; the next handhold or platform must be on screen before the jump to it. A centred camera shows only half a screen up, so compensate with a vertical anchor or target-focus.
- **Descents**: the landing must be visible before the drop. If the downward view is shorter than the drop, either add a look-down input with a visible prompt, a camera pull ahead of the drop, or treat the drop as a blind drop and remove it from the critical path (`platformer-checks.md` §2).
- **Never use projected focus vertically**; jumps and landings don't extrapolate.
- **Never scroll below a kill plane** (Celeste). Where the bottom is safe, show floor; where it is death, lock the frame above it so the edge itself communicates.
- **Vertical screens or shafts**: frame the full shaft width; tall shafts that scroll need an upward lead and a stable horizontal position [convention].

## 7. Camera paper checks

Run these on the ASCII map with the camera spec beside it; the full check table is in `platformer-checks.md` §2.

- At every take-off, is the landing inside the frame the camera will show at that moment, including lead and lock?
- Is every hazard on screen at least ~1 s of travel before the point of commitment (run speed × 1 s, e.g. ~11 tiles in Celeste)? If not, add an attractor, a pan, a telegraph sound or move the hazard.
- Does the view ever show below a death plane, or hide one? Lock it.
- In climbs, is the lead upward? In descents, does the downward view cover the drop?
- Where the player reverses often, is there hysteresis so the camera doesn't swing on every turn?
- Do region transitions keep the player and the next threat in view?

## 8. 3D cameras

Moved to `platformer-3d.md` §3–4: the shadow, the screen-plane rule, Koizumi's three problems, Nesky's airborne rules and choosing a camera mode per sequence.

## 9. Review checklist

- [ ] Camera spec line written for every region (window/lock, vertical rule, lead, bottom edge, attractors, transition)
- [ ] Window about one jump tall with platform-snapping, or a stated reason otherwise
- [ ] Hysteresis wherever the player reverses often; speed-up zones where scroll speed changes
- [ ] Every landing visible at take-off; every hazard visible ~1 s before commitment
- [ ] View never scrolls below a kill plane; safe bottoms show floor
- [ ] Climbs lead upward; descents show the landing or are off the critical path
- [ ] No projected focus vertically
- [ ] 3D: checked against `platformer-3d.md` §9
