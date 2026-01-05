from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Optional

from libs.core.factory import create_http_client
from libs.core.settings import PegasusSettings

API_VERSION = "2025-09-29"
USER_AGENT = "Pegasus-User"


class BaseService(ABC):
    def __init__(self, settings: PegasusSettings) -> None:
        self._http = create_http_client(settings)
        
    @abstractmethod
    async def _handle_request(self, coro):
        pass

    def _now_rfc3339(self) -> str:
        return (
            datetime.now(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )

    def _new_idempotency_key(self) -> str:
        from uuid import uuid4

        return str(uuid4())

    def _headers(
        self,
        *,
        idempotency_key: Optional[str] = None,
        request_id: Optional[str] = None,
        signature: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> dict[str, str]:
        """
        Build standard headers for Checkout API requests.
        Authorization is handled automatically by the HTTP client.
        """
        headers = {
            "API-Version": API_VERSION,
            "Content-Type": "application/json",
            "Accept-Language": "en-US",
            "User-Agent": USER_AGENT,
        }

        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        if request_id:
            headers["Request-Id"] = request_id
        if signature:
            headers["Signature"] = signature
        if timestamp:
            headers["Timestamp"] = timestamp

        return headers
