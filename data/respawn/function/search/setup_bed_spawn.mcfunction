execute if dimension minecraft:the_nether run return fail
execute if dimension minecraft:the_end run return fail

scoreboard players set #startX respawn.utils -1
scoreboard players set #startY respawn.utils 0
scoreboard players set #startZ respawn.utils -1
scoreboard players set #endX respawn.utils 1
scoreboard players set #endY respawn.utils 0
scoreboard players set #endZ respawn.utils 1

execute if block ~ ~ ~ #beds[facing=north] run scoreboard players add #endZ respawn.utils 1
execute if block ~ ~ ~ #beds[facing=south] run scoreboard players remove #startZ respawn.utils 1
execute if block ~ ~ ~ #beds[facing=east] run scoreboard players remove #startX respawn.utils 1
execute if block ~ ~ ~ #beds[facing=west] run scoreboard players add #endX respawn.utils 1

execute store result score #bunk_bed respawn.utils if block ~ ~-1 ~ #beds
execute if score #bunk_bed respawn.utils matches 1 run scoreboard players remove #startY respawn.utils 1

return 1