scoreboard players operation #currX respawn.utils = #startX respawn.utils
scoreboard players add #currZ respawn.utils 1

# Update value in storage (Pos[0] is updated at the end of each step so is unnecessary here)
execute store result entity @s Pos[2] double 1 run scoreboard players get #currZ respawn.utils