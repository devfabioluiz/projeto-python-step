# app/database/supabase_client.py
import requests

SUPABASE_URL = "https://xyzcompany.supabase.co"
SUPABASE_KEY = "sb_secret_XXXX"

supabase = {
    "url": SUPABASE_URL,
    "key": SUPABASE_KEY,
}


# ou se quiser criar um helper para requests
def supabase_request(path, method="GET", data=None):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    url = f"{SUPABASE_URL}/{path}"
    if method.upper() == "GET":
        return requests.get(url, headers=headers)
    if method.upper() == "POST":
        return requests.post(url, json=data, headers=headers)
