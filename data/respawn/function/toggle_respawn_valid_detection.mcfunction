scoreboard players operation #tmp respawn.utils = #do_respawn_valid_checks respawn.utils
execute if score #tmp respawn.utils matches 0 run scoreboard players set #do_respawn_valid_checks respawn.utils 1
execute unless score #tmp respawn.utils matches 0 run scoreboard players set #do_respawn_valid_checks respawn.utils 0

execute if score #do_respawn_valid_checks respawn.utils matches 0 run return run tellraw @s [{"text":"Toggled 'Respawn Valid' detection", "color":"gold"}, " ", {"text":"Off", "color":"dark_red"}]
execute if score #do_respawn_valid_checks respawn.utils matches 1 run return run tellraw @s [{"text":"Toggled 'Respawn Valid' detection", "color":"gold"}, " ", {"text":"On", "color":"dark_green"}]