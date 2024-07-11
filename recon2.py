import requests
from bs4 import BeautifulSoup
import time

# Palabras clave a buscar
keywords = ["access banking", "usuario", "clave", "icbc", "ingresar"]

# Leer los links desde el archivo
with open('potentialphishing.txt', 'r') as file:
    links = file.readlines()

# Limpiar los links para eliminar espacios en blanco
links = [link.strip() for link in links]

# Función para comprobar si una página contiene todas las palabras clave
def contains_all_keywords(url):
    try:
        # Verificar la accesibilidad del URL
        response = requests.head(url, allow_redirects=True, timeout=10)
        if response.status_code != 200:
            print(f"Error: {url} no es accesible (Código de estado: {response.status_code})")
            return False

        # Descargar el contenido de la página
        start_time = time.time()
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text().lower()
        elapsed_time = time.time() - start_time
        print(f"Tiempo de análisis para {url}: {elapsed_time:.2f} segundos")
        return all(keyword in text for keyword in keywords)
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return False

# Analizar cada link y recoger los que cumplen con las condiciones
matching_links = [link for link in links if contains_all_keywords(link)]

# Guardar los links que cumplen con las condiciones en un archivo
with open('links.txt', 'w') as file:
    for link in matching_links:
        file.write(link + '\n')

print("Páginas que contienen todas las palabras clave guardadas en links.txt.")
