import os
import json
import logging

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    print('::Result: '+str(result))
    
    if not 'Item' in result:
        print('::Get Failed')
        logging.error("Get Failed")
        raise Exception("Couldn't find the todo item.")
        return 

    try:
        print('::Get OK')
        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
        }
        return response
        
    except:
        print('::Get Failed')
        logging.error("Get Failed")
        raise Exception("Couldn't find the todo item.")
        return
