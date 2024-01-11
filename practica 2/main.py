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
        image = Image.open('asyncio_tkinter/practica 2/apple.jpg')
        image = ImageTk.PhotoImage(image)
        self.label_imagen = tk.Label(self.root, image=image)
        self.label_imagen.grid(row=4, column=1, sticky="nsew")

        # Crear y colocar la barra de progreso debajo de la imagen
        self.progressbar = ttk.Progressbar(self.root, orient="horizontal")
        self.progressbar.grid(row=3, column=1, padx=10, pady=10)
   
        # Crear el boton
        self.button = tk.Button(self.root, text="Buscar", command= lambda: self.loop.create_task(self._get_images()))
        self.button.grid(row=1, column=1, sticky="e", padx=30)   

    def _hide_button(self):
        if self.button.winfo_viewable():
            self.button.grid_forget()

    def _show_button(self):
        if not self.button.winfo_viewable():
            self.button.grid(row=1, column=1, sticky="e", padx=30)

    async def _fetch_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def __download_image_to_disk(self, session, url, filename):
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)

    async def _download_image_to_listbox(self, session, url):
        """
        Descarga una imagen y la añade a la Listbox de la interfaz
        """
        async with session.get(url) as response:
            image_data = await response.read()
            
            # Guarda el nombre en la listbox
            self.listbox.insert(tk.END, url.split('/')[-1].split('.')[0])

            # Guarda la imagen en memoria
            self.images.append(Image(ImageTk.PhotoImage(image_data)))

    async def _get_images_source_from_url(self, session) -> []:
        """
        Dada una URL en el textbox, devuelve una lista con las urls de las imagenes que contiene la pagina en cuestion.
        """
        self.images = [] # Las imagenes raw guardadas en memoria, no en disco

        url = self.textbox.get()

        html = await self._fetch_page(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        image_urls = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]

        # Validar las urls de las imagenes, pues algunas son estaticas
        image_urls = [img_url for img_url in image_urls if validators.url(img_url)]

        return image_urls


    async def __update_progress_bar(self):
        # Oculta el boton mientras se descargan las imagenes
        self._hide_button()

        for i in range(0, 100, 1):
            self.progressbar["value"] = i
            await asyncio.sleep(0.1)

        self._show_button()

    async def _get_images(self):
        """
        Llamada desde el boton de la interfaz, obtiene las imagenes de forma concurrente y las coloca
        en la lista conforme se descargan. Ademas, actualiza la barra de progreso conforme una imagen termina de descargarse.
        """
        async with aiohttp.ClientSession() as session:
            image_urls = await self._get_images_source_from_url(session)

            tasks = []
            for img_url in image_urls:
                task = asyncio.create_task(self._download_image_to_listbox(session, img_url))
                tasks.append(task)

            await asyncio.gather(*tasks)

    def _update_selected_image(self):
        selected_item = self.listbox.curselection()

        if(selected_item):
            selected_index = selected_item[0]

            self.label_imagen = tk.Label(self.root, image=self.images[selected_index])


    async def _update(self):
        while True:
            self.root.update()
            self._update_selected_image()
            await asyncio.sleep(.01)

app = App()

asyncio.run(app.exec())