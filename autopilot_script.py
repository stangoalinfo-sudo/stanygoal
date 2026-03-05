import os
import json
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore

# 1. SETUP FIREBASE (Kutumia Secret tuliyoweka GitHub)
# Tunachukua ile kodi ya JSON kutoka kwenye Secret ya FIREBASE_SERVICE_ACCOUNT
service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT'))
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. SETUP GEMINI (Kutumia Secret ya GEMINI_API_KEY)
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def start_autopilot():
    print("Inaanza kuchambua mechi...")
    
    # Hapa ni mfano wa mechi (Baadae tutaunganisha na API ya Live Scores)
    matches_to_analyze = [
        {"name": "Simba vs Yanga", "league": "NBC Premier League"},
        {"name": "Real Madrid vs Barcelona", "league": "La Liga"},
        {"name": "Arsenal vs Man City", "league": "EPL"}
    ]

    for match in matches_to_analyze:
        try:
            # Gemini inatengeneza uchambuzi
            prompt = f"Wewe ni mtaalamu wa soka nchini Tanzania. Chambua mechi ya {match['name']} na utoe utabiri mmoja (mfano: Home Win, Over 2.5, au GG) na sababu 3 za Kiswahili. Fupisha sana."
            response = model.generate_content(prompt)
            uchambuzi = response.text

            # Tuma data Firestore
            data = {
                "match_name": match['name'],
                "league": match['league'],
                "prediction": "Angalia Uchambuzi", # Unaweza kuiboresha zaidi hapa
                "reasoning_sw": uchambuzi,
                "status": "NS", # Not Started
                "score": "0-0",
                "timestamp": firestore.SERVER_TIMESTAMP
            }
            
            db.collection('matches').add(data)
            print(f"✅ Mechi ya {match['name']} imewekwa kwenye App!")

        except Exception as e:
            print(f"❌ Hitilafu kwenye {match['name']}: {e}")

if __name__ == "__main__":
    start_autopilot()
