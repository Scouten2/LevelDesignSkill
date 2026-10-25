| Kit | Value |
|---|---|
| units | m |
| player_width | 1 |

| Move | Distance | Height |
|---|---|---|
| jump | 4 | 1 |

| Node | Role | Landing | X | Y | Z |
|---|---|---|---|---|---|
| S | start | 2 | 0 | 0 | 0 |
| A | | 2 | 0 | 5.4 | 0 |
| B | | 2 | 0 | 11.2 | 0 |
| G | goal | 2 | 0 | 14 | 0 |

| From | To | Move | Gap | Rise | Camera | Fail |
|---|---|---|---|---|---|---|
| S | A | jump | 3.4 | 0 | along | respawn S |
| A | B | jump | | | across | respawn A |
| B | G | jump | 2 | 0 | across | respawn B |
