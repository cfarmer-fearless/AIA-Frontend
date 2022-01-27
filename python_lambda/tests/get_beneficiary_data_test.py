from datetime import datetime

import pytest
from moto import mock_ssm

from tests.test_utils import expected_response
from tests.conftest import setup_pg_ssm_parameter
from beneficiary import Beneficiary
from get_beneficiary_data import lambda_handler
from esrd_dialysis_data import EsrdDialysisData
import database_utils


# DB setup
esrd_record_1 = EsrdDialysisData(
    id=1,
    beneficiary_id="001A",
    coverage_period="01",
    coverage_effective_date="2019-01-01",
    coverage_termination_date="2019-01-11",
    coverage_source=database_utils.COVERAGE_SOURCE_PART_A_AND_DIALYSIS_TRAINING,
    coverage_termination_reason=database_utils.COVERAGE_TERMINATION_MONTH_OF_TRANSPLANT,
    dialysis_effective_date="2019-01-01",
    dialysis_termination_date="2019-01-11",
    transplant_effective_date="2019-01-01",
    transplant_termination_date="2019-01-11",
)

esrd_record_2 = EsrdDialysisData(
    id=2,
    beneficiary_id="001B",
    coverage_period="01",
    coverage_effective_date="2020-01-01",
    coverage_termination_date="2020-01-11",
    coverage_source=database_utils.COVERAGE_SOURCE_PART_A_AND_DIALYSIS_TRAINING,
    coverage_termination_reason=database_utils.COVERAGE_TERMINATION_MONTH_OF_TRANSPLANT,
    dialysis_effective_date="2020-01-01",
    dialysis_termination_date="2020-01-11",
    transplant_effective_date="2020-01-01",
    transplant_termination_date="2020-01-11",
)

esrd_record_3 = EsrdDialysisData(
    id=3,
    beneficiary_id="001A",
    coverage_period="01",
    coverage_effective_date="2020-01-01",
    coverage_termination_date="2020-01-11",
    coverage_source=database_utils.COVERAGE_SOURCE_PART_A_AND_DIALYSIS_TRAINING,
    coverage_termination_reason=database_utils.COVERAGE_TERMINATION_MONTH_OF_TRANSPLANT,
    dialysis_effective_date="2020-01-01",
    dialysis_termination_date="2020-01-11",
    transplant_effective_date="2020-01-01",
    transplant_termination_date="2020-01-11",
)

beneficiary_record_1 = Beneficiary(
    id="001A",
    first_name="Tom",
    middle_name="A",
    last_name="Johnson",
    gender=database_utils.GENDERS[0],
    date_of_birth="1970-01-01",
    date_of_death="2020-01-11",
    esrd_entitlement=0,
    esrd_benefits=0,
    esrd_dialysis_type=5,
    address="123 Street Rd, Alexandria VA 20000",
    esrd_dialysis_datas=[esrd_record_1, esrd_record_3],
    created_at=datetime.now(),
)

beneficiary_record_2 = Beneficiary(
    id="001B",
    first_name="Anne",
    middle_name="A",
    last_name="Johnson",
    gender=database_utils.GENDERS[0],
    date_of_birth="1970-01-01",
    date_of_death="2020-01-11",
    esrd_entitlement=0,
    esrd_benefits=0,
    esrd_dialysis_type=5,
    address="123 Street Rd, Alexandria VA 20000",
    esrd_dialysis_datas=[esrd_record_2],
    created_at=datetime.now(),
)


@pytest.fixture(autouse=True)
def run_around_tests(db_session):
    session = db_session
    session.query(EsrdDialysisData).delete()
    session.query(Beneficiary).delete()
    session.commit()
    session.bulk_save_objects([beneficiary_record_1, beneficiary_record_2])
    session.bulk_save_objects([esrd_record_1, esrd_record_2, esrd_record_3])
    session.commit()


@mock_ssm
def test_lambda_handler_returns_400_on_misformated_date_range():
    setup_pg_ssm_parameter()
    invalids = [
        {"start_date": "01-01-1996", "end_date": "01-01-2020", "beneficiary_id": "001A"},
        {"start_date": "1996-01-01", "end_date": "01-01-2020", "beneficiary_id": "001A"},
    ]
    for invalid in invalids:
        event = {"queryStringParameters": invalid}

        result = lambda_handler(event, None)
        assert result["statusCode"] == 400


@mock_ssm
def test_lambda_handler_returns_empty_array_on_no_beneficiary_found():
    setup_pg_ssm_parameter()
    beneficiary_id = "someid"

    event = {"queryStringParameters": {"beneficiary_id": beneficiary_id}}

    result = lambda_handler(event, None)
    assert result == expected_response([], 200)


@mock_ssm
def test_lambda_handler_returns_beneficiary_with_full_date_range():
    setup_pg_ssm_parameter()
    event = {"queryStringParameters": {"start_date": "2020-01-01", "end_date": "2020-01-11", "beneficiary_id": "001B"}}

    result = lambda_handler(event, None)
    assert result == expected_response(successful_beneficiaries_response_2(), 200)


