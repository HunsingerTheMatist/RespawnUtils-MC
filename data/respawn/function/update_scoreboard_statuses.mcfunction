execute if score #do_respawn_exists_checks respawn.utils matches 0 run scoreboard players display numberformat respawn.status respawn.exists fixed {text:"OFF", color:"red"}
execute unless score #do_respawn_exists_checks respawn.utils matches 0 run scoreboard players display numberformat respawn.status respawn.exists fixed {text:"ON", color:"green"}

execute if score #do_respawn_valid_checks respawn.utils matches 0 run scoreboard players display numberformat respawn.status respawn.valid fixed {text:"OFF", color:"red"}
execute unless score #do_respawn_valid_checks respawn.utils matches 0 run scoreboard players display numberformat respawn.status respawn.valid fixed {text:"ON", color:"green"}

execute if score #do_respawn_type_checks respawn.utils matches 0 run scoreboard players display numberformat respawn.status respawn.type fixed {text:"OFF", color:"red"}
execute unless score #do_respawn_type_checks respawn.utils matches 0 run scoreboard players display numberformat respawn.status respawn.type fixed {text:"ON", color:"green"}