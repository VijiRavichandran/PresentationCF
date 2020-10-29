import boto3
import os
import json


def lambda_handler(event, context):
    holiday_table = os.getenv("HOLIDAY_TABLE")
    cover_table = os.getenv("COVER_TABLE")
    dynamo_client = boto3.client("dynamodb")
    print(event)
    body = json.loads(event['body'])
    resp = dynamo_client.get_item(
        TableName=holiday_table,
        Key={
            "EmpName":
                {"S": body["EmpName"]}
        }
    )
    if "Item" not in resp:
        dynamo_client.put_item(
            TableName=holiday_table,
            Item={
                "EmpName":
                    {"S": body["EmpName"]},
                "Date":
                    {"S": body["HolDate"]}
            }
        )
    dynamo_client.put_item(
        TableName=cover_table,
        Item={
            "CoverName":
                {"S": body["CoverName"]},
            "EmpNotes":
                {"S": body["EmpNotes"]},
            "EmpName":
                {"S": body["EmpName"]}
        }
    )
    return {
        "statusCode": 200
    }
