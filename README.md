# Respawn Utils

A Minecraft datapack that shows where each player's respawn point is and whether it's currently valid, using in-world markers and scoreboard values.

**Supports Minecraft 1.21.5 - 26.3**

## Install

1. Download the latest zip from the [Releases](https://github.com/HunsingerTheMatist/RespawnUtils-MC/releases) page. Use the attached zip, not the "Source code" archives.
2. Put it in your world's `datapacks` folder.
3. Run `/reload`, or reopen the world.

## Visuals

Visuals and validity checks are on by default:

- **Blue box**: a player's respawn point
- **Green / red boxes**: the positions around a bed or respawn anchor where the player can or can't respawn, or whether a `/spawnpoint` position is valid
(Note: The green and red boxes need both the visuals and valid checks detection to be on)

## Toggles

| Command | What it does | Default |
|---|---|---|
| `/function respawn:toggle_respawn_visuals` | Shows the blue, green and red boxes | On |
| `/function respawn:toggle_respawn_valid_detection` | Checks whether each player's respawn point has a valid position to spawn at | On |
| `/function respawn:toggle_respawn_exists_detection` | Checks whether each player has a respawn point | Off |
| `/function respawn:toggle_respawn_type_detection` | Checks what type of respawn point each player has | Off |

Each toggle switches its feature and reports the new state in chat.

To turn a feature on or off regardless of its current state, set its score directly (`1` for on, `0` for off):

```
/scoreboard players set #show_respawn_visuals respawn.utils 1
/scoreboard players set #do_respawn_valid_checks respawn.utils 1
/scoreboard players set #do_respawn_exists_checks respawn.utils 1
/scoreboard players set #do_respawn_type_checks respawn.utils 1
```

`#check_valid_forced_spawn respawn.utils` (on by default) controls whether positions set with `/spawnpoint` are checked for validity.

Settings are kept across `/reload`.

## Scoreboard

To show the results on the sidebar:

```
/scoreboard objectives setdisplay sidebar respawn.valid
```

or `respawn.exists` / `respawn.type`. The top line of each shows whether that detection is ON or OFF.

Each player gets these scores while the matching detection is on:

| Objective | Values |
|---|---|
| `respawn.exists` | `1` has a respawn point, `0` doesn't |
| `respawn.valid` | `1` the respawn point is valid, `0` it isn't |
| `respawn.type` | `0` None, `1` Forced, `2` Bed, `3` Anchor |

Other datapacks can read these scores directly. Players with the `respawn_invalid_player` tag are skipped.

## Building

The release zip is built with Python 3:

```
py tools/build.py
```

This writes `builds/RespawnUtils-v<version>-mc<versions>-build<n>.zip`. The version comes from `load.mcfunction`, and the supported Minecraft versions come from `pack.mcmeta`. The build also generates the overlay that lets 1.21.5 - 26.2 read the predicates.

## License

See [LICENSE](LICENSE).
