import os
import json
import pytest
from datetime import datetime
from csv_etl import (
    CSVConverter,
    Rule,
    load_rules_from_yaml,
    RuleType,
    InputType,
    OutputType
)

from csv_etl.csv_etl import CustomEncoder

CWD = os.path.dirname(__file__)

TEST_CSV_FILE_PATH = CWD + '/resources/test_csv_data.csv'
TEST_CSV_CONVERTED_FILE_PATH = CWD + '/resources/test_csv_data_converted.csv'
TEST_JSON_CONVERTED_FILE_PATH = CWD + '/resources/test_json_data_converted.txt'
TEST_YAML_FILE_PATH = CWD + '/resources/test_config.yaml'
TEST_OUTFILE_PATH = CWD + '/resources/test_outfile.txt'


@pytest.fixture()
def csv_converter():
    rules = load_rules_from_yaml(TEST_YAML_FILE_PATH)
    csv_converter = CSVConverter(rules)
    return csv_converter


def test_csv_converter_convert(csv_converter):
    expected = [
        {
            'TestTarget': 'Test Value'
        }
    ]
    result = csv_converter.convert(TEST_CSV_FILE_PATH)
    assert result == expected


def test_csv_converter_convert_csv(csv_converter):
    file = open(TEST_CSV_CONVERTED_FILE_PATH)
    expected = file.read()
    file.close()
    result = csv_converter.convert(TEST_CSV_FILE_PATH, to='csv')
    result = result.replace('\r', '')
    assert result.strip() == expected.strip()


def test_csv_converter_convert_json(csv_converter):
    file = open(TEST_JSON_CONVERTED_FILE_PATH)
    expected = file.read()
    file.close()
    result = csv_converter.convert(TEST_CSV_FILE_PATH, to='json')
    assert result.strip() == expected.strip()


def test_csv_converter_convert_write_outfile(csv_converter):
    _ = csv_converter.convert(
            TEST_CSV_FILE_PATH,
            to='csv',
            outfile=TEST_OUTFILE_PATH
    )
    assert os.path.exists(TEST_OUTFILE_PATH)
    os.remove(TEST_OUTFILE_PATH)


def test_csv_converter_convert_raise_source_error():
    expected = [
        {
            'target': ''
        }
    ]
    rules = [
        Rule(
            source="source",
            target="target",
            type=RuleType.Calculation,
            input_type=InputType.String,
            output_type=OutputType.String,
            operations=[]
        )
    ]
    converter = CSVConverter(rules)
    result = converter.convert(TEST_CSV_FILE_PATH)
    assert result == expected


def test_csv_converter_convert_raise_value_error():
    expected = [
        {
            'target': ''
        }
    ]
    rules = [
        Rule(
            source="Test Source",
            target="target",
            type=RuleType.Calculation,
            input_type=InputType.Integer,
            output_type=OutputType.Integer,
            operations=[]
        )
    ]
    converter = CSVConverter(rules)
    result = converter.convert(TEST_CSV_FILE_PATH)
    assert result == expected


def test_custom_encoder_date():
    expected = '{"date": "2020-01-01"}'
    date = datetime(2020, 1, 1)
    result = json.dumps({'date': date}, cls=CustomEncoder)
    assert result == expected
