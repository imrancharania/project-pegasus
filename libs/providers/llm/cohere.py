from langchain_cohere import ChatCohere
from libs.providers.registry import register_llm
from libs.providers.settings import LLMSettings

@register_llm("cohere")
def create_cohere_llm(settings: LLMSettings):
    return ChatCohere(cohere_api_key=settings.api_key)