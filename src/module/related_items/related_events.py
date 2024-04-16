import json

from src.config.constant import MongodbCFG
from src.module.embedding.gemini_embedding import GeminiEmbeddingModel
from src.module.mongodb.mongodb_client import MongoDBClient
from src.utils.logger import logger


def insert_event_to_mongodb(event):
    try:
        document = document_builder(event)
        mongo = MongoDBClient(
            collection_name=MongodbCFG.MONGODB_COLLECTION_NAME_RELATED_EVENT
        )
        mongo.insert_records([document])
        return {"status": True}
    except Exception as e:
        logger.error(e)
        return {"status": False}


def retrieve_related_events(event):
    event_name = event.event_name
    event_tags = event.event_tags
    event_tags_str = ",".join(event_tags)
    event_query = f"{event_name} {event_tags_str}"

    mongo = MongoDBClient(
        collection_name=MongodbCFG.MONGODB_COLLECTION_NAME_RELATED_EVENT
    )
    related_events = mongo.vector_search(
        index_name=MongodbCFG.MONGODB_INDEX_NAME_RELATED_EVENT, 
        query=event_query
    )

    logger.info(
        "RETRIEVED RELATED EVENTS: %s",
        str(json.dumps(related_events, indent=4, ensure_ascii=True)),
    )

    response = {"related_events": related_events}
    return response


def document_builder(data):
    embedding = GeminiEmbeddingModel()

    event_id = data.event_id
    event_name = data.event_name
    event_tags = data.event_tags
    event_description = data.event_description

    event_tags_str = " ".join(event_tags)
    event_info = (
        f"{event_name}\nTAGS:\n{event_tags_str}\n\nDESCRIPTION:\n{event_description}"
    )
    event_info_embedding = embedding.get_embedding(
        event_info, task_type="retrieval_document", title="document"
    )

    document = {
        "event_id": event_id,
        "event_name": event_name,
        "event_tags": event_tags,
        "event_description": event_description,
        "event_info": event_info,
        "embedding": event_info_embedding.get("embedding"),
    }
    logger.info(
        "INSERTING DOCUMENT: %s", json.dumps(document, indent=4, ensure_ascii=True)
    )
    return document
