import os
from dotenv import load_dotenv
load_dotenv()


class GeminiAiCFG:
    API_KEY = os.environ["GEMINI_API_KEY"]
    API_MODEL = os.getenv("GEMINI_API_MODEL", "gemini-pro")
    API_EMBEDDING_MODEL = os.getenv("GEMINI_API_EMBEDDING_MODEL", "models/embedding-001")


class Neo4jCFG:
    URL = os.environ["NEO4J_URL"]
    USERNAME = os.environ["NEO4J_USERNAME"]
    PASSWORD = os.environ["NEO4J_PASSWORD"]


class MongodbCFG:
    MONGODB_USERNAME = os.environ["MONGODB_USERNAME"]
    MONGODB_PASSWORD = os.environ["MONGODB_PASSWORD"]
    MONGODB_HOST = os.environ["MONGODB_HOST"]
    MONGODB_NAME = os.environ["MONGODB_NAME"]
    MONGODB_COLLECTION_NAME_RELATED_EVENT = os.environ["MONGODB_COLLECTION_NAME_RELATED_EVENT"]
    MONGODB_INDEX_NAME_RELATED_EVENT = os.environ["MONGODB_INDEX_NAME_RELATED_EVENT"]
