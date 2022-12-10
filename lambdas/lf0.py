import json

import boto3


def lambda_handler(event, context):

    client = boto3.client('lexv2-runtime')

    print(event)

    response = client.recognize_text(
        botId='C1UK3PHZRE',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId="test_session",
        text=event["messages"][0]["unstructured"]["text"]
    )

    print(response)

    # default case
    botMessage = "Something went wrong!! Please try again"
    if response['messages'] is not None or len(response['messages']) > 0:
        botMessage = response['messages'][0]["content"]

    botResponse = [{
        'type': 'unstructured',
        'unstructured': {
            'text': botMessage
        }
    }]