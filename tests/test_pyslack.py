import unittest
from libpyslack.core import PySlack, PostMessageBuilder


class TestPySlack(unittest.TestCase):
    def test_set_authorization_token_string(self):
        py_slack = PySlack()
        py_slack.set_authorization_token(token='TestToken')

        headers = py_slack.headers

        self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
        self.assertEqual(headers['Authorization'], 'Bearer TestToken')

    def test_set_authorization_token_binary(self):
        py_slack = PySlack()
        py_slack.set_authorization_token(token='BinaryTestToken'.encode())

        headers = py_slack.headers

        self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
        self.assertEqual(headers['Authorization'], 'Bearer BinaryTestToken')

    @staticmethod
    def __message_builder():
        return PostMessageBuilder()\
            .channel('TestChannel')\
            .username('Test User Bot')\
            .text('Message Body')\
            .description("Message Description")\
            .emoji(':thumbsup:')\
            .attachments([
                PostMessageBuilder.attachment('title1', 'pretext1', 'text1', 'good', [
                    PostMessageBuilder.field('field-title 1', 'field-value 1', True),
                    PostMessageBuilder.field('field-title 2', 'field-value 2', True),
                    PostMessageBuilder.field('field-title 3', 'field-value 3', True),
                    PostMessageBuilder.field('field-title 4', 'field-value 4', True),
                    PostMessageBuilder.field('field-title 5', 'field-value 5'),
                    PostMessageBuilder.field('field-title 6', 'field-value 6')
                ])
            ])\
            .build()

    def test_message_builder(self):
        message = self.__message_builder()

        self.assertEqual(message['channel'], '#TestChannel')
        self.assertEqual(message['username'], 'Test User Bot')
        self.assertEqual(message['icon_emoji'], ':thumbsup:')

        attachment = message['attachments'][0]
        self.assertEqual(attachment['title'], 'title1')
        self.assertEqual(attachment['pretext'], 'pretext1')
        self.assertEqual(attachment['text'], 'text1')
        self.assertEqual(attachment['color'], 'good')

        for field in attachment['fields']:
            self.assertIn('field-title ', field['title'])
            self.assertIn('field-value ', field['value'])

    @unittest.skip('skipping post_message')
    def test_post_message(self):
        message = self.__message_builder()

        py_slack = PySlack()
        py_slack.set_authorization_token('Token')
        response = py_slack.post_message(message)

        self.assertEqual(response['ok'], True)


if __name__ == '__main':
    unittest.main()
