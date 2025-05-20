from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from src.agent import Agent
from src.tools import tavily_search_tool
from src.prompts import prompt_research

model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

agent = Agent(
  model,
  tools=[tavily_search_tool],
  system=prompt_research,
)


def ask(question: str):
  print(f"Question: {question}")

  messages = [HumanMessage(content=question)]

  result = agent.graph.invoke({"messages": messages})

  print(f"Answer: {result['messages'][-1].content}")