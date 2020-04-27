
# -*- coding: utf-8 -*-
# import module snippets
import hashlib
import json
import io
import os
import urllib
import boxsdk
from .client import Client


class File(Client):

    def info(self, file_id: str):
        url = self.client.get_url("files", file_id)
        try:
            response = self.client.make_request(
                method='GET',
                url=url
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def download(
        self, file_id: str, version_id: str = None,
        offset: int = None, length: int = None,
        output_path: str = None
    ):
        byte_range = None
        file_version = None

        if offset is not None and length is not None:
            byte_range = (offset, length)
        if version_id is not None:
            file_version = self.client.file_version(version_id)

        try:
            box_file = self.client.file(file_id=file_id)
        except boxsdk.exception.BoxAPIException as e:
            raise e
        try:
            if output_path is not None:
                box_file = box_file.get()
                file_path = os.path.join(output_path, box_file.name)
                writeable_stream = open(file_path, "wb")
                box_file.download_to(
                    writeable_stream,
                    file_version=file_version,
                    byte_range=byte_range
                )
                writeable_stream.close()
            else:
                return box_file.content(
                    file_version=file_version,
                    byte_range=byte_range
                )
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def upload(
        self, folder_id: str, stream: io.BytesIO,
        name: str, overwrite: bool = False
    ):
        stream.seek(0)
        try:
            box_file = self.client.folder(folder_id).upload_stream(stream, name)
            return box_file
        except boxsdk.exception.BoxAPIException as e:
            if e.code == "item_name_in_use" and overwrite:
                file = self.client.file(e.context_info['conflicts']['id'])
                upload_file = file.update_contents_with_stream(stream)
                return upload_file
            else:
                raise e

    def preflight(self, name: str, parent_id: str, size: int):
        url = self.client.get_url("files", "content")
        data = json.dumps({
            "name": name,
            "parent": {
                "id": parent_id
            },
            "size": size
        })
        try:
            response = self.client.make_request(
                method='OPTIONS',
                url=url,
                data=data
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e


    def multipart_upload(self, name: str, parent_id: str, size: int, data: io.BytesIO):
        try:
            folder = self.client.folder(parent_id)
            response = folder.upload_stream(
                file_stream = data,
                file_name = name,
                preflight_check=True,
                preflight_expected_size=size,
                upload_using_accelerator=True
            )
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def copy(
        self, file_id: str, parent_id: str,
        name: str = None, version_id: str = None
    ):
        try:
            file_to_copy = self.client.file(file_id)
            destination_folder = self.client.folder(parent_id)
            file_copy = file_to_copy.copy(destination_folder, name=name)
            response = file_copy.response_object
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def lock(
        self, file_id: str,
        expires_at: str = None,
        is_download_prevented: bool = None
    ):
        url = self.client.get_url("files", file_id)
        lock = {
            "type": "lock"
        }
        if expires_at is not None:
            lock["expires_at"] = expires_at
        if is_download_prevented is not None:
            lock["is_download_prevented"] = is_download_prevented
        data = json.dumps({
            "lock": lock
        })
        try:
            response = self.client.make_request(
                method='PUT',
                url=url,
                data=data
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def unlock(self, file_id: str):
        url = self.client.get_url("files", file_id)
        data = json.dumps({"lock": None})
        try:
            response = self.client.make_request(
                method='PUT',
                url=url,
                data=data
            ).json()
            return response
        except boxsdk.exception.BoxAPIException as e:
            raise e

    def uploader(stream, length, name, folder_id):
        try:
            if length <= 20000000:
                uploaded_file = self.upload(
                    folder_id=folder_id, stream=io.BytesIO(stream.read()),
                    name=name, overwrite=True
                )
                return uploaded_file.id, uploaded_file.name
            # Chunk upload
            session = self.client.folder(
                folder_id=folder_id
            ).create_upload_session(file_size=length, file_name=name)
            parts = []
            sha1 = hashlib.sha1()
            for part_index in range(session.total_parts):
                copied_length = 0
                chunk = b''
                while copied_length < session.part_size:
                    buffer = stream.read(session.part_size - copied_length)
                    if buffer is None:
                        continue
                    if len(buffer) == 0:
                        break
                    chunk += buffer
                    copied_length += len(buffer)
                    uploaded_part = session.upload_part_bytes(
                        chunk, part_index*session.part_size, length)
                    parts.append(uploaded_part)
                    updated_sha1 = sha1.update(chunk)
            content_sha1 = sha1.digest()
            uploaded_file = session.commit(
                content_sha1=content_sha1, parts=parts)
            return uploaded_file.id, uploaded_file.name
        except Exception as e:
            raise e
