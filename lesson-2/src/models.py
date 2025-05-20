from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
import operator


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]