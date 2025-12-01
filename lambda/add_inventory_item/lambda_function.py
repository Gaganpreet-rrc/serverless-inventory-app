// Testing workflows
import json
import boto3
import uuid
from decimal import Decimal
 
def lambda_handler(event, context):
    # Parse incoming JSON data
    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }
 
    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')
 
    # Generate a unique ID
    item_id = str(uuid.uuid4())
 
    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                'item_id': item_id,
                'item_location_id': int(data['item_location_id']),
                'item_name': data['item_name'],
                'item_description': data['item_description'],
                'item_qty_on_hand': int(data['item_qty_on_hand']),
                'item_price': Decimal(str(data['item_price']))
            }
        )
 
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} added successfully.")
        }
 
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
