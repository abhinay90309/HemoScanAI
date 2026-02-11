from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection
from model import predict_risk
from fastapi.middleware.cors import CORSMiddleware 
from ml_model import predict_anemia
from chatbot import router as chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows any origin (fine for local testing)
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

# Define the structure of incoming data
class PatientData(BaseModel):
    age: int
    gender: str
    hemoglobin: float
    fatigue: bool
    dizziness: bool

@app.post("/predict")
def predict(data: PatientData):
    conn = None
    try:
        # 1. Logic
        risk = predict_risk(data.hemoglobin, data.gender)
        
        features = [
    7.0,   # WBC
    30.0,  # LYMp
    60.0,  # NEUTp
    2.0,   # LYMn
    4.0,   # NEUTn
    4.5,   # RBC
    data.hemoglobin,  # HGB (real value)
    40.0,  # HCT
    85.0,  # MCV
    28.0,  # MCH
    33.0,  # MCHC
    250.0, # PLT
    12.0,  # PDW
    0.2    # PCT
]

        anemia_type = predict_anemia(features)

        # 2. Database Operation
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO patients 
        (age, gender, hemoglobin, fatigue, dizziness, risk_level, anemia_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
     """

        
        values = (
          data.age,
          data.gender,
          data.hemoglobin,
          data.fatigue,
          data.dizziness,
          risk,
          anemia_type
     ) 

        cursor.execute(query, values)
        conn.commit()

        return {
            "status": "success",
            "risk_level": risk,
            "anemia_type": anemia_type
}


    except Exception as e:
        # Proper error logging
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
     if conn:
        cursor.close()
        conn.close()

            
