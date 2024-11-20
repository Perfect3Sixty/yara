# services/qdrant.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, CollectionStatus
from qdrant_client.http.exceptions import UnexpectedResponse
from core.config import QDRANT_HOST, QDRANT_PORT
import time

def get_qdrant_client():
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def init_collection(collection_name: str, vector_size: int = 1536, max_retries: int = 3):
    """Initialize a Qdrant collection with retry logic"""
    client = get_qdrant_client()
    
    for attempt in range(max_retries):
        try:
            # Check if collection exists
            collections = client.get_collections()
            exists = any(col.name == collection_name for col in collections.collections)
            
            if exists:
                # Get collection info to check status
                collection_info = client.get_collection(collection_name)
                if collection_info.status == CollectionStatus.GREEN:
                    print(f"Collection {collection_name} already exists and is healthy")
                    return client
                else:
                    print(f"Collection {collection_name} exists but status is {collection_info.status}")
            
            # Create or recreate collection
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            
            # Wait for collection to be ready
            for _ in range(5):  # Check status up to 5 times
                collection_info = client.get_collection(collection_name)
                if collection_info.status == CollectionStatus.GREEN:
                    print(f"Collection {collection_name} successfully initialized")
                    return client
                time.sleep(1)  # Wait before checking again
                
            raise Exception(f"Collection {collection_name} not ready after initialization")
            
        except UnexpectedResponse as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise Exception(f"Failed to initialize collection after {max_retries} attempts: {str(e)}")
            
        except Exception as e:
            raise Exception(f"Error initializing collection: {str(e)}")
    
    return client