# -*- coding: utf-8 -*-
# import module snippets
import boxsdk
import json
from .util import find_method_params
from .client import Client


class User(Client):

    def me(self):
        url = self.client.get_url("users", "me")
        try:
            response = self.client.make_request(
                method='GET',
                url=url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def get(self, user_id: str):
        url = self.client.get_url("users", user_id)
        try:
            response = self.client.make_request(
                'GET',
                url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def avatar(self, user_id: str):
        url = self.client.get_url("users", user_id, "avatar")
        try:
            response = self.client.make_request(
                'GET',
                url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def list(
        self, filter_term: str = None,
        offset: int = 0,
        limit: int = 100,
        marker: str = None
    ):
        url = self.client.get_url("users")
        query = ['limit=%d' % limit, 'offset=%d' % offset]
        if marker is not None:
            query.append('marker=%s' % marker)
        if filter_term is not None:
            query.append('filter_term=%s' % filter_term)
        query = '&'.join(query)

        url = '%s?%s' % (url, query)
        response = self.client.make_request(
            'GET',
            url
        ).json()
        return response

    def create(
        self,
        login: str = None, name: str = None, role: str = None,
        is_platform_access_only: bool = False,
        language: str = None, is_sync_enabled: bool = None,
        job_title: str = None, phone: str = None, address: str = None,
        space_amount: str = None, can_see_managed_users: str = None,
        timezone: str = None, is_exempt_from_device_limits: bool = None,
        is_exempt_from_login_verification: bool = None,
        is_external_collab_restricted: bool = None,
        status: str = None,
        json_data: dict = None,
        json_path: str = None
    ):
        data = {}
        if json_data is not None:
            data = json_data
        elif json_path is not None:
            try:
                fd = open(json_path)
                data = json.load(fd)
                fd.close()
            except Exception as e:
                raise e
        else:
            data["is_platform_access_only"] = is_platform_access_only
            if not is_platform_access_only:
                if login is not None:
                    data["login"] = login
                if role is not None:
                    data["role"] = role
                if is_sync_enabled is not None:
                    data["is_sync_enabled"] = is_sync_enabled
                if is_exempt_from_device_limits is not None:
                    data["is_exempt_from_device_limits"] = is_exempt_from_device_limits
                if is_exempt_from_login_verification is not None:
                    data["is_exempt_from_login_verification"] = is_exempt_from_login_verification
            if name is not None:
                data["name"] = name
            if language is not None:
                data["language"] = language
            if job_title is not None:
                data["job_title"] = job_title
            if phone is not None:
                data["phone"] = phone
            if address is not None:
                data["address"] = address
            if space_amount is not None:
                data["space_amount"] = space_amount
            if status is not None:
                data["status"] =status
            if timezone is not None:
                data["timezone"] =timezone
            if can_see_managed_users is not None:
                data["can_see_managed_users"] = can_see_managed_users
            if is_external_collab_restricted is not None:
                data["is_external_collab_restricted"] = is_external_collab_restricted

        require = ("name" in data and "is_platform_access_only" in data)
        if not require:
            raise Exception("name not found")

        data = json.dumps(data)
        url = self.client.get_url("users")
        try:
            response = self.client.make_request(
                method='POST',
                url=url,
                data=data,
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def delete(self, user_id: str, notify: bool = False, force: bool = False):
        url = self.client.get_url("users", user_id)
        query = ['notify=%s' % notify, 'force=%s' % force]
        query = '&'.join(query).lower()
        url = '%s?%s' % (url, query)
        try:
            response = self.client.make_request(
                'DELETE',
                url
            )
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e
