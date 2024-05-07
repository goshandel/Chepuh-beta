import requests
from cregs import get_creds

iam_token, folder_id = get_creds()
def text_to_speech(text: str):



    # Аутентификация через IAM-токен
    headers = {
        'Authorization': f'Bearer {iam_token}',
    }
    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'filipp',
        'folderId': folder_id,
    }
    # Выполняем запрос
    response = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=headers, data=data)

    if response.status_code == 200:
        return True, response.content
    else:
        return False, "При запросе в SpeechKit возникла ошибка"

def speech_to_text(data):
    iam_token = "t1.9euelZqZyJGYx4mXzMaKlI7Iz5SOjO3rnpWanZHNz5iajprMlYvJk5uYnsrl8_chZQ9P-e8jNQ5H_t3z92ETDU_57yM1Dkf-zef1656Vmo2Rxs3MjZuJisebmJCPloqR7_zF656Vmo2Rxs3MjZuJisebmJCPloqRveuelZqSzsuVip6VmoqdjonKyMvLybXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.zIga_XK191_P79LXBg0UDHD26rj1kz2_XPvITAjKcC_DUAr1mKOXII42YZP089uqE9BI7xR2DJJVbVUS2A1SCQ"
    folder_id = "b1ga8pn188dspdv50cbv"

    params = "&".join([
        "topic=general",
        f"folderId={folder_id}",
        "lang=ru-RU"
    ])

    headers = {
        'Authorization': f'Bearer {iam_token}',
    }

    response = requests.post(
        f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}",
        headers=headers,
        data=data
    )
    decoded_data = response.json()
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")  # Возвращаем статус и текст из аудио
    else:
        return False, "При запросе в SpeechKit возникла ошибка"



