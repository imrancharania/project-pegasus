from langchain_cohere import ChatCohere
from libs.core.registry import register_llm
from libs.core.settings import LLMSettings

@register_llm("cohere")
def create_cohere_llm(settings: LLMSettings):
    return ChatCohere(cohere_api_key=settings.api_key)