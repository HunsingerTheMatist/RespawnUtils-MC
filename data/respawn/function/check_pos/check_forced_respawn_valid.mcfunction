# Forced spawn via '/spawnpoint' command has different criteria than regular respawn point:
# 1) Support is not required under the player
# 2) Blocks inside are not determined by block hitbox but instead by the block's material
#    so things like regular coral plants can be spawned inside since they are considered vegetation
#    while dead coral plants obstruct spawn since they are considered 'stone'

execute if block ~ ~ ~ #respawn:forced_spawn_invalid run return fail
execute if block ~ ~1 ~ #respawn:forced_spawn_invalid run return fail
execute unless block ~ ~ ~ #respawn:forced_spawn_valid run return fail
execute unless block ~ ~1 ~ #respawn:forced_spawn_valid run return fail

return 1