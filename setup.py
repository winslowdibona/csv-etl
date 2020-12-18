import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='csv-etl',
    packages=find_packages(include=['csv_etl']),
    include_package_data=True,
    version='0.1.3',
    description='A rules based approach to performing ETL operations on csv files.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/winslowdibona/csv-etl',
    author='Winslow DiBona',
    license='MIT',
    install_requires=['pyyaml', 'Click'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    entry_points='''
        [console_scripts]
        csv-etl=csv_etl.cli:main
    '''
)
