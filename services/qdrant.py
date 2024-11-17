from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from core.config import QDRANT_HOST, QDRANT_PORT

def get_qdrant_client():
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def init_collection(collection_name: str, vector_size: int = 768):
    client = get_qdrant_client()
    
    # Create collection if it doesn't exist
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    
    return client