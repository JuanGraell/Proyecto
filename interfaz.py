import tkinter as tk
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

class Canal:
    def __init__(self, canal, categoria="No categorizado"):
        self.canal = canal
        self.categoria = categoria
        
def indicate(lb,page):
    hide_indicate()
    lb.config(bg="#158aff")
    limpiarFrame()
    page()

def hide_indicate():
    home_button_indicate.config(bg="#c3c3c3")
    canales_button_indicate.config(bg="#c3c3c3")

def home():
    home_frame = tk.Frame(main_frame)
    lb=tk.Label(home_frame,text="Apartado Home",font=("Bold",30))
    lb.pack()
    home_frame.pack(pady=20)

def canales():
    canales_frame = tk.Frame(main_frame)
    lb=tk.Label(canales_frame,text="Apartado Canales",font=("Bold",30))
    lb.pack()

    # Obtener los canales a los que está suscrito el usuario como objetos Canal
    canales = obtener_canales_suscritos(youtube)

    # Crear una tabla para mostrar los canales
    tabla_canvas = tk.Canvas(canales_frame)
    tabla_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(canales_frame, orient=tk.VERTICAL, command=tabla_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tabla_canvas.configure(yscrollcommand=scrollbar.set)

    tabla = tk.Frame(tabla_canvas)
    tabla_canvas.create_window((0,0), window=tabla, anchor='nw')

    # Crear encabezados de la tabla
    tk.Label(tabla, text="Canal", font=("bold", 15)).grid(row=0, column=0, padx=10, sticky='w')
    tk.Label(tabla, text="Categoría", font=("bold", 15)).grid(row=0, column=1, padx=10, sticky='w')

    # Recorrer la lista de objetos Canal y mostrarlos en la tabla
    for i, canal in enumerate(canales):
        tk.Label(tabla, text=canal.canal, anchor='w').grid(row=i+1, column=0, padx=10, sticky='w')
        tk.Label(tabla, text=canal.categoria, anchor='w').grid(row=i+1, column=1, padx=10, sticky='w')

    tabla.update_idletasks()

    tabla_canvas.config(scrollregion=tabla_canvas.bbox('all'))

    canales_frame.pack(pady=20)

def obtener_canales_suscritos(yt):
    # Obtener los canales a los que está suscrito el usuario como objetos Canal
    canales = []
    request = yt.subscriptions().list(part="snippet", mine=True, maxResults=50)
    cuadro_texto = tk.Text(main_frame, height=30, width=50)
    cuadro_texto.pack()
    canales = obtener_canales_suscritos(youtube)
    for canal in canales:
        cuadro_texto.insert(tk.END, canal + "\n")

def obtener_canales_suscritos(yt):
    # Obtener los canales a los que está suscrito el usuario
    canales = []
    request = yt.subscriptions().list(part="snippet", mine=True, maxResults=50)
    print(request)
    
    while request is not None:
        response = request.execute()
        for item in response['items']:
            canal = item['snippet']['title']
            canales.append(Canal(canal))
        request = yt.subscriptions().list_next(request, response)
    return canales

def limpiarFrame():
    for frame in main_frame.winfo_children():
        frame.destroy()

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Autorización del flujo OAuth2 del usuario
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server(port=0)

# Construcción de la instancia del servicio de la API de YouTube
youtube = build('youtube', 'v3', credentials=credentials)

root = tk.Tk()
root.geometry("700x600")
root.title("Nombre app")


options_frame = tk.Frame(root, bg="#c3c3c3")

home_button=tk.Button(options_frame,text="Home",font=("bold",15),fg="#158aff",bd=0,bg="#c3c3c3",command=lambda: indicate(home_button_indicate,home))
home_button.place(x=10,y=50)
home_button_indicate=tk.Label(options_frame,text="",bg="#158aff")
home_button_indicate.place(x=3,y=50,width=5,height=40)

canales_button=tk.Button(options_frame,text="Canales",font=("bold",15),fg="#158aff",bd=0,bg="#c3c3c3",command=lambda: indicate(canales_button_indicate,canales))
canales_button.place(x=10,y=100)
canales_button_indicate=tk.Label(options_frame,text="",bg="#c3c3c3")
canales_button_indicate.place(x=3,y=100,width=5,height=40)

cerrar_button=tk.Button(options_frame,text="Cerrar",font=("bold",15),fg="#158aff",bd=0,bg="#c3c3c3",command=root.quit)
cerrar_button.place(x=10,y=150)
cerrar_button_indicate=tk.Label(options_frame,text="",bg="#c3c3c3")
cerrar_button_indicate.place(x=3,y=150,width=5,height=40)

options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=100, height=600)

main_frame = tk.Frame(root,highlightbackground="black", highlightthickness=2)

main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(width=600, height=700)
home()

root.mainloop()