@mock_ssm
def test_lambda_handler_returns_beneficiary_with_start_date():
    setup_pg_ssm_parameter()
    event = {"queryStringParameters": {"start_date": "2020-01-01", "beneficiary_id": "001B"}}

    result = lambda_handler(event, None)
    assert result == expected_response(successful_beneficiaries_response_2(), 200)


@mock_ssm
def test_lambda_handler_returns_beneficiary_data_with_no_date_range():
    setup_pg_ssm_parameter()
    event = {"queryStringParameters": {"beneficiary_id": "001B"}}

    result = lambda_handler(event, None)
    assert result == expected_response(successful_beneficiaries_response_2(), 200)


@mock_ssm
def test_lambda_handler_returns_empty_array_with_start_date_out_of_range():
    setup_pg_ssm_parameter()
    event = {"queryStringParameters": {"start_date": "2021-01-01"}}

    result = lambda_handler(event, None)
    assert result == expected_response([], 200)


@mock_ssm
def test_lambda_handler_beneficiary_with_single_dialysis_record_from_date_range_filter():
    setup_pg_ssm_parameter()
    beneficiary_id = "001A"
    event = {"queryStringParameters": {"start_date": "2019-01-01", "end_date": "2019-02-01", "beneficiary_id": beneficiary_id}}
    include_second_esrd_record = False

    result = lambda_handler(event, None)

    assert result == expected_response(successful_beneficiaries_response(include_second_esrd_record), 200)


@mock_ssm
def test_lambda_handler_returns_returns_all_data_within_date_range():
    setup_pg_ssm_parameter()
    event = {"queryStringParameters": {"start_date": "2019-01-01", "end_date": "2021-01-01"}}

    result = lambda_handler(event, None)

    expected_result = successful_beneficiaries_response() + successful_beneficiaries_response_2()
    assert result == expected_response(expected_result, 200)


@mock_ssm
def test_lambda_handler_returns_no_parameters_returns_all_data():
    setup_pg_ssm_parameter()
    event = {"queryStringParameters": None}

    result = lambda_handler(event, None)

    expected_result = successful_beneficiaries_response() + successful_beneficiaries_response_2()
    assert result == expected_response(expected_result, 200)


def successful_beneficiaries_response(include_second_record=True):
    result = [
        {
            "id": "001A",
            "name": {"firstName": "Tom", "middleName": "A", "lastName": "Johnson"},
            "dateOfBirth": "1970-01-01",
            "dateOfDeath": "2020-01-11",
            "gender": "U",
            "esrdEntitlementCode": 0,
            "esrdBenefitsCode": 0,
            "esrdDialysisType": 5,
            "address": "123 Street Rd, Alexandria VA 20000",
            "dialysisRecords": [
                {
                    "id": 1,
                    "beneficiaryId": "001A",
                    "coveragePeriod": "01",
                    "coverageEffectiveDate": "2019-01-01",
                    "coverageTerminationDate": "2019-01-11",
                    "coverageSource": "A",
                    "coverageTerminationReason": "A",
                    "dialysisEffectiveDate": "2019-01-01",
                    "dialysisTerminationDate": "2019-01-11",
                    "transplantEffectiveDate": "2019-01-01",
                    "transplantTerminationDate": "2019-01-11",
                },
            ],
        }
    ]
    if include_second_record:
        result[0]["dialysisRecords"].append(
            {
                "id": 3,
                "beneficiaryId": "001A",
                "coveragePeriod": "01",
                "coverageEffectiveDate": "2020-01-01",
                "coverageTerminationDate": "2020-01-11",
                "coverageSource": "A",
                "coverageTerminationReason": "A",
                "dialysisEffectiveDate": "2020-01-01",
                "dialysisTerminationDate": "2020-01-11",
                "transplantEffectiveDate": "2020-01-01",
                "transplantTerminationDate": "2020-01-11",
            }
        )
    return result


def successful_beneficiaries_response_2():
    return [
        {
            "id": "001B",
            "name": {"firstName": "Anne", "middleName": "A", "lastName": "Johnson"},
            "dateOfBirth": "1970-01-01",
            "dateOfDeath": "2020-01-11",
            "gender": "U",
            "esrdEntitlementCode": 0,
            "esrdBenefitsCode": 0,
            "esrdDialysisType": 5,
            "address": "123 Street Rd, Alexandria VA 20000",
            "dialysisRecords": [
                {
                    "id": 2,
                    "beneficiaryId": "001B",
                    "coveragePeriod": "01",
                    "coverageEffectiveDate": "2020-01-01",
                    "coverageTerminationDate": "2020-01-11",
                    "coverageSource": "A",
                    "coverageTerminationReason": "A",
                    "dialysisEffectiveDate": "2020-01-01",
                    "dialysisTerminationDate": "2020-01-11",
                    "transplantEffectiveDate": "2020-01-01",
                    "transplantTerminationDate": "2020-01-11",
                }
            ],
        }
    ]
