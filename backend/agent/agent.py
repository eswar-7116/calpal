import os
from typing import List

from langchain_core.messages import BaseMessage
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from pydantic import BaseModel

from backend.agent.tools import tools

google_api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=1.0
)
agent_node = create_react_agent(llm, tools)

class WorkflowState(BaseModel):
    messages: List[BaseMessage]

workflow = StateGraph(WorkflowState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.set_finish_point("agent")

graph = workflow.compile()
