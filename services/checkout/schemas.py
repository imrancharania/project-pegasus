from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Union, Literal

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class Address(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    line_one: str
    line_two: Optional[str] = None
    city: str
    state: str
    country: str
    postal_code: str


class Buyer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None


class Item(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    quantity: int = Field(..., ge=1)


class PaymentProvider(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: Literal["stripe"]
    supported_payment_methods: List[Literal["card"]]


class PaymentData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    token: str
    provider: Literal["stripe"]
    billing_address: Optional[Address] = None


class LineItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    item: Item
    base_amount: int
    discount: int
    subtotal: int
    tax: int
    total: int


class Total(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal[
        "items_base_amount",
        "items_discount",
        "subtotal",
        "discount",
        "fulfillment",
        "tax",
        "fee",
        "total",
    ]
    display_text: str
    amount: int
    description: Optional[str] = None


class FulfillmentOptionShipping(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["shipping"]
    id: str
    title: str
    subtitle: Optional[str] = None
    carrier: Optional[str] = None
    earliest_delivery_time: Optional[datetime] = None
    latest_delivery_time: Optional[datetime] = None
    subtotal: int
    tax: int
    total: int


class FulfillmentOptionDigital(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["digital"]
    id: str
    title: str
    subtitle: Optional[str] = None
    subtotal: int
    tax: int
    total: int


FulfillmentOption = Union[
    FulfillmentOptionShipping,
    FulfillmentOptionDigital,
]


class MessageInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["info"]
    param: Optional[str] = None
    content_type: Literal["plain", "markdown"]
    content: str


class MessageError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["error"]
    code: Literal[
        "missing",
        "invalid",
        "out_of_stock",
        "payment_declined",
        "requires_sign_in",
        "requires_3ds",
    ]
    param: Optional[str] = None
    content_type: Literal["plain", "markdown"]
    content: str


Message = Union[MessageInfo, MessageError]


class Link(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal[
        "terms_of_use",
        "privacy_policy",
        "seller_shop_policies",
    ]
    url: str


class Order(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    checkout_session_id: str
    permalink_url: str


class CheckoutSessionBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    status: Literal[
        "not_ready_for_payment",
        "ready_for_payment",
        "completed",
        "canceled",
        "in_progress",
    ]
    currency: str

    buyer: Optional[Buyer] = None
    payment_provider: Optional[PaymentProvider] = None

    line_items: List[LineItem]
    fulfillment_address: Optional[Address] = None
    fulfillment_options: List[FulfillmentOption]
    fulfillment_option_id: Optional[str] = None

    totals: List[Total]
    messages: List[Message]
    links: List[Link]


class CheckoutSession(CheckoutSessionBase):
    pass


class CheckoutSessionWithOrder(CheckoutSessionBase):
    order: Order


class CheckoutSessionCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    buyer: Optional[Buyer] = None
    items: List[Item] = Field(..., min_length=1)
    fulfillment_address: Optional[Address] = None


class CheckoutSessionUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    buyer: Optional[Buyer] = None
    items: Optional[List[Item]] = None
    fulfillment_address: Optional[Address] = None
    fulfillment_option_id: Optional[str] = None


class CheckoutSessionCompleteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    buyer: Optional[Buyer] = None
    payment_data: PaymentData


class Error(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal[
        "invalid_request",
        "request_not_idempotent",
        "processing_error",
        "service_unavailable",
    ]
    code: str
    message: str
    param: Optional[str] = None
