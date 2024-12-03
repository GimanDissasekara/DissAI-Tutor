from fastapi import FastAPI
from pydantic import BaseModel
import random  # Placeholder for your expert system logic
from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins (or specify your frontend URL)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



app = FastAPI()

# Request model for user input
class UserInput(BaseModel):
    message: str

# Define some simple chatbot responses (replace with your expert system logic)
def get_bot_response(user_message):
    responses = [
        "Hello! How can I assist you today?",
        "I'm here to help you.",
        "Can you tell me more about your problem?",
        "Let me think about that..."
    ]
    return random.choice(responses)

@app.post("/chatbot/")
async def chat(input: UserInput):
    user_message = input.message
    bot_response = get_bot_response(user_message)
    return {"response": bot_response}

# To run the app: uvicorn app:app --reload
