# -*- coding: utf-8 -*-
# import module snippets
import boxsdk
import json
from .client import Client


class Metadata(Client):

    def list(self, file_id: str = None, folder_id: str = None):
        if folder_id is not None:
            res = "folders"
            id = folder_id
        if file_id is not None:
            res = "files"
            id = file_id
        if folder_id is None and file_id is None:
            return []

        url = self.client.get_url(res, id, "metadata")
        try:
            response = self.client.make_request(
                method='GET',
                url=url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def get(
        self, scope: str, template: str,
        file_id: str = None, folder_id: str = None
    ):
        if folder_id is not None:
            res = "folders"
            id = folder_id
        if file_id is not None:
            res = "files"
            id = file_id
        if folder_id is None and file_id is None:
            return []
        url = self.client.get_url(res, id, "metadata", scope, template)
        try:
            response = self.client.make_request(
                method='GET',
                url=url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def create(
        self, scope: str, template: str, data: dict = None,
        data_path: str = None,
        file_id: str = None, folder_id: str = None
    ):
        if folder_id is not None:
            res = "folders"
            id = folder_id
        if file_id is not None:
            res = "files"
            id = file_id
        if folder_id is None and file_id is None:
            return []
        if data_path is not None:
            try:
                fd = open(data_path)
                data = json.load(fd)
                fd.close()
            except Exception as e:
                raise e
        data = json.dumps(data)
        url = self.client.get_url(res, id, "metadata", scope, template)

        try:
            response = self.client.make_request(
                method='POST',
                url=url,
                data=data,
                headers={"Content-Type": "application/json"}
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def update(
        self, scope: str, template: str, data: dict,
        file_id: str = None, folder_id: str = None
    ):
        if folder_id is not None:
            res = "folders"
            id = folder_id
        if file_id is not None:
            res = "files"
            id = file_id
        if folder_id is None and file_id is None:
            return []
        data = json.dumps(data)
        url = self.client.get_url(res, id, "metadata", scope, template)

        try:
            response = self.client.make_request(
                method='PUT',
                url=url,
                data=data,
                headers={"Content-Type": "application/json-patch+json"}
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def delete(
        self, scope: str, template: str,
        file_id: str = None, folder_id: str = None
    ):
        if folder_id is not None:
            res = "folders"
            id = folder_id
        if file_id is not None:
            res = "files"
            id = file_id
        if folder_id is None and file_id is None:
            return []
        url = self.client.get_url(res, id, "metadata", scope, template)

        try:
            response = self.client.make_request(
                method='DELETE',
                url=url
            )
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e



class MetadataTemplate(Client):

    def list(
        self,
        scope: str = 'enterprise',limit: int = None, marker: str = None
    ):
        try:

            query = {}
            if limit is not None:
                query = ['limit=%d' % limit]
            if marker is not None:
                query.append('marker=%s' % marker)

            query = '&'.join(query)
            url = self.client.get_url('metadata_templates', scope)
            url = '%s?%s' % (url, query)

            response = self.client.make_request(
                method='GET',
                url=url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def get(
        self,
        scope: str = 'enterprise', template: str = None, id: str = None
    ):
        try:
            url = self.client.get_url('metadata_templates', scope, template, "schema")
            if id  is not None:
                url = self.client.get_url('metadata_templates', id)
            if id is None and template is None:
                pass
            response = self.client.make_request(
                'GET',
                url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def create(self, template_path: str = None, template_json: str = None):
        try:
            if template_path is not None:
                try:
                    fd = open(template_path)
                    template_json = json.load(fd)
                    fd.close()
                except Exception as e:
                    raise e
                data = json.dumps(template_json)
            elif template_json is not None:
                data = template_json
            if template_json is None and template_path is None:
                pass
            url = self.client.get_url('metadata_templates', "schema")
            response = self.client.make_request(
                'POST',
                url,
                data=data
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def delete(
        self,
        scope: str = 'enterprise', template: str = None
	):
        try:
            url = self.client.get_url('metadata_templates', scope, template, "schema")
            response = self.client.make_request(
                'DELETE',
                url
            )
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def update(self,
        scope: str = 'enterprise', template: str = None,
		template_path: str = None, template_json: str = None
	):
        try:
            url = self.client.get_url('metadata_templates', scope, template, "schema")
            if template_path is not None:
                try:
                    fd = open(template_path)
                    template_json = json.load(fd)
                    fd.close()
                except Exception as e:
                    raise e
                data = json.dumps(template_json)
            elif template_json is not None:
                data = template_json
            if template_json is None and template_path is None:
                pass
            response = self.client.make_request(
                'PUT',
                url,
                data=data
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e
