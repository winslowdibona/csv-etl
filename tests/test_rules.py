import os
import pytest
from csv_etl import (
    Rule,
    load_rules_from_yaml,
    SourceNotFound,
    RuleType,
    InputType,
    OutputType
)
from datetime import datetime

TEST_YAML_FILE_PATH = os.path.dirname(__file__) + '/resources/test_config.yaml'


def test_static_rule():
    rule = Rule(
        source='test',
        target='Target',
        type=RuleType.Static,
        input_type=InputType.String,
        output_type=OutputType.String,
        operations=[]
    )
    t, v = rule.execute({})
    assert t == 'Target'
    assert v == 'test'


def test_simple_rule():
    test_data = {'test': 'value'}
    rule = Rule(
        source='test',
        target='Target',
        type=RuleType.Calculation,
        input_type=InputType.String,
        output_type=OutputType.String,
        operations=[]
    )
    t, v = rule.execute(test_data)
    assert t == 'Target'
    assert v == 'value'


def test_calculation_rule_operations():
    test_data = {'test': 'test value'}
    rule = Rule(
        source='test',
        target='Target',
        type=RuleType.Calculation,
        input_type=InputType.String,
        output_type=OutputType.String,
        operations=['s.title()']
    )
    t, v = rule.execute(test_data)
    assert t == 'Target'
    assert v == 'Test Value'


def test_calculation_rule():
    test_data = {'num1': '2', 'num2': '6,123'}
    rule = Rule(
        source=['num1', 'num2'],
        target='Target',
        type=RuleType.Calculation,
        input_type=InputType.Decimal,
        output_type=OutputType.Decimal,
        operations=['s[0] * s[1]']
    )
    t, v = rule.execute(test_data)
    assert t == 'Target'
    assert v == float(12246)


def test_date_calculation_rule():
    test_data = {
        'month': '1',
        'day': '1',
        'year': '2020'
    }
    rule = Rule(
        source=['day', 'month', 'year'],
        target='Target',
        type=RuleType.Calculation,
        input_type=InputType.Integer,
        output_type=OutputType.Date,
        operations=['datetime(s[2], s[1], s[0])']
    )
    t, v = rule.execute(test_data)
    assert t == 'Target'
    assert v == datetime(2020, 1, 1)


def test_rule_cast_type_string():
    value = 3
    rule = Rule()
    result = rule._cast_type(value, OutputType.String.value)
    assert result == '3'


def test_rule_cast_type_int():
    value = '3'
    rule = Rule()
    result = rule._cast_type(value, OutputType.Integer.value)
    assert result == 3


def test_rule_cast_type_decimal():
    value = '3'
    rule = Rule()
    result = rule._cast_type(value, OutputType.Decimal.value)
    assert result == float(3)


def test_rule_raise_source_not_found():
    test_data = {'t': 'value'}
    rule = Rule(
        source='test',
        target='Target',
        type=RuleType.Calculation,
        input_type=InputType.String,
        output_type=OutputType.String,
        operations=[]
    )
    with pytest.raises(SourceNotFound):
        t, v = rule.execute(test_data)


def test_calculation_rule_raise_error():
    test_data = {
        'm': '1',
        'd': '1',
        'y': '2020'
    }
    rule = Rule(
        source=['day', 'month', 'year'],
        target='Target',
        type=RuleType.Calculation,
        input_type=InputType.Integer,
        output_type=OutputType.Date,
        operations=['datetime(s[2], s[1], s[0])']
    )
    with pytest.raises(SourceNotFound):
        t, v = rule.execute(test_data)


def test_load_rules_from_yaml():
    rules = load_rules_from_yaml(TEST_YAML_FILE_PATH)
    assert len(rules) == 1
    assert rules[0].as_dict() == {
        'target': 'TestTarget',
        'type': 'Calculation',
        'input_type': 'String',
        'output_type': 'String',
        'source': 'Test Source',
        'operations': []
    }
