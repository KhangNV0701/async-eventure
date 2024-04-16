import google.generativeai as genai
from src.config.constant import GeminiAiCFG
from src.utils.logger import logger


class GeminiEmbeddingModel:

    def __init__(self):
        genai.configure(api_key=GeminiAiCFG.API_KEY)
        self.model = GeminiAiCFG.API_EMBEDDING_MODEL

    def get_embedding(self, text: str, task_type, title=""):
        logger.info("TASK TYPE %s", task_type)
        if task_type in "retrieval_query":
            return genai.embed_content(
                model=self.model,
                content=text,
                task_type=task_type,
            )

        embedding = genai.embed_content(
            model=self.model,
            content=text,
            task_type=task_type,
            title=title
        )

        return embedding
