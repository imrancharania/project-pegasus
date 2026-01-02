from abc import ABC, abstractmethod
from typing import Iterable
from langchain_core.documents import Document


class BaseStore(ABC):
    """Base interface for all stores."""

    @abstractmethod
    async def get(self, key: str) -> dict | None:
        pass

    @abstractmethod
    async def put(self, document: Document) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def query(
        self, filters: dict, limit: int = 20, offset: int = 0
    ) -> Iterable[dict]:
        pass

    @abstractmethod
    async def upsert_text(
        self, id: str, text: str, metadata: dict | None = None
    ) -> None:
        pass

    @abstractmethod
    async def similarity_search(self, query: str, k: int = 5) -> Iterable[dict]:
        pass

    @abstractmethod
    async def hybrid_search(self, query: str) -> Iterable[dict]:
        pass
