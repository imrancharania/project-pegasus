# libs/core/merchant_api_client.py
from authlib.integrations.httpx_client import AsyncOAuth2Client
from typing import Optional

from libs.core.settings import MerchantAPISettings


class HttpClient:
    """
    Async HTTP client for merchant APIs with OAuth2 client credentials.
    """

    def __init__(self, settings: MerchantAPISettings):
        # Use Authlib to handle token acquisition and refresh
        self._client = AsyncOAuth2Client(
            client_id=settings.oauth.client_id,
            client_secret=settings.oauth.client_secret,
            token_endpoint=settings.oauth.token_url,
            scope=settings.oauth.scope,
        )
        self._base_url = settings.base_url

    async def get(self, path: str, params: Optional[dict] = None, **kwargs) -> dict:
        resp = await self._client.get(f"{self._base_url}{path}", params=params, **kwargs)
        resp.raise_for_status()
        return resp.json()

    async def post(self, path: str, json: Optional[dict] = None, **kwargs) -> dict:
        resp = await self._client.post(f"{self._base_url}{path}", json=json, **kwargs)
        resp.raise_for_status()
        return resp.json()

    async def patch(self, path: str, json: Optional[dict] = None, **kwargs) -> dict:
        resp = await self._client.patch(f"{self._base_url}{path}", json=json, **kwargs)
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self._client.aclose()
