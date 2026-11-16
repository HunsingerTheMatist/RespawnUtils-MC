scoreboard players operation #tmp respawn.utils = #show_respawn_visuals respawn.utils
execute if score #tmp respawn.utils matches 0 run scoreboard players set #show_respawn_visuals respawn.utils 1
execute unless score #tmp respawn.utils matches 0 run scoreboard players set #show_respawn_visuals respawn.utils 0

execute if score #show_respawn_visuals respawn.utils matches 0 run return run tellraw @s [{"text":"Toggled respawn visuals", "color":"gold"}, " ", {"text":"Off", "color":"dark_red"}]
execute if score #show_respawn_visuals respawn.utils matches 1 run return run tellraw @s [{"text":"Toggled respawn visuals", "color":"gold"}, " ", {"text":"On", "color":"dark_green"}]