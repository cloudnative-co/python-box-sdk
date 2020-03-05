# -*- coding: utf-8 -*-
# import module snippets
import json
import boxsdk
from .client import Client


class Webhook(Client):

    def list(self, marker: str = None, limit: int = 100):
        url = "https://api.box.com/2.0/webhooks"
        query = ['limit=%d' % limit]
        if marker is not None:
            query.append('marker=%s' % marker)
        query = '&'.join(query)
        url = '%s?%s' % (url, query)
        response = self.client.make_request(
            'GET',
            url
        ).json()
        return response

    def get(self, id: str):
        url = "https://api.box.com/2.0/webhooks/{}".format(id)
        try:
            response = self.client.make_request(
                'GET',
                url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def create(
        self,
        target_type: str = "folder",
        target_id: str = "0",
        triggers: list = ['SHARED_LINK.CREATED'],
        notification_url=None
    ):
        target = {
            "id": target_id,
            "type": target_type
        }
        data = {
            "target": target,
            "address": notification_url,
            "triggers": triggers
        }
        data = json.dumps(data)
        url = "https://api.box.com/2.0/webhooks"
        try:
            response = self.client.make_request(
                'POST',
                url,
                data=data
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def update(
        self, id: str,
        notification_url: str,
        target_type: str = "folder",
        target_id: str = "0",
        triggers: list = ['FILE.UPLOADED']
    ):
        target = {
            "id": target_id,
            "type": target_type
        }
        data = {
            "target": target,
            "address": notification_url,
            "triggers": triggers
        }
        data = json.dumps(data)
        url = "https://api.box.com/2.0/webhooks/%s" % id
        try:
            response = self.client.make_request(
                'PUT',
                url,
                data=data
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def delete(self, id: str):
        url = "https://api.box.com/2.0/webhooks/{}".format(id)
        try:
            response = self.client.make_request(
                'DELETE',
                url
            )
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e
