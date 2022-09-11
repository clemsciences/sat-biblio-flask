import datetime

from sat_biblio_server import LogEventDB
from sat_biblio_server.utils import EventEnum


class LogEventManager:

    def __init__(self, db):
        self.db = db

    def _add_event(self,
                   event_type: EventEnum,
                   object_id: int,
                   event_datetime: datetime.datetime,
                   event_owner_id: int,
                   table_name: str,
                   values: str):
        log_event_db = LogEventDB(event_type=event_type.value, object_id=object_id, event_datetime=event_datetime,
                                  event_owner_id=event_owner_id, table_name=table_name, values=values)
        self.db.session.add(log_event_db)
        self.db.session.commit()

    def add_create_event(self, object_id: int, event_owner_id: int, table_name: str, values: str = None):
        self._add_event(EventEnum.create, object_id, datetime.datetime.now(), event_owner_id, table_name, values)

    def add_delete_event(self, object_id: int, event_owner_id: int, table_name: str, values: str = None):
        self._add_event(EventEnum.delete, object_id, datetime.datetime.now(), event_owner_id, table_name, values)

    def add_update_event(self, object_id: int, event_owner_id: int, table_name: str, values: str = None):
        self._add_event(EventEnum.update, object_id, datetime.datetime.now(), event_owner_id, table_name, values)
