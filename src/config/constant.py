import os

from dotenv import load_dotenv

load_dotenv()

class geminiAiCFG:
    API_KEY = os.environ["GEMINI_API_KEY"]
    API_MODEL = os.getenv("GEMINI_API_MODEL", "gemini-pro")


class neo4jCFG:
    URL = os.environ["NEO4J_URL"]
    USERNAME = os.environ["NEO4J_USERNAME"]
    PASSWORD = os.environ["NEO4J_PASSWORD"]

class mongodbCFG:
    USERNAME = os.environ["MONGODB_USERNAME"]
    PASSWORD = os.environ["MONGODB_PASSWORD"]
    MONGODB_NAME = os.environ["MONGODB_NAME"]
    MONGODB_COLLECTION_NAME = os.environ["MONGODB_COLLECTION_NAME"]
    CLIP_MODEL_NAME = os.environ["CLIP_MODEL_NAME"]

# class cudaCFG:
#     cuda = os.environ["CUDA"]

