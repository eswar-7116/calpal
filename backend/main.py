from dotenv import load_dotenv
from fastapi import FastAPI
from backend.agent.agent import graph, WorkflowState
from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages
from backend.schema import ChatRequest
from fastapi.middleware.cors import CORSMiddleware

# Load .env
load_dotenv("./.env")

# In-memory message store
state = WorkflowState(messages=[])

# Initialize app
app = FastAPI()

# Allow frontend to call
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat(req: ChatRequest):
    global state

    # Extract user message from request
    msg = req.chat

    # Add new message
    messages = add_messages(state.messages, [HumanMessage(content=msg)])
    state = WorkflowState(messages=messages)

    # Call LangGraph agent
    result = graph.invoke(state)
    state = WorkflowState(messages=result["messages"])

    # Extract bot response
    ai_reply = state.messages[-1].content

    return {
        "message": ai_reply
    }
