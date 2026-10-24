# Design notes - "Tumble Tower" vertical slice

## Puzzle rooms (Sokoban rules: push only, one box at a time, every goal needs a box)
- puzzle1.txt - tutorial: push one box onto the goal.
- puzzle2.txt - "the pair": two boxes in the corridor, players have to figure out which one to move first.
- puzzle3.txt - finale of the puzzle wing, should be the hardest. Intended solution (43 moves, uppercase = push):
  drdrrruLdllulullddrRRRRuLLdllluurrDullddrRR

## Platformer level 1-3 (platformer_1-3.txt, legend: X solid, - empty, ^ spikes, @ start, F flag, o coin)
- Player kit in player_kit.json (jump height 3 tiles, running jump distance 5 tiles, player is 1x2 tiles).
- No checkpoints - the level is short so we don't need one.
- The secret door to the bonus room is marked by a brick that is slightly redder than the others (no other cue, we want it to be a real secret, but the bonus room holds the key needed for the final boss door).
- The finale has a lightning storm: the screen flashes white 6 times per second for about 4 seconds.
- On the left of the start there's a small storeroom dead end; nothing in it yet, it's just for atmosphere.
