from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import os

app = FastAPI()

# Impostare questa variabile su True per bypassare l'autenticazione durante il debug
DEBUG_MODE = True

# Configurazione del client OAuth2
CLIENT_CONFIG = {
    "web": {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost:8000/callback"]
    }
}

def create_flow():
    return Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )

@app.get("/login")
async def login(request: Request):
    if DEBUG_MODE:
        return {"message": "Autenticazione bypassata in modalità debug"}
    
    flow = create_flow()
    authorization_url, _ = flow.authorization_url(prompt="consent")
    return RedirectResponse(authorization_url)

@app.get("/callback")
async def callback(request: Request):
    if DEBUG_MODE:
        return {"message": "Callback bypassato in modalità debug"}
    
    flow = create_flow()
    flow.fetch_token(code=request.query_params["code"])
    credentials = flow.credentials
    
    # Qui puoi salvare le credenziali o restituirle al client
    return {"message": "Autenticazione completata con successo"}

def get_credentials():
    if DEBUG_MODE:
        # Restituisci delle credenziali fittizie o None in modalità debug
        return None
    
    # Implementa la logica per recuperare le credenziali salvate
    # Questo è solo un esempio, nella pratica dovresti implementare
    # una gestione sicura delle credenziali
    if os.path.exists("token.json"):
        return Credentials.from_authorized_user_file("token.json")
    return None

# Esempio di utilizzo in un'altra parte dell'applicazione
def protected_route():
    credentials = get_credentials()
    if credentials is None and not DEBUG_MODE:
        return RedirectResponse("/login")
    # Procedi con la logica protetta
    return {"message": "Accesso consentito alla risorsa protetta"}