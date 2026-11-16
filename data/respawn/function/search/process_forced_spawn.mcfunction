execute if score #check_valid_forced_spawn respawn.utils matches 0 run return fail

execute store success score #valid_spawn respawn.utils run function respawn:check_pos/check_forced_respawn_valid
execute unless score #show_respawn_visuals respawn.utils matches 0 positioned ~ ~0.335 ~ run function respawn:visuals/display_respawn_valid
execute if score #valid_spawn respawn.utils matches 1 run return 1
return fail