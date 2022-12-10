import json
import boto3
from botocore.exceptions import ClientError
import requests

import os



def get_message_from_SQS():
    # manually pull mes from SQS
    sqs = boto3.client('sqs')
    response = sqs.receive_message(
        QueueUrl=sqs.get_queue_url(QueueName="SQS1")["QueueUrl"],
        AttributeNames=['All'],
        MaxNumberOfMessages=1
    )

    return response


def search_cuisine_ElasticSearch(cuisine):
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    host = os.environ['ELASTIC_SOURCE']
    index = 'restaurants'
    url = host + '/' + index + '/_search'
    query = {
        "size": 100,
        "query": {
            "multi_match": {
                "query": cuisine,
            }
        }
    }
    
    
    headers = {"Content-Type": "application/json"}
    r = requests.get(url, auth= ( os.environ["ELASTIC_USER"] , os.environ["ELASTIC_PASS"] ) ,
                     headers=headers, data=json.dumps(query))
    response = r.json()
    

    HITS = response["hits"]["hits"]
    business_id = []

    for hit in HITS:
        business_id.append(str(hit['_id']))

    return business_id[:3]


def get_restaurant_from_DynamoDB(business_ids):
    res = []
    client = boto3.resource('dynamodb')
    table = client.Table('yelpRestaurants')
    for id in business_ids:
        response = table.get_item(Key={'Business_ID': id})
        res.append((response["Item"]["Address"], response["Item"]["Name"]))
    return res


def sentMail_SES(cuisine, noOfPeople, booking_date, booking_time, email, restaurant_list):
    # Using Elastic response to user by SES

    SENDER = "diningconciergechatbot@proton.me"
    RECIPIENT = email
    ses_client = boto3.client('ses', 'us-east-1')


    BODY_TEXT = "Hello! Here are my {Restcuisine} restaurant suggestions for {numberOfPeople} people, for {diningDate} at {diningTime}: 1. {restaurantName1}, located at {address1}, 2. {restaurantName2}, located at {address2}, 3. {restaurantName3}, located at {address3}. Enjoy your meal!".format(
        Restcuisine=cuisine, numberOfPeople=noOfPeople, diningDate=booking_date, diningTime=booking_time, restaurantName1=restaurant_list[0][1], address1=restaurant_list[0][0], restaurantName2=restaurant_list[1][1], address2=restaurant_list[1][0], restaurantName3=restaurant_list[2][1], address3=restaurant_list[2][0],)

    try:
        # Provide the contents of the email.
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {

                    'Data': "Testing"
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        return response



def delete_message_SQS(receipt_handle):
    sqs = boto3.client('sqs')
    response = sqs.delete_message( QueueUrl= sqs.get_queue_url(QueueName="SQS1")["QueueUrl"], ReceiptHandle=receipt_handle )
    return response

def lambda_handler(event, context):
    # TODO implement
    
    ## Get message from SQS 
    queue_message = get_message_from_SQS()
    
    
    ## Make all data lowercase
    message_body_list = list(
        map(lambda x: x.lower(), queue_message["Messages"][0]["Body"].split(",")))

    ## Get reciept handle of the messgae for deletion later  
    receipt_handle = queue_message["Messages"][0]["ReceiptHandle"]

    # get data from message
    cuisine = message_body_list[0]
    noOfPeople = message_body_list[4]
    time = message_body_list[1]
    date = message_body_list[2]
    email = message_body_list[-1]

    ## Get Recommendations
    business_ids = search_cuisine_ElasticSearch(cuisine)
    restaurants = get_restaurant_from_DynamoDB(business_ids)
    response = sentMail_SES(cuisine, noOfPeople, time, date, email, restaurants)


    #Delete message from SQS 
    response = delete_message_SQS(receipt_handle)

    return response
