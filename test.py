import tkinter as tk
from tkinter import ttk

root = tk.Tk()

tree = ttk.Treeview(root)
tree.pack()

tree["columns"] = ("one", "two", "three")

tree.column("#0", width=100, minwidth=100)
tree.column("one", width=100, minwidth=100)
tree.column("two", width=100, minwidth=100)
tree.column("three", width=100, minwidth=100)

tree.heading("#0", text="ID", anchor=tk.CENTER)
tree.heading("one", text="Columna 1", anchor=tk.CENTER)
tree.heading("two", text="Columna 2", anchor=tk.CENTER)
tree.heading("three", text="Columna 3", anchor=tk.CENTER)

tree.insert("", 0, text="Item 1", values=("1A", "1B", "1C"))
tree.insert("", 1, text="Item 2", values=("2A", "2B", "2C"))
tree.insert("", 2, text="Item 3", values=("3A", "3B", "3C"))

# Función que se ejecuta cuando se presiona el botón
def on_button_press():
    # Obtener el elemento seleccionado
    item = tree.selection()[0]
    print(item)
    # Modificar los valores del elemento seleccionado
    tree.item(item, values=("Nuevo valor 1", "Nuevo valor 2"))

# Crear un botón
button = tk.Button(root, text="Modificar elemento", command=on_button_press)
button.pack()

root.mainloop()