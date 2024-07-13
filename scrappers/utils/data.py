
import os
import json
from utils import repo_path


def load_data_json(file_name):
    with open(os.path.join(repo_path(), 'data', file_name), 'r') as f:
        return json.loads(f.read())
