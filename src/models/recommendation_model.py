from typing import List, Optional

from pydantic import BaseModel


class RecommendationUserModel(BaseModel):
    id: str
    categories: List[str]


class RecommendationEventModel(BaseModel):
    id: str
    name: str
    categories : List[str]
    tags: Optional[List[str]] = []
    # end_date: str


class RecommendationUserEventEdge(BaseModel):
    user_id: str
    event_id: str

class RecommendationEventResponse(BaseModel):
    event_id: str

class RecommendationUserResponse(BaseModel):
    user_id: str

class RecommendationUserEventResponse(BaseModel):
    event_id: str
    user_id: str

class RecommendationItemResponse(BaseModel):
    item_list: List[str]
