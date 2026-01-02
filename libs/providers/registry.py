from typing import Callable, Dict

STORE_PROVIDERS: Dict[str, Callable] = {}
EMBEDDING_PROVIDERS: Dict[str, Callable] = {}
LLM_PROVIDERS: Dict[str, Callable] = {}


def register_store(name: str):
    def decorator(factory: Callable):
        STORE_PROVIDERS[name] = factory
        return factory

    return decorator


def register_embedding(name: str):
    def decorator(factory: Callable):
        EMBEDDING_PROVIDERS[name] = factory
        return factory

    return decorator


def register_llm(name: str):
    def decorator(factory: Callable):
        LLM_PROVIDERS[name] = factory
        return factory

    return decorator
