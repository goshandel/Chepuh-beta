import requests
import logging
from config import FOlder_id, Iam_token, MAX_MODEL_TOKENS
from cregs import get_creds
from error import error3

iam_token, folder_id = get_creds()
class Question_gpt2:
    def __init__(self):
        self.max_tokens = 200

    def promt(self, text):
        try:

            headers = {
                'Authorization': f'Bearer {iam_token}',
                'Content-Type': 'application/json'
            }
            data = {
                "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.6,
                    "maxTokens": self.max_tokens

                },
                "messages": [
                    {
                        "role": "user",
                        "text": text
                    }
                ]
            }
            response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                                     headers=headers,
                                     json=data)

            if response.status_code == 200:
                text = response.json()["result"]["alternatives"][0]["message"]["text"]
                print(text)
                return text
            else:
                raise RuntimeError(
                    'Invalid response received: code: {}, message: {}'.format(
                        {response.status_code}, {response.text}
                    )
                )

        except Exception as e:
                error_gpt1 = error3
                logging.error(str(e))
                return error_gpt1


class Continue_text_gpt:
    def __init__(self):
        self.max_tokens = 50

    def promt(self, text, user, CONTINUE_STORY):
        try:
            iam_token = Iam_token
            folder_id = FOlder_id
            headers = {
                'Authorization': f'Bearer {iam_token}',
                'Content-Type': 'application/json'
            }
            data = {
                "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.6,
                    "maxTokens": self.max_tokens

                },
                "messages": [
                    {
                        "role": "user",
                        "text": text + CONTINUE_STORY + user
                    }
                ]
            }
            response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                                     headers=headers,
                                     json=data)

            if response.status_code == 200:
                text = response.json()["result"]["alternatives"][0]["message"]["text"]
                return text
            else:
                raise RuntimeError(
                    'Invalid response received: code: {}, message: {}'.format(
                        {response.status_code}, {response.text}
                    )
                )

        except Exception as e:
                error_gpt1 = error3
                logging.error(str(e))
                return error_gpt1


def count_tokens(text):
    iam_token = Iam_token
    folder_id = FOlder_id
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
       "modelUri": f"gpt://{folder_id}/yandexgpt-lite/latest",
       "maxTokens": MAX_MODEL_TOKENS,
       "text": text
    }
    return len(
        requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",
            json=data,
            headers=headers
        ).json()['tokens']
    )