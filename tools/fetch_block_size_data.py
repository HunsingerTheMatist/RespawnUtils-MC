import re
import json

file_path = r"C:\Users\madhu\Downloads\block_data.json"

with open(file_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

heights = json_data["properties"]["height_external"]["entries"]
widths = json_data["properties"]["width_external"]["entries"]
bottoms = json_data["properties"]["collision_bottom_external"]["entries"]
block_ids = json_data["properties"]["java_block_id"]["entries"]
variants = json_data["properties"]["variants"]["entries"]

special_cases = {"Cluster": "Amethyst Cluster", "Large Bud": "Large Amethyst Bud", "Medium Bud": "Medium Amethyst Bud", "Small Bud": "Small Amethyst Bud"}

def get_block_id(name):
    if name in special_cases:
        name = special_cases[name]
    for key, value in block_ids.items():
        if isinstance(value, dict):
            for key2, val2 in value.items():
                if key2 == name:
                    return val2
        elif key == name:
            return value

tags = {}

for key, value in json_data["properties"].items():
    if not key.startswith("tag_"):
        continue
    tag_name = key.replace("tag_", "#")
    if len(value["entries"]) == 1 and False:
        stop = False
        for i, j in value["entries"].items():
            if not isinstance(j, dict):
                tags[tag_name] = i
                stop = True
                break
        if stop:
            continue
    tags[tag_name] = []
    for i, j in value["entries"].items():
        if not isinstance(j, dict):
            l = variants[i]
            if isinstance(l, list):
                for m in l:
                    block_id = get_block_id(m)
                    tags[tag_name].append(block_id)
            else:
                block_id = get_block_id(i)
                tags[tag_name].append(block_id)
        else:
            for k, l in j.items():
                if l == "Yes":
                    for m in k.split("<br>"):
                        block_id = get_block_id(m)
                        tags[tag_name].append(block_id)

#[print(str(i[0])) for i in tags.items()]
#exit()

top_exceptions = ["Anvil","Azalea","Cauldron","Composter","Doors","Dragon Egg","Glass Pane","Hopper","Iron Bars","Piston","Shulker Box","Stairs"]

bottom_exceptions = ["Anvil","Azalea","Lectern","Pale Moss Carpet","Piston","Shulker Box","Snow","Stairs","Walls"]

width_exceptions = ["Shulker Box"]

tags_to_use = ["air","all_hanging_signs","all_signs","wool_carpets","anvil","bamboo_blocks","banners","bars","base_stone_nether","base_stone_overworld","beacon_base_blocks","beds","beehives","buttons","campfires","candles","candle_cakes","cauldrons","cave_vines","ceiling_hanging_signs","chains","climbable","coal_ores","concrete_powder","copper","copper_chests","copper_golem_statues","copper_ores","corals","coral_blocks","crops","diamond_ores","dirt","doors","emerald_ores","fences","fence_gates","fire","flowers","flower_pots","gold_ores","ice","iron_ores","lanterns","lapis_ores","leaves","lightning_rods","logs","nylium","planks","pressure_plates","rails","redstone_ores","replaceable","sand","saplings","shulker_boxes","signs","slabs","small_flowers","stairs","stone_bricks","terracotta","trapdoors","underwater_bonemeals","walls","wall_hanging_signs","wart_blocks","wooden_shelves","wool","wool_carpets"]

tags_to_use2 = ["anvil","bamboo_blocks","bars","base_stone_nether","base_stone_overworld","beacon_base_blocks","beehives","cauldrons","coal_ores","concrete_powder","copper","copper_ores","coral_blocks","diamond_ores","dirt","doors","emerald_ores","fences","gold_ores","ice","iron_ores","lapis_ores","leaves","logs","nylium","planks","redstone_ores","sand","shulker_boxes","stairs","stone_bricks","terracotta","wall_hanging_signs","wart_blocks","wooden_shelves","wool"]

top16 = []
bottom16 = []
width16 = []

bottom0 = []

for key, value in block_ids.items():
    if key not in heights or key in top_exceptions:
        if isinstance(value, dict):
            for key2, val2 in value.items():
                top16.append(val2)
        else:
            top16.append(value)
top16.append("minecraft:bamboo")
for key, value in block_ids.items():
    if isinstance(value, dict):
        for key2, val2 in value.items():
            if "wall_hanging_sign" in val2:
                top16.append(val2)

for key, value in block_ids.items():
    if key not in bottoms or key in bottom_exceptions:
        if isinstance(value, dict):
            for key2, val2 in value.items():
                bottom16.append(val2)
        else:
            bottom16.append(value)
bottom16.append("minecraft:bamboo")
for key, value in block_ids.items():
    if isinstance(value, dict):
        for key2, val2 in value.items():
            if "wall" not in val2 and "piston" not in val2 and ("head" in val2 or "skull" in val2):
                bottom16.append(val2)

for key, value in block_ids.items():
    if key not in widths or key in width_exceptions:
        if isinstance(value, dict):
            for key2, val2 in value.items():
                width16.append(val2)
        else:
            width16.append(value)
width16.append("minecraft:piston")
width16.append("minecraft:sticky_piston")

for key, value in block_ids.items():
    if key in bottoms and isinstance(bottoms[key], str):
        if isinstance(value, dict):
            for key2, val2 in value.items():
                bottom0.append(val2)
        else:
            bottom0.append(value)
bottom0.append("#doors")
bottom0.append("#ceiling_hanging_signs")
bottom0.append(get_block_id("Bamboo Shoot"))
bottom0.append(get_block_id("Big Dripleaf Stem"))
bottom0.append("minecraft:ladder")

full_cubes = [i for i in top16 if i in bottom16 and i in width16]
top16 = [i for i in top16 if i not in full_cubes]
bottom16 = [i for i in bottom16 if i not in full_cubes]
#print("\"" + "\",\n\"".join().replace("minecraft:","") + "\"")

#exit()

lens3 = [i for i in top16 if i not in bottom16]
lens4 = [i for i in bottom16 if i not in top16]

new_top16 = [i for i in top16]
for key, value in tags.items():
    if key[1:] in tags_to_use and set(value).issubset(set(top16)):
        at_least_1 = False
        for block in value:
            if block in new_top16:
                at_least_1 = True
                new_top16.remove(block)
        if at_least_1:
            new_top16.append(key)
new_top16.remove("minecraft:ladder")

new_bottom16 = [i for i in bottom16]
for key, value in tags.items():
    if key[1:] in tags_to_use and set(value).issubset(set(bottom16)):
        at_least_1 = False
        for block in value:
            if block in new_bottom16:
                at_least_1 = True
                new_bottom16.remove(block)
        if at_least_1:
            new_bottom16.append(key)
new_bottom16.remove("minecraft:cake")
new_bottom16.remove("minecraft:ladder")
new_bottom16.remove("#doors")

new_bottom0 = [i for i in bottom0]
for key, value in tags.items():
    if set(value).issubset(set(bottom0)) and len(value) > 1:
        at_least_1 = False
        for block in value:
            if block in new_bottom0:
                at_least_1 = True
                new_bottom0.remove(block)
        if at_least_1:
            new_bottom0.append(key)

#new_bottom16 = [i for i in new_bottom16 if "glass_pane" not in i]
#new_bottom16.append("#tr:glass_panes")
new_bottom0.sort()
print("\"" + "\",\n\"".join(new_bottom0).replace("minecraft:","") + "\"")
#print([i for i in lens if i not in new_lens])
#print("\"" + "\",\n\"".join([i for i in new_lens if i not in lens]).replace("minecraft:","") + "\"")

exit()

lens3.sort()
print("HEIGHT Exclusives:")
print("\"" + "\",\n\"".join(lens3).replace("minecraft:","") + "\"")

lens4.sort()
print("\nBOTTOM Exclusives:")
print("\"" + "\",\n\"".join(lens4).replace("minecraft:","") + "\"")

exit()

values = {}

q = 0
def collect_lengths(states, obj):
    global values, q
    if isinstance(obj, dict):
        for key, value in obj.items():
            collect_lengths(states + "&" + key, value)
    elif isinstance(obj, list):
        for item in obj:
            collect_lengths(states, item)
    else:
        state_list = states.split("&")
        actual_states = [i for i in state_list if ":" in i]
        other_list = [i for i in state_list if ":" not in i]
        other_list.reverse()
        non_block_id_list = []
        block_id = None
        for item in other_list:
            block_id = get_block_id(item)
            if block_id:
                break
            elif item in tags.values():
                block_id = [i for i in tags.items() if i[1] == item][0][0]
                break
            elif item in block_ids:
                block_id = block_ids[item]
                break
            else:
                non_block_id_list.append(item)
        if not block_id:
            print(f"ERROR with {state_list[0]}")
            exit()
        if isinstance(block_id, dict):
            for _, value in block_id.items():
                process_length(value, actual_states, obj)
        elif isinstance(block_id, list):
            for value in block_id:
                process_length(value, actual_states, obj)
        else:
            process_length(block_id, actual_states, obj)
#        print(f"state_list: {state_list}")
#        print(f"actual_states: {actual_states}")
#        print(f"non_block_id_list: {non_block_id_list}")
#        print(f"block_id: {block_id}")
#        print()
#        q += 1
#        if q > 20:
#            exit()

def insert_val(block_id, val):
    global values
    if block_id not in values:
        values[block_id] = 0
    values[block_id] = max(values[block_id], val)

def process_length(block_id, states, length):
    global values, q
    if length == "Not Applicable":
        length = 0
    if isinstance(length, str):
        print(f"STRING: {length}")
        exit()
    if block_id == "#walls":
        insert_val(block_id, length)
        return
    all_states = get_all_states(states, 0)
    for state_list in all_states:
        full_block_id = block_id
        for state in state_list:
            full_block_id += f"[{state}]"
        insert_val(full_block_id, length)
#    q += 1
#    if q > 60:
#        [print(i) for i in values.items()]
#        exit()

#overrides = {"minecraft:piston_head": 16, "minecraft:piston[extended: true]": 16,

def get_all_states(states, depth):
    if depth >= len(states):
        return [[]]
    cur_states = get_all_states(states, depth + 1)
    new_states = []
    for i in states[depth].split("<br>"):
        for j in cur_states:
            new_states.append(j + [i])
    return new_states

for key, value in heights.items():
    collect_lengths(key, value)

#for 
[print(i) for i in values.items() if i[0].count("[") > 1]
#[print(i) for i in values.items() if "wall" in i[0] or "Wall" in i[0]]

exit()

def add_val(top, val):
    if val in lang_data_rev:
        return
    if top not in values:
        values[top] = set()
    values[top].add(val)

def collect_keys_recursively(top, obj):
    global values
#    print(obj)
#    exit()
    if isinstance(obj, dict):
        for key, value in obj.items():
            for _key in key.split("<br>"):
                add_val(top, _key)
#                print(f"{top} : {_key}")
            collect_keys_recursively(top, value)
    elif isinstance(obj, list):
        for item in obj:
            collect_keys_recursively(top, item)
            if isinstance(item, str):
                add_val(top, item)
#    elif isinstance(obj, str):
#        add_val(top, obj)

pixels = set()

#def search_recursive(obj):
#    global pixels
#    if isinstance(obj, dict):
#        for key, value in obj.items():
#            search_recursive(value)
#    elif isinstance(obj, list):
#        for item in obj:
#            search_recursive(item)
#    else:
#        pixels.add(obj)

for key, value in heights.items():
    search_recursive(value)

for item in pixels:
    print(item)

exit()

for property, section in json_data["properties"].items():
    entries = section.get("entries")
    if entries and "default_value" in section:
        default_val = section["default_value"]
        for key, value in entries.items():
            if value == default_val:
                print(property)
                print(f"- {key}")
    continue

    if entries:
        for key, value in entries.items():
            collect_keys_recursively(key, value)
#        break

for key, value in sorted(values.items()):
    print(f"\n[{key}]")
    for item in sorted(value):
        print(f"  - {item}")

exit()

def natural_key(s):
    parts = re.split(r'(\d+)', s)
    return [int(part) if part.isdigit() else part.lower() for part in parts]

def compare(a, b):
    if isinstance(a, str):
        return natural_key(a) <= natural_key(b)
    return a <= b

def is_sorted_naturally(values):
    return all(natural_key(values[i]) <= natural_key(values[i + 1]) for i in range(len(values) - 1))

def add_to_path(path, addition):
    addition = str(addition)
    if len(addition) >= 20 and "<br>" in addition:
        addition = addition[:20] + "..."
    return f"{path}.\"{addition}\""

count = 0

def check_order(path, depth, node):
    global count
    prev_item = None
    if isinstance(node, dict):
        for key, value in node.items():
            if prev_item is not None and compare(key, prev_item) and depth != 1:
                print(f"{(count := count + 1)}) {path}")
                print(f"- {prev_item}")
                print(f"- {key}\n")
            prev_item = key
            check_order(add_to_path(path, key), depth + 1, key)
            check_order(add_to_path(path, key), depth + 1, value)
    if isinstance(node, list):
        for value in node:
            if prev_item is not None and compare(value, prev_item):
                print(f"{(count := count + 1)}) {path}")
                print(f"- {prev_item}")
                print(f"- {value}\n")
            prev_item = value
            check_order(add_to_path(path, value), depth + 1, value)
    if isinstance(node, str):
        vals = node.split("<br>")
        if not is_sorted_naturally(vals):
            sorted_vals = sorted(vals, key=natural_key)
            new_str = "<br>".join(sorted_vals)
            print(f"{(count := count + 1)}) {path}")
            print(f"- {new_str}\n")

check_order("\"properties\"", 0, json_data["properties"])
exit()

def find_id(name):
    id = "[NONE]"
    if name in lang_data_rev:
        id = lang_data_rev[name][len("block."):].replace(".",":")
    elif "Wall Banner" in name:
        id = name.lower().replace(" ", "_")
        return f"minecraft:{id}"
    else:
        print(f"{name} has no ID!")
        exit()
    return id

for grouping, blocks in json_data["properties"]["variants"]["entries"].items():
    if isinstance(blocks, list):
#        values[grouping] = {}
        print(f"\"{grouping}\": {{")
        l = []
        for block in blocks:
             l.append(f"    \"{block}\": \"{find_id(block)}\"")
#            print(f"\"{block}\": \"{find_id(block)}\",
#            values[grouping][block] = find_id(block)
        print(",\n".join(l))
        print("},")
#    elif grouping != blocks:
#        print(f"{grouping} != {blocks}")
#        exit()
    else:
        print(f"\"{grouping}\": \"{find_id(blocks)}\",")
#        values[grouping] = {blocks, find_id(blocks)}
    

exit()

for property, section in json_data["properties"].items():
    entries = section.get("entries")
    if entries:
        for key, value in entries.items():
            collect_keys_recursively(key, value)
#        break

for key, value in sorted(values.items()):
    print(f"\n[{key}]")
    for item in sorted(value):
        print(f"  - {item}")

#for entry in heights:
#    print(entry)
#    exit()


#print(len())