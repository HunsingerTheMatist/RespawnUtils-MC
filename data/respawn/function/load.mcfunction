# Set the current version
data modify storage respawn:data Version set value "1.0"

scoreboard objectives add respawn.utils dummy
scoreboard objectives add respawn.exists dummy "Has Respawn Pos"
scoreboard objectives add respawn.valid dummy "Respawn is Valid"
scoreboard objectives add respawn.type dummy "Respawn Type"
scoreboard objectives modify respawn.type numberformat fixed {text:"None", color:"red"}

# For chunk-flooring stuff with forceloads
scoreboard players set #16 respawn.utils 16

scoreboard players add #do_respawn_exists_checks respawn.utils 0
execute unless score #do_respawn_valid_checks respawn.utils matches 0.. run scoreboard players set #do_respawn_valid_checks respawn.utils 1
scoreboard players add #do_respawn_type_checks respawn.utils 0
execute unless score #show_respawn_visuals respawn.utils matches 0.. run scoreboard players set #show_respawn_visuals respawn.utils 1
execute unless score #check_valid_forced_spawn respawn.utils matches 0.. run scoreboard players set #check_valid_forced_spawn respawn.utils 1

scoreboard players display name respawn.status respawn.exists {text: "STATUS:", color:"yellow"}
scoreboard players display name respawn.status respawn.valid {text: "STATUS:", color:"yellow"}
scoreboard players display name respawn.status respawn.type {text: "STATUS:", color:"yellow"}
scoreboard players set respawn.status respawn.exists 1000
scoreboard players set respawn.status respawn.valid 1000
scoreboard players set respawn.status respawn.type 1000