import pytest

from beneficiary import Beneficiary


def test_create_from_csv_row_beneficiary_is_created_correctly():
    test_input = valid_dictionary()

    result = Beneficiary.create_from_csv_row(test_input)

    assert result.id == test_input["Beneficiary_ID"]
    assert result.first_name == test_input["First_Name"]
    assert result.middle_name == test_input["Middle_Name"]
    assert result.last_name == test_input["Last_Name"]
    assert result.gender == test_input["Gender_Code"]
    assert result.date_of_birth.strftime("%m/%d/%Y") == "01/11/1927"
    assert result.date_of_death is None
    assert result.esrd_entitlement == 0
    assert result.esrd_benefits == 0
    assert result.esrd_dialysis_type == 0
    assert result.address == test_input["Address"]


def test_create_from_csv_row_date_of_death_is_set_correctly_if_not_empty():
    test_input = valid_dictionary()
    test_input["Date_of_Death"] = "10102021"

    result = Beneficiary.create_from_csv_row(test_input)
    assert result.date_of_death.strftime("%m/%d/%Y") == "10/10/2021"


def test_invalid_inputs_for_codes_raise_exception_with_nice_error_message():
    code_keys = ["Gender_Code", "ESRD_Entitlement_code", "ESRD_Benefits_code", "ESRD_Dialysis_Type"]
    for key in code_keys:
        test_input = valid_dictionary()
        test_input[key] = "INVALID INPUT!"

        with pytest.raises(ValueError):
            Beneficiary.create_from_csv_row(test_input)

            raise NameError("I should not be called!")


def valid_dictionary():
    return {
        "Beneficiary_ID": "13468500S",
        "Last_Name": "WHITE",
        "Middle_Name": "A",
        "First_Name": "Joey",
        "Gender_Code": "M",
        "Date_of_Birth": "1111927",
        "Date_of_Death": "",
        "ESRD_Entitlement_code": "0",
        "ESRD_Benefits_code": "0",
        "ESRD_Dialysis_Type": "0",
        "Address": "9525 Manchester Lane Bay Shore, NY 11706",
    }
