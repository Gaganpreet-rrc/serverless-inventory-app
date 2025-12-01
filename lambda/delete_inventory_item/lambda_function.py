import boto3
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Inventory')

    # Validate path parameter
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    try:
        response = table.query(
            KeyConditionExpression=Key('item_id').eq(item_id)
        )

        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps(f"No items found with id '{item_id}'")
            }
        deleted_count = 0

        for item in items:
            table.delete_item(
                Key={
                    'item_id': item['item_id'],
                    'item_location_id': item['item_location_id']
                }
            )
            deleted_count += 1

        return {
            'statusCode': 200,
            'body': json.dumps(
                f"Item with ID {item_id} deleted successfully."
            )
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item(s): {str(e)}")
        }