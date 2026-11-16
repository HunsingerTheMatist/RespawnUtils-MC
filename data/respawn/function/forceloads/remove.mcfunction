# Constant chunk width
scoreboard players set #16 respawn.utils 16

# Align marker to X chunk border
execute store result score #pos respawn.utils run data get entity @s Pos[0]
scoreboard players operation #pos respawn.utils /= #16 respawn.utils
execute store result entity @s Pos[0] double 16 run scoreboard players get #pos respawn.utils

# Align marker to Z chunk border
execute store result score #pos respawn.utils run data get entity @s Pos[2]
scoreboard players operation #pos respawn.utils /= #16 respawn.utils
execute store result entity @s Pos[2] double 16 run scoreboard players get #pos respawn.utils

# Align marker to lowest Y block
data modify entity @s Pos[1] set value -64

# Check chunk for markers from other packs
tag @s remove global.forceload
execute at @s unless entity @n[tag=global.forceload,dx=15,dy=320,dz=15] run forceload remove ~ ~

kill @s