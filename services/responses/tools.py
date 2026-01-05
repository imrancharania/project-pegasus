from collections import defaultdict
import json
from typing import List
from langchain.tools import tool, ToolRuntime

from libs.core.context import AgentContext
from services.models import Product, ProductDocument
from services.responses.schemas import ProductCard, ProductVariant


@tool(response_format="content_and_artifact")
def search_products(input: str, runtime: ToolRuntime[AgentContext]):
    """
    Retrieves a list of products from the products collection by the product description

    Returns:
        A dictionary containing the list of products if found.
    """

    documents = runtime.context.store.hybrid_search(input)

    print(len(documents))

    products = documents_to_grouped_cards(documents)

    return {"products": products}


def documents_to_grouped_cards(docs: List[ProductDocument]) -> str:
    """
    Convert a list of ProductDocument objects into grouped ProductCard objects
    and serialize the result as a JSON string.
    """
    grouped: dict[str, dict] = defaultdict(
        lambda: {"variants": [], "card_fields": None}
    )

    for doc in docs:
        # Convert metadata to typed Product
        product = Product.model_validate(doc.metadata)
        product.description = doc.page_content

        # Determine group ID
        group_id = product.item_group_id or product.id

        # Create variant using Pydantic v2 model_fields
        variant_fields = ProductVariant.model_fields
        variant = ProductVariant(
            **{f: getattr(product, f) for f in variant_fields if hasattr(product, f)}
        )

        grouped[group_id]["variants"].append(variant)

        # Card-level fields (everything not in variant)
        if grouped[group_id]["card_fields"] is None:
            product_dict = product.model_dump()
            for f in variant_fields:
                product_dict.pop(f, None)
            grouped[group_id]["card_fields"] = product_dict

    # Build ProductCard objects
    product_cards = []
    for group_id, data in grouped.items():
        card_data = data["card_fields"]
        card_data["variants"] = data["variants"]
        product_cards.append(ProductCard(**card_data))

    # Serialize the list of ProductCards to JSON
    return json.dumps([card.model_dump() for card in product_cards], indent=2)


tools = [search_products]
