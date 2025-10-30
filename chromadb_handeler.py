# chromadb_handler.py
from chromadb import PersistentClient
from chromadb.utils import embedding_functions

class ChromaDBHandler:
    def __init__(self, persist_dir: str, collection_name: str, model_name: str):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name
        )

        self.client = PersistentClient(path=self.persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function
        )

    def reset_collection(self):
        """Delete and recreate the collection."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function
        )


