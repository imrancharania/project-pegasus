from __future__ import annotations

from orders.schemas import (
    WebhookEvent,
    WebhookAcceptedResponse,
    Error,
    OrderSocketMessage,
)
from pydantic import ValidationError


# ---------------------------------------------------------------------
# OrderService
# ---------------------------------------------------------------------
class OrderService:
    """
    Routes order lifecycle events from the webhook interface
    to connected websocket clients.

    Uses:
    - WebhookEvent -> OrderSocketMessage
    - Returns WebhookAcceptedResponse
    - Returns Error on failure
    """

    def __init__(
        self,
        *,
        webhook_verifier,
        websocket_hub,
    ) -> None:
        self._verify_webhook = webhook_verifier
        self._sockets = websocket_hub

    # ------------------------------------------------------------------
    # Webhook ingress
    # ------------------------------------------------------------------
    def handle_webhook(
        self,
        *,
        raw_body: bytes,
        headers: dict[str, str],
    ) -> WebhookAcceptedResponse | Error:
        """
        Receives a raw webhook payload, verifies it, converts to socket
        messages, and broadcasts to the relevant channel.
        """

        # 1. Verify signature / authenticity
        try:
            self._verify_webhook(raw_body, headers)
        except Exception as exc:
            return Error(
                type="invalid_request",
                code="invalid_signature",
                message=str(exc),
                param=None,
            )

        # 2. Parse webhook event
        try:
            event = WebhookEvent.model_validate_json(raw_body)
        except ValidationError as ve:
            return Error(
                type="invalid_request",
                code="invalid_payload",
                message=str(ve),
                param=None,
            )

        # 3. Transform to websocket message
        socket_message = OrderSocketMessage(
            type="order.created" if event.type == "order_create" else "order.updated",
            data=event.data,
        )

        # 4. Broadcast to websocket(s)
        self._sockets.broadcast(
            channel=self._channel_for(event),
            message=socket_message.model_dump(mode="json"),
        )

        # 5. Return acknowledgement
        return WebhookAcceptedResponse(
            received=True,
            request_id=headers.get("Request-Id"),
        )

    # ------------------------------------------------------------------
    # Routing helper
    # ------------------------------------------------------------------
    def _channel_for(self, event: WebhookEvent) -> str:
        """
        Minimal channel routing:
        each checkout session has its own websocket channel.
        """
        return f"checkout_session:{event.data.checkout_session_id}"
