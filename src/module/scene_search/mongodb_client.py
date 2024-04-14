import time

from PIL import Image
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sentence_transformers import SentenceTransformer
from tenacity import retry, stop_after_attempt, stop_after_delay, wait_fixed

from src.config.constant import geminiAiCFG, mongodbCFG
from src.module.gemini.gemini_client import GeminiAI
from src.module.gemini.prompts import PROMPT_PREPROCESS_QUERY
from src.module.scene_search.keyframe_extraction import KeyframeExtractionModule


class MongoDBClient:
    def __init__(self, video_id=None, video_path=None, weight_path=None):
        self.mongo_name = mongodbCFG.MONGODB_NAME
        self.collection_name = mongodbCFG.MONGODB_COLLECTION_NAME
        self.embedding_model = SentenceTransformer(mongodbCFG.CLIP_MODEL_NAME)
        self.username = mongodbCFG.USERNAME
        self.password = mongodbCFG.PASSWORD
        self.video_id = video_id
        self.keyframe_extraction = KeyframeExtractionModule(weight_path=weight_path, video_path=video_path)
        self.client = self.connect_db()
        self.mongo_collection = self.client[self.mongo_name][self.collection_name]
    
    def connect_db(self):
        uri = f"mongodb+srv://{self.username}:{self.password}@test-cluster.6mmbsir.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            # print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        return client

    def reset_db(self):
        self.mongo_collection.delete_many({})

    def insert_records(self, records):
        self.mongo_collection.insert_many(records)

    def embed_images(self, keyframes, frame_pos, fps):
        records = []

        for i in range(len(keyframes)):
            keyframe = keyframes[i]
            position = frame_pos[i]
            image_emb = self.embedding_model.encode(Image.fromarray(keyframe))
            record = {
                'time_frame': time.strftime('%H:%M:%S', time.gmtime(int(position / fps))),
                'video_id': self.video_id,
                'embedding': image_emb.tolist()
            }
            records.append(record)
        return records

    def process_video(self):
        keyframes, frame_pos, video_fps = self.keyframe_extraction.extract_keyframe() 
        # print(keyframes)
        # print(frame_pos)

        records = self.embed_images(keyframes, frame_pos, video_fps)
        self.insert_records(records)

    @retry(stop=(stop_after_delay(30) | stop_after_attempt(3)), wait=wait_fixed(1))
    def call_model_gen_content(self, prompt):
        gemini_client = GeminiAI(
            API_KEY=geminiAiCFG.API_KEY,
            API_MODEL=geminiAiCFG.API_MODEL
        )
        generated_content = gemini_client.generate_content_json(prompt)
        return generated_content

    def preprocess_query(self, query):
        formatted_prompt = PROMPT_PREPROCESS_QUERY.format(query=query)
        generated_content = self.call_model_gen_content(formatted_prompt)
        return generated_content
    
    def vector_search(self, query, record_num = 100, limit_num = 10):
        processed_query = self.preprocess_query(query)['query']
        # processed_query = query
        # print(query, processed_query)
        query_emb = self.embedding_model.encode(processed_query).tolist()
        pipeline = [{
        "$vectorSearch": {
                "index":"vector_index",
                "path": "embedding",
                "queryVector": query_emb,
                "numCandidates": record_num,
                "limit": limit_num,
                "filter": {
                "video_id": { "$eq": self.video_id}
                }
            }
        },{
            "$project": {
                "embedding": 0,
                "_id": 0,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }]

        results = list(self.mongo_collection.aggregate(pipeline))
        return results