import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import validators
import io

IMG_W = 300
IMG_H = 300


class App(tk.Tk):
## metodos publicos
    async def exec(self):
        self.loop = asyncio.get_event_loop()
        await self._update() 

## metodos privados
    def __init__(self):
        self.loop = None
        self.images = []

        # Crea la ventana principal
        self.root = tk.Tk()
        self.root.title("Descargas de imagenes con asyncio")

        # Configura los pesos del grid
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

        # Crea el Label
        self.label_url = tk.Label(self.root, text="URL a procesar:")
        self.label_url.grid(row=0, column=0, sticky="e", padx=(0, 5))

        # Crea el TextBox
        self.textbox = tk.Entry(self.root)
        self.textbox.grid(row=0, column=1, columnspan=2, sticky="ew", padx=(0, 10))

        # Crea el frame donde se encuentran el listbox y el scrollbar
        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.grid(row=2, column=0, sticky='ew')

        # Crea el ListBox
        self.listbox = tk.Listbox(self.listbox_frame)
        self.listbox.grid(row=0, column=0, sticky="ns")

        # Crea el scrollbar y anexarlo a la Listbox
        self.scrollbar = tk.Scrollbar(self.listbox_frame)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.listbox.config(yscrollcommand= self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Crea una imagen vacia
        self._set_empty_image()

        # Crea y colocar la barra de progreso debajo de la imagen
        self.progressbar = ttk.Progressbar(self.root, orient="horizontal")
        self.progressbar.grid(row=3, column=1, padx=10, pady=10)
   
        # Crea el boton
        self.button = tk.Button(self.root, text="Buscar", command= lambda: self.loop.create_task(self._get_images()))
        self.button.grid(row=1, column=1)   

    def _set_empty_image(self):
        # Cargar una imagen vacia
        self.image = Image.new('RGB', size=(IMG_W, IMG_H), color=(255, 255, 255))
        self.image = ImageTk.PhotoImage(self.image)
        self.label_imagen = tk.Label(self.root, image=self.image)
        self.label_imagen.grid(row=2, column=1, sticky="nsew", padx=(0, 10))

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
        # Guarda el nombre en la listbox
        self.listbox.insert(tk.END, url.split('/')[-1].split('.')[0])        

        async with session.get(url) as response:
            image_data = await response.content.read()

            try:
                # Guarda la imagen en memoria
                temp_image = Image.open(io.BytesIO(image_data)).resize((IMG_W, IMG_H))
                temp_image = ImageTk.PhotoImage(temp_image)
                self.images.append(temp_image)
            except Exception as e:
                print(f'>Ha ocurrido una excepción al descargar la imagen de la url={url} con el siguiente resultado: {e}')



    async def _get_images_source_from_url(self, session) -> []:
        """
        Dada una URL en el textbox, devuelve una lista con las urls de las imagenes que contiene la pagina en cuestion.
        """
        # Reinicia la imagen mostrada, la listbox y la lista de imagenes
        self.images = [] # Las imagenes raw guardadas en memoria, no en disco
        self.listbox.delete(0, tk.END)
        self._set_empty_image()

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

        if (not selected_item) or (selected_item[0]<0) or (selected_item[0] >= len(self.images)):
            return 
        
        selected_index = selected_item[0]

        self.image = self.images[selected_index]

        self.label_imagen = tk.Label(self.root, image=self.image)
        self.label_imagen.grid(row=2, column=1, sticky="nsew", padx=(0, 10))

    async def _update(self):
        while True:
            self.root.update()
            self._update_selected_image()
            await asyncio.sleep(.01)

app = App()

asyncio.run(app.exec())
