# -*- coding: utf-8 -*-
# import module snippets
import datetime
from .client import Client
from .util import get_arguments


class Event(Client):

    def items(
        self,
        created_after: datetime.datetime = None,
        created_before: datetime.datetime = None,
        event_type: list = None,
        limit: int = None,
        stream_position: str = None,
        stream_type: str = None
    ):
        query = get_arguments(locals())
        return self.client.make_request(
            method="GET",
            url=self.client.get_url("events"),
            params=query
        ).json()

    def endpoint(self):
        return self.client.events().generate_events_with_long_polling()
