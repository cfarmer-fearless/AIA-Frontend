import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import boto3

import database_utils
from beneficiary import Beneficiary
from esrd_dialysis_data import EsrdDialysisData

S3_BUCKET_ENVIRONMENT_KEY = "DATA_BUCKET"
S3_BUCKET_BENEFICIARY_DATA_KEY = "BENEFICIARY_DATA"
S3_BUCKET_ESRD_DIALYSIS_DATA_KEY = "ESRD_DIALYSIS_DATA"


BENEFICIARY_FILENAME = "beneficiaries.csv"
ESRD_DIALYSIS_FILENAME = "esrd.csv"


def load_data(event, context):  # pylint: disable=unused-argument
    database_session = drop_and_recreate_database()

    beneficiaries = parse_beneficiaries()
    esrd_data = parse_esrd_dialysis_data()

    database_session.bulk_save_objects(beneficiaries)
    database_session.bulk_save_objects(esrd_data)
    database_session.commit()

    print(f"Inserted #{len(beneficiaries)} beneficiaries, and #{len(esrd_data)} rows of ESRD dialysis data.")


def drop_and_recreate_database():
    db_engine = create_engine(database_utils.connection_string())
    database_utils.BASE.metadata.drop_all(db_engine)
    database_utils.BASE.metadata.create_all(db_engine)
    session = sessionmaker(db_engine)
    return session()


def download_and_parse_csv(source_s3_data_key, local_filename):
    file_path = get_lambda_file_path(local_filename)
    s3_client = boto3.client("s3")
    s3_client.download_file(os.environ[S3_BUCKET_ENVIRONMENT_KEY], source_s3_data_key, file_path)
    return csv.DictReader(open(file_path))


def parse_beneficiaries():
    beneficiary_csv_list = download_and_parse_csv(os.environ[S3_BUCKET_BENEFICIARY_DATA_KEY], BENEFICIARY_FILENAME)
    beneficiary_list = []
    for row in beneficiary_csv_list:
        beneficiary_list.append(Beneficiary.create_from_csv_row(row))
    return beneficiary_list


def parse_esrd_dialysis_data():
    esrd_csv_list = download_and_parse_csv(os.environ[S3_BUCKET_ESRD_DIALYSIS_DATA_KEY], ESRD_DIALYSIS_FILENAME)
    esrd_list = []
    for row in esrd_csv_list:
        esrd_list.append(EsrdDialysisData.create_from_csv_row(row))
    return esrd_list


def get_lambda_file_path(filename):
    # Bandit tries to flag this /tmp usage below as insecure... but Lambdas may ONLY use /tmp for files so we need to ignore this check
    return f"/tmp/{filename}"  # nosec
