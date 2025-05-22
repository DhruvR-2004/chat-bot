from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Allow requests from your frontend (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for prompt input
class PromptRequest(BaseModel):
    prompt: str

# Default route - just a health check or welcome message
@app.get("/")
async def root():
    return {"message": "Gemini chat API is up and running."}

# Chat endpoint
@app.post("/chat")
async def chat_with_gemini(prompt_request: PromptRequest):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt_request.prompt)
    return {"response": response.text}

# Optional: entry point for uvicorn, no hardcoded port here
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Use PORT env var or default to 8000
    uvicorn.run("your_module_name:app", host="0.0.0.0", port=port, reload=True)
