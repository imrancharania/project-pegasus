from libs.providers.registry import LLM_PROVIDERS, STORE_PROVIDERS
from libs.providers.settings import HagridSettings


def create_store(settings: HagridSettings):
    provider = settings.store.provider

    if provider not in STORE_PROVIDERS:
        raise ValueError(f"Unknown store provider: {provider}")

    return STORE_PROVIDERS[provider](settings.store)

def create_llm(settings: HagridSettings):
    provider = settings.llm.provider
    if provider not in LLM_PROVIDERS:
        raise ValueError(f"Unknown LLM provider: {provider}")
    
    return LLM_PROVIDERS[provider](settings.llm)