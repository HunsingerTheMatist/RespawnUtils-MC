scoreboard players set #any_valid respawn.utils 0

execute store result score #posX respawn.utils run data get storage respawn:macro respawn.x
execute store result score #posY respawn.utils run data get storage respawn:macro respawn.y
execute store result score #posZ respawn.utils run data get storage respawn:macro respawn.z

scoreboard players operation #startX respawn.utils += #posX respawn.utils
scoreboard players operation #startY respawn.utils += #posY respawn.utils
scoreboard players operation #startZ respawn.utils += #posZ respawn.utils

scoreboard players operation #endX respawn.utils += #posX respawn.utils
scoreboard players operation #endY respawn.utils += #posY respawn.utils
scoreboard players operation #endZ respawn.utils += #posZ respawn.utils

scoreboard players operation #currX respawn.utils = #startX respawn.utils
scoreboard players operation #currY respawn.utils = #startY respawn.utils
scoreboard players operation #currZ respawn.utils = #startZ respawn.utils

execute store result entity @s Pos[0] double 1 run scoreboard players get #currX respawn.utils
execute store result entity @s Pos[1] double 1 run scoreboard players get #currY respawn.utils
execute store result entity @s Pos[2] double 1 run scoreboard players get #currZ respawn.utils

function respawn:search/search_step