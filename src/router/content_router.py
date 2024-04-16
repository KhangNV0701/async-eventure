from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from src.models.event_content_model import EventContentModel
from src.module.text_generator.generate_content import (
    generate_event_content,
    generate_event_faq,
)
from src.utils.logger import logger

router = APIRouter(prefix="/api/v1/content", tags=["content"])


@router.post(path="/generate/event-info")
def generate_event_content_api(data: EventContentModel) -> Dict[str, Any]:
    logger.info("API - Generate event content")
    try:
        response = generate_event_content(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)


@router.post(path="/generate/event-faq")
def generate_event_faq_api(data: EventContentModel) -> Dict[str, Any]:
    logger.info("API - Generate event FAQ")
    try:
        response = generate_event_faq(data)
        return response
    except TimeoutError as err:
        raise HTTPException(status_code=408, detail=err)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)
