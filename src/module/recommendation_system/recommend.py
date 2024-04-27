from src.config.constant import Neo4jCFG
from src.models.recommendation_model import (RecommendationEventResponse,
                                             RecommendationUserEventResponse,
                                             RecommendationUserResponse)
from src.module.recommendation_system.neo4j_client import Neo4jClient
from src.module.recommendation_system.neo4j_init import Neo4jInit
from src.utils.logger import logger


def call_neo4j_client():
    neo4j_client = Neo4jClient(
        url=Neo4jCFG.URL, username=Neo4jCFG.USERNAME, password=Neo4jCFG.PASSWORD
    )
    return neo4j_client


def upsert_event(event):
    event = event.__dict__
    event["tags"] = "|".join(event["tags"])
    logger.info("CREATE/UPDATE EVENT")
    neo4j_client = call_neo4j_client()
    neo4j_client.upsert_event(event=event)

    response_object = RecommendationEventResponse(event_id=str(event["id"]))

    return {"STATUS": "SUCCESS", "CONTENT": response_object}


def delete_event(event_id):
    logger.info("DELETE EVENT")
    neo4j_client = call_neo4j_client()
    neo4j_client.delete_event(event_id=event_id)

    response_object = RecommendationEventResponse(event_id=event_id)

    return {"STATUS": "SUCCESS", "CONTENT": response_object}


def upsert_user(user):
    user = user.__dict__
    logger.info("CREATE/UPDATE USER")
    neo4j_client = call_neo4j_client()
    neo4j_client.upsert_user(user=user)
    response_object = RecommendationUserResponse(user_id=user["id"])

    return {"STATUS": "SUCCESS", "CONTENT": response_object}


def delete_user(user_id):
    logger.info("DELETE USER")
    neo4j_client = call_neo4j_client()
    neo4j_client.delete_user(user_id=user_id)

    response_object = RecommendationUserResponse(user_id=user_id)

    return {"STATUS": "SUCCESS", "CONTENT": response_object}


def view_event(data):
    data = data.__dict__
    user_id = data["user_id"]
    event_id = data["event_id"]
    logger.info("VIEW EVENT")
    neo4j_client = call_neo4j_client()
    neo4j_client.view_event(user_id=user_id, event_id=event_id)

    response_object = RecommendationUserEventResponse(
        event_id=event_id, user_id=user_id
    )

    return {"STATUS": "SUCCESS", "CONTENT": response_object}


def like_event(data):
    data = data.__dict__
    user_id = data["user_id"]
    event_id = data["event_id"]
    logger.info("LIKE EVENT")
    neo4j_client = call_neo4j_client()
    neo4j_client.like_event(user_id=user_id, event_id=event_id)

    response_object = RecommendationUserEventResponse(
        event_id=event_id, user_id=user_id
    )

    return {"STATUS": "SUCCESS", "CONTENT": response_object}


def unlike_event(data):
    data = data.__dict__
    user_id = data["user_id"]
    event_id = data["event_id"]
    logger.info("UNLIKE EVENT")
    neo4j_client = call_neo4j_client()
    neo4j_client.unlike_event(user_id=user_id, event_id=event_id)

    response_object = RecommendationUserEventResponse(
        event_id=event_id, user_id=user_id
    )

    return {"STATUS": "SUCCESS", "CONTENT": response_object}


def get_user_recommendation(user_id):
    logger.info("GENERATE RECOMMENDATION OF USER")
    neo4j_client = call_neo4j_client()
    recommendations = neo4j_client.get_recommendation(user_id=user_id)
    logger.info(f"USER ID: {user_id}")
    logger.info(f"EVENT IDS: {recommendations}")

    # response_object = RecommendationItemResponse(item_list=recommendations)

    return {"STATUS": "SUCCESS", "CONTENT": recommendations}

def init_neo4j():
    logger.info("INIT NEO4J STARTING")
    neo4j_init = Neo4jInit(url=Neo4jCFG.URL, username=Neo4jCFG.USERNAME, password=Neo4jCFG.PASSWORD)
    neo4j_init.init_neo4j()
    logger.info("INIT NEO4J COMPLETED")
    
    return {"STATUS": "SUCCESS", "CONTENT": "onichan baka"}
