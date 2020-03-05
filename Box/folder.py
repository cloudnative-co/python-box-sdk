
# -*- coding: utf-8 -*-
# import module snippets
import boxsdk
import json
import io
import os
from .client import Client


class Folder(Client):

    def info(self, folder_id: int):
        url = self.client.get_url("folders", folder_id)
        try:
            response = self.client.make_request(
                method='GET',
                url=url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def items(
        self,
        folder_id: int,
        fields: list = None,
        usemarker: bool = None,
        marker: str = None,
        offset: int = None,
        sort: str= None,
        direction: str = None,
        limit: int = None
    ):
        url = self.client.get_url("folders", folder_id, "items")
        query = []
        if fields is not None:
            fields = ",".join(fields)
            query.append("fields={}".format(fields))
        if usemarker is not None:
            query.append("usemarker={}".format(usemarker))
        if marker is not None:
            query.append("marker={}".format(marker))
        if offset is not None:
            query.append("offset={}".format(offset))
        if sort is not None:
            query.append("sort={}".format(sort))
        if direction is not None:
            query.append("direction={}".format(direction))
        if limit is not None:
            query.append("limit={}".format(limit))

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

    def create(
        self,
        name: str,
        parent_id: int,
        fields: list = None,
    ):
        url = self.client.get_url("folders")
        query = []
        if fields is not None:
            fields = ",".join(fields)
            query.append("fields={}".format(fields))
            query = '&'.join(query)
            url = '%s?%s' % (url, query)

        data = json.dumps({
            "name": name,
            "parent": {
                "id": parent_id
            }
        })

        try:
            response = self.client.make_request(
                method='POST',
                url=url,
                data=data
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def delete(self, folder_id: str):
        url = "https://api.box.com/2.0/folders/{}".format(folder_id)
        try:
            response = self.client.make_request(
                'DELETE',
                url
            )
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e
