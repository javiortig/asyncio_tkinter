import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


class App:
    async def exec(self):
        loop = asyncio.get_event_loop()
        self.window = Window(loop)
        await self.window.show()


class Window(tk.Tk):
    def __init__(self, loop):
        self.loop = loop

        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Ventana con Tkinter")

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
        image = Image.open('asyncio_tkinter/practica 2/apple.jpg')
        image = ImageTk.PhotoImage(image)
        self.label_imagen = tk.Label(self.root, image=image)
        self.label_imagen.grid(row=4, column=1, sticky="nsew")

        # Crear y colocar la barra de progreso debajo de la imagen
        self.progressbar = ttk.Progressbar(self.root, orient="horizontal")
        self.progressbar.grid(row=3, column=1, padx=10, pady=10)
   
        # Crear el boton
        self.button = tk.Button(self.root, text="Buscar", command= lambda: self.loop.create_task(self.update_progress_bar()))
        self.button.grid(row=1, column=1, sticky="e", padx=30)

    def hide_button(self):
        if self.button.winfo_viewable():
            self.button.grid_forget()

    def show_button(self):
        if not self.button.winfo_viewable():
            self.button.grid(row=1, column=1, sticky="e", padx=30)

    async def update_progress_bar(self):
        # Oculta el boton mientras se descargan las imagenes
        self.hide_button()

        for i in range(0, 100, 1):
            self.progressbar["value"] = i
            await asyncio.sleep(0.1)

        self.show_button()

    async def get_images_source_from_url(self):


    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(.01)



asyncio.run(App().exec())