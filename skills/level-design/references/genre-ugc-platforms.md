# UGC Platform Level Design (Fortnite UEFN, Roblox, Mario Maker)

## Contents
1. Design against the discovery funnel
2. What Fortnite Discover measures
3. What Roblox measures: onboarding and the five-minute curve
4. The first five minutes: spawn into action
5. Session depth, return and social reasons
6. Originality versus reuse
7. Budgets are hard constraints (UEFN memory)
8. Single-level UGC: Mario Maker
9. Greybox, publish and iterate with analytics
10. Review checklist
11. Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

On a UGC platform the level competes for attention inside someone else's storefront, and the platform's ranking signals are part of the brief. Onboarding theory lives in `principles.md` and `fun-checks.md`; mobile-style retention curves in `genre-casual-mobile.md`; platformer level craft for Mario Maker in `platformer-craft.md`.

---

## 1. Design against the discovery funnel

Every UGC level passes through the same funnel. Write the brief against each stage:

1. **Thumbnail and title** → does the player click? (Thumbnail must show real gameplay.)
2. **First minutes** → do they bounce? (Fortnite's bounce threshold is "often 5 minutes"; Roblox watches 5-minute survival.)
3. **Session depth** → average playtime, play-through rate.
4. **Return** → retention (D1/D7).
5. **Social** → invites, party play.

Level implications, in order: spawn into action; teach the core loop's *what* and *why* in context; front-load progress; give reasons to invite friends; give goals that bring players back. Each is a level-design decision, not only a systems one.

## 2. What Fortnite Discover measures

From Epic's "How Discover works in Fortnite" (Epic developer docs, current at 2026). Note: an older "Attraction / Engagement / Satisfaction" framing comes from a stale summary; use the current list.

- **"Engagement drives distribution."** Core signals are "Average Playtime, retention, Quality play-through rate (QPTR)… evaluated on a per-player basis, so deep engagement can even outperform a large audience."
- **Metrics:** average minutes per session (capped at 120); **bounce rate**, "the fraction of sessions where a player stayed for less time than a row-specific threshold (often 5 minutes)"; retention; social metrics (invites, returning in a party, share of play in parties); **QPTR**, an "engagement-weighted version of play-through"; 7-day players.
- **Test window:** "When you publish a new island, Discover tests your content for up to 2 weeks." First impressions are measured on what you ship, so ship a polished first five minutes.
- **Near-duplicates are shown less often**; reusing Verse code, devices and systems is fine (§6).
- **Thumbnails** must represent real gameplay; no plain or gradient backgrounds, no stamped-on weapons. Genre tags decide which rows an island can appear in.
- **Payouts** distribute a share of net revenue to publishers by engagement "from Fortnite players who have made a real money purchase", with components for island retention and for acquiring new and returning players (Epic, "Engagement payout"). Epic doesn't publish metric weights; don't claim them.

## 3. What Roblox measures: onboarding and the five-minute curve

From Roblox Creator Docs ("Onboarding"; "Engagement analytics"):

- Onboarding covers "the first few minutes of gameplay"; success is "Day 1 retention" plus onboarding goals. A/B-test tutorial steps.
- **Teach the essentials**: the core loop's *what* and *why*.
- **Get to the fun quickly**: "New players typically decide their interest in a game within minutes." Tools: low early XP thresholds, social motivators, starter items.
- **Leave players wanting more**: short-, mid- and long-term goals and moments of joy.
- The New User First Session Retention chart shows how many new users are still playing X minutes after joining; if the share still playing after 5 minutes drops week-on-week, check onboarding changes and error reports. "Balance the progression system to not gate off the fun."

## 4. The first five minutes: spawn into action

Both platforms judge a level in its first minutes, so design them as a separate level with its own beat chart (`process.md`). Defaults are [convention]:

- **Spawn into action.** The first meaningful verb within about 10–30 s of spawning; no lobby walk, no text wall, no long cinematic.
- **Teach in context, never punish while teaching.** Interactive teaching beats explanation (Hodent: "DON'T PUNISH WHILE TEACHING"; at most 3 new items at once in learning mode). Put the first lesson where failing is free.
- **Show the why.** Within the first minute, show what the loop is for: a visible upgrade, a leaderboard, a door you'll open, a rival team.
- **Front-load progress.** First reward or unlock within the first one to two minutes; low early thresholds (Roblox). The first session should complete at least one full loop.
- **One clear landmark goal from spawn** (`layout-and-flow.md`): players who don't know where to go bounce.
- **Respawn fast.** Early deaths cost seconds, not minutes; spawn players back near the action.

## 5. Session depth, return and social reasons

- **Define the play-through.** QPTR rewards players reaching the end of a meaningful run, so give the island a clear end state reachable in one session (a round, a run, a course), then a reason to start another. [convention]
- **Rounds over marathons** [convention]: short, repeatable rounds keep average playtime high without forcing long commitments; chain them with meta-progress.
- **Reasons to return**: short-, mid- and long-term goals (Roblox), visible locked areas or upgrades seen from the spawn, rotating content.
- **Reasons to invite** [convention]: modes that are better with friends (team roles, co-op puzzles, versus), a party-friendly lobby, and spaces that show off other players (cosmetics, builds, leaderboards). Fortnite counts invites and party play directly.
- **Verticality as a hook** [convention]: an aspirational structure visible from spawn (a tower, a summit, a vault) is a cheap reason to stay and return (`verticality.md`).

## 6. Originality versus reuse

- Epic down-ranks near-duplicate islands and metadata but allows reuse of systems. Build a distinct hook (verb, theme or rule twist) on a proven genre template, and say what the hook is in the title and thumbnail.
- Run the grey description test (`fun-checks.md`): if the island described without its theme is identical to the top islands in its row, it is a near-duplicate in play even if the art differs.

## 7. Budgets are hard constraints (UEFN memory)

- "The bar shows a maximum of 100,000 memory units… if any area in your level exceeds 100,000, you will not be able to publish your island" (Epic, "Memory management in UEFN"). Collaborators on console can be kicked when hardware memory runs out.
- Plan the budget from blockout: divide the island into areas with a per-area budget, reuse a small kit, and instance devices. Epic's tooling includes texture, LOD and draw-call tools, Memory Snapshot, Spatial Profiler and validation. Specific tactics (HLOD only for far-visible objects, Data Layers, lower Nanite keep-triangle percentage) come from community guides [unverified].
- No Roblox technical budgets were found; measure on the lowest target device. [convention]

## 8. Single-level UGC: Mario Maker

Furia and Mocci's study of Super Mario Maker 2 (arXiv 2025):

- "the median level is rated normal, and has a clear rate of 0.25 (i.e., 25%)". Most levels are harder than their makers think.
- A small number of popular levels get "massive amounts of plays, likes, and comments"; the median gets "modest, yet non-negligible, engagement". Levels with many plays tend to be harder.
- "makers with more experience tend to design easier levels (possibly because they are better designers)". Older styles (SMB1) are associated with easier levels.
- Negative comments are more common on hard levels, but frequent topics "express appreciation—when the difficulty is justified by a high-quality design". Easy levels draw generic praise or "complain about an abuse of (visual) effects".

What to do:
- **Build easier than feels right**; calibrate with other players' clears, not your own (the maker's clear proves only that it's possible).
- **Hard levels need visible fairness**: telegraphed hazards, checkpoints, no hidden kill blocks, consistent rules (`platformer-checks.md`).
- **Don't spam effects**; every element should serve the level's idea.
- **One idea, riffed.** Nintendo-made courses revolve around a single idea and riff on it [unverified]; this matches Hayashida's "a clear concept in the beginning, and that's carried through absolutely all the way" (`platformer-craft.md`).
- **Tezuka's tips** (Nintendo of America, 2019): don't overthink; upload even in rough form, because aiming for praise makes it hard to start; come up with the level's name first, since it suggests what the level should be; study other players' levels.

## 9. Greybox, publish and iterate with analytics

- **Fun in grey first.** Epic's UEFN docs define greyboxing as "making a playable rough draft of a level to get a sense of its gameplay before polishing its look… Add props and art once you are happy with how the level plays", with checks such as platforms at reachable heights and no "boring or over-accessorized" spaces.
- **Rough versus polished launch** [contested]: Tezuka's "upload rough" suits Mario Maker, where there is no ranking test; Fortnite's two-week test window measures what you ship, so polish the first five minutes before publishing there.
- **Iterate on data**: A/B-test onboarding steps (Roblox); watch the 5-minute survival curve and bounce rate after every change; read drop-off points as level problems (where do new players quit?). See `playtesting-and-critique.md`.
- Dreams (Media Molecule) ended live support in 2023, a reminder that strong tools without discovery limit reach [unverified].

## Review checklist

- [ ] Brief names the platform's funnel signals the level targets (bounce, playtime, QPTR, retention, social)
- [ ] Thumbnail and title show real gameplay and the hook
- [ ] First meaningful verb within ~10–30 s of spawn; no text wall or long walk [convention]
- [ ] Core loop's what and why taught in context, with failure free while teaching
- [ ] First reward within the first minutes; one full loop completes in the first session
- [ ] Clear end state per play-through, plus a reason to play again
- [ ] Reasons to return (goals at three horizons) and to invite (better with friends)
- [ ] Hook is distinct from near-duplicates; grey description test passed
- [ ] Per-area memory budget planned; no area over UEFN's 100,000-unit cap
- [ ] Single-level UGC: one idea riffed; tested by others; easier than the maker's instinct; no effect spam
- [ ] Analytics plan: bounce/5-minute survival, drop-off points, A/B tests on onboarding

## Levels to study

- **Fortnite Creative/UEFN:** the current top islands in your genre row, studied for their first five minutes (time to first verb, first reward, first invite prompt).
- **Roblox:** top experiences in your genre, studied the same way; Roblox's onboarding docs' examples.
- **Super Mario Maker 2:** Nintendo's own story-mode courses (one idea riffed); highly liked hard courses vs disliked ones for fairness.
- **Dreams** (Media Molecule): as a toolset case study [unverified].

Sources: Epic developer docs (How Discover works; Engagement payout; Memory management; Memory and optimization; Greyboxing in UEFN); FCHQ (UEFN memory tactics); Roblox Creator Docs (Onboarding; Engagement analytics); Furia & Mocci, arXiv 2507.21078; Super Mario Wiki (Tezuka's tips); Superjump; Hodent GDC 2016.
