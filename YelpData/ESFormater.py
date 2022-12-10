import json
from decimal import Decimal

GLOBAL_INDEX = 0


def generate_es_data(file_path):
    global GLOBAL_INDEX
    restaurants = json.load(open(file_path), parse_float=Decimal)
    ndjson = ""
    for rstr in restaurants:
        source = {
            'id': rstr['Business_ID'],
            'cuisine': rstr['Cuisine']
        }
        action = {"index": {"_id": str(GLOBAL_INDEX)}}
        GLOBAL_INDEX += 1

        ndjson += json.dumps(action) + '\n' + json.dumps(source) + '\n'

    return ndjson


temp = generate_es_data("yelpData.json")


print(temp)
