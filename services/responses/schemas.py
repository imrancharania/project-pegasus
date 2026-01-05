from typing import List, Optional, Annotated
from datetime import date
from pydantic import BaseModel, field, HttpUrl, constr, conint, confloat

from services.models import (
    AgeGroupEnum,
    AvailabilityEnum,
    BooleanEnum,
    ConditionEnum,
    GenderEnum,
    PickupMethodEnum,
    RelationshipTypeEnum,
)


# -----------------------------
# Variant Model
# -----------------------------
class ProductVariant(BaseModel):
    model_config = {"extra": "forbid"}

    sku: str = field()
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
    price: str = field()
    sale_price: Optional[str] = field(default=None)
    sale_price_effective_date: Optional[str] = field(default=None)
    availability: AvailabilityEnum = field()
    availability_date: Optional[date] = field(default=None)
    inventory_quantity: Annotated[int, conint(ge=0)] = field()
    pickup_method: Optional[PickupMethodEnum] = field(default=None)
    pickup_sla: Optional[str] = field(default=None)
    geo_price: Optional[str] = field(default=None)
    geo_availability: Optional[str] = field(default=None)


# -----------------------------
# Grouped Product Card
# -----------------------------
class ProductCard(BaseModel):
    model_config = {"extra": "forbid"}

    # Basic Product Data
    item_group_id: Optional[Annotated[str, constr(max_length=70)]] = field(default=None)
    item_group_title: Optional[Annotated[str, constr(max_length=150)]] = field(
        default=None
    )
    id: str = field()  # Main SKU for reference
    gtin: Optional[Annotated[str, constr(regex=r"^\d{8,14}$")]] = field(default=None)
    mpn: Optional[Annotated[str, constr(max_length=70)]] = field(default=None)
    title: Annotated[str, constr(max_length=150)] = field()
    description: Annotated[str, constr(max_length=5000)] = field()
    link: HttpUrl = field()

    # Item Information
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

    # Media
    image_link: HttpUrl = field()
    additional_image_link: Optional[List[HttpUrl]] = field(default=None)
    video_link: Optional[HttpUrl] = field(default=None)
    model_3d_link: Optional[HttpUrl] = field(default=None)

    # Fulfillment
    shipping: Optional[List[str]] = field(default=None)
    delivery_estimate: Optional[date] = field(default=None)

    # Merchant Info
    seller_name: Annotated[str, constr(max_length=70)] = field()
    seller_url: HttpUrl = field()
    seller_privacy_policy: Optional[HttpUrl] = field(default=None)
    seller_tos: Optional[HttpUrl] = field(default=None)

    # Returns
    return_policy: HttpUrl = field()
    return_window: Annotated[int, conint(gt=0)] = field()

    # Performance Signals
    popularity_score: Optional[Annotated[float, confloat(ge=0, le=5)]] = field(
        default=None
    )
    return_rate: Optional[Annotated[float, confloat(ge=0, le=100)]] = field(
        default=None
    )

    # Compliance
    warning: Optional[str] = field(default=None)
    warning_url: Optional[HttpUrl] = field(default=None)
    age_restriction: Optional[Annotated[int, conint(gt=0)]] = field(default=None)

    # Reviews & Q&A
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

    # Related Products
    related_product_id: Optional[List[str]] = field(default=None)
    relationship_type: Optional[RelationshipTypeEnum] = field(default=None)

    # OpenAI Flags
    enable_search: BooleanEnum = field()
    enable_checkout: BooleanEnum = field()

    # Variants
    variants: List[ProductVariant] = field(default_factory=list)
