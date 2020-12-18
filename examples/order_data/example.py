from csv_etl import (
    CSVConverter
    Rule,
    RuleType,
    InputType,
    OutputType,
    load_rules_from_yaml
)

# Programmatically
rules1 = [
	Rule(
        source='Order Number',
        target='OrderId',
        type=RuleType.Calculation,
        input_type=InputType.Integer,
        output_type=OutputType.Integer
    ),
    Rule(
        source=['Day', 'Month', 'Year'],
        target='OrderDate',
        type=RuleType.Calculation,
        input_type=InputType.Integer,
        output_type=OutputType.Date,
        operations=['datetime(s[2], s[1], s[0])']
    ),
	Rule(
        source='Product Numer',
        target='ProductId',
        type=RuleType.Calculation,
        input_type=InputType.String,
        output_type=OutputType.String
    ),
	Rule(
        source='Product Name',
        target='ProductName',
        type=RuleType.Calculation,
        input_type=InputType.String,
        output_type=OutputType.String,
        operations=['s.title()']
    ),
	Rule(
        source='Count',
        target='Quantity',
        type=RuleType.Calculation,
        input_type=InputType.Decimal,
        output_type=OutputType.Decimal
    ),
	Rule(
        source='kg',
        target='Unit',
        type=RuleType.Static
    )
]

converter1 = CSVConverter(rules1)
converter1.convert('test_data.csv')


# Configuration
rules2 = load_rules_from_yaml('config.yaml')

converter2 = CSVConverter(rules2)
converter2.convert('test_data.csv')
