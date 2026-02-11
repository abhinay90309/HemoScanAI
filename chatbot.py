import os
import pandas as pd
import google.generativeai as genai
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# 1. Configure Gemini
GENAI_KEY = os.getenv("GEMINI_API_KEY")

if not GENAI_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GENAI_KEY)

# 2. Load dataset
try:
    df = pd.read_csv("diagnosed_cbc_data_v4.csv")
    diseases = df['Diagnosis'].unique().tolist()
except Exception:
    diseases = ["Anemia types unavailable"]

# 3. System Prompt
system_prompt = (
    f"You are HemaBot, an AI assistant for an Anemia Detection project. "
    f"The system detects: {', '.join(diseases)}.\n\n"
    "Rules:\n"
    "- If asked about symptoms, mention fatigue, pale skin, dizziness.\n"
    "- If asked for diagnosis, tell user to use Predict form.\n"
    "- Use short bullet points.\n"
    "- Always end with: Educational project only. Consult a doctor."
)

# 4. Load Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)


# 5. Chat Endpoint
@router.get("/chat")
async def chat_with_bot(query: str):
    try:
        response = model.generate_content(query)

        if response and response.text:
            return {"reply": response.text}
        else:
            return {"reply": "I couldn't generate a response."}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
