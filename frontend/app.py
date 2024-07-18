import streamlit as st
import requests
import pandas as pd
import io
import os

# Configurazione dell'URL del backend
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Estrattore di Dati da Documenti", layout="wide")

st.title("Estrattore di Dati da Documenti")

# Caricamento degli schemi dalla cartella data/schemas
schemas_folder = "../data/schemas"
schema_files = [f for f in os.listdir(schemas_folder) if f.endswith('.csv')]

# Sidebar per la selezione dello schema
with st.sidebar:
    st.title("Selezione Schema")
    selected_schema_file = st.selectbox("Scegli uno schema", schema_files)

    # Caricamento dello schema selezionato
    selected_schema_path = os.path.join(schemas_folder, selected_schema_file)
    schema_df = pd.read_csv(selected_schema_path)
    schema = dict(zip(schema_df['Campo'], schema_df['Descrizione']))

# Resto del codice per l'upload del file e l'estrazione dei dati
uploaded_file = st.file_uploader("Carica un file PDF o ZIP", type=["pdf", "zip"])

extraction_type = st.radio("Tipo di estrazione", ("Singola entità", "Entità multiple"))

if uploaded_file is not None and st.button("Estrai dati"):
    files = {"file": uploaded_file}
    upload_response = requests.post(f"{BACKEND_URL}/upload", files=files)
    
    if upload_response.status_code == 200:
        extract_request = {
            "schema": {"fields": schema},
            "file_type": uploaded_file.type,
            "extraction_type": "single" if extraction_type == "Singola entità" else "multiple"
        }
        extract_response = requests.post(f"{BACKEND_URL}/extract", json=extract_request)
        
        if extract_response.status_code == 200:
            data = extract_response.json()
            df = pd.DataFrame(data)
            st.write(df)
            
            # Opzioni di download
            csv = df.to_csv(index=False)
            st.download_button(
                label="Scarica come CSV",
                data=csv,
                file_name="extracted_data.csv",
                mime="text/csv",
            )
            
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            excel_data = excel_buffer.getvalue()
            st.download_button(
                label="Scarica come Excel",
                data=excel_data,
                file_name="extracted_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("Errore durante l'estrazione dei dati")
    else:
        st.error("Errore durante il caricamento del file")

# Elaborazione cartella Google Drive
st.header("Elaborazione Google Drive")
drive_folder_id = st.text_input("ID cartella Google Drive")
if drive_folder_id and st.button("Elabora cartella Google Drive"):
    response = requests.post(f"{BACKEND_URL}/process-drive-folder", json={"folder_id": drive_folder_id})
    if response.status_code == 200:
        st.success("Elaborazione della cartella Google Drive completata")
    else:
        st.error("Errore durante l'elaborazione della cartella Google Drive")