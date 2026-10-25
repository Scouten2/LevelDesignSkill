Softlock pit, a respawn past a one-way drop, a lethal required drop, a missing fail result.

| Kit | Value |
|---|---|
| units | m |
| player_width | 1 |
| damage_fall | 5 |
| lethal_fall | 10 |

| Move | Distance | Height |
|---|---|---|
| jump | 4 | 1 |

| Node | Role | Landing |
|---|---|---|
| S | start | 3 |
| A | | 3 |
| P | | 3 |
| B | | 3 |
| C | | 3 |
| G | goal | 3 |

| From | To | Move | Gap | Rise | Fail |
|---|---|---|---|---|---|
| S | A | jump | 2 | 0 | fall P |
| A | B | drop | 0 | -12 | |
| B | C | jump | 2 | 0 | respawn C |
| C | G | jump | 2 | 0 | |
