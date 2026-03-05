import os
import json
import requests
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# 1. SETUP
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT'))
cred = credentials.Certificate(service_account_info)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

FOOTBALL_API_KEY = os.environ.get('FOOTBALL_API_KEY')

def get_matches():
    # Tunatafuta mechi za leo (Tarehe ya mfumo)
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    headers = {'x-apisports-key': FOOTBALL_API_KEY}
    response = requests.get(url, headers=headers)
    all_fixtures = response.json().get('response', [])
    
    # Tunachuja ligi tunazozitaka tu (EPL=39, NBC TZ=357, La Liga=140)
    target_leagues = [39, 357, 140, 78] 
    filtered = [f for f in all_fixtures if f['league']['id'] in target_leagues]
    return filtered

def start_autopilot():
    matches = get_matches()
    print(f"Zimepatikana mechi {len(matches)} za leo.")

    for m in matches[:15]:
        home = m['teams']['home']['name']
        away = m['teams']['away']['name']
        league = m['league']['name']
        
        try:
            # Gemini inafanya kazi yake
            prompt = f"Chambua mechi ya {home} vs {away} ya {league}. Toa utabiri mmoja wa uhakika (mf. GG, Over 2.5, au Home Win) na sababu moja fupi ya Kiswahili."
            response = model.generate_content(prompt)
            uchambuzi = response.text

            # Tuma Firestore
            db.collection('matches').add({
                "match_name": f"{home} vs {away}",
                "league": league,
                "prediction": "Uchambuzi wa AI",
                "reasoning_sw": uchambuzi,
                "status": m['fixture']['status']['short'],
                "score": f"{m['goals']['home']}-{m['goals']['away']}" if m['goals']['home'] is not None else "0-0",
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            print(f"✅ Imehifadhiwa: {home} vs {away}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_autopilot()
