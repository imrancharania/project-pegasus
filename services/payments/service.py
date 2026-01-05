from __future__ import annotations
from typing import Optional

import httpx

from payments.schemas import DelegatePaymentRequest, DelegatePaymentResponse, Error
from services.base import BaseService

API_VERSION = "2025-09-29"
DELEGATE_PAYMENT_PATH = "/agentic_commerce/delegate_payment"


class PaymentsService(BaseService):
    """
    Async client for the Delegate Payment API.

    Responsibilities:
    - Send payment delegation requests to merchant APIs
    """

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

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
        except httpx.HTTPStatusError as exc:
            try:
                err_json = exc.response.json()
                err = Error.model_validate(err_json)
            except Exception:
                # Fallback if the response is not a valid Error
                raise RuntimeError(f"Payments API request failed: {exc}") from exc
            raise RuntimeError(
                f"Payments API Error: {err.type} / {err.code} / {err.message}"
            ) from exc

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
