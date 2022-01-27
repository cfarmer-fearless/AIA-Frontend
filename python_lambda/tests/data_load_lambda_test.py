import os

from moto import mock_s3, mock_ssm
import boto3
from sqlalchemy.orm import selectinload

from beneficiary import Beneficiary
from tests.conftest import setup_pg_ssm_parameter
from esrd_dialysis_data import EsrdDialysisData
import data_load_lambda


# pylint: disable=line-too-long
TEST_BENEFICIARY_DATA_CSV = b"""Beneficiary_ID,Last_Name,Middle_Name,First_Name,Gender_Code,Date_of_Birth,Date_of_Death,ESRD_Entitlement_code,ESRD_Benefits_code,ESRD_Dialysis_Type,Address
00121420L,Doe,M,Marie,F,9141951,,0,1,1,"254 Saxon St. Goodlettsville, TN 37072"
"""

TEST_ESRD_DIALYSIS_DATA_CSV = b"""Beneficiary_ID,Coverage_Period,ESRD_Coverage_Effective_date,ESRD_Coverage_Termination_date,Coverage_Source_code,Coverage_Termination_reason,Dialysis_Effective_date,Dialysis_Termination_date,Transplant_Effective_date,Transplant_Termination_date
00121420L,1,1212015,12162015,D,E,4052015,5052015,,
"""  # pylint: disable=line-too-long


@mock_s3
@mock_ssm
def test_load_data_loads_beneficiaries_and_esrd_data_from_s3(db_session):
    setup_pg_ssm_parameter()
    create_s3_bucket_with_records()

    data_load_lambda.load_data({}, {})

    result = db_session.query(Beneficiary).options(selectinload(Beneficiary.esrd_dialysis_datas))
    assert result[0].id == "00121420L"
    assert result.count() == 1
    assert result[0].esrd_dialysis_datas[0].coverage_effective_date.strftime("%m/%d/%Y") == "01/21/2015"
    assert len(db_session.query(EsrdDialysisData).all()) == 1


def create_s3_bucket_with_records():
    os.environ[data_load_lambda.S3_BUCKET_ENVIRONMENT_KEY] = "my_test_bucket"
    os.environ[data_load_lambda.S3_BUCKET_BENEFICIARY_DATA_KEY] = "beneficiary.csv"
    os.environ[data_load_lambda.S3_BUCKET_ESRD_DIALYSIS_DATA_KEY] = "esrd.csv"

    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket=os.environ[data_load_lambda.S3_BUCKET_ENVIRONMENT_KEY])

    beneficiary_object = conn.Object(
        os.environ[data_load_lambda.S3_BUCKET_ENVIRONMENT_KEY], os.environ[data_load_lambda.S3_BUCKET_BENEFICIARY_DATA_KEY]
    )
    beneficiary_object.put(Body=TEST_BENEFICIARY_DATA_CSV)

    esrd_object = conn.Object(os.environ[data_load_lambda.S3_BUCKET_ENVIRONMENT_KEY], os.environ[data_load_lambda.S3_BUCKET_ESRD_DIALYSIS_DATA_KEY])
    esrd_object.put(Body=TEST_ESRD_DIALYSIS_DATA_CSV)
