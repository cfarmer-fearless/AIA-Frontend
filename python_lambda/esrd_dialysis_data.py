from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Enum, Integer, Index, ForeignKey
from sqlalchemy.orm import relationship
import database_utils


base = declarative_base()


class EsrdDialysisData(database_utils.BASE):  # pylint: disable=too-few-public-methods
    """This class is used for representing and parsing ESRD Dialysis data."""

    __tablename__ = "esrd_dialysis_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    beneficiary_id = Column(String, ForeignKey("beneficiary.id"), nullable=False)
    coverage_period = Column(Enum(*database_utils.COVERAGE_PERIOD_NUMBERS, name="coverage_period_code"))
    coverage_effective_date = Column(DateTime)
    coverage_termination_date = Column(DateTime)
    coverage_source = Column(Enum(*database_utils.COVERAGE_SOURCES, name="coverage_source_code"))
    coverage_termination_reason = Column(Enum(*database_utils.COVERAGE_TERMINATIONS, name="coverage_termination_code"))
    dialysis_effective_date = Column(DateTime)
    dialysis_termination_date = Column(DateTime)
    transplant_effective_date = Column(DateTime)
    transplant_termination_date = Column(DateTime)
    beneficiary = relationship("Beneficiary", back_populates="esrd_dialysis_datas")
    __table_args__ = (Index("esrd_dialysis_data_dialysis_date_index", "dialysis_effective_date", "dialysis_termination_date"),)

    @staticmethod
    def create_from_csv_row(dictionary):
        return EsrdDialysisData(
            beneficiary_id=dictionary["Beneficiary_ID"],
            coverage_period=database_utils.ensure_value_in_list(dictionary["Coverage_Period"].zfill(2), database_utils.COVERAGE_PERIOD_NUMBERS),
            coverage_effective_date=database_utils.parse_nullable_date(dictionary["ESRD_Coverage_Effective_date"]),
            coverage_termination_date=database_utils.parse_nullable_date(dictionary["ESRD_Coverage_Termination_date"]),
            coverage_source=database_utils.ensure_nullable_value_in_list(dictionary["Coverage_Source_code"], database_utils.COVERAGE_SOURCES),
            coverage_termination_reason=database_utils.ensure_nullable_value_in_list(
                dictionary["Coverage_Termination_reason"], database_utils.COVERAGE_TERMINATIONS
            ),
            dialysis_effective_date=database_utils.parse_nullable_date(dictionary["Dialysis_Effective_date"]),
            dialysis_termination_date=database_utils.parse_nullable_date(dictionary["Dialysis_Termination_date"]),
            transplant_effective_date=database_utils.parse_nullable_date(dictionary["Transplant_Effective_date"]),
            transplant_termination_date=database_utils.parse_nullable_date(dictionary["Transplant_Termination_date"]),
        )
