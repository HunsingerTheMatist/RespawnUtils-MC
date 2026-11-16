execute unless loaded ~ ~ ~ run return run function respawn:forceloads/add

execute unless score #show_respawn_visuals respawn.utils matches 0 positioned ~ ~0.13 ~ run function respawn:visuals/display_respawn_pos

execute store result score #respawn_type respawn.utils run function respawn:search/get_respawn_type
execute unless score #do_respawn_type_checks respawn.utils matches 0 run scoreboard players operation @s respawn.type = #respawn_type respawn.utils

execute if score #do_respawn_valid_checks respawn.utils matches 0 run return fail

execute if entity @n[type=marker,tag=invalid_respawn,tag=respawn_processed,distance=..1] run return fail
$execute if entity @n[type=marker,tag=respawn_x$(x)_y$(y)_z$(z),tag=respawn_processed,distance=..5] run return 1

scoreboard players set #bunk_bed respawn.utils 0
execute if score #respawn_type respawn.utils matches 0 run return fail
execute if score #respawn_type respawn.utils matches 1 run return run function respawn:search/process_forced_spawn
execute if score #respawn_type respawn.utils matches 2 unless function respawn:search/setup_bed_spawn run return fail
execute if score #respawn_type respawn.utils matches 3 unless function respawn:search/setup_respawn_anchor_spawn run return fail

$execute if score #show_respawn_visuals respawn.utils matches 0 as @n[type=marker,tag=respawn_x$(x)_y$(y)_z$(z),tag=!bunk_bed,distance=..5] at @s if function respawn:check_pos/check_respawn_valid run return run tag @s add respawn_processed
$execute if score #show_respawn_visuals respawn.utils matches 0 as @n[type=marker,tag=respawn_x$(x)_y$(y)_z$(z),tag=bunk_bed,distance=..5] if block ~ ~-1 ~ #beds at @s if function respawn:check_pos/check_respawn_valid run return run tag @s add respawn_processed

execute unless entity @n[type=marker,tag=respawn_iter] run summon marker ~ ~ ~ {Tags:["respawn_iter"]}
execute as @n[type=marker,tag=respawn_iter] run function respawn:search/search_setup

execute if score #any_valid respawn.utils matches 1 as @n[type=marker,tag=respawn_iter] run return run function respawn:search/add_valid_respawn_tags with storage respawn:macro respawn
execute as @n[type=marker,tag=respawn_iter] run return run function respawn:search/add_invalid_respawn_tags