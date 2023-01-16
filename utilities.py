import yaml
import random
import string


def yaml_loadfile(filepath):
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data


def consumer_group_id():
    num_of_string_char = 10
    consumer_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num_of_string_char))
    return str(consumer_id)
