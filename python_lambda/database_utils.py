import os
import json
from datetime import datetime

import boto3
from sqlalchemy.ext.declarative import declarative_base

PARAMETER_STORE_POSTGRES_KEY = "PARAMETER_STORE_PG_KEY"


BASE = declarative_base()


GENDER_UNKNOWN = "U"
GENDER_MALE = "M"
GENDER_FEMALE = "F"
GENDERS = [GENDER_UNKNOWN, GENDER_MALE, GENDER_FEMALE]


ESRD_ENTITLEMENT_DOES_NOT_APPLY = 0
ESRD_ENTITLEMENT_CHILD_OR_SPOUSE = 1
ESRD_ENTITLEMENT_BOTH_CONDITIONS = 2
ESRD_ENTITLEMENT_CODES = [ESRD_ENTITLEMENT_DOES_NOT_APPLY, ESRD_ENTITLEMENT_CHILD_OR_SPOUSE, ESRD_ENTITLEMENT_BOTH_CONDITIONS]


ESRD_BENEFITS_DOES_NOT_APPLY = 0
ESRD_BENEFITS_SELF_CARE_DIALYSIS = 1
ESRD_BENEFITS_ENTITLEMENT_DUE_TO_TRANSPLANT = 2
ESRD_BENEFITS_BOTH_CONDITIONS_PRESENT = 3
ESRD_BENEFITS_CODES = [
    ESRD_BENEFITS_DOES_NOT_APPLY,
    ESRD_BENEFITS_SELF_CARE_DIALYSIS,
    ESRD_BENEFITS_ENTITLEMENT_DUE_TO_TRANSPLANT,
    ESRD_BENEFITS_BOTH_CONDITIONS_PRESENT,
]


ESRD_DIALYSIS_DOES_NOT_APPLY = 0
ESRD_DIALYSIS_HEMODIALYSIS = 1
ESRD_DIALYSIS_CONTINUOUS_AMBULATORY_PERITONEAL_DIALYSIS = 2
ESRD_DIALYSIS_CONTINUOUS_CYCLING_PERITONEAL_DIALYSIS = 3
ESRD_DIALYSIS_PERITONEAL_DIALYSIS = 4
ESRD_DIALYSIS_UNKNOWN = 5
ESRD_DIALYSIS_TYES = [
    ESRD_DIALYSIS_DOES_NOT_APPLY,
    ESRD_DIALYSIS_HEMODIALYSIS,
    ESRD_DIALYSIS_CONTINUOUS_AMBULATORY_PERITONEAL_DIALYSIS,
    ESRD_DIALYSIS_CONTINUOUS_CYCLING_PERITONEAL_DIALYSIS,
    ESRD_DIALYSIS_PERITONEAL_DIALYSIS,
    ESRD_DIALYSIS_UNKNOWN,
]


COVERAGE_PERIOD_NUMBERS = ["01", "02", "03", "04", "05"]


COVERAGE_SOURCE_PART_A_AND_DIALYSIS_TRAINING = "A"
COVERAGE_SOURCE_PART_A_AND_DIALYZING_NO_3_MONTH_WAIT = "B"
COVERAGE_SOURCE_PART_A_AND_3_MONTHS_AFTER_DIALYSIS = "C"
COVERAGE_SOURCE_PART_A_AND_FUNCTIONING_TRANSPLANT = "D"
COVERAGE_SOURCE_PART_A_AND_PRETRANSPLANT_STAY = "E"
COVERAGE_SOURCE_PART_A_AND_ESRD = "F"
COVERAGE_SOURCES = [
    COVERAGE_SOURCE_PART_A_AND_DIALYSIS_TRAINING,
    COVERAGE_SOURCE_PART_A_AND_DIALYZING_NO_3_MONTH_WAIT,
    COVERAGE_SOURCE_PART_A_AND_3_MONTHS_AFTER_DIALYSIS,
    COVERAGE_SOURCE_PART_A_AND_FUNCTIONING_TRANSPLANT,
    COVERAGE_SOURCE_PART_A_AND_PRETRANSPLANT_STAY,
    COVERAGE_SOURCE_PART_A_AND_ESRD,
]


COVERAGE_TERMINATION_MONTH_OF_TRANSPLANT = "A"
COVERAGE_TERMINATION_LAST_MONTH_OF_CHRONIC_DIALYSIS = "B"
COVERAGE_TERMINATION_PART_A_TERMINATION = "C"
COVERAGE_TERMINATION_DEATH = "D"
COVERAGE_TERMINATION_ESRD_ENDED = "E"
COVERAGE_TERMINATIONS = [
    COVERAGE_TERMINATION_MONTH_OF_TRANSPLANT,
    COVERAGE_TERMINATION_LAST_MONTH_OF_CHRONIC_DIALYSIS,
    COVERAGE_TERMINATION_PART_A_TERMINATION,
    COVERAGE_TERMINATION_DEATH,
    COVERAGE_TERMINATION_ESRD_ENDED,
]


def connection_string(db_password=None):
    if db_password is None:
        ssm = boto3.client("ssm")
        db_password = ssm.get_parameter(Name=os.environ[PARAMETER_STORE_POSTGRES_KEY], WithDecryption=True)["Parameter"]["Value"]
    return "postgresql://{}:{}@{}:{}/{}".format(
        os.environ["POSTGRES_USER"], db_password, os.environ["POSTGRES_HOSTNAME"], "5432", os.environ["POSTGRES_DB"]
    )


def ensure_value_in_list(value, code_list):
    if value in code_list:
        return value
    raise ValueError(f'Error: "#{value}" does not exist in #{code_list}')


def ensure_nullable_value_in_list(value, code_list):
    if value != "":
        return ensure_value_in_list(value, code_list)
    return None


def parse_date(date_string):
    left_padded_string = date_string.zfill(8)
    return datetime.strptime(left_padded_string, "%m%d%Y")


def parse_nullable_date(date_string):
    if date_string != "":
        return parse_date(date_string)
    return None


def nullable_date_formatter(date):
    return date.strftime("%Y-%m-%d") if date is not None else ""


def build_response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(body),
    }
