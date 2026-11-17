# Check if the block below the spawn has a height of 16 pixels or greater
execute if block ~ ~ ~ #respawn:top_24 run return run scoreboard players set #height respawn.utils 80
execute if block ~ ~ ~ #respawn:top_16 run return run scoreboard players set #height respawn.utils 0
execute if predicate respawn:top_24 run return run scoreboard players set #height respawn.utils 80
execute if predicate respawn:top_16 run return run scoreboard players set #height respawn.utils 0