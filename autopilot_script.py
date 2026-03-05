import os
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore

# Setup
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
cred = credentials.Certificate("firebase-key.json") # Hakikisha una faili hili
firebase_admin.initialize_app(cred)
db = firestore.client()

def start_autopilot():
    model = genai.GenerativeModel('gemini-pro')
    
    # Mfano wa mechi (Hapa utazitoa kwenye Football API)
    matches = [
        {"name": "Simba vs Yanga", "league": "NBC Tanzania"},
        {"name": "Real Madrid vs Barcelona", "league": "La Liga"}
    ]

    for m in matches:
        prompt = f"Wewe ni mtaalamu wa soka. Toa sababu 3 kwa Kiswahili kwanini mechi ya {m['name']} itakuwa na magoli mengi. Usizidishe maneno 50."
        response = model.generate_content(prompt)
        
        db.collection('matches').add({
            "match_name": m['name'],
            "league": m['league'],
            "prediction": "Over 2.5",
            "reasoning_sw": response.text,
            "status": "NS",
            "score": "0-0",
            "probability": 85
        })
        print(f"Mechi ya {m['name']} imewekwa!")

if __name__ == "__main__":
    start_autopilot()