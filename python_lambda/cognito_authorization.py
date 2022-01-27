import os
import json
import boto3
import botocore
from database_utils import build_response


def cognito_client():
    return boto3.client("cognito-idp")


def lambda_handler(event, context):  # pylint: disable=unused-argument
    if "body" in event:
        body_json = json.loads(event["body"])
        username = body_json["username"] if "username" in body_json else None
        password = body_json["password"] if "password" in body_json else None
        if username is None or password is None:
            return build_response(400, {"ErrorMessage": "Required username and/or password credentials are missing from request"})

        try:
            response = cognito_client().initiate_auth(
                ClientId=os.getenv("APP_CLIENT_ID"), AuthFlow="USER_PASSWORD_AUTH", AuthParameters={"USERNAME": username, "PASSWORD": password}
            )

            if "AuthenticationResult" in response:
                id_token = response["AuthenticationResult"]["IdToken"]
                # access_token = response["AuthenticationResult"]["AccessToken"]
                expiration = response["AuthenticationResult"]["ExpiresIn"]
            else:
                build_response(400, {"ErrorMessage": "User must complete additional authorization steps"})

            return build_response(200, {"token": id_token, "expiration": expiration})

        except botocore.exceptions.ClientError as exception:
            print("Failed Authentication with Exception: {}".format(exception))
            return build_response(500, {"ErrorMessage": "Failed to authenticate username and password"})
    else:
        return build_response(400, {"ErrorMessage": "Required request body containing user credentials is missing from request"})
