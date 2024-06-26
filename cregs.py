import json
import logging
import time
from datetime import datetime
import requests
LOGS = 'logs.txt'
IAM_TOKEN_PATH = '/home/student/Chepuh-beta/cregs_new/iam_token.txt'
FOLDER_ID_PATH = '/home/student/Chepuh-beta/cregs_new/folder_id.txt'


logging.basicConfig(filename=LOGS, level=logging.INFO,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

def get_creds():
    try:
        with open(IAM_TOKEN_PATH, 'r') as f:
            file_data = json.load(f)
            expiration = datetime.strptime(file_data["expires_at"][:26], '%Y-%m-%dT%H:%M:%S.%f')
            if expiration < datetime.now():
                create_new_token()
    except:
        create_new_token()

    with open(IAM_TOKEN_PATH, 'r') as f:
        file_data = json.load(f)
        aim_token = file_data["access_token"]

    with open(FOLDER_ID_PATH, 'r') as f:
        folder_id = f.read().strip()

    return aim_token, folder_id

def create_new_token():
    url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
    headers = {
        "Metadata-Flavor": "Google"
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            token_data = response.json()
            token_data['expires_at'] = time.time() + token_data['expires_at']
            with open(IAM_TOKEN_PATH, 'w') as f:
                json.dump(token_data, f)
    except Exception as e:
        logging.error(f"Ошибка получения токена: {e}")
