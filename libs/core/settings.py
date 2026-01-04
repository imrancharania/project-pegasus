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


class OAuthSettings(BaseModel):
    client_id: str
    client_secret: str
    token_url: str
    scope: str


class MerchantAPISettings(BaseModel):
    base_url: str
    timeout: Optional[int] = 10
    oauth: OAuthSettings


class PegasusSettings(BaseModel):
    store: StoreSettings
    agent: AgentSettings
    merchant_api: MerchantAPISettings
