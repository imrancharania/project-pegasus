from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict, Literal

from pydantic import BaseModel, Field, ConfigDict


class Address(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., max_length=256)
    line_one: str = Field(..., max_length=60)
    line_two: Optional[str] = Field(None, max_length=60)
    city: str = Field(..., max_length=60)
    state: str
    country: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="ISO-3166-1 alpha-2",
    )
    postal_code: str = Field(..., max_length=20)


class PaymentMethodCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["card"]
    card_number_type: Literal["fpan", "network_token"]
    number: str

    exp_month: Optional[str] = Field(None, max_length=2)
    exp_year: Optional[str] = Field(None, max_length=4)
    name: Optional[str] = None
    cvc: Optional[str] = Field(None, max_length=4)

    cryptogram: Optional[str] = None
    eci_value: Optional[str] = Field(None, max_length=2)

    checks_performed: Optional[List[Literal["avs", "cvv", "ani", "auth0"]]] = None

    iin: Optional[str] = Field(None, max_length=6)

    display_card_funding_type: Literal["credit", "debit", "prepaid"]
    display_wallet_type: Optional[str] = None
    display_brand: Optional[str] = None
    display_last4: Optional[str] = Field(None, max_length=4)

    metadata: Dict[str, str]


class Allowance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: Literal["one_time"]
    max_amount: int = Field(
        ...,
        description="Minor units (e.g., $20 → 2000)",
    )
    currency: str = Field(
        ...,
        pattern="^[a-z]{3}$",
        description="ISO-4217 lowercase (e.g., usd)",
    )
    checkout_session_id: str
    merchant_id: str = Field(..., max_length=256)
    expires_at: datetime


class RiskSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["card_testing"]
    score: int
    action: Literal["blocked", "manual_review", "authorized"]


class DelegatePaymentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payment_method: PaymentMethodCard
    allowance: Allowance
    billing_address: Optional[Address] = None
    risk_signals: List[RiskSignal] = Field(..., min_length=1)
    metadata: Dict[str, str]


class DelegatePaymentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(
        ...,
        description="Unique vault token identifier (vt_...)",
    )
    created: datetime
    metadata: Dict[str, str]


class Error(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal[
        "invalid_request",
        "rate_limit_exceeded",
        "processing_error",
        "service_unavailable",
    ]
    code: Literal[
        "invalid_card",
        "duplicate_request",
        "idempotency_conflict",
    ]
    message: str
    param: Optional[str] = Field(
        None,
        description="JSONPath of offending field",
    )
