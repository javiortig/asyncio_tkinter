import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import validators


class App(tk.Tk):
## metodos publicos
    async def exec(self):
        self.loop = asyncio.get_event_loop()
        await self._update() 

## metodos privados
    def __init__(self):
        self.loop = None
        self.images = []

        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Descargas de imagenes con asyncio")

        # Configurar el layout
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Crear el Label
        self.label_url = tk.Label(self.root, text="URL a procesar")
        self.label_url.grid(row=0, column=0, sticky="e")

        # Crear el TextBox
        self.textbox = tk.Entry(self.root)
        self.textbox.grid(row=0, column=1, sticky="ew")

        # Crear el ListBox
        self.listbox = tk.Listbox(self.root)
        self.listbox.grid(row=2, column=0, sticky="ns")

        # Cargar una iamgen de prueba
        image = Image.open('asyncio_tkinter/practica 2/dado.png')
        image = ImageTk.PhotoImage(image)
        self.label_imagen = tk.Label(self.root, image=image)
        self.label_imagen.grid(row=3, column=1)

    async def _update(self):
        while True:
            self.root.update()
            await asyncio.sleep(.01)

app = App()

asyncio.run(app.exec())

