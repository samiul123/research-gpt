from flask import Blueprint, request, jsonify, Response, stream_with_context
from io import BytesIO
from app.services.ingestion_service import pipeline
from app.services.query_service import query_engine
from app.services.pinecone_service import pinecone_service
from utils import PyMuPDFReader_v2
import time

query_bp = Blueprint("query", __name__)

@query_bp.route("/", methods=["POST"])
def query():
    query_text = request.form.get("query")
    if not query_text:
        return jsonify({"error": "Query is required"}), 400

    # Handle file upload
    file = request.files.get("file")
    if file:
        try:
            if not file.filename.endswith(".pdf"):
                return jsonify({"error": "Only PDF files are supported"}), 400

            file_stream = BytesIO(file.read())
            loader = PyMuPDFReader_v2()
            documents = loader.load_data(stream=file_stream)
            pipeline.run(documents=documents)

            while not pinecone_service.pinecone_index.describe_index_stats().total_vector_count:
                time.sleep(1)
        except Exception as e:
            return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

    # Query the engine
    try:
        llm_response = query_engine.query(query_text)
        
        def generate():
            for chunk in llm_response.response_gen:
                yield chunk

        return Response(stream_with_context(generate()))
    except Exception as e:
        return jsonify({"error": f"Query failed: {str(e)}"}), 500
