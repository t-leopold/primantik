import json
from collections import defaultdict
from os import path
from typing import cast

type RawValue = str | int | float | bool
type ProValue = str | int

pretty_print: bool = False
input_file: str = path.join(path.dirname(__file__), 'results-raw.txt')
output_file: str = path.join(path.dirname(__file__), 'results-processed.txt')
keys_to_keep_isi: dict[str, list[str]] = {
    'sender_id' : ['sender_id', 'str'],
    'prime' : ['prime', 'str'],
    'target' : ['target', 'str'],
    'timeout' : ['soa_soll', 'num'],
    'duration' : ['soa_ist', 'num']
}
keys_to_keep_dec: dict[str, list[str]] = {
    'sender_id' : ['sender_id', 'str'],
    'correct' : ['response', 'bool'],
    'duration' : ['rt', 'num']
}

def truncate_sender_id(sender_id: str) -> str:
    return '_'.join(sender_id.split('_')[:-1])

def test_dict(obj: dict[str, RawValue]) -> bool:
    return obj.get('sender') in ('Isi', 'Decision') and obj.get('condition') == 'w'

def reduce_obj(obj: dict[str, RawValue]) -> dict[str, ProValue]:
    keys_to_keep: dict[str, list[str]] = keys_to_keep_isi if obj['sender'] == 'Isi' else keys_to_keep_dec
    reduced_obj_bool: dict[str, str] = {v[0]: str(obj.get(k, 'Timeout')) for k, v in keys_to_keep.items() if v[1] == 'bool'}
    reduced_obj_num: dict[str, int] = {v[0]: round(cast(float, obj[k])) for k, v in keys_to_keep.items() if v[1] == 'num'}
    if obj['sender'] == 'Decision':
        reduced_obj_num['rt'] = -1 if reduced_obj_bool['response'] == 'Timeout' else reduced_obj_num['rt']
    reduced_obj_str: dict[str, str] = {v[0]: cast(str, obj[k]) for k, v in keys_to_keep.items() if v[1] == 'str'}
    reduced_obj_str['sender_id'] = truncate_sender_id(cast(str, obj['sender_id']))
    return {**reduced_obj_str, **reduced_obj_num, **reduced_obj_bool}

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line_number, line in enumerate(infile, 1):
        try:
            json_array: list[dict[str, RawValue]] = json.loads(line)[1:]

            # Step 1: Filter and transform
            processed_objects: list[dict[str, ProValue]] = []
            for obj in json_array:
                if not test_dict(obj):
                    continue
                processed_objects.append(reduce_obj(obj))

            # Step 2: Group by sender_id
            grouped: defaultdict[str, list[dict[str, ProValue]]] = defaultdict(list)
            for obj in processed_objects:
                sid: str = cast(str, obj['sender_id'])
                grouped[sid].append({k: v for k, v in obj.items() if k != 'sender_id'})
            filtered_dict: dict[str, list[dict[str, ProValue]]] = {k: v for k, v in grouped.items() if len(v) == 2}

            # Step 3: Merge objects with same sender_id
            merged_array: list[dict[str, ProValue]] = []
            for items in filtered_dict.values():
                merged: dict[str, ProValue] = {**items[0], **items[1]}
                merged_array.append(merged)

            # Step 4: Write result
            if len(merged_array) != 0:
                outfile.write(json.dumps(merged_array, ensure_ascii=False, indent=2 if pretty_print else None) + '\n')

        except json.JSONDecodeError as e:
            print(f'Line {line_number}: Invalid JSON. Skipping. Error: {e}')
