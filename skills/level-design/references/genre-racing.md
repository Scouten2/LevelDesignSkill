# Racing and Kart Tracks

## Contents
1. Choose the racing model first: arcade, sim or kart
2. The five track metrics (McMillan)
3. Corner anatomy and difficulty
4. Sequencing corners and the speed profile
5. Width, lanes and scale
6. Camber and height variation
7. Overtaking zones and racing quality
8. Landmarks, punctuation and readability
9. Arcade empowerment tricks
10. Kart tracks: items, route choice, shortcuts
11. Time trial and Trackmania-style tracks
12. Process: greybox the line, measure, iterate
13. Review checklist
14. Tracks to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

The main source is Luke McMillan, "A Rational Approach to Racing Game Track Design" (Game Developer feature), built on case studies of Initial D Arcade Stage 4's Mt. Akina and Maximum Tune 3's Hanshin Expressway. Metric method is in `metrics.md`; verticality functions in `verticality.md`.

---

## 1. Choose the racing model first: arcade, sim or kart

The model decides the track's speed profile, so pick it in the brief before drawing a line:

- **Arcade** (Daytona, Initial D, Ridge Racer): flowing speed, on-camber corners, speed variation kept tight (§4), corners that make players feel masterful.
- **Sim** (Gran Turismo, Forza Motorsport): mixed camber, long straights into heavy braking, passing decided under braking.
- **Kart** (Mario Kart): items, route choice and shortcuts layered on an arcade base; field size and catch-up drive width.
- **Time trial / stunt** (Trackmania): authored for rhythm, memorisation and shortcut discovery.

