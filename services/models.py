from langchain_core.documents import Document
from typing import List, Optional, Annotated
from datetime import date
from pydantic import (
    BaseModel,
    field,
    HttpUrl,
    constr,
    conint,
    confloat,
    ConfigDict,
    field_validator,
    model_validator,
)
from enum import Enum


# -----------------------------
# Enums
# -----------------------------


class BooleanEnum(str, Enum):
    true = "true"
    false = "false"


class ConditionEnum(str, Enum):
    new = "new"
    refurbished = "refurbished"
    used = "used"


class AgeGroupEnum(str, Enum):
    newborn = "newborn"
    infant = "infant"
    toddler = "toddler"
    kids = "kids"
    adult = "adult"


class AvailabilityEnum(str, Enum):
    in_stock = "in_stock"
    out_of_stock = "out_of_stock"
    preorder = "preorder"


class PickupMethodEnum(str, Enum):
    in_store = "in_store"
    reserve = "reserve"
    not_supported = "not_supported"


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    unisex = "unisex"


class RelationshipTypeEnum(str, Enum):
    part_of_set = "part_of_set"
    required_part = "required_part"
    often_bought_with = "often_bought_with"
    substitute = "substitute"
    different_brand = "different_brand"
    accessory = "accessory"


# -----------------------------
# Flattened ProductFeedItem
# -----------------------------


