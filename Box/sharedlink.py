
# -*- coding: utf-8 -*-
# import module snippets
import hashlib
import json
import io
import os
import urllib
import boxsdk
from .client import Client


class SharedLink(Client):

    def get(self, file_id: str):
        url = self.client.get_url("files", file_id)
        query = ["fields={}".format("shared_link")]
        query = '&'.join(query)
        url = '%s?%s' % (url, query)
        try:
            response = self.client.make_request(
                method='GET',
                url=url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def unshared(self, file_id: str):
        url = self.client.get_url("files", file_id)
        query = ["fields={}".format("shared_link")]
        data = json.dumps({
            "shared_link": None
        })
        query = '&'.join(query)
        url = '%s?%s' % (url, query)
        try:
            response = self.client.make_request(
                method='PUT',
                url=url,
                data=data
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e
