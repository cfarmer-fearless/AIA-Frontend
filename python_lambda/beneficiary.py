from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Enum, Integer
from sqlalchemy.orm import relationship

import database_utils

base = declarative_base()


class Beneficiary(database_utils.BASE):  # pylint: disable=too-few-public-methods
    """This class is used for representing and parsing beneficiary data."""

    __tablename__ = "beneficiary"

    id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String, nullable=False)
    gender = Column(Enum(*database_utils.GENDERS, name="gender_codes"))
    date_of_birth = Column(DateTime, nullable=False)
    date_of_death = Column(DateTime)
    esrd_entitlement = Column(Integer)
    esrd_benefits = Column(Integer)
    esrd_dialysis_type = Column(Integer)
    address = Column(String)
    created_at = Column(DateTime, nullable=False)
    esrd_dialysis_datas = relationship("EsrdDialysisData", back_populates="beneficiary")

    @staticmethod
    def create_from_csv_row(dictionary):
        return Beneficiary(
            id=dictionary["Beneficiary_ID"],
            first_name=dictionary["First_Name"],
            middle_name=dictionary["Middle_Name"],
            last_name=dictionary["Last_Name"],
            gender=database_utils.ensure_value_in_list(dictionary["Gender_Code"], database_utils.GENDERS),
            date_of_birth=database_utils.parse_date(dictionary["Date_of_Birth"]),
            date_of_death=database_utils.parse_nullable_date(dictionary["Date_of_Death"]),
            esrd_entitlement=database_utils.ensure_value_in_list(int(dictionary["ESRD_Entitlement_code"]), database_utils.ESRD_ENTITLEMENT_CODES),
            esrd_benefits=database_utils.ensure_value_in_list(int(dictionary["ESRD_Benefits_code"]), database_utils.ESRD_BENEFITS_CODES),
            esrd_dialysis_type=database_utils.ensure_value_in_list(int(dictionary["ESRD_Dialysis_Type"]), database_utils.ESRD_DIALYSIS_TYES),
            address=dictionary["Address"],
            created_at=datetime.now(),
        )
