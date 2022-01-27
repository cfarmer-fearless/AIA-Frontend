from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, contains_eager
import database_utils
from database_utils import build_response
from beneficiary import Beneficiary
from esrd_dialysis_data import EsrdDialysisData


def lambda_handler(event, context):  # pylint: disable=unused-argument
    database_engine = create_engine(database_utils.connection_string())
    session_maker = sessionmaker(database_engine)
    session = session_maker()

    start_date = None
    end_date = None
    beneficiary_id = None
    if event["queryStringParameters"] is not None:
        if "start_date" in event["queryStringParameters"]:
            start_date_string = event["queryStringParameters"]["start_date"]
            try:
                # Confirm formatting of date range, if provided
                start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
            except ValueError as exception:
                print("Failed to parse date string into date with exception {}".format(exception))
                return build_response(400, {"ErrorMessage": "The given date range is not properly ISO formatted: {}".format(start_date_string)})
        if "end_date" in event["queryStringParameters"]:
            end_date_string = event["queryStringParameters"]["end_date"]
            try:
                # Confirm formatting of date range, if provided
                end_date = datetime.strptime(end_date_string, "%Y-%m-%d")
            except ValueError as exception:
                print("Failed to parse date string into date with exception {}".format(exception))
                return build_response(400, {"ErrorMessage": "The given date range is not properly ISO formatted: {}".format(end_date_string)})
        if "beneficiary_id" in event["queryStringParameters"]:
            beneficiary_id = event["queryStringParameters"]["beneficiary_id"]

    beneficiary_query = session.query(Beneficiary).join(Beneficiary.esrd_dialysis_datas).options(contains_eager(Beneficiary.esrd_dialysis_datas))
    if beneficiary_id is not None:
        beneficiary_query = beneficiary_query.filter(Beneficiary.id == beneficiary_id)
    if start_date is not None:
        beneficiary_query = beneficiary_query.filter(EsrdDialysisData.dialysis_effective_date >= start_date)
    if end_date is not None:
        beneficiary_query = beneficiary_query.filter(EsrdDialysisData.dialysis_termination_date <= end_date)

    beneficiaries = beneficiary_query.all()

    # Serialize beneficiary data & return
    serialized_beneficiary = serialize_beneficiaries(beneficiaries)
    return build_response(200, serialized_beneficiary)


def serialize_beneficiaries(beneficiaries):
    result = []
    for ben in beneficiaries:
        esrd_datas = []
        for data in ben.esrd_dialysis_datas:
            esrd_datas.append(
                {
                    "id": data.id,
                    "beneficiaryId": data.beneficiary_id,
                    "coveragePeriod": data.coverage_period,
                    "coverageEffectiveDate": database_utils.nullable_date_formatter(data.coverage_effective_date),
                    "coverageTerminationDate": database_utils.nullable_date_formatter(data.coverage_termination_date),
                    "coverageSource": data.coverage_source,
                    "coverageTerminationReason": data.coverage_termination_reason,
                    "dialysisEffectiveDate": database_utils.nullable_date_formatter(data.dialysis_effective_date),
                    "dialysisTerminationDate": database_utils.nullable_date_formatter(data.dialysis_termination_date),
                    "transplantEffectiveDate": database_utils.nullable_date_formatter(data.transplant_effective_date),
                    "transplantTerminationDate": database_utils.nullable_date_formatter(data.transplant_termination_date),
                }
            )
        result.append(
            {
                "id": ben.id,
                "name": {"firstName": ben.first_name, "middleName": ben.middle_name, "lastName": ben.last_name},
                "dateOfBirth": database_utils.nullable_date_formatter(ben.date_of_birth),
                "dateOfDeath": database_utils.nullable_date_formatter(ben.date_of_death),
                "gender": ben.gender,
                "esrdEntitlementCode": ben.esrd_entitlement,
                "esrdBenefitsCode": ben.esrd_benefits,
                "esrdDialysisType": ben.esrd_dialysis_type,
                "address": ben.address,
                "dialysisRecords": esrd_datas,
            }
        )

    return result
