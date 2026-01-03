from libs.core.context import AgentContext
from libs.core.factory import create_agent_graph, create_store
from libs.core.settings import PegasusSettings
from responses.tools import tools


class ResponsesService:
    def __init__(self, settings: PegasusSettings):
        self.agent = create_agent_graph(settings, tools)
        self.context = AgentContext(create_store(settings))

    def respond(self, input: str):
        return self.agent.run(input=input, context=self.context)
