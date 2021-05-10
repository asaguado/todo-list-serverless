import os
import json
import logging
import boto3


dynamodb = boto3.resource('dynamodb')
aws_translate = boto3.client('translate')


def translate(event, context):

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    if not result:
        logging.error("Translate Failed")
        raise Exception("Couldn't find the todo item.")
        return    
    
    text_to_translate = result['Item']['text']
    target_language_code = event['pathParameters']['language']
    
    result_txt = aws_translate.translate_text(Text=text_to_translate, SourceLanguageCode='en', TargetLanguageCode=target_language_code)
    print("Translation output: " + str(result_txt))

    # create a response
    response = {
        "statusCode": 200,
        "body": str(result_txt)
    }

    return response
