import tkinter as tk
from tkinter import ttk
from google.oauth2 import service_account
import google_auth_oauthlib
from googleapiclient.discovery import build
import pandas as pd

# Carga la clave de API
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server(port=0)

# Crea una instancia de la API de YouTube
youtube = build('youtube', 'v3', credentials=credentials)

# Realiza la búsqueda de canales en YouTube
def search_channels(query):
    request = youtube.search().list(
        part='id,snippet',
        q=query,
        type='channel',
        maxResults=30
    )
    response = request.execute()

    # Extrae la información relevante de la respuesta de la API de YouTube
    channels = []
    for item in response['items']:
        channel_id = item['id']['channelId']
        channel_title = item['snippet']['title']
        channel_description = item['snippet']['description']
        channels.append({'Título': channel_title, 'Descripción': channel_description})

    # Devuelve los resultados de búsqueda en forma de DataFrame de pandas
    return pd.DataFrame(channels)

# Crea una tabla para mostrar los resultados de búsqueda
def create_table(parent, df):
    tree = ttk.Treeview(parent, columns=list(df.columns), show="headings")
    for col in df.columns:
        tree.heading(col, text=col)
    for row in df.to_numpy().tolist():
        tree.insert("", "end", values=row)
    tree.pack(side='left', fill='both', expand=True)
    return tree

# Controlador de eventos del botón de búsqueda
def on_search():
    query = search_entry.get()
    df = search_channels(query)
    create_table(table_frame, df)

# Crea la aplicación de Tkinter
root = tk.Tk()
root.title("Búsqueda de canales de YouTube")

# Crea un marco para la entrada de búsqueda y el botón
search_frame = tk.Frame(root)
search_frame.pack(side='top', fill='x')

search_label = tk.Label(search_frame, text="Término de búsqueda:")
search_label.pack(side='left', padx=5, pady=5)

search_entry = tk.Entry(search_frame)
search_entry.pack(side='left', fill='x', padx=5, pady=5, expand=True)

search_button = tk.Button(search_frame, text="Buscar", command=on_search)
search_button.pack(side='left', padx=5, pady=5)

# Crea un marco para la tabla de resultados de búsqueda
table_frame = tk.Frame(root)
table_frame.pack(side='top', fill='both', expand=True)

# Inicia la aplicación
root.mainloop()