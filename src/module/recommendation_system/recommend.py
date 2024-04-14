from src.config.constant import neo4jCFG
from src.module.recommendation_system.neo4j_client import Neo4jClient
from src.utils.logger import logger
from src.models.recommendation_model import RecommendationEventResponse, RecommendationItemResponse, RecommendationUserEventResponse, RecommendationUserResponse

def call_neo4j_client():
    neo4j_client = Neo4jClient(url=neo4jCFG.URL,
                               username=neo4jCFG.USERNAME,
                               password=neo4jCFG.PASSWORD)
    return neo4j_client


def upsert_event(event):
    event = event.__dict__
    event['tags'] = '|'.join(event['tags'])
    logger.info("CREATE/UPDATE EVENT")
    neo4j_client = call_neo4j_client()
    neo4j_client.upsert_event(event=event)

    response_object = RecommendationEventResponse(event_id=event['id'])

    return {'STATUS': 'SUCCESS',
            'CONTENT': response_object}


def delete_event(event_id):
    print(event_id, type(event_id))
    logger.info("DELETE EVENT")
    neo4j_client = call_neo4j_client()
    neo4j_client.delete_event(event_id=event_id)

    response_object = RecommendationEventResponse(event_id=event_id)

    return {'STATUS': 'SUCCESS',
            'CONTENT': response_object}


def upsert_user(user):
    user = user.__dict__
    logger.info("CREATE/UPDATE USER")
    neo4j_client = call_neo4j_client()
    neo4j_client.upsert_user(user=user)
    response_object = RecommendationUserResponse(user_id=user['id'])
    
    return {'STATUS': 'SUCCESS',
            'CONTENT': response_object}


def delete_user(user_id):
    logger.info("DELETE USER")
    neo4j_client = call_neo4j_client()
    neo4j_client.delete_user(user_id=user_id)

    response_object = RecommendationUserResponse(user_id=user_id)

    return {'STATUS': 'SUCCESS',
            'CONTENT': response_object}


def view_event(data):
    data = data.__dict__
    user_id = data['user_id']
    event_id = data['event_id']
    logger.info("VIEW EVENT")
    neo4j_client = call_neo4j_client()
    neo4j_client.view_event(user_id=user_id, event_id=event_id)

    response_object = RecommendationUserEventResponse(event_id=event_id, user_id=user_id)

    return {'STATUS': 'SUCCESS',
            'CONTENT': response_object}


def like_event(data):
    data = data.__dict__
    user_id = data['user_id']
    event_id = data['event_id']
    logger.info("LIKE EVENT")
    neo4j_client = call_neo4j_client()
    neo4j_client.like_event(user_id=user_id, event_id=event_id)

    response_object = RecommendationUserEventResponse(event_id=event_id, user_id=user_id)

    return {'STATUS': 'SUCCESS',
            'CONTENT': response_object}


def unlike_event(data):
    data = data.__dict__
    user_id = data['user_id']
    event_id = data['event_id']
    logger.info("UNLIKE EVENT")
    neo4j_client = call_neo4j_client()
    neo4j_client.unfollow_event(user_id=user_id, event_id=event_id)

    response_object = RecommendationUserEventResponse(event_id=event_id, user_id=user_id)

    return {'STATUS': 'SUCCESS',
            'CONTENT': response_object}


def get_user_recommendation(user_id):
    logger.info("GENERATE RECOMMENDATION OF USER")
    neo4j_client = call_neo4j_client()
    recommendations = neo4j_client.get_recommendation(user_id=user_id)
    logger.info(f"USER ID: {user_id}")
    logger.info(f"EVENT IDS: {recommendations}")

    response_object = RecommendationItemResponse(item_list=recommendations)

    return {'STATUS': 'SUCCESS',
            'CONTENT': recommendations}
