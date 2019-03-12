# pysc2-replay-data-extraction

extract state data from `.SC2Replay` files for machine learning training.

## Usage

extract data:

```bash
python main.py --replays path-to-replays/ --agent agent.ObserverAgent (on Linux)
```

generate replays:

```bash
python -m pysc2.bin.agent --map Simple64 --save_replay True --max_episodes 1 --parallel 8 (on Linux)
```

## Dependency

- pysc2 == 2.0.1
- s2client-proto == 4.1.2

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

## Notice

typically 100kb per step
