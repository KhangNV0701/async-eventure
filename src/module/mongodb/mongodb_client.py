import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.config.constant import MongodbCFG
from src.module.embedding.gemini_embedding import GeminiEmbeddingModel
from src.utils.logger import logger


class MongoDBClient:

    def __init__(
        self, 
        collection_name=MongodbCFG.MONGODB_COLLECTION_NAME_RELATED_EVENT
    ):
        self.client = self.connect_db()
        self.mongo_collection = self.client[MongodbCFG.MONGODB_NAME][collection_name]

    def connect_db(self):
        uri = f"mongodb+srv://{MongodbCFG.MONGODB_USERNAME}:{MongodbCFG.MONGODB_PASSWORD}@{MongodbCFG.MONGODB_HOST}/?retryWrites=true&w=majority"
        logger.info("MONGO URI %s", uri)
        client = MongoClient(uri, server_api=ServerApi("1"))
        try:
            client.admin.command("ping")
            # print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        return client

    def reset_db(self):
        self.mongo_collection.delete_many({})

    def insert_records(self, records):
        self.mongo_collection.insert_many(records)

    def vector_search(self, index_name, query, record_num=100, limit_num=10):
        embedding = GeminiEmbeddingModel()
        query_emb = embedding.get_embedding(query, task_type="retrieval_query")
        query_emb = query_emb.get("embedding")
        pipeline = [
            {
                "$vectorSearch": {
                    "index": index_name,
                    "path": "embedding",
                    "queryVector": query_emb,
                    "numCandidates": record_num,
                    "limit": limit_num,
                }
            },
            {
                "$project": {
                    "embedding": 0,
                    "_id": 0,
                    "score": {"$meta": "vectorSearchScore"},
                }
            },
        ]

        results = list(self.mongo_collection.aggregate(pipeline))
        logger.info(
            "VECTOR SEARCH RESULTS: %s",
            json.dumps(results, indent=4, ensure_ascii=False),
        )

        extracted_results = [event.get("event_id") for event in results]
        return extracted_results
