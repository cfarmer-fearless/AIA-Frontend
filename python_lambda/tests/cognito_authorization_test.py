import json
from cognito_authorization import lambda_handler
from tests.test_utils import expected_response


def test_lambda_handler_returns_400_with_no_request_body():
    event = {}

    response = lambda_handler(event, None)
    assert response == expected_response({"ErrorMessage": "Required request body containing user credentials is missing from request"}, 400)


def test_lambda_handler_returns_400_for_no_username():
    event = {"body": json.dumps({"some": "data", "password": "pwd"})}

    response = lambda_handler(event, None)
    assert response == expected_response({"ErrorMessage": "Required username and/or password credentials are missing from request"}, 400)


def test_lambda_handler_returns_400_for_no_password():
    event = {"body": json.dumps({"some": "data", "username": "usr"})}

    response = lambda_handler(event, None)
    assert response == expected_response({"ErrorMessage": "Required username and/or password credentials are missing from request"}, 400)
