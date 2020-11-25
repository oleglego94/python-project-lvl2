from collections import OrderedDict
from gendiff.loading import load_file


def build_diff_dict(old_dict, new_dict):
    diff_dict = {}

    old_keys = set(old_dict.keys())
    new_keys = set(new_dict.keys())

    added_keys = new_keys - old_keys
    for key in added_keys:
        diff_dict[key] = ['ADDED', new_dict[key]]

    removed_keys = old_keys - new_keys
    for key in removed_keys:
        diff_dict[key] = ['REMOVED', old_dict[key]]

    common_keys = old_keys & new_keys
    for key in common_keys:
        old_value = old_dict[key]
        new_value = new_dict[key]
        if isinstance(old_value, dict) and isinstance(new_value, dict):
            diff_dict[key] = ['NESTED', build_diff_dict(old_value, new_value)]
        elif old_value != new_value:
            diff_dict[key] = ['CHANGED', old_value, new_value]
        else:
            diff_dict[key] = ['UNCHANGED', old_value]

    return OrderedDict(sorted(diff_dict.items()))


def generate_diff(file_path_before, file_path_after, formatter):
    old_file = load_file(file_path_before)
    new_file = load_file(file_path_after)
    diff = build_diff_dict(old_file, new_file)
    return formatter(diff)
