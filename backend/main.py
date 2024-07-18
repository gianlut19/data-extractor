from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
import requests
import PyPDF2
import zipfile
import io

app = FastAPI()

# Configurazione CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sostituire con l'origine del frontend in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelli di dati
class Schema(BaseModel):
    fields: Dict[str, str]

class ExtractRequest(BaseModel):
    schema: Schema
    file_type: str
    extraction_type: str

# Rotte API
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    if file.filename.endswith('.pdf'):
        return process_pdf(io.BytesIO(content))
    elif file.filename.endswith('.zip'):
        return process_zip(io.BytesIO(content))
    else:
        raise HTTPException(status_code=400, detail="Formato file non supportato")

@app.post("/extract")
async def extract_data(request: ExtractRequest):
    # Simulazione della chiamata all'API LLM
    llm_response = call_llm_api("Testo del documento", request.schema.fields)
    
    # Elaborazione della risposta LLM
    df = pd.DataFrame(llm_response)
    
    if request.extraction_type == "single":
        return df.to_dict(orient="records")[0]
    else:
        return df.to_dict(orient="records")

@app.get("/schemas")
async def get_schemas():
    # Simulazione del recupero degli schemi dal database
    return [
        {"name": "Schema 1", "fields": {"campo1": "descrizione1", "campo2": "descrizione2"}},
        {"name": "Schema 2", "fields": {"campo3": "descrizione3", "campo4": "descrizione4"}}
    ]

@app.post("/google-auth")
async def google_auth():
    flow = Flow.from_client_secrets_file(
        "client_secrets.json",
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    authorization_url, _ = flow.authorization_url(prompt="consent")
    return {"authorization_url": authorization_url}

@app.post("/process-drive-folder")
async def process_drive_folder(folder_id: str):
    # Implementazione per elaborare una cartella di Google Drive
    # Questo richiederebbe l'autenticazione dell'utente e l'uso delle API di Google Drive
    pass

# Funzioni di utilità
def process_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return {"text": text}

def process_zip(file):
    with zipfile.ZipFile(file) as z:
        return {name: z.read(name).decode('utf-8') for name in z.namelist() if name.endswith('.pdf')}

def call_llm_api(text: str, schema: Dict[str, str]) -> List[Dict[str, Any]]:
    # Simulazione della chiamata all'API LLM
    # In un'implementazione reale, qui faresti una richiesta HTTP all'API LLM
    return [{"campo1": "valore1", "campo2": "valore2"}]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)