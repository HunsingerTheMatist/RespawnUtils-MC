tag @s add respawn_processed

# The block state has both keys so every version reads it: `Name` up to 26.2, `id` from 26.3
execute if score #valid_spawn respawn.utils matches 1 run data modify entity @s[type=block_display] block_state set value {Name: "lime_stained_glass", id: "lime_stained_glass"}
execute if score #valid_spawn respawn.utils matches 1 run return run data modify entity @s[type=block_display] glow_color_override set value -16711893

execute if score #valid_spawn respawn.utils matches 0 run data modify entity @s[type=block_display] block_state set value {Name: "red_stained_glass", id: "red_stained_glass"}
execute if score #valid_spawn respawn.utils matches 0 run return run data modify entity @s[type=block_display] glow_color_override set value -1505015