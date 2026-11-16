# Checks to see if the current position is valid for the player to respawn at

# Criteria for a valid respawn position:
# 1) The block below must be of pixel height 16+ OR the block at current position must be of pixel height [0 < height < 16]
#    Notes: Only the upper-most collision of the block is considered, so things like the bowl of a cauldron are ignored
#           Anything climbable (including open trapdoors) is considered having a height of 0
#           Scaffolding is invalid for either the block below or the current block
# 2) The player hitbox (offset by the height determined by #1) must not collide with any block hitboxes
#    Notes: Scaffolding is considered as having a bottom collision of 2 (ie: 2 from the top)
#           End portals & End gateways are in the #invalid_spawn_inside tag and cannot be at the current block or the block above,
#             but they can be in the 2nd block above & therefore collided with on respawn, which is likely a bug in the game

# If the current block's height is 16 or the block above is a full block the spawn is not valid
execute if block ~ ~ ~ #respawn:top_16 run return fail
execute if block ~ ~1 ~ #respawn:full_blocks run return fail

# Check for invalid spawn special-cases
execute if block ~ ~ ~ #invalid_spawn_inside run return fail
execute if block ~ ~1 ~ #invalid_spawn_inside run return fail

# Check the current block or the block below for a valid top surface to spawn on
scoreboard players set #respawn.height tmp -1
execute positioned ~ ~-1 ~ run function respawn:check_pos/check_below_spawn
execute positioned ~ ~ ~ run function respawn:check_pos/check_at_spawn

# Failed to find a valid top surface to spawn on
execute if score #respawn.height tmp matches -1 run return fail

# Add player height to top surface, subtract the height of a block, and then subtract that from the height of a block
#  to obtain the maximum allowed 'bottom' collision value for the block above
# Equation: max_bottom = 160 - (288 + height - 160) -> max_bottom = 32 - height
scoreboard players set #respawn.max_bottom tmp 32
scoreboard players operation #respawn.max_bottom tmp -= #respawn.height tmp

# Check block above to see if the player can fit
execute positioned ~ ~1 ~ unless function respawn:check_pos/check_above_spawn run return fail

# If necessary, check block 2 above to see if the player can fit
execute unless score #respawn.max_bottom tmp matches ..-1 run return 1
scoreboard players add #respawn.max_bottom tmp 160
execute positioned ~ ~2 ~ run return run function respawn:check_pos/check_above_spawn