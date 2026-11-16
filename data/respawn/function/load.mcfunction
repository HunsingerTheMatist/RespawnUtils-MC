scoreboard objectives add respawn.utils dummy
scoreboard objectives add respawn.exists dummy "Has Respawn Pos"
scoreboard objectives add respawn.valid dummy "Respawn is Valid"
scoreboard objectives add respawn.type dummy "Respawn Type"
scoreboard objectives modify respawn.type numberformat fixed {text:"None", color:"red"}

# For chunk-flooring stuff with forceloads
scoreboard players set #16 respawn.utils 16

scoreboard players add #do_respawn_exists_checks respawn.utils 0
scoreboard players add #do_respawn_valid_checks respawn.utils 0
scoreboard players add #do_respawn_type_checks respawn.utils 0
scoreboard players add #show_respawn_visuals respawn.utils 0
execute unless score #check_valid_forced_spawn respawn.utils matches 0.. run scoreboard players set #check_valid_forced_spawn respawn.utils 1

execute unless entity c7475e5a-8dc0-45be-bdf0-fce9868902e3 run summon marker 0 0 0 {UUID:[I;-951624102,-1916779074,-1108280087,-2037841181], Tags:["respawn_scoreboard"]}
scoreboard players display name c7475e5a-8dc0-45be-bdf0-fce9868902e3 respawn.exists {text: "STATUS:", color:"yellow"}
scoreboard players display name c7475e5a-8dc0-45be-bdf0-fce9868902e3 respawn.valid {text: "STATUS:", color:"yellow"}
scoreboard players display name c7475e5a-8dc0-45be-bdf0-fce9868902e3 respawn.type {text: "STATUS:", color:"yellow"}
scoreboard players set c7475e5a-8dc0-45be-bdf0-fce9868902e3 respawn.exists 1000
scoreboard players set c7475e5a-8dc0-45be-bdf0-fce9868902e3 respawn.valid 1000
scoreboard players set c7475e5a-8dc0-45be-bdf0-fce9868902e3 respawn.type 1000