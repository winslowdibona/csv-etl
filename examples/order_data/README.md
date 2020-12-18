# Order Data Example

Say we keep a record of orders in the following format

|Column name|Type   |
|-----------|-------|
|OrderID    |Integer|
|OrderDate  |Date   |
|ProductId  |String |
|ProductName|String |
|Quantity   |Decimal|
|Unit       |String |

And we want to reconcile this data we have against the data in a customer's books. However the customer formats their orders differently Their orders follow this schema

|Column name   |String format|
|--------------|-------------|
|Order Number  |d+           |
|Year          |YYYY         |
|Month         |MM           |
|Day           |dd           |
|Product Number|[A-Z0-9]+    |
|Product Name  |[A-Z]+       |
|Count         |# ##0.0#     |


To convert the customer data into our format, we could perform the following rules

1. Rename Order Number → OrderID and parse as Integer
2. Add a new column, concatenating Year, Month, Day → OrderDate and parse as
DateTime
3. Rename Product Number → ProductId and parse as String
4. Proper case Product Name , rename it → ProductName and parse as String
5. Rename Count → Quantity and parse as BigDecimal
6. Add a new column with the fixed value 'kg' → Unit and parse as String

If we run these rules over the following set of data we get data formatted in a dictionary

|Order Number|Year|Month|Day|Product Number|Product Name   |Count   |
|------------|----|-----|---|--------------|---------------|--------|
|1000        |2018|1    |1  |P-10001       |Arugola        |5,250.50|
|1001        |2017|12   |12 |P-10002       |Iceberg lettuce|500.00  |


```python
rules = [
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
		source='Product Number',
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

csv_converter = CSVConverter(rules)
result = csv_converter.convert(CSV_FILE_PATH)
```

```python
[
    {
        'OrderId': 1000,
        'OrderDate': datetime.datetime(2018, 1, 1, 0, 0),
        'ProductId': 'P-10001',
        'ProductName': 'Arugola',
        'Quantity': 5250.5,
        'Unit': 'kg'
    },
    {
        'OrderId': 1001,
        'OrderDate': datetime.datetime(2017, 12, 12, 0, 0),
        'ProductId': 'P-10002',
        'ProductName': 'Iceberg Lettuce',
        'Quantity': 500.0,
        'Unit': 'kg'
    }
]
```

we can also get the data formatted back into `csv` by running

```python
result = csv_converter.convert(CSV_FILE_PATH, to='csv')
```

|OrderId|OrderDate          |ProductId|ProductName    |Quantity|Unit|
|-------|-------------------|---------|---------------|--------|----|
|1000   |2018-01-01    |P-10001  |Arugola        |5250.50 |kg  |
|1001   |2017-12-12    |P-10002  |Iceberg lettuce|500.00  |kg  |



These rules can also be represented as yaml

```yaml
rules:
  -
    target: OrderId
    type: Calculation
    input_type: Integer
    output_type: Integer
    source: Order Number
  -
    target: OrderDate
    type: Calculation
    input_type: Integer
    output_type: Date
    source:
      - Day
      - Month
      - Year
    operations:
      - 'datetime(s[2], s[1], s[0])'
  -
    target: ProductId
    type: Calculation
    input_type: String
    output_type: String
    source: Product Number
  -
    target: ProductName
    type: Calculation
    input_type: String
    output_type: String
    source: Product Name
    operations:
      - 's.title()'
  -
    target: Quantity
    type: Calculation
    input_type: Decimal
    output_type: Decimal
    source: Count
  -
    target: Unit
    type: Calculation
    input_type: String
    output_type: String
    source: kg

```

and we could use them just the same.

```python
from csv_etl import (
	load_rules_from_yaml,
	CSVConverter
)

rules = load_rules_from_yaml('path/to/config/file')
csv_converter = CSVConverter(rules)
result = csv_converter.convert('path/to/csv/file')
```
