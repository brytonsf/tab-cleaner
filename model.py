from datetime import datetime
from typing import List
from dbmodel import DBModel
from pydantic import Field


# Represents a usage of the app where all tabs are recorded/noted.
#
class TabStorageOperation(DBModel):
    __collection_name__ = "tab_storage_operations"
    urls: List[str]
    titles: List[str] # The title of each URL. We have this information at tab retrieval time,
        # and it does convey useful info, so let's store it.
    date: datetime = Field(default_factory=lambda: datetime.now())
