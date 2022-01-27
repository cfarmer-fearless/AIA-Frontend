import os

import pytest
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database_utils

os.environ[database_utils.PARAMETER_STORE_POSTGRES_KEY] = "pg_test_password"
os.environ["AWS_DEFAULT_REGION"] = "us-east-2"


def setup_pg_ssm_parameter():
    ssm = boto3.client("ssm")
    ssm.put_parameter(
        Name=os.environ[database_utils.PARAMETER_STORE_POSTGRES_KEY],
        Description="PG database password",
        Value=os.environ["POSTGRES_PASSWORD"],
        Type="SecureString",
    )


@pytest.fixture()
def db_session():
    database_engine = create_engine(database_utils.connection_string(os.environ["POSTGRES_PASSWORD"]))
    session_maker = sessionmaker(database_engine)
    yield session_maker()
