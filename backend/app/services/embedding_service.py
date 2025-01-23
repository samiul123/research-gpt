from app.config import Config

# TODO: Incorporate factory pattern
class EmbeddingService:
    def __init__(self):
        self.openai_api_key = Config.OPENAI_API_KEY
        self.model = None

    def get_embedding_model(self): 
        from llama_index.embeddings.openai import OpenAIEmbedding
        if self.model is None:
            self.model = OpenAIEmbedding(api_key=self.openai_api_key)
        return self.model
    

embedding_service = EmbeddingService()