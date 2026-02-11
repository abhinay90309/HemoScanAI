import os
import pandas as pd
import google.generativeai as genai
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Request body structure
class ChatInput(BaseModel):
    prompt: str

# Configure Gemini
GENAI_KEY = os.getenv("GEMINI_API_KEY")

if not GENAI_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GENAI_KEY)

# Load dataset
try:
    df = pd.read_csv("diagnosed_cbc_data_v4.csv")
    diseases = df['Diagnosis'].unique().tolist()
except Exception:
    diseases = ["Anemia types unavailable"]

# System prompt
system_prompt = (
    f"You are HemaBot, an AI assistant for an Anemia Detection project. "
    f"The system detects: {', '.join(diseases)}.\n\n"
    "Rules:\n"
    "- If asked about symptoms, mention fatigue, pale skin, dizziness.\n"
    "- If asked for diagnosis, tell user to use Predict form.\n"
    "- Use short bullet points.\n"
    "- Always end with: Educational project only. Consult a doctor."
)

model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=system_prompt
)

# Chat endpoint (FIXED)
@router.post("/chat")
async def chat_with_bot(data: ChatInput):
    try:
        response = model.generate_content(data.prompt)

        if response and response.text:
            return {"response": response.text}
        else:
            return {"response": "I couldn't generate a response."}

    except Exception as e:
        return {"response": f"Error: {str(e)}"}
