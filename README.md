# pysc2-replay-data-extraction

extract state data from `.SC2Replay` files for machine learning training.

## Usage

```
$ python run.py --replays ~/StarCraftII/Replays/local
```

## Structure

- **info** (replay information)
  - mapName
  - localMapPath
  - PlayerInfo
    - PlayerID
    - raceRequested
    - raceActual
    - playerResult
      - playerId
      - result
    - playerApm
  - gameDurationLoops
  - gameDurationSeconds
  - gameVersion
  - dataBuild
  - baseBuild
  - dataVersion
- **state** (game state info per step)
  - minimap
    - visibility
    - creep
    - player_id
    - player_relative
  - screen
    - visibility
    - creep
    - power
    - player_id
    - player_relative
    - unit_type
    - unit_density
  - player
  - available_actions
  - actual_actions

## Ack

typically 100kb size per step
