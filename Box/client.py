# -*- coding: utf-8 -*-
# import module snippets
import boxsdk
import functools


class Client(object):

    auth = None
    __client = None

    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        enterprise_id: str = None,
        jwt_key_id: str = None,
        rsa_private_key_data: str = None,
        rsa_private_key_file_sys_path: str = None,
        rsa_private_key_passphrase: str = None,
        client = None,
    ):
        if client is not None:
            self.__client = client
        else:
            if rsa_private_key_data is not None:
                self.auth = functools.partial(
                    boxsdk.JWTAuth,
                    client_id=client_id,
                    client_secret=client_secret,
                    enterprise_id=enterprise_id,
                    jwt_key_id=jwt_key_id,
                    rsa_private_key_data=rsa_private_key_data,
                    rsa_private_key_passphrase=rsa_private_key_passphrase
               )
            else:
                self.auth = functools.partial(
                    boxsdk.JWTAuth,
                    client_id=client_id,
                    client_secret=client_secret,
                    enterprise_id=enterprise_id,
                    jwt_key_id=jwt_key_id,
                    rsa_private_key_file_sys_path=rsa_private_key_file_sys_path,
                    rsa_private_key_passphrase=rsa_private_key_passphrase
                )
            sdk = self.auth()
            self.__client = boxsdk.Client(sdk)

    def login(self, username: str):
        users = self.__client.users(filter_term=username)
        user = None
        for u in users:
            user = u
        user_auth = self.__client._oauth
        user_auth.authenticate_app_user(user)
        self.__client = boxsdk.Client(user_auth)

    def get_client(self):
        return self.__client

    def set_client(self, client):
        self.__client = client

    client = property(get_client, set_client)
