from io import BytesIO
import pip
from utils import PyMuPDFReader_v2
from flask import Flask, Response, request, jsonify, stream_with_context
import sys
import logging
root = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
root.addHandler(handler)

from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


import time
from pinecone.grpc import PineconeGRPC
from pinecone import ServerlessSpec

from llama_index.vector_stores.pinecone import PineconeVectorStore
# Initialize connection to Pinecone
pc = PineconeGRPC(api_key=PINECONE_API_KEY)
index_name = "research-gpt"

# Create your index (can skip this step if your index already exists)

if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)

pc.create_index(
    index_name,
    dimension=1536,
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)

while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)

# Initialize your index 
pinecone_index = pc.Index(index_name)

# Initialize VectorStore
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)


from llama_index.core.node_parser import SemanticSplitterNodeParser, TextSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.ingestion import IngestionPipeline

# This will be the model we use both for Node parsing and for vectorization
embed_model = OpenAIEmbedding(api_key=OPENAI_API_KEY)

# Define the initial pipeline
pipeline = IngestionPipeline(
    transformations=[
        SemanticSplitterNodeParser(buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model),
        embed_model,
        ],
        vector_store=vector_store,
    )

from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever

vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=5)

from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import get_response_synthesizer
synth = get_response_synthesizer(streaming=True)
query_engine = RetrieverQueryEngine(retriever=retriever, response_synthesizer=synth)


app = Flask(__name__)
CORS(app)
# handler = logging.StreamHandler()
# app.logger.addHandler(handler)

@app.route("/query", methods=["POST"])
def query():
    query = request.form.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    # Handle file if provided
    file = request.files.get('file')
    if file:
        try:
            if not file.filename.endswith('.pdf'):
                return jsonify({"error": "Only PDF files are supported"}), 400
            
            file_stream = BytesIO(file.read())
            loader = PyMuPDFReader_v2()
            documents = loader.load_data(stream=file_stream)
            app.logger.debug(f"Loaded {len(documents)} documents from file")
            pipeline.run(documents=documents)
            
            while pinecone_index.describe_index_stats().total_vector_count == 0:
                time.sleep(1)
                
        except Exception as e:
            return jsonify({"error": f"Failed to process file: {str(e)}"}), 500
    
    # Query the engine
    try:
        llm_response = query_engine.query(query)
        # print(llm_response.print_response_stream())
        def generate():
            for chunk in llm_response.response_gen:
                yield chunk
                
        return Response(stream_with_context(generate()))
        # return jsonify({"response": "success"})
    
    except Exception as e:
        return jsonify({"error": f"Query failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
        
        
        
        
        

        

