execute store success score #tmp respawn.utils run data modify storage respawn:macro respawn set from entity @s respawn
execute unless score #do_respawn_exists_checks respawn.utils matches 0 run scoreboard players operation @s respawn.exists = #tmp respawn.utils
execute if score #show_respawn_visuals respawn.utils matches 0 if score #do_respawn_valid_checks respawn.utils matches 0 if score #do_respawn_type_checks respawn.utils matches 0 run return 1

execute if score #tmp respawn.utils matches 0 unless score #do_respawn_valid_checks respawn.utils matches 0 run scoreboard players set @s respawn.valid 0
execute if score #tmp respawn.utils matches 0 unless score #do_respawn_type_checks respawn.utils matches 0 run scoreboard players set @s respawn.type 0
execute if score #tmp respawn.utils matches 0 unless score #do_respawn_type_checks respawn.utils matches 0 run function respawn:update_respawn_type_text
execute if score #tmp respawn.utils matches 0 run return 1

data modify storage respawn:macro respawn.x set from storage respawn:macro respawn.pos[0]
data modify storage respawn:macro respawn.y set from storage respawn:macro respawn.pos[1]
data modify storage respawn:macro respawn.z set from storage respawn:macro respawn.pos[2]
execute unless data storage respawn:macro respawn.dimension run data modify storage respawn:macro respawn.dimension set value "minecraft:overworld"

execute store success score #tmp respawn.utils run function respawn:relocate_to_respawn_pos with storage respawn:macro respawn
execute unless score #do_respawn_type_checks respawn.utils matches 0 run function respawn:update_respawn_type_text
execute unless score #do_respawn_valid_checks respawn.utils matches 0 run scoreboard players operation @s respawn.valid = #tmp respawn.utils

return 1