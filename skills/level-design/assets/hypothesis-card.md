# Hypothesis Card

> "Game designs are hypotheses / Playtests are experiments" (Ambinder, Valve, GDC 2009). Write one card per risky beat, per U item from a rubric review, and per assist hook you need to prove. Fill it in **before** the test; thresholds set afterwards don't count. Numbers in the examples are [convention].

## Card

```
ID:             H<n>                      Beat / space: <beat # from the beat chart, space id>
Gate:           G<n> (when this must be answered)      Rubric criterion: <# from review-rubric.md>

We believe:     <observable player behaviour, with a number>
Because:        <evidence: design reason, earlier playtest, reference game, script output>
If wrong:       <what breaks for the player: lost, stuck, bored, unfair death, churn>

Metric:         <one primary metric, defined exactly (e.g. "% of first-time testers who …")>
Method:         paper/script | small playtest | telemetry at scale | bot simulation
Sample:         <n, who (fresh / returning / with impairments / preset / assists on), how many rounds>
Pass threshold: <number set now>
Fail action:    <the change to make first (cheapest), then the next>
Kill criterion: <when to cut or re-brief instead of iterating, e.g. "fails after 2 iterations">

Events:         enter_<beat>  exit_<beat>  death_<beat>  checkpoint_<id>  [+ choice_ / assist_ / skip_]
Observe:        <what observers note beyond the metric: look direction, hesitation, quotes>

Result:         <date, n, measured value, pass/fail>
Decision:       <keep / change (diff) / cut>; next card: <id>
```

## Rules

1. **One card, one metric.** A card with three metrics is three cards.
2. **Match the method to the question** (`playtesting-and-critique.md` §5): solvability, reachability and replay budgets are answered by scripts and need no players; noticing, understanding and getting lost need 5–8 fresh players [convention]; difficulty balance, churn and pass rates need data at scale (King's level 65 converted best and churned most; only long A/B tests showed it).
3. **Behaviour over opinion.** Prefer what players do (time, route, deaths) over what they say; use self-report only for experience questions, and phrase it neutrally.
4. **Thresholds are design intent.** Derive them from the brief (target duration, expected deaths, the beat's intensity) so a pass means "the level did what we designed it to do."
5. **Fail action is the cheapest fix first:** cue → light → geometry tweak → re-layout → cut (`playtesting-and-critique.md` §2). Log each change as a coordinate diff.
6. **Events come from the beat chart ids.** `enter_b04`, `exit_b04`, `death_b04` (payload: position with floor plane, cause, preset, assists on), `checkpoint_CP2`. Optional: `choice_b04_ladder`, `assist_ledgeguard_b07`, `skip_p03`. Funnel = exits ÷ enters; time in beat = exit − enter.

## Filled examples

```
ID: H1   Beat / space: b01 bridge ledge   Gate: G2   Rubric criterion: 3 (guidance)
We believe:     ≥ 80% of first-time testers look at the tower within 20 s of entering b01
Because:        tower framed by the arch and back-lit; only lit silhouette on the horizon
If wrong:       players don't know the goal; beats 3–6 lose their orienting landmark
Metric:         % of testers whose camera centres the tower within 20 s of enter_b01
Method:         small playtest (screen capture + camera log)
Sample:         6 fresh players, default preset, assists off
Pass threshold: ≥ 5 of 6
Fail action:    add moving birds circling the tower; then widen the arch; then move the entry 3 m left
Kill criterion: < 4 of 6 after two iterations → re-brief the reveal (start the level facing the tower)
Events:         enter_b01, exit_b01
Observe:        first look direction; any comment naming the tower
```

```
ID: H3   Beat / space: b07 tower climb   Gate: G3   Rubric criterion: 7 (challenge and failure)
We believe:     median deaths on b07 ≤ 2 and median replay per death ≤ 10 s
Because:        CP4 at the tower base; mid-tower ledge respawn; spiral keeps the goal in view
If wrong:       peak beat becomes a wall; quit risk at the climax
Metric:         deaths per player between enter_b07 and exit_b07; seconds from checkpoint_ to death_
Method:         small playtest now; telemetry at scale after launch
Sample:         8 fresh players across presets 2–3; then all players, first week
Pass threshold: median deaths ≤ 2; ≥ 90% reach exit_b07 within 6 attempts
Fail action:    add a mid-climb checkpoint; then remove one ranged enemy; then widen the third ledge
Kill criterion: funnel exit_b07 ÷ enter_b07 < 85% after two iterations → split the climb into two beats
Events:         enter_b07, death_b07, checkpoint_CP4, exit_b07, assist_ledgeguard_b07
Observe:        death causes (fall vs shot); whether players blame themselves
```
