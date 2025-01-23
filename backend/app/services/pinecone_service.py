import time
from pinecone.grpc import PineconeGRPC
from pinecone import ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from app.config import Config

# TODO: Incorporate Factory pattern which vectore store to use
class PineconeService:
    def __init__(self):
        try:
            self.pc = PineconeGRPC(api_key=Config.PINECONE_API_KEY)
            self.index_name = Config.INDEX_NAME

            # Create or reset the index
            self._initialize_index()
            self.pinecone_index = self.pc.Index(self.index_name)

            # Initialize the vector store
            self.vector_store = PineconeVectorStore(pinecone_index=self.pinecone_index)
        except Exception as e:
            print(f"Error initializing Pinecone service: {e}")
            raise e

    def _initialize_index(self):
        try:
            if self.index_name in self.pc.list_indexes().names():
                self.pc.delete_index(self.index_name)

            self.pc.create_index(
                self.index_name,
                dimension=Config.EMBEDDING_DIMENSION,
                spec=ServerlessSpec(cloud=Config.CLOUD, region=Config.PINECONE_ENV),
            )

            while not self.pc.describe_index(self.index_name).status["ready"]:
                time.sleep(1)
        except Exception as e:
            print(f"Error initializing Pinecone index: {e}")
            raise e

pinecone_service = PineconeService()