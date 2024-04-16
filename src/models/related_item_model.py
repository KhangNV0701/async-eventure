from typing import List, Optional

from pydantic import BaseModel


class RelatedItemModel(BaseModel):
    event_id: Optional[int] = 0
    event_name: Optional[str] = ""
    event_tags: Optional[List[str]] = []
    event_description: Optional[str] = ""
