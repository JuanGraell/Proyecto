import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#pip install pandas
#pip install sqlalchemy
#pip install pysqlite3

class Canal:
    def __init__(self, id_canal, canal, categoria="No categorizado"):
        self.id_canal = id_canal
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
    suscribirse_button_indicate.config(bg="#c3c3c3")
    cerrar_button_indicate.config(bg="#c3c3c3")

def home():
    home_frame = tk.Frame(main_frame)
    lb=tk.Label(home_frame,text="Home",font=("Bold",30))
    lb.pack()
    imgLabel = tk.Label(home_frame,image=img_home)
    imgLabel.pack()
    home_frame.pack(pady=20)

def canales():

    def editar():
        item = tabla.selection()[0]
        valor = tabla.item(item, "values")
        tabla.item(item, values=(valor[0], cbCategoria.get(),valor[2]))

    def anular_subscripcion():
        selected_row = tabla.focus()
        if selected_row:
            channel_id = tabla.item(selected_row)['values'][2]
            print(channel_id)
            
            subs = youtube.subscriptions().list(
                part='id,snippet',
                mine=True,
                maxResults=5
            ).execute()

            subscription_id = None
            for sub in subs['items']:
                if sub['snippet']['resourceId']['channelId'] == channel_id:
                    subscription_id = sub['id']
                    break

            if subscription_id:
                youtube.subscriptions().delete(
                    id=subscription_id
                ).execute()
                messagebox.showinfo("Éxito", "Se anuló la suscripción al canal.")
                tabla.delete(selected_row)
            else:
                messagebox.showwarning("Advertencia", "No se ha encontrado la suscripción a este canal.")
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado canal para anular suscripción.")

            

    def selectItem(a):
        item = tabla.selection()[0]
        valor = tabla.item(item, "values")
        root.update()
        cbCategoria.set(valor[1])
        lbCanal.config(text=valor[0])
        return valor

    def obtener_canales_suscritos(yt):
        canales = []
        request = yt.subscriptions().list(part="snippet", mine=True, maxResults=50)#
        print(request)
        
        while request is not None:
            response = request.execute()
            for item in response['items']:
                canal_id = item['snippet']['resourceId']['channelId']
                canal_nombre = item['snippet']['title']
                canales.append(Canal(canal_id, canal_nombre))
            request = yt.subscriptions().list_next(request, response)
        return canales

    canales_frame = tk.Frame(main_frame)
    lb = tk.Label(canales_frame, text="Canales Suscritos", font=("Bold", 30))
    lb.pack()

    canales = obtener_canales_suscritos(youtube)

    tabla = ttk.Treeview(canales_frame, columns=("Canal", "Categoría", "ID"), show="headings")
    tabla.heading("Canal", text="Canal")
    tabla.heading("Categoría", text="Categoría")
    tabla.heading("ID", text="ID")
    tabla.pack(pady=20)

    for i, canal in enumerate(canales):
        tabla.insert("", "end", values=(canal.canal, canal.categoria, canal.id_canal))

    
    texto=tabla.bind('<ButtonRelease-1>', selectItem)

    lbCanal=tk.Label(canales_frame, text="No se ha seleccionado un canal.")
    lbCanal.pack()

    bAnular = tk.Button(canales_frame, text="Anular suscripción", command=anular_subscripcion)
    bAnular.pack(pady=5)

    n = tk.StringVar()
    cbCategoria = ttk.Combobox(canales_frame, width = 27, textvariable = n,state="readonly")
    cbCategoria['values'] = ("No categorizado",' Entretenimiento',' Educacion',' Videojuegos')
    cbCategoria.current(0)
    cbCategoria.place(x=190,y=380)

    bEditar = Button(canales_frame,text="Editar",command=editar)
    bEditar.place(x=380,y=378)

    canales_frame.pack(pady=20,fill=tk.Y,expand=True)

