from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = "881288169563-1h7o3ocu33tv8f907720ddh6l3n2d6l1.apps.googleusercontent.com"

def verify_google_token(token: str):
    return id_token.verify_oauth2_token(
        token,
        requests.Request(),
        audience=GOOGLE_CLIENT_ID
    )
