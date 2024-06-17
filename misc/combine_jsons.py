import os
import glob
import json

# For experiment 1 (w principles)
w_files = glob.glob('misc/json_files/*w_principle_*')
print('Using principle files :', len(w_files))

# For experiment 2 (wo principle)
wo_files = glob.glob('misc/json_files/*wo_principle_*')
print('Without principle files :', len(wo_files))

# For experiment 3 (w & wo principle)
files = glob.glob('misc/json_files/*_principle_*')
print('Mixed principle files :', len(wo_files))

global_data = []
dir1 = 'misc/json_files/w_principles.json'
for file in w_files:
    data = json.load(open(file))
    global_data.extend(data)
json.dump(global_data, open(dir1, 'w'))

global_data = []
dir1 = 'misc/json_files/wo_principles.json'
for file in wo_files:
    data = json.load(open(file))
    global_data.extend(data)
json.dump(global_data, open(dir1, 'w'))

global_data = []
dir1 = 'misc/json_files/mix_principles.json'
for file in files:
    data = json.load(open(file))
    global_data.extend(data)
json.dump(global_data, open(dir1, 'w'))