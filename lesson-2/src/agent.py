from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import StateGraph, END
from src.models import AgentState


class Agent:
  def __init__(self, model, tools, system):
    self.system = system

    graph = StateGraph(AgentState)

    # first node is calling the LLM
    graph.add_node("llm", self.call_openai)

    # second node is checking if the LLM should take an action
    graph.add_node("action", self.take_action)

    # this edge connects the llm node to the action node
    # or to the END node if the LLM should not take an action
    graph.add_conditional_edges(
      "llm",
      self.exists_action,
      {True: "action", False: END}
    )

    # this edge connects the action node to the llm node
    graph.add_edge("action", "llm")

    # the llm node is the graph entry point
    graph.set_entry_point("llm")
    
    self.graph = graph.compile()

    # store the tools for easy access
    self.tools = {t.name: t for t in tools}

    # let the model know it has these tools available to call
    self.model = model.bind_tools(tools)


  def call_openai(self, state: AgentState):
    messages = state['messages']

    if self.system:
      messages = [SystemMessage(content=self.system)] + messages
    
    message = self.model.invoke(messages)

    return {'messages': [message]}

  def exists_action(self, state: AgentState):
    return len(state['messages'][-1].tool_calls) > 0

  def take_action(self, state: AgentState):
    results = []

    tools_calls = state['messages'][-1].tool_calls

    for tool_call in tools_calls:
      print(f"\nCalling: {tool_call}")

      if not tool_call['name'] in self.tools:
        print("\n ....bad tool name....")

        result = "Bad tool name... retry"
      else:
        result = self.tools[tool_call['name']].invoke(tool_call['args'])

      results.append(ToolMessage(tool_call_id=tool_call['id'], name=tool_call['name'], content=str(result)))
    
    print("\nBack to the model!\n")

    return {'messages': results}