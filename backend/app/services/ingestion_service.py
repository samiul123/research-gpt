from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.ingestion import IngestionPipeline
from app.services.pinecone_service import pinecone_service
from app.services.embedding_service import embedding_service


embedding_model = embedding_service.get_embedding_model()
# Define the ingestion pipeline
pipeline = IngestionPipeline(
    transformations=[
        SemanticSplitterNodeParser(buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embedding_model),
        embedding_model,
    ],
    vector_store=pinecone_service.vector_store,
)
