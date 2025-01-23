from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import get_response_synthesizer
from app.services.pinecone_service import pinecone_service

# Initialize vector store index
vector_index = VectorStoreIndex.from_vector_store(vector_store=pinecone_service.vector_store)

# Create retriever and query engine
retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=5)
synth = get_response_synthesizer(streaming=True)
query_engine = RetrieverQueryEngine(retriever=retriever, response_synthesizer=synth)