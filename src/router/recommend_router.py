from typing import Any, Dict

from fastapi import APIRouter, HTTPException

import src.module.recommendation_system.recommend as recsys
from src.models.recommendation_model import (RecommendationEventModel,
                                             RecommendationUserEventEdge,
                                             RecommendationUserModel)
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/recommendation", tags=["recommendation"])


@router.post(path="/event")
def upsert_event_api(data: RecommendationEventModel) -> Dict[str, Any]:
    logger.info("API - Upsert event")
    try:
        response = recsys.upsert_event(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)


@router.delete(path="/event/{id}")
def delete_event_api(id: str) -> Dict[str, Any]:
    logger.info("API - Delete event")
    try:
        response = recsys.delete_event(id)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)


@router.post(path="/user")
def upsert_user_api(data: RecommendationUserModel) -> Dict[str, Any]:
    logger.info("API - Upsert user")
    try:
        response = recsys.upsert_user(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)


@router.delete(path="/user/{id}")
def delete_user_api(id: str) -> Dict[str, Any]:
    logger.info("API - Delete user")
    try:
        response = recsys.delete_user(id)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)


@router.put(path="/view")
def view_event_api(data: RecommendationUserEventEdge) -> Dict[str, Any]:
    logger.info("API - User views event")
    try:
        response = recsys.view_event(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)


@router.put(path="/like")
def follow_event_api(data: RecommendationUserEventEdge) -> Dict[str, Any]:
    logger.info("API - User likes event")
    try:
        response = recsys.like_event(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)


@router.delete(path="/like")
def unfollow_event_api(data: RecommendationUserEventEdge) -> Dict[str, Any]:
    logger.info("API - User unlikes event")
    try:
        response = recsys.unlike_event(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)


@router.get(path="/user/{id}")
def get_user_recommendation_api(id: str) -> Dict[str, Any]:
    logger.info("API - Get user recommendation")
    try:
        response = recsys.get_user_recommendation(id)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)
