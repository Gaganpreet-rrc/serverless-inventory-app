// Testing workflows.
import boto3
import json
from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal

deserializer = TypeDeserializer()

def convert_decimal(obj):

    if isinstance(obj, Decimal):

        if obj == obj.to_integral_value():
            return int(obj)
        return float(obj)
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    return obj

def deserialize_item(av_map):
    py_item = {}
    for k, v in av_map.items():
        py_item[k] = deserializer.deserialize(v)
    return convert_decimal(py_item)

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'
    if 'pathParameters' not in event or not event['pathParameters'] or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    try:
        response = dynamo_client.query(
            TableName=table_name,
            KeyConditionExpression='item_id = :v_id',
            ExpressionAttributeValues={':v_id': {'S': item_id}}
        )

        items_av = response.get('Items', [])

        if not items_av:
            return {
                'statusCode': 404,
                'body': json.dumps(f"No items found with id '{item_id}'")
            }

        items = [deserialize_item(av) for av in items_av]

        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
