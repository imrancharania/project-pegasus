import os
from pathlib import Path
import yaml

from libs.providers.settings import HagridSettings

from dotenv import load_dotenv

load_dotenv()


def load_settings():
    config_path = Path(__file__).parent / "settings.yaml"
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)

    settings = HagridSettings.model_validate(config_data)

    if settings.store.embeddings:
        api_key = os.environ.get("EMBEDDINGS_MODEL_API_KEY")
        if api_key is None:
            raise RuntimeError(
                "EMBEDDINGS_MODEL_API_KEY environment variable is required"
            )
        settings.store.embeddings.api_key = api_key

    if settings.store.provider == "mongodb":
        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            raise RuntimeError("MONGO_URI environment variable is required")
        settings.store.mongodb.uri = mongo_uri

    if settings.llm:
        api_key = os.environ.get("CHAT_MODEL_API_KEY")
        if api_key is None:
            raise RuntimeError("CHAT_MODEL_API_KEY environment variable is required")
        settings.llm.api_key = api_key

    return settings