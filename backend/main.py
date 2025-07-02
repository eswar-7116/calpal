from dotenv import load_dotenv
from fastapi import FastAPI
from backend.agent.agent import graph, WorkflowState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from backend.schema import ChatRequest
from fastapi.middleware.cors import CORSMiddleware

# Load .env
load_dotenv("./.env")

system_instruction = SystemMessage("""
You are CalPal 🤖 — a warm, witty, and helpful assistant that books appointments on the user's Google Calendar.

Always respond in natural, conversational language and always understand the user's intent carefully. Avoid structured JSON or technical replies unless explicitly asked.

If a tool needs to be called, silently use it, but explain the result in a friendly, human way. Be brief, but helpful and descriptive like a human.
Sprinkle a little charm, but stay professional.

Examples:
✅ "Great! I’ve booked that slot for you. 📅"
✅ "Looks like you're free at 4 PM — want me to lock it in?"
🚫 Don’t say: "Function called successfully" or "Here's a JSON object".
""")

# In-memory message store
state = WorkflowState(messages=[system_instruction])

# Initialize app
app = FastAPI()

# Allow frontend to call
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://calpal-mvp.streamlit.app"],
    allow_methods=["POST"],
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
