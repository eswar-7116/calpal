import time
from fastapi import FastAPI
from schema import ChatRequest

# Initialize app
app = FastAPI()

# POST /chat
@app.post("/chat")
def chat(req: ChatRequest):
    # Simulate loading
    time.sleep(3)
    
    # Extract request data
    msg = req.chat
    
    # Return message
    return {
        "message": msg
    }