def suscribirse():
    def agregar_datos_busqueda():
        tabla.delete(*tabla.get_children())

        query = search_entry.get()
        busqueda = youtube.search().list(
            q=query,
            type='channel',
            part='id,snippet',
            maxResults=5
        ).execute()

        for item in busqueda['items']:
            id_canal = item['id']['channelId']
            nombre_canal = item['snippet']['title']
            descripcion_canal = item['snippet']['description']
            tabla.insert("",tk.END,text=str(nombre_canal), values=(str(descripcion_canal),str(id_canal)))
            
    def suscribirse_acc():
        item = tabla.selection()[0]
        valor = tabla.item(item, "values")
        try:
            response = youtube.subscriptions().insert(
                part='snippet',
                body={
                    'snippet': {
                        'resourceId': {
                            'kind': 'youtube#channel',
                            'channelId': valor[1]
                        }
                    }
                }
            ).execute()
            messagebox.showinfo("Éxito", "Se ha suscrito el canal a su cuenta")
            print(f"Se ha suscrito al canal '{valor[0]}' en YouTube.")
        except HttpError as e:
            print(f"Error al suscribirse al canal '{valor[0]}' en YouTube: {e}")
            messagebox.showerror("Error", f"No se ha podido suscribir al canal {valor[0]}")

        
    suscribirse_frame=tk.Frame(main_frame)
    lb=tk.Label(suscribirse_frame,text="Buscar canales",font=("Bold",30))
    lb.pack()

    search_label = tk.Label(suscribirse_frame, text="Término de búsqueda:")
    search_label.place(x=40,y=65)

    search_entry = tk.Entry(suscribirse_frame)
    search_entry.place(x=165,y=65)

    search_button = tk.Button(suscribirse_frame, text="Buscar",command=agregar_datos_busqueda)
    search_button.place(x=300,y=60)

    tabla=ttk.Treeview(suscribirse_frame,columns=("col1","col2"))

    tabla.column("#0",width=130)
    tabla.column("col1",width=200)
    tabla.column("col2",width=170)

    tabla.heading("#0",text="Nombre",anchor=tk.CENTER)
    tabla.heading("col1",text="Descripcion",anchor=tk.CENTER)
    tabla.heading("col2",text="ID",anchor=tk.CENTER)
                
    tabla.pack(pady=60)

    subscribe_button = tk.Button(suscribirse_frame, text="Suscribirse",command=suscribirse_acc)#command=on_subscribe)
    subscribe_button.pack(side=tk.BOTTOM)

    suscribirse_frame.pack(pady=20)

def limpiarFrame():
    for frame in main_frame.winfo_children():
        frame.destroy()

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server(port=0)

youtube = build('youtube', 'v3', credentials=credentials)

root = tk.Tk()
root.geometry("1000x600")
root.title("TubeTag")
root.iconphoto(False,tk.PhotoImage(file="icon.png"))

img_home = tk.PhotoImage(file="logo.png",)
#img_home = img_home.zoom(1.5,1.5)
img_options = tk.PhotoImage(file="logo.png")
img_options = img_options.subsample(5,5)


options_frame = tk.Frame(root, bg="#c3c3c3")

image_frame = tk.Label(options_frame,image=img_options,bg="#c3c3c3")
image_frame.place(x=2,y=-25)

home_button=tk.Button(options_frame,text="Home",font=("bold",15),fg="#158aff",bd=0,bg="#c3c3c3",command=lambda: indicate(home_button_indicate,home))
home_button.place(x=8,y=90)
home_button_indicate=tk.Label(options_frame,text="",bg="#158aff")
home_button_indicate.place(x=3,y=90,width=5,height=40)

canales_button=tk.Button(options_frame,text="Canales",font=("bold",15),fg="#158aff",bd=0,bg="#c3c3c3",command=lambda: indicate(canales_button_indicate,canales))
canales_button.place(x=8,y=140)
canales_button_indicate=tk.Label(options_frame,text="",bg="#c3c3c3")
canales_button_indicate.place(x=3,y=140,width=5,height=40)

suscribirse_button=tk.Button(options_frame,text="Suscribir",font=("bold",15),fg="#158aff",bd=0,bg="#c3c3c3",command=lambda: indicate(suscribirse_button_indicate,suscribirse))
suscribirse_button.place(x=8,y=190)
suscribirse_button_indicate=tk.Label(options_frame,text="",bg="#c3c3c3")
suscribirse_button_indicate.place(x=3,y=190,width=5,height=40)

cerrar_button=tk.Button(options_frame,text="Cerrar",font=("bold",15),fg="#158aff",bd=0,bg="#c3c3c3",command=root.quit)
cerrar_button.place(x=8,y=240)
cerrar_button_indicate=tk.Label(options_frame,text="",bg="#c3c3c3")
cerrar_button_indicate.place(x=3,y=240,width=5,height=40)

options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=100, height=600)

main_frame = tk.Frame(root,highlightbackground="black", highlightthickness=2)

main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(width=1000, height=700)
home()

root.resizable(False,False)
root.mainloop()