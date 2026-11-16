# Add a forceload for the current chunk, store it for later removal, and then return fail for exiting early out of 'search_for_valid_respawn'

forceload add ~ ~
summon marker ~ ~ ~ {Tags: ["respawn.forceload","global.forceload"]}
return fail