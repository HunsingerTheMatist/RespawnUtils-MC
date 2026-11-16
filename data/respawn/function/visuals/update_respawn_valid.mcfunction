tag @s add respawn_processed

execute if score #valid_spawn respawn.utils matches 1 run data modify entity @s[type=block_display] block_state.Name set value "lime_stained_glass"
execute if score #valid_spawn respawn.utils matches 1 run return run data modify entity @s[type=block_display] glow_color_override set value -16711893

execute if score #valid_spawn respawn.utils matches 0 run data modify entity @s[type=block_display] block_state.Name set value "red_stained_glass"
execute if score #valid_spawn respawn.utils matches 0 run return run data modify entity @s[type=block_display] glow_color_override set value -1505015