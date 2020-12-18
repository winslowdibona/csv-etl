# csv-etl

A rules based approach to performing ETL operations on csv files.

## Installation

Requires Python 3

Latest Release = `0.1.3`

### Using pip

```bash
python -m venv venv
source venv/bin/activate
pip install csv-etl
```

### Locally

```bash
git clone https://github.com/winslowdibona/csv-etl.git
cd csv-etl
python -m venv venv
source venv/bin/activate
pip install --editable .
```

### Developing

```bash
git clone https://github.com/winslowdibona/csv-etl.git
cd csv-etl
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Overview

The goal of this project is to provide a re-usable way to perform ETL operations on csv files. This implementation takes a given row of data from a csv file and applies a set of rules to generate a new format of the data.

### Rule Overview

The `Rule` in this project has the following properties

 - `target`
 - `source`
 - `type`
 - `input_type`
 - `output_type`
 - `operations`

Using different combinations of values for these properties can give us a flexible toolset for extracting data.

##### target - `str`

Once we have the extracted the value from the csv and applied our rule to it, the resulting value will appear under this value as the key in the result

##### source - `str/list`

This is where we want to pull the data from in the csv. If the source is a string, it will fetch that single column. If the source is a list, it will fetch all of the values.

##### type - `RuleType`

This can be one of two options

 - `Static`
 - `Calculation`

If RuleType.Static, the rule will simply return the value stored in Rule.source under Rule.target

If RuleType.Calculation, the rule will fetch the value(s) defined in Rule.source, and perform the operations on them

##### input_type - `InputType`

The data type you would like to read the value in from the csv as.

This can be one of three options

 - `String`
 - `Integer`
 - `Decimal`

##### output_type - `OutputType`

The data type you would like the resulting value to be.

This can be one of four options

 - `String`
 - `Integer`
 - `Decimal`
 - `Date`

##### operations - `list`

A list of strings that will be run through python `eval` statement. The value(s) extracted from the csv will be available for use in these operations. If there is only a single source, the value will be assigned to the variable `s`. If there are multiple sources, the values will be passed in as a list under the variable `s`.

### Defining Rules

These rules can be defined programmatically, or via a YAML configuration. The configuraiton follows the below structure

```yaml
rules:
  -
    target: target_name
    type: Static || Calculation
    input_type: String || Integer || Decimal
    output_type: String || Integer || Decimal || Date
    source: source_name || [source, names]
    operations: ['operations', 'to', 'run']
```

### Converting CSV Data

Once we have a set of rules, we can use the `CSVConverter` class to execute our rules on a data set.

```python
from csv_etl import CSVConverter

csv_converter = CSVConverter(rules)

result = csv_converter.convert('path/to/csv_file')
```

This will give us back a list of dictionaries, with each item in the list representing the modified data for each row in the initial csv file.

We can also get the result fed back to us in `json`/`csv` format as a string

```python
result = csv_converter.convert('path/to/csv/file', to='json')
result = csv_converter.convert('path/to/csv/file', to='csv')
```

## Usage

### CLI

```bash
$ csv-etl ./examples/order_data/config.yaml ./examples/order_data/test_data.csv
[
    {
        "OrderId": 1000,
        "OrderDate": "2018-01-01",
        "ProductId": "P-10001",
        "ProductName": "Arugola",
        "Quantity": 5250.5,
        "Unit": "kg"
    },
    {
        "OrderId": 1001,
        "OrderDate": "2017-12-12",
        "ProductId": "P-10002",
        "ProductName": "Iceberg Lettuce",
        "Quantity": 500.0,
        "Unit": "kg"
    }
]

$ csv-etl --help
Usage: csv-etl [OPTIONS] CONFIG CSV

Options:
  --outfile TEXT  File path to write the result to
  --format TEXT   Format the result should be. "json" or "csv"
  --help          Show this message and exit.
```

### Examples

More detailed usage and programmatic examples are provided

 - [Order Data Example](https://github.com/winslowdibona/csv-etl/tree/master/examples/order_data)
 - [Example Rule Configs](https://github.com/winslowdibona/csv-etl/tree/master/examples/config)

## Helpful Make Commands

### Generating Documentation

```bash
make docs
open html/csv_etl/index.html
```

### Running Tests

```bash
make pytest
```

### Getting Test Coverage

```bash
make test-cov
open cov_html/index.html
```

## What Next?

### Better error handling

Currently the errors are just printed to the console. Might be nice to have an option to gather them and have them represented in the resulting data set somehow.

### Better handling of eval statements

Right now the use of `eval` statements is a little tailored for the original problem
and could use some more exploration on how they can be further utilized and how to handle
potential errors.

Also right now the ability to perform multiple operations on a single extracted value is doable, but performing multiple operations on multiple extracted values will not. `eval` statements don't allow assignment of variables, and this prevents us from performing some logic, and being able to use the resulting values again in a list. Further exploration here may find a way to do multiple operations with multiple extracted values.
