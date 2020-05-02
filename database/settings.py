from orator import DatabaseManager
import yaml
import os

config_file_path = '{directory_path}/../database.yaml'.format(
    directory_path=os.path.dirname(os.path.abspath(__file__))
)
settings = yaml.safe_load(open(config_file_path))['development']

host = settings['host']
database = settings['database']
username = settings['username']
password = settings['password']
pool_size = settings['pool']
encoding = settings['encoding']

config = {
    'mysql': {
        'driver': 'mysql',
        'host': host,
        'database': database,
        'user': username,
        'password': password,
        'charset': encoding,
        'log_queries': True
    }
}

db = DatabaseManager(config)