class Product(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # -----------------------------
    # OpenAI Flags
    # -----------------------------
    enable_search: BooleanEnum = field()
    enable_checkout: BooleanEnum = field()

    # -----------------------------
    # Basic Product Data
    # -----------------------------
    id: Annotated[str, constr(max_length=100)] = field()
    gtin: Optional[Annotated[str, constr(regex=r"^\d{8,14}$")]] = field(default=None)
    mpn: Optional[Annotated[str, constr(max_length=70)]] = field(default=None)
    title: Annotated[str, constr(max_length=150)] = field()
    description: Annotated[str, constr(max_length=5000)] = field()
    link: HttpUrl = field()

    # -----------------------------
    # Item Information
    # -----------------------------
    condition: Optional[ConditionEnum] = field(default=ConditionEnum.new)
    product_category: str = field()
    brand: Annotated[str, constr(max_length=70)] = field()
    material: Annotated[str, constr(max_length=100)] = field()
    dimensions: Optional[str] = field(default=None)
    length: Optional[str] = field(default=None)
    width: Optional[str] = field(default=None)
    height: Optional[str] = field(default=None)
    weight: str = field()
    age_group: Optional[AgeGroupEnum] = field(default=None)

    # -----------------------------
    # Media
    # -----------------------------
    image_link: HttpUrl = field()
    additional_image_link: Optional[List[HttpUrl]] = field(default=None)
    video_link: Optional[HttpUrl] = field(default=None)
    model_3d_link: Optional[HttpUrl] = field(default=None)

    # -----------------------------
    # Price & Promotions
    # -----------------------------
    price: str = field()
    sale_price: Optional[str] = field(default=None)
    sale_price_effective_date: Optional[str] = field(default=None)
    unit_pricing_measure: Optional[str] = field(default=None)
    base_measure: Optional[str] = field(default=None)
    pricing_trend: Optional[Annotated[str, constr(max_length=80)]] = field(default=None)

    # -----------------------------
    # Availability & Inventory
    # -----------------------------
    availability: AvailabilityEnum = field()
    availability_date: Optional[date] = field(default=None)
    inventory_quantity: Annotated[int, conint(ge=0)] = field()
    expiration_date: Optional[date] = field(default=None)
    pickup_method: Optional[PickupMethodEnum] = field(default=None)
    pickup_sla: Optional[str] = field(default=None)

    # -----------------------------
    # Variants
    # -----------------------------
    item_group_id: Optional[Annotated[str, constr(max_length=70)]] = field(default=None)
    item_group_title: Optional[Annotated[str, constr(max_length=150)]] = field(
        default=None
    )
    color: Optional[Annotated[str, constr(max_length=40)]] = field(default=None)
    size: Optional[Annotated[str, constr(max_length=20)]] = field(default=None)
    size_system: Optional[Annotated[str, constr(min_length=2, max_length=2)]] = field(
        default=None
    )
    gender: Optional[GenderEnum] = field(default=None)
    offer_id: Optional[str] = field(default=None)
    custom_variant1_category: Optional[str] = field(default=None)
    custom_variant1_option: Optional[str] = field(default=None)
    custom_variant2_category: Optional[str] = field(default=None)
    custom_variant2_option: Optional[str] = field(default=None)
    custom_variant3_category: Optional[str] = field(default=None)
    custom_variant3_option: Optional[str] = field(default=None)

    # -----------------------------
    # Fulfillment
    # -----------------------------
    shipping: Optional[List[str]] = field(default=None)
    delivery_estimate: Optional[date] = field(default=None)

    # -----------------------------
    # Merchant Info
    # -----------------------------
    seller_name: Annotated[str, constr(max_length=70)] = field()
    seller_url: HttpUrl = field()
    seller_privacy_policy: Optional[HttpUrl] = field(default=None)
    seller_tos: Optional[HttpUrl] = field(default=None)

    # -----------------------------
    # Returns
    # -----------------------------
    return_policy: HttpUrl = field()
    return_window: Annotated[int, conint(gt=0)] = field()

    # -----------------------------
    # Performance Signals
    # -----------------------------
    popularity_score: Optional[Annotated[float, confloat(ge=0, le=5)]] = field(
        default=None
    )
    return_rate: Optional[Annotated[float, confloat(ge=0, le=100)]] = field(
        default=None
    )

    # -----------------------------
    # Compliance
    # -----------------------------
    warning: Optional[str] = field(default=None)
    warning_url: Optional[HttpUrl] = field(default=None)
    age_restriction: Optional[Annotated[int, conint(gt=0)]] = field(default=None)

    # -----------------------------
    # Reviews & Q&A
    # -----------------------------
    product_review_count: Optional[Annotated[int, conint(ge=0)]] = field(default=None)
    product_review_rating: Optional[Annotated[float, confloat(ge=0, le=5)]] = field(
        default=None
    )
    store_review_count: Optional[Annotated[int, conint(ge=0)]] = field(default=None)
    store_review_rating: Optional[Annotated[float, confloat(ge=0, le=5)]] = field(
        default=None
    )
    q_and_a: Optional[str] = field(default=None)
    raw_review_data: Optional[str] = field(default=None)

    # -----------------------------
    # Related Products
    # -----------------------------
    related_product_id: Optional[List[str]] = field(default=None)
    relationship_type: Optional[RelationshipTypeEnum] = field(default=None)

    # -----------------------------
    # Geo Tagging
    # -----------------------------
    geo_price: Optional[str] = field(default=None)
    geo_availability: Optional[str] = field(default=None)

    # -----------------------------
    # Validators
    # -----------------------------
    @model_validator(mode="before")
    def validate_gtin_or_mpn(cls, values):
        if not values.get("gtin") and not values.get("mpn"):
            raise ValueError("Either gtin or mpn must be provided")
        return values

    @field_validator("enable_checkout")
    def validate_checkout_requires_search(cls, v, info):
        if v == BooleanEnum.true and info.data.get("enable_search") != BooleanEnum.true:
            raise ValueError(
                "enable_checkout can only be true if enable_search is true"
            )
        return v

    @model_validator(mode="before")
    def validate_sale_price(cls, values):
        price = values.get("price")
        sale_price = values.get("sale_price")
        if sale_price:
            price_value = float(price.split()[0])
            sale_value = float(sale_price.split()[0])
            if sale_value > price_value:
                raise ValueError("sale_price cannot exceed price")
            if not values.get("sale_price_effective_date"):
                raise ValueError(
                    "sale_price_effective_date required if sale_price is provided"
                )
        return values

    @model_validator(mode="before")
    def validate_availability_date(cls, values):
        if values.get("availability") == AvailabilityEnum.preorder and not values.get(
            "availability_date"
        ):
            raise ValueError("availability_date required when availability is preorder")
        return values


class ProductDocument(Document):
    def __init__(self, product: Product) -> None:
        super().__init__(
            page_content=product.description, metadata=product.model_dump()
        )
