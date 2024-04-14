from src.module.scene_search.mongodb_client import MongoDBClient
from src.models.scene_search_model import SearchResultResponseModel, SearchResultModel, VideoResponseModel

def call_mongodb_client(video_id=None, video_path=None):
    weight_path = 'src/module/scene_search/weight/superpoint.pth'
    mongodb_client = MongoDBClient(video_id=video_id,
                            video_path=video_path,
                            weight_path=weight_path)
    return mongodb_client

def insert_video(data):
    data = data.__dict__
    video_id = data['video_id']
    video_path = data['video_path']
    # print(video_id, video_path)
    client = call_mongodb_client(video_id=video_id, video_path=video_path)
    client.process_video()

    response_object = VideoResponseModel(video_id=video_id)

    return {'STATUS': 'SUCCESS',
            'CONTENT': response_object}

def search_by_text(data):
    data = data.__dict__
    video_id = data['video_id']
    query = data['query']

    client = call_mongodb_client(video_id=str(video_id))
    result = client.vector_search(query)

    # for time_frame, video_id, score in result:
    #     print(time_frame, video_id, score)
    
    result_list = [SearchResultModel(time_frame=item['time_frame'], 
                                     video_id=item['video_id'], 
                                     score=item['score']) for item in result]
    # print(result_list)
    response_object = SearchResultResponseModel(result_list=result_list)

    return {'STATUS': 'SUCCESS',
            'CONTENT': response_object}

def delete_all():
    client = call_mongodb_client()
    client.reset_db()
    return {'STATUS': 'SUCCESS',
            'CONTENT': None}