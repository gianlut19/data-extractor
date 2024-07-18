from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

def get_drive_service(credentials):
    return build('drive', 'v3', credentials=credentials)

def list_files_in_folder(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)"
    ).execute()
    return results.get('files', [])

def download_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    return file.getvalue()

def process_drive_folder(credentials, folder_id):
    service = get_drive_service(credentials)
    files = list_files_in_folder(service, folder_id)
    
    processed_files = []
    for file in files:
        if file['mimeType'] == 'application/pdf':
            file_content = download_file(service, file['id'])
            # Qui puoi aggiungere la logica per processare il contenuto del file
            processed_files.append({
                'name': file['name'],
                'content': file_content  # Questo è il contenuto binario del PDF
            })
    
    return processed_files

# Esempio di utilizzo
if __name__ == "__main__":
    # Questo è solo un esempio. Nella pratica, otterrai le credenziali
    # attraverso il flusso di autenticazione OAuth2.
    creds = Credentials.from_authorized_user_file('token.json')
    folder_id = 'your_folder_id_here'
    results = process_drive_folder(creds, folder_id)
    print(f"Processati {len(results)} file dalla cartella di Google Drive")