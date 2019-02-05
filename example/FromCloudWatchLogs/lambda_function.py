# coding:utf-8

import boto3
import zlib
import json
import logging
import time
import os

from base64 import b64decode
from libpyslack import PySlack, PostMessageBuilder


ENCRYPTED_EXPECTED_TOKEN = os.environ['kmsEncryptedToken']

kms = boto3.client('kms')
token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    decoded_event = zlib.decompress(b64decode(event['awslogs']['data']), 16 + zlib.MAX_WBITS)
    data_json = json.loads(decoded_event)

    for event in data_json['logEvents']:
        log_level = 'UNKNOWN'

        sec, ms = divmod(event['timestamp'], 1000)
        error_fields = [
            PostMessageBuilder.field('TimeStamp', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec)), True),
            PostMessageBuilder.field('LogGroup', data_json['logGroup'], False),
            PostMessageBuilder.field('LogStream', data_json['logStream'], False)]

        if 'extractedFields' in event:
            fields = event['extractedFields']
            # fields の構成はログ次第なので適宜 error_fields に append してください
            error_fields.append(
                PostMessageBuilder.field('Message', fields['message'], False))

        else:
            error_fields.append(
                PostMessageBuilder.field('Message', event['message'], False))

        notify_color = 'danger'

        message = PostMessageBuilder() \
            .channel(os.environ['channel']) \
            .username(os.environ['botUserName']) \
            .text('サーバーで通知対象のエラーが発生しました.') \
            .emoji(':pepper:') \
            .attachments([
                PostMessageBuilder.attachment(color=notify_color, fields=error_fields)
            ]) \
            .build()

        pyslack = PySlack(token)
        pyslack.post_message(message)

    return {
        'statusCode': 200,
        'body': '200 OK'
    }
