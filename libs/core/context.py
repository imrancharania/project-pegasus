from dataclasses import dataclass
from libs.core.stores.base import BaseStore

@dataclass
class AgentContext:
    store: BaseStore