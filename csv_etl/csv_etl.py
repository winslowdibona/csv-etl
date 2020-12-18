import io
import csv
import json
from datetime import datetime

from .rules import SourceNotFound, ConversionError

ERROR_MSG_TEMPLATE = '''
Error executing:
    Rule: {}
On:
    Data: {}
Error details:
    {}

'''


class CustomEncoder(json.JSONEncoder):
    '''Custom json encoder to handle datetime'''
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d')

        return json.JSONEncoder.default(self, o)  # pragma: no cover


class CSVConverter:
    '''
    Handles reading in CSV files, executing rules, and returns the data
    in the desired format(python dict, json string, csv string)

    ...

    Attributes
    ----------
    rules : list
        the set of rules the execute when converting CSV files
    '''

    def __init__(self, rules):
        self.rules = rules

    def _write_to_outfile(self, data, outfile):
        '''Internal method to write converted results to outfile.

        Args:
            data (str/dict): The data to be written.
            outfile (str): The file path to write the result to.

        '''
        file = open(outfile, 'w')
        file.write(str(data))
        file.close()

    def _convert_to_csv(self, data):
        '''Internal method to convert json data into csv data.

        Args:
            data (dict): The data to be converted.

        '''
        csv_result = io.StringIO()

        # Create the headers
        field_names = []
        for rule in self.rules:
            field_names.append(rule.target)

        writer = csv.DictWriter(csv_result, field_names)
        writer.writeheader()

        # Write the data row by row
        for row in data:
            writer.writerow(row)

        return csv_result.getvalue()

    def convert(self, csv_file, to=None, outfile=None):
        '''Executes rules on a given csv file and returns the result

        Args:
            csv_file (str): The file path of the csv file to convert.
            to (str): What to return the output as, either `csv` or `json`.
            outfile (str): Optional - The file path to write the result to.

        Returns:
            By default, a list of python dictionaries.
            If `to` = `csv` or `json` then a string representation of the
            data in that format will be returned.
        '''
        result = []

        # read in the csv file
        source_file = open(csv_file)
        reader = csv.DictReader(source_file)

        # iterate row by row, and execute the rules
        for row in reader:

            row_result = {}

            for rule in self.rules:

                try:
                    k, v = rule.execute(row)
                    row_result[k] = v

                except SourceNotFound:
                    rule_data = str(rule.as_dict())
                    row_data = str(row)
                    error_details = 'Unable to retrieve source data from'
                    error_msg = ERROR_MSG_TEMPLATE.format(
                        rule_data,
                        row_data,
                        error_details
                    )
                    print(error_msg)
                    row_result[rule.target] = ''

                except ConversionError as e:
                    rule_data = str(rule.as_dict())
                    row_data = str(row)
                    error_details = e.custom_message
                    error_msg = ERROR_MSG_TEMPLATE.format(
                        rule_data,
                        row_data,
                        error_details
                    )
                    print(error_msg)
                    row_result[rule.target] = ''

            result.append(row_result)

        if to == 'csv':
            result = self._convert_to_csv(result)

        if to == 'json':
            result = json.dumps(result, indent=4, cls=CustomEncoder)

        if outfile:
            self._write_to_outfile(result, outfile)

        source_file.close()
        return result
