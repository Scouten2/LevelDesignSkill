# Movement Kit

For 3D sequences, embedded jump puzzles and movement maps, use `assets/jump-sequence-spec.md` instead (its Moves table feeds `scripts/jump_links.py`).

Fill this **before** drawing any platformer level (method: `references/platformer-metrics.md` §1–4, §11).
One kit per character or power-up state. Write "assumed" next to any number not read from code or measured
in a gym; write "n/a" for moves the game lacks. Units: tiles and seconds (3D: metres, or player widths).
The Celeste column is a filled reference from its released `Player.cs` (1 tile = 8 px; derived rows are
approximate simulations). Don't copy it into your game.

```
Game / character / state:                       Version or date:
Source of numbers: code | gym measurement | design target (assumed)
Tile size: ___ px (or ___ m)    Frame rate: ___ fps    Player hitbox: ___ x ___ tiles
```

| Quantity | Your game | Celeste reference | Notes |
|---|---|---|---|
| **Ground** | | | |
| Walk speed (tiles/s) | | n/a (one run speed) | |
| Run speed (tiles/s) | | 11.25 | distance ÷ this = replay seconds |
| Time to full speed (s) | | ~0.09 | long accel = needs runways |
| Stop / turn time (s) | | ~0.09 (same accel) | long stops punish precision |
| **Jump** | | | |
| Full-hold apex (tiles) | | ≈ 3.6 | → `jump_height` (round down) |
| Tap apex (tiles) | | ≈ 0.9 | shortest controllable hop |
| Variable-height hold window (s) | | 0.2 | |
| Flat distance, full hold at run (tiles) | | ≈ 8.0 | → `jump_distance` |
| Flat distance, tap at run (tiles) | | ≈ 3.2 | |
| Flat distance, full hold at walk (tiles) | | n/a | |
| Airtime, full hold (s) | | 0.68 | |
| Reach at Δh +1 / +2 / +3 (tiles) | | ≈ 7.3 / 6.7 / 5.8 | band gaps against these |
| Gravity up / down; max fall (tiles/s) | | 112.5 tiles/s²; max fall 20 (fast 30) | |
| Apex hang rule | | gravity ×0.5 while \|vy\| < 5 tiles/s, jump held | |
| Air control (none / partial / full; ratio) | | full, 0.65 of ground accel | → `air_control` |
| **Forgiveness** | | | |
| Coyote time (s) | | 0.1 | → `coyote_time` |
| Jump buffer (s) | | not in released file (~0.08 quoted, unverified) | |
| Corner correction (tiles) | | 0.5 (jump and dash) | |
| Ledge / semi-solid pop | | yes | |
| Hurtbox vs hitbox | | hurtbox 2 px shorter | |
| Lift momentum storage | | yes, "a few frames" | |
| **Extra moves** | | | |
| Double jump (apex, distance) | | n/a | → `double_jump` |
| Dash (distance tiles, time s, directions) | | 4.5, 0.15, 8-way | → `dash_distance` |
| Dash / resource refill rule | | on landing and every screen transition | entry-state check |
| Wall jump (reach tiles; super variant) | | 0.25; super ~0.6 | → `wall_jump` |
| Wall slide / climb (speed; stamina) | | climb 5.6 tiles/s; stamina 110 (~13–14 tiles up) | |
| Glide / slow fall | | n/a | |
| Stomp / enemy bounce height (tiles) | | not derived (auto-jump 0.1 s) | treat bounceable enemies as platforms |
| **Falls and failure** | | | |
| Safe fall height (tiles) | | unlimited | → `safe_fall_height` (null) |
| Damage / lethal fall height (tiles) | | none; kill planes only | → `fall_damage_height` (null) |
| Respawn time (s) | | not found in released code | replay budget input |
| Respawn point | | screen entry | |

## Derived envelope and bands

Fill from the rows above (bands are [convention]; see `references/platformer-metrics.md` §6–8).

```
Max flat gap D = ____ tiles      Max apex H = ____ tiles      Reach at Δh +2 = ____ tiles
Intro gaps        ≤ 0.40 D = ____      Intro ledges     ≤ 0.50 H = ____
Routine gaps   0.50–0.75 D = ____      Routine ledges   ≤ 0.70 H = ____
Skill checks   0.75–0.90 D = ____      Skill ledges  0.70–0.90 H = ____
Optional only  0.90–1.00 D = ____      Optional      0.90–1.00 H = ____
Avoid          1.00–1.30 D = ____      Avoid         1.00–1.30 H = ____
Clearly impossible ≥ 1.5 D = ____      ≥ 1.5 H = ____
Drops: free ≤ ____ (two-way)   committed ≤ ____ (one-way)   costly ≥ ____   lethal: kill plane / ≥ ____
Hazard warning distance (run speed × 1 s) = ____ tiles      Camera window height (H + 1) = ____ tiles
```

Celeste example: D ≈ 8, H ≈ 3.6 → intro gaps ≤ 3.2, routine 4–6, skill checks 6–7.2, avoid 8–10.4, impossible ≥ 12;
warning distance ≈ 11 tiles; window ≈ 4.6 tiles tall.

## Kit JSON for `platformer_reach.py`

Lengths in tiles, times in seconds. Round reach **down** and hitbox **up**. Keys are exactly these:

```json
{"jump_height": 0.0, "jump_distance": 0.0, "player_width": 1, "player_height": 1,
 "air_control": true, "coyote_time": 0.0, "double_jump": false, "wall_jump": false,
 "dash_distance": 0, "fall_damage_height": null, "safe_fall_height": null}
```

Celeste reference:

```json
{"jump_height": 3.5, "jump_distance": 8.0, "player_width": 1, "player_height": 2,
 "air_control": true, "coyote_time": 0.1, "double_jump": false, "wall_jump": true,
 "dash_distance": 4.5, "fall_damage_height": null, "safe_fall_height": null}
```

Not captured by the JSON (state these in the level notes): apex hang, acceleration and runway needs, momentum and lift
boosts, enemy bounces, stamina, resource refills, moving platforms. Re-run the reach checks on every level after any change here.
