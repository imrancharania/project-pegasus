from langchain.messages import HumanMessage

from langgraph.graph.state import CompiledStateGraph

from libs.core.context import AgentContext


class Agent:
    def __init__(self, agent: CompiledStateGraph):
        self.agent = agent

    def run(self, input: str, context: AgentContext) -> str:
        return self.agent.invoke(input={"messages": [HumanMessage(input)]}, context=context)
