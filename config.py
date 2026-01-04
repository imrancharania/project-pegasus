import os
from pathlib import Path
import yaml

from libs.core.settings import PegasusSettings

from dotenv import load_dotenv

load_dotenv()


def load_settings():
    config_path = Path(__file__).parent / "settings.yaml"
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)

    settings = PegasusSettings.model_validate(config_data)

    embed_api_key = os.environ.get("EMBEDDINGS_MODEL_API_KEY")
    if embed_api_key is None:
        raise RuntimeError("EMBEDDINGS_MODEL_API_KEY environment variable is required")
    settings.store.embeddings.api_key = embed_api_key

    chat_api_key = os.environ.get("CHAT_MODEL_API_KEY")
    if chat_api_key is None:
        raise RuntimeError("CHAT_MODEL_API_KEY environment variable is required")
    settings.agent.llm.api_key = chat_api_key

    oauth_client_id = os.environ.get("OAUTH_CLIENT_ID")
    if oauth_client_id is None:
        raise RuntimeError("OAUTH_CLIENT_ID is required")
    settings.merchant_api.oauth.client_id = oauth_client_id

    oauth_client_secret = os.environ.get("OAUTH_CLIENT_SECRET")
    if oauth_client_secret is None:
        raise RuntimeError("OAUTH_CLIENT_SECRET is required")
    settings.merchant_api.oauth.client_secret = oauth_client_secret

    token_url = os.environ.get("OAUTH_TOKEN_URL")
    if token_url is None:
        raise RuntimeError("OAUTH_TOKEN_URL is required")
    settings.merchant_api.oauth.token_url = token_url

    if settings.store.provider == "mongodb":
        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            raise RuntimeError("MONGO_URI environment variable is required")
        settings.store.mongodb.uri = mongo_uri

    return settings
