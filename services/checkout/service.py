from __future__ import annotations

from typing import Optional

import httpx
from checkout.schemas import (
    CheckoutSession,
    CheckoutSessionWithOrder,
    CheckoutSessionCreateRequest,
    CheckoutSessionUpdateRequest,
    CheckoutSessionCompleteRequest,
    Error,
)

from services.base import BaseService

API_VERSION = "2025-09-29"
CHECKOUT_BASE_PATH = "/agentic_checkout/sessions"


class CheckoutService(BaseService):
    """
    Async client for the Agentic Checkout API.

    Responsibilities:
    - Create checkout sessions
    - Mutate checkout state
    - Complete checkout with delegated payment
    """

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

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
            "User-Agent": "Pegasus-User",
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

    async def _handle_request(self, coro):
        """
        Centralized HTTP error handling.
        Converts httpx.HTTPStatusError responses into `Error` schema.
        """
        try:
            return await coro
        except httpx.HTTPStatusError as exc:
            try:
                err_json = exc.response.json()
                err = Error.model_validate(err_json)
            except Exception:
                # Fallback if the response is not a valid Error
                raise RuntimeError(f"Checkout API request failed: {exc}") from exc
            raise RuntimeError(
                f"Checkout API Error: {err.type} / {err.code} / {err.message}"
            ) from exc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def create_session(
        self,
        request: CheckoutSessionCreateRequest,
        *,
        idempotency_key: Optional[str] = None,
        request_id: Optional[str] = None,
        signature: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> CheckoutSession:
        """POST /agentic_checkout/sessions"""
        response = await self._handle_request(
            self._http.post(
                path=CHECKOUT_BASE_PATH,
                json=request.model_dump(mode="json"),
                headers=self._headers(
                    idempotency_key=idempotency_key or self._new_idempotency_key(),
                    request_id=request_id,
                    signature=signature,
                    timestamp=timestamp or self._now_rfc3339(),
                ),
            )
        )
        return CheckoutSession.model_validate(response)

    async def get_session(
        self,
        checkout_session_id: str,
        *,
        request_id: Optional[str] = None,
    ) -> CheckoutSession:
        """GET /agentic_checkout/sessions/{id}"""
        response = await self._handle_request(
            self._http.get(
                path=f"{CHECKOUT_BASE_PATH}/{checkout_session_id}",
                headers=self._headers(
                    idempotency_key=None,
                    request_id=request_id,
                    signature=None,
                    timestamp=None,
                ),
            )
        )
        return CheckoutSession.model_validate(response)

    async def update_session(
        self,
        checkout_session_id: str,
        request: CheckoutSessionUpdateRequest,
        *,
        idempotency_key: Optional[str] = None,
        request_id: Optional[str] = None,
        signature: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> CheckoutSession:
        """PATCH /agentic_checkout/sessions/{id}"""
        response = await self._handle_request(
            self._http.patch(
                path=f"{CHECKOUT_BASE_PATH}/{checkout_session_id}",
                json=request.model_dump(mode="json", exclude_unset=True),
                headers=self._headers(
                    idempotency_key=idempotency_key or self._new_idempotency_key(),
                    request_id=request_id,
                    signature=signature,
                    timestamp=timestamp or self._now_rfc3339(),
                ),
            )
        )
        return CheckoutSession.model_validate(response)

    async def complete_session(
        self,
        checkout_session_id: str,
        request: CheckoutSessionCompleteRequest,
        *,
        idempotency_key: Optional[str] = None,
        request_id: Optional[str] = None,
        signature: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> CheckoutSessionWithOrder:
        """POST /agentic_checkout/sessions/{id}/complete"""
        response = await self._handle_request(
            self._http.post(
                path=f"{CHECKOUT_BASE_PATH}/{checkout_session_id}/complete",
                json=request.model_dump(mode="json"),
                headers=self._headers(
                    idempotency_key=idempotency_key or self._new_idempotency_key(),
                    request_id=request_id,
                    signature=signature,
                    timestamp=timestamp or self._now_rfc3339(),
                ),
            )
        )
        return CheckoutSessionWithOrder.model_validate(response)
