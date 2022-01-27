import pytest

from esrd_dialysis_data import EsrdDialysisData


def test_create_from_csv_row_esrd_is_created_correctly():
    test_input = valid_dictionary()

    result = EsrdDialysisData.create_from_csv_row(test_input)

    assert result.beneficiary_id == test_input["Beneficiary_ID"]
    assert result.coverage_period == "01"
    assert result.coverage_effective_date.strftime("%m/%d/%Y") == "12/15/2015"
    assert result.coverage_termination_date.strftime("%m/%d/%Y") == "02/02/2016"
    assert result.coverage_source == "A"
    assert result.coverage_termination_reason == "C"
    assert result.dialysis_effective_date.strftime("%m/%d/%Y") == "06/03/2016"
    assert result.dialysis_termination_date.strftime("%m/%d/%Y") == "06/12/2016"
    assert result.transplant_effective_date.strftime("%m/%d/%Y") == "07/03/2017"
    assert result.transplant_termination_date.strftime("%m/%d/%Y") == "07/29/2017"


def test_create_from_csv_allows_blank_coverage_termination_reason():
    test_input = valid_dictionary()

    test_input["Coverage_Termination_reason"] = ""

    result = EsrdDialysisData.create_from_csv_row(test_input)

    assert result.coverage_termination_reason is None


def test_invalid_inputs_for_codes_raise_exception_with_nice_error_message():
    code_keys = ["Coverage_Period", "Coverage_Source_code", "Coverage_Termination_reason"]
    for key in code_keys:
        test_input = valid_dictionary()
        test_input[key] = "INVALID INPUT!"

        with pytest.raises(ValueError):
            EsrdDialysisData.create_from_csv_row(test_input)

            raise NameError("I should not be called!")


def valid_dictionary():
    return {
        "Beneficiary_ID": "13468500S",
        "Coverage_Period": "1",
        "ESRD_Coverage_Effective_date": "12152015",
        "ESRD_Coverage_Termination_date": "2022016",
        "Coverage_Source_code": "A",
        "Coverage_Termination_reason": "C",
        "Dialysis_Effective_date": "6032016",
        "Dialysis_Termination_date": "6122016",
        "Transplant_Effective_date": "7032017",
        "Transplant_Termination_date": "7292017",
    }
