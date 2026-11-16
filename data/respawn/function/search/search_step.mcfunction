execute at @s store success score #valid_spawn respawn.utils run function respawn:check_pos/check_respawn_valid
scoreboard players operation #any_valid respawn.utils > #valid_spawn respawn.utils
execute if score #show_respawn_visuals respawn.utils matches 0 if score #valid_spawn respawn.utils matches 1 run return 1

execute unless score #show_respawn_visuals respawn.utils matches 0 at @s positioned ~0.5 ~0.335 ~0.5 run function respawn:visuals/display_respawn_valid

scoreboard players add #currX respawn.utils 1
execute if score #currX respawn.utils > #endX respawn.utils run function respawn:search/search_increment_z
execute if score #currZ respawn.utils > #endZ respawn.utils run function respawn:search/search_increment_y
execute if score #currY respawn.utils > #endY respawn.utils run return fail
execute store result entity @s Pos[0] double 1 run scoreboard players get #currX respawn.utils

function respawn:search/search_step