import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.read()

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        content = await fetch(session, url)
        return content  # Retorna los datos de la imagen

async def find_and_download_images(page_url):
    async with aiohttp.ClientSession() as session:
        page_content = await fetch(session, page_url)
        soup = BeautifulSoup(page_content, 'html.parser')
        image_urls = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]

        images = []
        for image_url in image_urls:
            print(f"Descargando {image_url}")
            image_data = await download_image(image_url)
            images.append(image_data)
        
        return images  # Retorna una lista con los datos de todas las imágenes

# URL de la página de donde quieres descargar imágenes
page_url = 'https://supervivencial.com/curso-de-supervivencia/'

# Iniciar el loop de eventos de asyncio
loop = asyncio.get_event_loop()
images = loop.run_until_complete(find_and_download_images(page_url))

# Ahora, `images` contiene los datos binarios de las imágenes descargadas
print(f"Descargadas {len(images)} imágenes.")
