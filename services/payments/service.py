from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from libs.core.factory import create_http_client
from libs.core.settings import PegasusSettings
from payments.schemas import DelegatePaymentRequest, DelegatePaymentResponse, Error

API_VERSION = "2025-09-29"
DELEGATE_PAYMENT_PATH = "/agentic_commerce/delegate_payment"


class PaymentsService:
    """
    Async client for the Agentic Commerce Protocol — Delegate Payment API.

    Responsibilities:
    - Send payment delegation requests to merchant APIs
    """

    def __init__(self, settings: PegasusSettings) -> None:
        self._http = create_http_client(settings)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _now_rfc3339(self) -> str:
        return (
            datetime.now(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )

    def _new_idempotency_key(self) -> str:
        return str(uuid4())

    def _headers(
        self,
        *,
        idempotency_key: Optional[str] = None,
        signature: Optional[str] = None,
        timestamp: Optional[str] = None,
        request_id: Optional[str] = None,
        accept_language: str = "en-US",
        user_agent: str = "Pegasus-User",
    ) -> dict[str, str]:
        """
        Build protocol headers. OAuth handled by HTTP client automatically.
        """
        headers = {
            "API-Version": API_VERSION,
            "Content-Type": "application/json",
            "Accept-Language": accept_language,
            "User-Agent": user_agent,
        }
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        if signature:
            headers["Signature"] = signature
        if timestamp:
            headers["Timestamp"] = timestamp
        if request_id:
            headers["Request-Id"] = request_id
        return headers

    async def _handle_request(self, coro):
        """
        Centralized HTTP error handling.
        Converts HTTP errors into structured Error schema.
        """
        try:
            return await coro
        except Exception as exc:
            # Try to parse JSON error from merchant API
            if hasattr(exc, "response") and exc.response is not None:
                try:
                    err = Error.model_validate(exc.response.json())
                    raise RuntimeError(
                        f"{err.type} / {err.code} / {err.message}"
                    ) from exc
                except Exception:
                    pass
            raise RuntimeError(f"Payments API request failed: {exc}") from exc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def delegate_payment(
        self,
        request: DelegatePaymentRequest,
        *,
        idempotency_key: Optional[str] = None,
        signature: Optional[str] = None,
        timestamp: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> DelegatePaymentResponse:
        """
        POST /agentic_commerce/delegate_payment
        """
        response = await self._handle_request(
            self._http.post(
                path=DELEGATE_PAYMENT_PATH,
                json=request.model_dump(mode="json"),
                headers=self._headers(
                    idempotency_key=idempotency_key or self._new_idempotency_key(),
                    signature=signature,
                    timestamp=timestamp or self._now_rfc3339(),
                    request_id=request_id,
                ),
            )
        )
        return DelegatePaymentResponse.model_validate(response)
