# Get the height of the block the player is attempting to spawn inside

# Handle the most common case
execute if block ~ ~ ~ #air run return 0

# Handle scaffolding special-case
execute if block ~ ~ ~ scaffolding run return run scoreboard players set #respawn.height tmp -1

# Handle all other cases
execute if block ~ ~ ~ #respawn:top_24 run return run scoreboard players set #respawn.height tmp -1
# Tag #top_16 is handled by base function
execute if block ~ ~ ~ #respawn:top_15 run return run scoreboard players set #respawn.height tmp 150
execute if block ~ ~ ~ #respawn:top_14 run return run scoreboard players set #respawn.height tmp 140
execute if block ~ ~ ~ #respawn:top_13 run return run scoreboard players set #respawn.height tmp 130
execute if block ~ ~ ~ #respawn:top_12 run return run scoreboard players set #respawn.height tmp 120
execute if block ~ ~ ~ #respawn:top_11 run return run scoreboard players set #respawn.height tmp 110
execute if block ~ ~ ~ #respawn:top_10 run return run scoreboard players set #respawn.height tmp 100
execute if block ~ ~ ~ #respawn:top_9 run return run scoreboard players set #respawn.height tmp 90
execute if predicate respawn:top_24 run return run scoreboard players set #respawn.height tmp -1
execute if predicate respawn:top_16 run return run scoreboard players set #respawn.height tmp -1
execute if predicate respawn:top_15 run return run scoreboard players set #respawn.height tmp 150
execute if predicate respawn:top_14 run return run scoreboard players set #respawn.height tmp 140
execute if predicate respawn:top_13 run return run scoreboard players set #respawn.height tmp 130
execute if predicate respawn:top_12 run return run scoreboard players set #respawn.height tmp 120
execute if predicate respawn:top_10 run return run scoreboard players set #respawn.height tmp 100
execute if predicate respawn:top_9.5 run return run scoreboard players set #respawn.height tmp 95

# Exit early if the block below had a height of 24
execute if score #respawn.height tmp matches 80 run return 0

execute if block ~ ~ ~ #respawn:top_8 run return run scoreboard players set #respawn.height tmp 80
execute if block ~ ~ ~ #respawn:top_7 run return run scoreboard players set #respawn.height tmp 70
execute if block ~ ~ ~ #respawn:top_6 run return run scoreboard players set #respawn.height tmp 60
execute if block ~ ~ ~ #respawn:top_2 run return run scoreboard players set #respawn.height tmp 20
execute if block ~ ~ ~ #respawn:top_1.5 run return run scoreboard players set #respawn.height tmp 15
execute if block ~ ~ ~ #respawn:top_1 run return run scoreboard players set #respawn.height tmp 10
execute if predicate respawn:top_8 run return run scoreboard players set #respawn.height tmp 80
execute if predicate respawn:top_7 run return run scoreboard players set #respawn.height tmp 70
execute if predicate respawn:top_6 run return run scoreboard players set #respawn.height tmp 60
execute if predicate respawn:top_5 run return run scoreboard players set #respawn.height tmp 50
execute if predicate respawn:top_4 run return run scoreboard players set #respawn.height tmp 40
execute if predicate respawn:top_3 run return run scoreboard players set #respawn.height tmp 30
execute if predicate respawn:top_2 run return run scoreboard players set #respawn.height tmp 20