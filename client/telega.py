import settings
from client import models
from utils.rest_client import RestClient


class TelegaBot(object):

    def __init__(self):
        self.rest_client = RestClient(host=f'https://api.telegram.org/bot{settings.telega_token}')

    def set_webhook(self) -> models.WebhookSetOrDelete:
        method: str = '/setWebhook'
        response = self.rest_client.post(path=method, params={'url': settings.telega_webhook_url})

        return models.WebhookSetOrDelete(**response.json())

    def delete_webhook(self) -> models.WebhookSetOrDelete:
        method: str = '/deleteWebhook'
        response = self.rest_client.get(path=method)

        return models.WebhookSetOrDelete(**response.json())

    def get_chat_id(self) -> int:
        method: str = '/getUpdates'
        last_update_info: models.Update = models.Update(**self.rest_client.get(method).json())

        return last_update_info.result[0].message.chat.id

    def send_message(self, message: str, chat_id, dis_preview: bool = True, parse_mode: str = None,
                     dis_notification: bool = False, inline_keyboard=None, entities=None) -> models.Message:
        method: str = '/sendMessage'

        json = {
            'chat_id': chat_id,
            'text': message,
            'disable_web_page_preview': dis_preview,
            'parse_mode': parse_mode,
            'disable_notification': dis_notification
        }
        if inline_keyboard:
            json['reply_markup'] = {'inline_keyboard': inline_keyboard}
        if entities:
            json['entities'] = entities

        response = self.rest_client.post(method, json=json)
        if response.ok:
            return models.Message(**response.json()['result'])
        else:
            return models.Error(**response.json())

    def send_audio(self, audio: str, caption: str, chat_id, inline_keyboard=None) -> models.Message:
        method: str = '/sendAudio'

        json = {
            'chat_id': chat_id,
            'audio': audio,
            'caption': caption
        }
        if inline_keyboard:
            json['reply_markup'] = {'inline_keyboard': inline_keyboard}

        response = self.rest_client.post(method, json=json)
        if response.ok:
            return models.Message(**response.json()['result'])
        else:
            return models.Error(**response.json())

    def answer_callback_query(self, callback_query_id: str, text: str):
        method: str = '/answerCallbackQuery'

        json = {
            'callback_query_id': callback_query_id,
            'text': text,
        }

        self.rest_client.post(method, json=json)
