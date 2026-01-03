from langchain.tools import tool, ToolRuntime

from libs.core.context import AgentContext
from services.models import Product


@tool(response_format="content_and_artifact")
def search_products(input: str, runtime: ToolRuntime[AgentContext]):
    """
    Retrieves a list of products from the products collection by the product description

    Returns:
        A dictionary containing the list of products if found.
    """

    documents = runtime.context.store.hybrid_search(input)

    print(len(documents))

    products = [
        Product.model_validate(document.metadata).model_dump(serialize_as_any=True)
        for idx, document in enumerate(documents)
    ]

    return {"products": products}


tools = [search_products]
