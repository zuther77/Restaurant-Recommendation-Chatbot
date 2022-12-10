# Restaurant Recommendation and Reservation Chatbot using AWS Services
Cloud Computing Assignment 1 (CS-GY 9223)

### Description
In this assignment you have implement a serverless, microservice-driven web application. Specifically, you will build a Dining Concierge chatbot that sends you restaurant suggestions given a set of preferences that you provide the chatbot with through conversation.

The restaurant data is scraped from Yelp API. It is a collection 5000+ unique restaurants if varying cuisines specifically in Manhattan. While we have only scraped it for Manhattan it can easily be extended to more locations.

It contains field suchs as Resturant_ID, Name, Location Coordinates, Cuisine, Number of Reviews and more.

Our chatbot will give us reccomendations filtered by cuisine given by the user and some other inputs from the user such as number of people,reservation date and time.

### AWS Services
For achieving this we will be using the following AWS Services for the same.

1. AWS Lex v2 - For creating and provisioning state of the art NLP models and defining chatbot actions

2. Amazon OpenSearch Service(Elastic Search) - An implementation of the popular Elastic Search service which is used as a distributed search and analytics engine.

3. Amazon Dynamo DB -  A NoSQL database provided by AWS which is ideal for use cases when the data (like restaurant data) is not in typical relational(SQL like) format.

Other Service like

- AWS Lambda - Event-driven, serverless computing platform.This handles all the code and logic for controlling all the component. We have implemented three lambda functions in Python - LF0,LF1 and LF2.

- AWS CloudWatch - Logs and Metrics for every AWS component.

- AWS SQS(Simple Queue Service) - Distibuted Queue Services for all AWS components.

- AWS SES(Simple Email Service) - For emailing recommendations to User.

### Example User Interaction with Chatbot

User: Hello

Bot: Hi there, how can I help?

User: I need some restaurant suggestions.

Bot: Great. I can help you with that. What city or city area are you looking to dine in?

User: Manhattan

Bot: Got it, Manhattan. What cuisine would you like to try?

User: Japanese

Bot: Ok, how many people are in your party?

User:Two

Bot: A few more to go. What date?

User: Today

Bot: What time?

User: 7 pm, please

Bot: Great. Lastly, I need your email so I can send you my findings.

User: john.doe@aws.com

Bot: You’re all set. Expect my suggestions shortly! Have a good day.

User: Thank you!

Bot: You’re welcome.

(a few minutes later)
User gets the following text message:
“Hello! Here are my Japanese restaurant suggestions for 2 people, for today at 7 pm: 1. Sushi Nakazawa, located at 23 Commerce St, 2. Jin Ramen, located at 3183 Broadway, 3. Nikko, located at 1280 Amsterdam Ave. Enjoy your meal!”

### Architecture

![alt text](https://github.com/abhishek66642/Restaurant-Recommendation-Chatbot-Cloud/blob/main/images/Architecture.png)
