from langchain_cohere import CohereEmbeddings

from libs.core.registry import register_embedding
from libs.core.settings import EmbeddingSettings


@register_embedding("cohere")
def create_cohere_embeddings(settings: EmbeddingSettings):
    return CohereEmbeddings(
        model=settings.model or "embed-english-v3.0",
        cohere_api_key=settings.api_key,
    )
