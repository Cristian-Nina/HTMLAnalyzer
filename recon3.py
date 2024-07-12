from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import WebDriverException
import time

# Configurar opciones para navegación en modo headless
options = Options()
options.headless = True
service = Service(executable_path=r'C:\\Users\\nmalizia\\Downloads\\geckodriver-v0.34.0-win32\\geckodriver.exe')
driver = webdriver.Firefox(options=options, service=service)

# Palabras clave a buscar
keywords = ["access banking", "usuario", "clave", "icbc", "ingresar"]

def main():
    with open('potentialphishing.txt') as file:
        websites = file.readlines()
    for website in websites:
        website = website.strip()
        check_website(website)

def clean_url(url):
    if url.startswith("https://*"):
        return url.replace("https://*.", "https://")
    return url

def check_website(url):
    url = clean_url(url)  # Limpiar la URL si es necesario
    try:
        driver.get(url)
        time.sleep(3)  # Esperar a que la página cargue
        html = driver.page_source.lower()  # Obtener el HTML en minúsculas para facilitar la búsqueda

        # Buscar palabras clave
        if all(keyword in html for keyword in keywords):
            print(f'Palabras clave encontradas en: {url}')
            with open("links.txt", "a") as file:
                file.write(f'{url}\n')
        else:
            print(f'No se encontraron palabras clave en: {url}')
    except WebDriverException:
        print(f'{url} es una URL inválida')

if __name__ == "__main__":
    main()
    driver.quit()
