function respawn:update_scoreboard_statuses

execute if score #show_respawn_visuals respawn.utils matches 0 run kill @e[type=block_display,tag=respawn_visual]

execute if score #do_respawn_exists_checks respawn.utils matches 0 if score #do_respawn_valid_checks respawn.utils matches 0 \
if score #do_respawn_type_checks respawn.utils matches 0 if score #show_respawn_visuals respawn.utils matches 0 run return run function respawn:forceloads/remove_all

function respawn:check_all_player_respawns