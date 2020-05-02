import yaml
import os

config_file_path = '{directory_path}/../application.yaml'.format(
    directory_path=os.path.dirname(os.path.abspath(__file__))
)

config = yaml.safe_load(open(config_file_path))

application_config = config['application']
adventurer_square_config = config['adventurer_square']
logging_config = config['logging']

management_channel_id = config['management_channel']

