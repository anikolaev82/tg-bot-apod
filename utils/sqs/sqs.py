import dataclasses

import boto3
from aiogram import types
from config import AWSACCESSKEYID, AWSSECRETACCESSKEY
from wsnasa.entity.apod import ResponseAPOD
import json


class Sqs:

    def __init__(self):
        self._subs_apod = 'https://message-queue.api.cloud.yandex.net/b1gl199g1atnhk0ru9uv/dj6000000005ctf405ab/apod-subscribe'
        self._resp_apod = 'https://message-queue.api.cloud.yandex.net/b1gl199g1atnhk0ru9uv/dj6000000005cpro05ab/apod-response'
        self._client = boto3.client(
            service_name='sqs',
            endpoint_url='https://message-queue.api.cloud.yandex.net',
            region_name='ru-central1',
            aws_access_key_id=AWSACCESSKEYID,
            aws_secret_access_key=AWSSECRETACCESSKEY
        )

    def pull_apod(self):
        messages = self._client.receive_message(
            QueueUrl=self._resp_apod,
            MaxNumberOfMessages=10,
            VisibilityTimeout=60,
            WaitTimeSeconds=20
        ).get('Messages')
        ret = []
        for msg in messages:
            ret.append(msg.get('Body'))
            self._client.delete_message(QueueUrl=self._resp_apod, ReceiptHandle=msg.get('ReceiptHandle'))
        return ret

    def push_apod(self, message: types.Message):
        msg = {"user": str(message.from_user.id), "chat_id": str(message.chat.id), "action": "subscribe"}
        self._client.send_message(
            QueueUrl=self._subs_apod,
            MessageBody=msg
        )

    def push_response(self, message: types.Message, response: ResponseAPOD):
        msg = {"user": str(message.from_user.id), "response": json.dumps(dataclasses.asdict(response))}
        self._client.send_message(
            QueueUrl=self._resp_apod,
            MessageBody=json.dumps(msg)
        )
