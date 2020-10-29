import os
import boto3
import datetime as dt


def lambda_handler(event, context):

    holiday_table = boto3.resource("dynamodb").Table(os.getenv("HOLIDAY_TABLE"))
    cover_table = boto3.resource("dynamodb").Table(os.getenv("COVER_TABLE"))
    s3 = boto3.client("s3")

    holidays = holiday_table.scan(
        AttributesToGet=["EmpName", "Date"]
    )['Items']

    for holiday in holidays:
        holiday_date = dt.datetime.strptime(holiday['Date'], "%Y-%m-%d").date()
        if holiday_date > dt.date.today():
            projects = cover_table.scan(
                AttributesToGet=["CoverName", "EmpNotes"],
                ScanFilter={
                    "EmpName": {
                        "AttributeValueList": [
                            holiday['EmpName']
                        ],
                        "ComparisonOperator": "EQ"
                    }
                }
            )['Items']
            holiday_doc = "---\n"
            holiday_doc += "Holiday Planning Report!!!\n"
            holiday_doc += f"Prepare for {holiday['EmpName']} on {holiday['Date']}!\n"
            holiday_doc += "Projects list:\n"
            for project in projects:
                holiday_doc += f"- {project['CoverName']} - {project['EmpNotes']}\n"
            holiday_doc += "---\n"
            s3.put_object(
                Bucket=os.getenv("REPORTS_BUCKET"),
                Body=holiday_doc,
                Key=f"{holiday['EmpName']}.txt",
            )

    return {
        "statusCode": 200
    }
