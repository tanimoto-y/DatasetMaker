import glob
import sys
import json
import os

folder_path = sys.argv[1]
if folder_path[1:] == '/':
    folder_path = folder_path[:-1]

json_files_list = sorted(glob.glob(folder_path + "/*.json"))


class Item:
    def __init__(self):
        self.data_index = -1
        self.common_clothes_list_index = -1
        self.id = -1

        self.category_name = ''
        self.category_id = 0
        self.style = 0
        self.bounding_box = []
        self.landmarks = []
        self.segmentation = []
        self.scale = 0
        self.occlusion = 0
        self.zoom_in = 0
        self.viewpoint = 0


class Data:
    def __init__(self):
        self.file_name = ''

        self.source = ''
        self.pair_id = 0
        self.item = []


class CommonClothes:
    def __init__(self):
        self.list = []


data = []
items = {}
common_item_list = []
data_index = 0
next_item_id = 0
for count, json_file_path in enumerate(json_files_list):
    print(str(count+1) + '/' + str(len(json_files_list)))

    new_data = Data()
    new_data.file_name = os.path.splitext(os.path.basename(json_file_path))[0]
    with open(json_file_path) as json_file:
        new_data_dict = json.load(json_file)

    new_data.source = new_data_dict['source']
    new_data.pair_id = new_data_dict['pair_id']

    index = 1
    for item in new_data_dict:
        if item[:4] != 'item':
            continue

        new_item = Item()
        new_item.data_index = data_index

        new_item.category_name = new_data_dict['item'+str(index)]['category_name']
        new_item.category_id = new_data_dict['item'+str(index)]['category_id']
        new_item.style = new_data_dict['item'+str(index)]['style']
        new_item.bounding_box = new_data_dict['item'+str(index)]['bounding_box']
        new_item.landmarks = new_data_dict['item'+str(index)]['landmarks']
        new_item.segmentation = new_data_dict['item'+str(index)]['segmentation']
        new_item.scale = new_data_dict['item'+str(index)]['scale']
        new_item.occlusion = new_data_dict['item'+str(index)]['occlusion']
        new_item.zoom_in = new_data_dict['item'+str(index)]['zoom_in']
        new_item.viewpoint = new_data_dict['item'+str(index)]['viewpoint']

        new_data.item.append(new_item)

        index += 1

    if str(new_data.pair_id) in items:
        item_number = 0
        for new_data_item in new_data.item:
            if new_data_item.style == 0:
                continue

            new_data_item_dict = {
                'data_index': new_data.file_name,
                'item_number': item_number
            }
            if str(new_data_item.style) in items[str(new_data.pair_id)]:
                items[str(new_data.pair_id)][str(new_data_item.style)].append(new_data_item_dict)
            else:
                items[str(new_data.pair_id)][str(new_data_item.style)] = [new_data_item_dict]

            item_number += 1
    else:
        items[str(new_data.pair_id)] = {}

        item_number = 0
        for new_data_item in new_data.item:
            if new_data_item.style == 0:
                continue

            new_data_item_dict = {
                'data_index': new_data.file_name,
                'item_number': item_number
            }
            items[str(new_data.pair_id)][str(new_data_item.style)] = [new_data_item_dict]

            item_number += 1

    data.append(new_data)
    data_index += 1

print(items)
