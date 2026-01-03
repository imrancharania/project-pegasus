from libs.providers.factory import create_agent_graph
from responses.tools import tools


class ResponsesService:
    def __init__(self, settings):
        self.agent = create_agent_graph(settings, tools)

    def respond(self, input: str):
        return self.agent.run(input)
