import certifi

from langchain_core.documents import Document

from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_mongodb.retrievers import MongoDBAtlasHybridSearchRetriever

from pymongo import MongoClient
from pymongo.collection import Collection

from libs.core.stores.base import BaseStore
from libs.core.registry import EMBEDDING_PROVIDERS, register_store
from libs.core.settings import StoreSettings


class MongoDBStore(BaseStore):
    def __init__(
        self,
        collection: Collection,
        vector_store: MongoDBAtlasVectorSearch = None,
        search_index_name: str | None = None,
    ):
        self.collection = collection
        self.vector_store = vector_store
        self.hybrid_retriever = (
            MongoDBAtlasHybridSearchRetriever(
                vectorstore=vector_store, search_index_name=search_index_name
            )
            if vector_store and search_index_name
            else None
        )

    def get(self, key: str):
        return self.collection.find_one({"_id": key})

    def put(self, document: Document):
        if not self.vector_store:
            raise RuntimeError("No vector store configured")
        self.vector_store.add_documents(documents=[document])

    def delete(self, key: str):
        self.collection.delete_one({"_id": key})

    def query(self, filters: dict, limit=20, offset=0):
        cursor = self.collection.find(filters).skip(offset).limit(limit)
        return list(cursor)

    def upsert_text(self, id: str, text: str, metadata: dict | None = None):
        if not self.vector_store:
            raise RuntimeError("No vector store configured")
        self.vector_store.add_texts([text], metadatas=[metadata or {}], ids=[id])

    def similarity_search(self, query: str, k: int = 5):
        if not self.vector_store:
            raise RuntimeError("Similarity search requires a vector store")
        return self.vector_store.similarity_search(query, k=k)

    def hybrid_search(self, query: str):
        if not self.hybrid_retriever:
            raise RuntimeError("Hybrid search requires a vector store")
        return self.hybrid_retriever.invoke(input=query)


@register_store("mongodb")
def create_mongo_store(settings: StoreSettings):
    client = MongoClient(settings.mongodb.uri, tlsCAFile=certifi.where())
    collection = client[settings.mongodb.database][settings.mongodb.collection]

    vector_store = None
    if settings.embeddings:
        embeddings_factory = EMBEDDING_PROVIDERS[settings.embeddings.provider]
        embeddings = embeddings_factory(settings.embeddings)

        vector_store = MongoDBAtlasVectorSearch(
            collection=collection,
            embedding=embeddings,
            index_name=settings.mongodb.vector_index,
        )

    return MongoDBStore(
        collection=collection,
        vector_store=vector_store,
        search_index_name=settings.mongodb.search_index
    )
