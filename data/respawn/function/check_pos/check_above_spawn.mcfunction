# Check if the player is able to fit under/inside the current block, dependent on their height offset

# The player can always spawn inside blocks with no collision ('bottom0')
execute if block ~ ~ ~ #respawn:bottom_0 run return 1
execute if predicate respawn:bottom_0 run return 1

# The player can never spawn inside blocks with collision on the bottom-most face ('bottom16')
execute if block ~ ~ ~ #respawn:bottom_16 run return fail
execute if predicate respawn:bottom_16 run return fail

# Exit early if the player wouldn't be able to fit under any future blocks
execute if score #respawn.max_bottom tmp matches ..19 run return fail
execute if block ~ ~ ~ #respawn:bottom_2 run return 1

execute if score #respawn.max_bottom tmp matches ..29 run return fail
execute if predicate respawn:bottom_3 run return 1

execute if score #respawn.max_bottom tmp matches ..39 run return fail
execute if predicate respawn:bottom_4 run return 1

execute if score #respawn.max_bottom tmp matches ..49 run return fail
execute if predicate respawn:bottom_5 run return 1

execute if score #respawn.max_bottom tmp matches ..69 run return fail
execute if predicate respawn:bottom_7 run return 1

execute if score #respawn.max_bottom tmp matches ..79 run return fail
execute if predicate respawn:bottom_8 run return 1

execute if score #respawn.max_bottom tmp matches ..89 run return fail
execute if predicate respawn:bottom_9 run return 1

execute if score #respawn.max_bottom tmp matches ..94 run return fail
execute if predicate respawn:bottom_9.5 run return 1

execute if score #respawn.max_bottom tmp matches ..99 run return fail
execute if predicate respawn:bottom_10 run return 1

execute if score #respawn.max_bottom tmp matches ..109 run return fail
execute if block ~ ~ ~ #respawn:bottom_11 run return 1
execute if predicate respawn:bottom_11 run return 1

execute if score #respawn.max_bottom tmp matches ..119 run return fail
execute if block ~ ~ ~ #respawn:bottom_12 run return 1
execute if predicate respawn:bottom_12 run return 1

execute if score #respawn.max_bottom tmp matches ..129 run return fail
execute if block ~ ~ ~ #respawn:bottom_13 run return 1
execute if predicate respawn:bottom_13 run return 1

execute if score #respawn.max_bottom tmp matches ..139 run return fail
execute if predicate respawn:bottom_14 run return 1

execute if score #respawn.max_bottom tmp matches ..149 run return fail
execute if block ~ ~ ~ #respawn:bottom_15 run return 1

# Stuff for debug purposes
summon item_frame ~ ~ ~ {Invisible: true, Tags:["respawn_current"]}
tellraw @a [{text: "Unknown block for respawn check located at pos: ", color:"red"},{entity:"@n[type=item_frame,tag=respawn_current]", nbt:"block_pos"}]
kill @n[type=item_frame,tag=respawn_current]

return fail