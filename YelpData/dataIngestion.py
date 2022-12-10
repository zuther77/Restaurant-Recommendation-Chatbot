import boto3
import json
import datetime
from decimal import Decimal


with open('yelpData.json', 'r', encoding="utf8") as f:
    data_list = json.load(f, parse_float=Decimal)
    # print(data_list)


dyn_resource = boto3.resource('dynamodb')
table = dyn_resource.Table('yelpRestaurants')

count = 0
with table.batch_writer() as batch:
    for restaurants in data_list:
        restaurants_name = restaurants["Name"]
        restaurants["insertedAtTimestamp"] = str(datetime.datetime.now())
        print("Adding " + str(restaurants_name))
        batch.put_item(Item=restaurants)
        count += 1

    print(" Successfully added " + str(count) + " items")
