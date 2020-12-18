import click

from .rules import load_rules_from_yaml
from .csv_etl import CSVConverter


@click.command()
@click.argument('config', type=click.Path(exists=True))
@click.argument('csv', type=click.Path(exists=True))
@click.option('--outfile',
              default=None,
              help='File path to write the result to'
              )
@click.option('--format',
              default='json',
              help='Format the result should be. "json" or "csv"'
              )
def main(config, csv, outfile, format):
    rules = load_rules_from_yaml(config)
    converter = CSVConverter(rules)
    result = converter.convert(csv, to=format, outfile=outfile)
    if outfile:
        print('Done')
    else:
        print(result)
