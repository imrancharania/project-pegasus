from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel, Field, ConfigDict


class Refund(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["store_credit", "original_payment"]
    amount: int


class EventDataOrder(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["order"]
    checkout_session_id: str
    permalink_url: str
    status: Literal[
        "created",
        "manual_review",
        "confirmed",
        "canceled",
        "shipped",
        "fulfilled",
    ]
    refunds: List[Refund]


class WebhookEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["order_create", "order_update"]
    data: EventDataOrder


class WebhookAcceptedResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    received: bool
    request_id: Optional[str] = None


class Error(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal[
        "invalid_request",
        "processing_error",
        "service_unavailable",
    ]
    code: str
    message: str
    param: Optional[str] = None


class OrderSocketMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["order.created", "order.updated"]
    data: EventDataOrder
