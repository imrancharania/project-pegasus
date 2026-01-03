from langchain_core.tools import BaseTool

from langchain.messages import SystemMessage
from langchain.agents import create_agent

from libs.core.agent import Agent
from libs.core.stores.base import BaseStore
from libs.core.registry import LLM_PROVIDERS, STORE_PROVIDERS
from libs.core.settings import PegasusSettings


def create_store(settings: PegasusSettings) -> BaseStore:
    provider = settings.store.provider

    if provider not in STORE_PROVIDERS:
        raise ValueError(f"Unknown store provider: {provider}")

    return STORE_PROVIDERS[provider](settings.store)


def create_llm(settings: PegasusSettings):
    provider = settings.agent.llm.provider
    if provider not in LLM_PROVIDERS:
        raise ValueError(f"Unknown LLM provider: {provider}")

    return LLM_PROVIDERS[provider](settings.agent.llm)


def create_agent_graph(settings: PegasusSettings, tools: list[BaseTool]):
    return Agent(create_agent(
        model=create_llm(settings=settings),
        tools=tools,
        system_prompt=SystemMessage(
            content=[{"type": "text", "text": settings.agent.prompt}]
        ),
    ))
