execute if dimension minecraft:overworld run return fail
execute if dimension minecraft:the_end run return fail

execute unless data storage respawn:macro respawn{forced: 1b} if block ~ ~ ~ respawn_anchor[charges=0] run return fail

scoreboard players set #startX respawn.utils -1
scoreboard players set #startY respawn.utils -1
scoreboard players set #startZ respawn.utils -1
scoreboard players set #endX respawn.utils 1
scoreboard players set #endY respawn.utils 1
scoreboard players set #endZ respawn.utils 1

return 1