from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from src.models.related_item_model import RelatedItemModel
from src.module.related_items.related_events import (
    insert_event_to_zilliz,
    retrieve_related_events_zilliz
)
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/related-items", tags=["related-items"])


@router.post(path="/insert-event")
def insert_event_api(data: RelatedItemModel) -> Dict[str, Any]:
    logger.info("API - Insert event to Zilliz")
    try:
        response = insert_event_to_zilliz(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)


@router.post(path="/retrieve-related-events")
def get_related_events_api(data: RelatedItemModel) -> Dict[str, Any]:
    logger.info("API - Retrieve related events")
    try:
        response = retrieve_related_events_zilliz(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)
