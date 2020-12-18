import os
import pytest
from click.testing import CliRunner
from csv_etl import cli

CWD = os.path.dirname(__file__)

TEST_CSV_FILE_PATH = CWD + '/resources/test_csv_data.csv'
TEST_JSON_CONVERTED_FILE_PATH = CWD + '/resources/test_json_data_converted.txt'
TEST_YAML_FILE_PATH = CWD + '/resources/test_config.yaml'
TEST_OUTFILE_PATH = CWD + '/resources/test_outfile.txt'


@pytest.fixture()
def expected_json():
    file = open(TEST_JSON_CONVERTED_FILE_PATH)
    expected = file.read()
    file.close()
    return expected


@pytest.fixture()
def runner():
    return CliRunner()


def test_cli_default(runner, expected_json):
    result = runner.invoke(cli.main, [TEST_YAML_FILE_PATH, TEST_CSV_FILE_PATH])
    assert result.exit_code == 0
    assert result.stdout == expected_json


def test_cli_outfile(runner, expected_json):
    result = runner.invoke(
        cli.main,
        [
            TEST_YAML_FILE_PATH,
            TEST_CSV_FILE_PATH,
            '--outfile={}'.format(TEST_OUTFILE_PATH)
        ]
    )
    assert result.exit_code == 0
    assert result.stdout.strip() == 'Done'
    assert os.path.exists(TEST_OUTFILE_PATH)

    os.remove(TEST_OUTFILE_PATH)
