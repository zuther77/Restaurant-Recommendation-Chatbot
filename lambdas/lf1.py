import json
import boto3
import re
import datetime
import dateutil.parser

def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False

def validationResultMessage(valid,violationSlot,message):
    if (message==None):
        return {
            "isValid":valid,
            "violatedSlot":violationSlot
        }
    return {
        "isValid":valid,
        "violatedSlot":violationSlot,
        "message":{"contentType":"PlainText","content":message}
    }
    
def validateSlots(cuisine,location,numberOfPeople,diningDate,diningTime,email):
    cuisine_list = ['chinese', 'american', 'mexican','korean','japanese','italian','french','indian','thai']
    if (cuisine and cuisine["value"]["interpretedValue"]):
        if (cuisine["value"]["interpretedValue"] not in cuisine_list):
            return validationResultMessage(False,"Cuisine","We do not have recommendations for this cuisine yet.")
    if (location and location["value"]["interpretedValue"]):
        if (location["value"]["interpretedValue"]!="manhattan"):
            return validationResultMessage(False,"Location","Only Manhattan Restaurants are available for now.")
    if (numberOfPeople and numberOfPeople["value"]["interpretedValue"]):
        if (int(numberOfPeople["value"]["interpretedValue"])<1 or int(numberOfPeople["value"]["interpretedValue"])>20):
            return validationResultMessage(False,"NumberOfPeople","Enter a number between 1 and 20")
    if (diningDate and diningDate["value"]["interpretedValue"]):
        if not isvalid_date(diningDate["value"]["interpretedValue"]):
            return validationResultMessage(False, 'DiningDate', 'I did not understand that date, can you enter again?')
        elif datetime.datetime.strptime(diningDate["value"]["interpretedValue"], '%Y-%m-%d').date() < datetime.date.today():
            return validationResultMessage(False, 'DiningDate', 'I cannot book for this date as its already passed,can you enter a different date?')
    if (email and email["value"]["originalValue"]):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (not re.match(email_regex,email["value"]["originalValue"])):
            return validationResultMessage(False,"Email","Enter a valid Email")
    return validationResultMessage(True,None,None)

def fulfill_intent(intentName,message_content):
    return {
            "sessionState":{
                "dialogAction":{
                    "slotElicitationStyle":"Default",
                    "type":"Close"
                },
                "intent": {
                "confirmationState": "Confirmed",
                "name": intentName,
                "state":"Fulfilled"
                }
            },
            "messages": [
            {
            "contentType": "PlainText",
            "content": message_content
            }
            ]
        }

def invalid_slot(validityMessage,violatedSlot,intentName,slots):
    return {
        "messages": [
            validityMessage
            ], 
        "sessionState": {
        "dialogAction": {
            "slotToElicit": violatedSlot,
            "type": "ElicitSlot"
        },
        "intent": {
            "name": intentName,
            "slots": slots
            }
            }
        }

def get_slots(slots):
    return slots["Cuisine"],slots["Location"],slots["NumberOfPeople"],slots["DiningDate"],slots["DiningTime"],slots["Email"]

def lambda_handler(event, context):
    # TODO implement
    curIntent = event['sessionState']['intent']['name']
    sqs_client = boto3.client('sqs')

    if (curIntent=="GreetingIntent"):
        return fulfill_intent(curIntent,"Hi there, how can I help?")
    elif (curIntent == "ThankYouIntent"):
        return fulfill_intent(curIntent,"You're welcome!!")
    elif (curIntent =="DiningSuggestionIntent"):
        slots = event["sessionState"]["intent"]["slots"]
        cuisine,location,numberOfPeople,diningDate,diningTime,email = get_slots(slots)
        if (event["invocationSource"]=="DialogCodeHook"): # Only if slots are still left
            validObject = validateSlots(cuisine,location,numberOfPeople,diningDate,diningTime,email)
            if (not validObject["isValid"]):
                slots[validObject["violatedSlot"]]=None
                return invalid_slot(validObject["message"],validObject["violatedSlot"],curIntent,slots)
            
            if (not email): # Code block for next slot
                return {
                    "sessionState":event.get("proposedNextState")
                }
    
        message_body = {
            "cuisine":cuisine["value"]["interpretedValue"],
            "diningTime":diningTime["value"]["interpretedValue"],
            "diningDate":diningDate["value"]["interpretedValue"],
            "location":location["value"]["interpretedValue"],
            "noOfPeople":numberOfPeople["value"]["interpretedValue"],
            "email":email["value"]["interpretedValue"]
        }
        queue_message = ",".join(message_body.values())
        response = sqs_client.send_message(QueueUrl=sqs_client.get_queue_url(QueueName="SQS1")["QueueUrl"],MessageBody=queue_message)
        print ("Succesfully sent message to Queue" + queue_message)
        return fulfill_intent(curIntent,"You’re all set. Expect my suggestions shortly! Have a good day.")