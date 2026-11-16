tag @s remove respawn_iter
tag @s add valid_respawn
tag @s add respawn_processed
$tag @s add respawn_x$(x)_y$(y)_z$(z)

# If the bed is a 'bunk bed' and the current y value is at the position of the lower bed, add the 'bunk_bed' tag for tracking purposes
execute if score #bunk_bed respawn.utils matches 1 if score #currY respawn.utils matches -1 run tag @s add bunk_bed

return 1