KZ-style strip: a crouch-jump gate, a ladder, a diagonal corner cut, a sinking block,
first-person camera, and a mislabelled crouch-jump that a plain jump can make.

| Kit | Value |
|---|---|
| units | u |
| player_width | 32 |
| damage_fall | 200 |
| lethal_fall | 600 |

| Move | Distance | Height | Gate |
|---|---|---|---|
| jump | 240 | 56 | |
| crouchjump | 240 | 65 | yes |

| Node | Role | Landing | X | Y | Z |
|---|---|---|---|---|---|
| S | start | 256x256 | 0 | 0 | 64 |
| A | | 128x128 | 288 | 0 | 64 |
| B | | 128x128 | 288 | 320 | 64 |
| C | | 128x128 | 404 | 320 | 122 |
| D | | 64x64 | 404 | 320 | 314 |
| E | checkpoint | 128x128 | 500 | 470 | 314 |
| G | goal | 256x256 | 760 | 470 | 330 |

| From | To | Move | Gap | Rise | Camera | Fail | Window |
|---|---|---|---|---|---|---|---|
| S | A | jump | | | first-person | none | |
| A | B | jump | | | first-person | respawn S | |
| B | C | crouchjump | | | first-person | respawn S | |
| C | D | ladder | | | | | |
| D | E | crouchjump | | | first-person | respawn S | 0.8 |
| E | G | jump | | | first-person | respawn E | |
