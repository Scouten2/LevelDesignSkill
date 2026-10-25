| Move | Distance | Height |
|---|---|---|
| jump | 4 | 1 |
| double_jump | 6.5 | 2.2 |

| Node | Role |
|---|---|
| S | start |
| G | goal |
| T1 | |
| T2 | |
| T3 | |

| From | To | Move | Gap | Rise | Fail |
|---|---|---|---|---|---|
| S | G | jump | 2 | 0 | death |
| S | T1 | teaser | 7 | 0 | |
| S | T2 | teaser | 10 | 0 | |
| S | T3 | teaser:double_jump | 5 | 1.5 | |
