# coding: utf-8
import json
from urllib.request import Request, urlopen


class PostMessageBuilder:
    def __init__(self):
        self.message = {}

    def channel(self, channel: str) -> 'PostMessageBuilder':
        self.message['channel'] = '#{0}'.format(channel)
        return self

    def username(self, username: str = 'PySlackBot') -> 'PostMessageBuilder':
        self.message['username'] = username
        return self

    def text(self, text: str = None) -> 'PostMessageBuilder':
        if text is not None:
            self.message['text'] = text
        return self

    def description(self, description: str = None) -> 'PostMessageBuilder':
        if description is not None:
            self.message['description'] = description
        return self

    def emoji(self, emoji: str = None) -> 'PostMessageBuilder':
        if emoji is not None:
            self.message['icon_emoji'] = emoji
        return self

    def attachments(self, attachments: list) -> 'PostMessageBuilder':
        self.message['attachments'] = attachments
        return self

    @staticmethod
    def attachment(title: str = None, pretext: str = None, text: str = None, color: str = None, fields: list = None):
        attachment = {
        }

        if title is not None:
            attachment['title'] = title

        if pretext is not None:
            attachment['pretext'] = pretext

        if text is not None:
            attachment['text'] = text

        if color is not None:
            attachment['color'] = color

        if fields is not None:
            attachment['fields'] = fields

        return attachment

    @staticmethod
    def field(title: str, value: str, is_short: bool = False):
        return {
            'title': title,
            'value': value,
            'short': is_short
        }

    def build(self):
        return self.message


class PySlack:
    def __init__(self, token=None):
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        if token is not None:
            self.set_authorization_token(token)

    def set_authorization_token(self, token=None):
        assert token is not None
        decoded_token = token if type(token) is not bytes else token.decode()
        self.headers['Authorization'] = 'Bearer {0}'.format(decoded_token)

    def post_message(self, message):
        """
        see: https://api.slack.com/methods/chat.postMessage
        """
        url = 'https://slack.com/api/chat.postMessage'
        json_data = json.dumps(message).encode()

        request = Request(url=url, data=json_data, headers=self.headers, method='POST')
        with urlopen(request, timeout=3) as response:
            response_body = response.read().decode("utf-8")

        return json.loads(response_body)
