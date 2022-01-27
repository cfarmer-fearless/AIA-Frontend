import json


def expected_response(message, code=400):
    return {
        "statusCode": code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(message),
    }
