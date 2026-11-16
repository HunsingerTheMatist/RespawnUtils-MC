scoreboard players operation #currZ respawn.utils = #startZ respawn.utils
scoreboard players add #currY respawn.utils 1

# Update values in storage
execute store result entity @s Pos[1] double 1 run scoreboard players get #currY respawn.utils
execute store result entity @s Pos[2] double 1 run scoreboard players get #currZ respawn.utils