Arcade and sim advice conflicts on purpose (McMillan's speed-variation target vs sim braking zones); decide which one this track follows and don't mix them by accident.

## 2. The five track metrics (McMillan)

McMillan names five rational metrics: **race line, clipping points, track width, camber, height variation.** Author each explicitly, corner by corner, in a corner table:

| # | Type | Entry / clip / exit | Angle (°) | Gap to next (m) | Width | Camber | Δheight | Landmark | Target speed |
|---|---|---|---|---|---|---|---|---|---|

Two workflows both work: draw a spline and plan its clipping points, or place clipping points and derive the line through them.

## 3. Corner anatomy and difficulty

- **Every corner has an ideal entry point, clipping (apex) point and exit point** (McMillan).
- **Difficulty rule:** "Difficulty of a corner increases if the angle between these three points is more acute and/or if the distance between these points is reduced." Grade corners by these two numbers.
- **Compound corners** have several clipping points.
- **Vehicle-specific corners.** Maximum Tune puts clipping points "less than 50 percent of the way through a corner" by making corner exits wider than entries; a missed clipping point becomes an overtaking opportunity. A progressively tighter compound corner favours lighter vehicles; a progressively more obtuse one favours heavier, more powerful vehicles. Use this to balance a mixed field.
- **Entry and exit are punctuation**: "There will always be definite entry and exit points… as a type of 'punctuation' to help memorize the circuit."

## 4. Sequencing corners and the speed profile

McMillan's heuristics:

- "Corners need to be progressively tighter": within a section, sequence corners from easy to hard (teach → develop → twist).
- Straights must be short enough that "the player is never able to significantly overshoot the ideal corner entry speed" (arcade).
- **Speed variation:** keep the "standard deviation in vehicle speed… ideally within a plus or minus 30 percent region" (arcade).
- His telemetry comparison: Gran Turismo 5's Trial Mountain showed the highest speed deviation (long braking after straights) and the arcade tracks the lowest; Mt. Akina balanced mixed vehicles "even without significant rubber-banding".
- **Check:** estimate target speed per segment from the corner table (or playtest telemetry) and compute the spread. Arcade: flag segments outside ±30% of the mean. Sim: confirm the heavy-braking zones are where you want passing.
- **Rhythm**: mix hairpins, sweepers and chicanes; avoid abrupt radius reversals unless you want a braking or passing zone there. [convention]
- Procedural research uses diversity of curvature and speed (entropy of the profiles) as a fitness measure for interesting tracks (Loiacono, Cardamone & Lanzi 2011) [unverified: snippet]; a flat speed profile is a warning sign either way.

## 5. Width, lanes and scale

- **Lanes:** "each lane should be 1.6 car widths wide, allowing three cars to be side by side in two lanes" (McMillan).
- **Shoulder:** "around 50 percent to 75 percent the width of a car".
- **Wider is easier:** "making the road wider will make corners easier". Use width as a difficulty knob alongside angle and spacing.
- **Scale up ~33% for third-person cameras:** "the environment should be scaled up by a factor of around 33 percent, and the same applies for racing games… to allow space for the camera… and also to create passing opportunities."
- **Field size:** widen for larger fields and item combat. [convention] Kart roads commonly fit about 4–6 karts abreast.

## 6. Camber and height variation

- **Arcade corners on-camber.** "Ideally, all corners in an arcade style racing game will be on-camber"; Daytona USA used on-camber turns for "impossible corner entry and exit speeds". Gran Turismo mixes on- and off-camber corners to test players.
- **Height variation balances vehicles.** Climbs favour heavy, powerful cars and descents favour light ones; height also creates tension, relief and "vista moments".
- **Sightline mood.** "Limited line of sight will result in the player being anxious… increased line of sight, they feel empowered." Use crests and blind entries for tension, and open descents for release.
- "Height variations should always be used… Rapid changes in height should be avoided."
- Verticality in tracks (`verticality.md`): preview the route ahead from a crest (survey), show a summit or later section across a valley (aspiration), and cross over earlier sections (memory). Jumps need readable landing zones and must not cause unintended airtime (§11).

## 7. Overtaking zones and racing quality

([convention] unless noted.)

- **Overtaking zones:** a straight that ends in a heavy-braking corner, or corners with more than one viable line (double apex, compound radius). Put the passing zone after a corner that feeds a straight, so exit speed decides the pass.
- **Missed apexes create passes** (McMillan's Maximum Tune corners): exits wider than entries let a trailing driver take a better line.
- **Sightlines to braking points:** drivers who can't see the corner brake early, and passing dies.
- **Lap time is not racing quality.** A layout tuned for pure lap time "produces fast lap times and terrible racing" (racetrackdesigner.com, via a secondary citation). Judge a track by passes and close finishes in multi-car tests, not by the fastest lap.

## 8. Landmarks, punctuation and readability

- "Use straights to create 'punctuation'… Separate corners using landmarks or iconic features" (McMillan). Give every corner a unique landmark players can memorise and name.
- "Road markings are essential to creating a sense of speed."
- **Art serves the line** (stance 11): barriers, kerbs, markings and lighting must make entry, apex and exit readable at speed. Re-check after the art pass; scenery that hides a braking point is a bug.
- Hazards readable from a distance; lethal or off-track edges look different from runoff. [convention]

## 9. Arcade empowerment tricks

- **On-camber corners** (§6) let players carry speeds that feel impossible.
- **"Needle threading" corners:** a very wide entry, one clipping point, then the *perception* of a very narrow exit, added as a barricade after designing a wide exit. They make players feel masterful (McMillan).
- **Vistas after climbs** (§6) as release beats.

## 10. Kart tracks: items, route choice, shortcuts

- **Route choice driven by items and situation.** Of Mario Kart 8 Deluxe's Rainbow Road, Kosuke Yabuki: "the two routes form an intertwined spiral… The design allows for lots of different tactical gameplay depending on your items and the situation around you, such as changing your route, or taking a shortcut between the two paths… this is also the part where drivers… are most likely to fall off" (Nintendo UK). Smart Steering is the accessibility answer to that risk.
- **Branches offer different risks and rewards**, not equal alternatives. MK8's anti-gravity sections let routes branch to dodge or grab items [unverified: snippet].
- **Catch-up lives in item tables, not geometry.** MK8 picks each item distribution "depending on the distance from the frontrunner in the moment the Item Box was opened" (Super Mario Wiki). Keep the track fair; let items handle rubber-banding.
- **Item box rows** [convention]: rows that span the full road width so every position can grab one; place rows where the field bunches (after chokes, before branch points).
- **Shortcuts trade risk for reward** [convention]: off-road unless boosted, narrow gaps, jumps that need a mushroom or real skill. A shortcut nobody can use is decoration; one everybody uses is the real route.
- **Simple tracks can work.** Baby Park's tiny oval was reportedly inspired by short-track speed skating [unverified].
- [convention] Kart laps commonly run around 30–60 s over three laps; measure yours.

## 11. Time trial and Trackmania-style tracks

Community practice only [unverified: Trackmania Exchange snippets]:

- **Checkpoint placement decides which shortcuts are viable**; place checkpoints to rule shortcuts in or out deliberately.
- **Avoid unintended airtime** and gotchas the player can't read on a first run.
- **Validate with an author time** and set medal times with slack.
- Rhythm and memorisation are the content: each section should have a recognisable flow pattern and landmark.

## 12. Process: greybox the line, measure, iterate

- **Prove the line in grey with real handling** (stance 11). Gran Turismo's Kazunori Yamauchi: "the longest part of creating a fantasy track is the design of the course itself"; only after it is finalised does the team decide where in the world it sits and capture textures (GTPlanet).
- **Iterate relentlessly.** Hideki Konno on Mario Kart 8: "we work on courses and we create them and then we work on them again, and again, and again, and we revise until we come up with something that we think is going to be fun for everyone to play over and over again" (Nintendo Life, 2014).
- **Measure**: per-corner entry/exit speeds, crash and off-track heatmaps, pass locations, lap-time spread across skill levels and vehicles. Fairness across vehicle classes is an active research question (Majid & Crawfis 2024) [unverified: snippet].
- Write the corner table (§2) before the first test and update it after each.

## Review checklist

- [ ] Racing model chosen (arcade/sim/kart/time trial) and speed-profile target stated
- [ ] Corner table filled: entry/clip/exit, angle, spacing, width, camber, height, landmark, target speed
- [ ] Corner difficulty graded by angle and spacing; sections get progressively tighter
- [ ] Arcade: speed spread within ~±30%; straights never let players far overshoot corner entry speed; corners on-camber
- [ ] Sim: braking zones after straights placed where passing is wanted
- [ ] Lanes ~1.6 car widths; shoulder 50–75% car width; ~33% scale-up for third-person camera; width matches field size
- [ ] Height variation used for balance and mood; no rapid height changes; jumps land readably
- [ ] At least two overtaking zones per lap; braking points visible on approach
- [ ] Every corner has a unique landmark; markings and art keep the line readable (re-checked after art)
- [ ] Kart: branches with different risk/reward; shortcuts usable but costly; item rows span the road; catch-up in item tables
- [ ] Time trial: checkpoints rule shortcuts in or out on purpose; no unintended airtime; author time set
- [ ] Multi-car playtest judged on passes and close racing, not only lap time

## Tracks to study

- **Arcade:** Initial D Arcade Stage 4's Mt. Akina; Maximum Tune 3's Hanshin Expressway (McMillan's case studies); Daytona USA (on-camber corners).
- **Sim:** Gran Turismo's Trial Mountain (high speed variation, braking zones); real circuits with famous passing zones.
- **Kart:** Mario Kart 8 Deluxe's Rainbow Road (intertwined routes, item-driven choice); Baby Park (minimal layout, constant contact).
- **Time trial:** popular Trackmania campaign and Exchange tracks, for checkpoint placement and rhythm.

Sources: McMillan, "A Rational Approach to Racing Game Track Design" (Game Developer) and its news summary; MyNintendoNews quoting Nintendo UK (Yabuki); Nintendo Life (Konno, 2014); Super Mario Wiki (MK8 item distributions); Siliconera (MK8 anti-gravity); GTPlanet (How Gran Turismo is made); Trackmania Exchange; arXiv 2311.04710 survey, GECCO 2011, PCG Workshop 2024; racetrackdesigner.com (secondary citation).
