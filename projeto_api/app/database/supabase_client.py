
import os
import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = {
    "url": SUPABASE_URL,
    "key": SUPABASE_KEY
}

# ou se quiser criar um helper para requests
def supabase_request(path, method="GET", data=None):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    url = f"{SUPABASE_URL}/{path}"
    if method.upper() == "GET":
        return requests.get(url, headers=headers)
    elif method.upper() == "POST":
        return requests.post(url, json=data, headers=headers)
            