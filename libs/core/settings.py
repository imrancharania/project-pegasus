from pydantic import BaseModel
from typing import Optional


class MongoDBSettings(BaseModel):
    uri: str | None = None
    database: str
    collection: str
    vector_index: str | None = None
    search_index: str | None = None


class EmbeddingSettings(BaseModel):
    provider: str
    model: Optional[str] = None
    api_key: Optional[str] = None


class StoreSettings(BaseModel):
    provider: str
    mongodb: Optional[MongoDBSettings] = None
    embeddings: Optional[EmbeddingSettings] = None


class LLMSettings(BaseModel):
    provider: str
    api_key: Optional[str] = None


class AgentSettings(BaseModel):
    llm: LLMSettings
    prompt: str
    max_iterations: int = 5


class PegasusSettings(BaseModel):
    store: StoreSettings
    agent: AgentSettings
