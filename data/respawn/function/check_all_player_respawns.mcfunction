tag @e[type=marker,tag=respawn_processed] remove respawn_processed
tag @e[type=block_display,tag=respawn_processed] remove respawn_processed

execute as @a[tag=!respawn_invalid_player] run function respawn:check_single_player_respawn

kill @e[type=marker,tag=valid_respawn,tag=!respawn_processed]
kill @e[type=marker,tag=invalid_respawn,tag=!respawn_processed]
kill @e[type=block_display,tag=respawn_visual,tag=!respawn_processed]