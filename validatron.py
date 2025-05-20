import random
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)


def obtener_password_aleatorio_de_archivo(filename="passwords.txt"):
    try:
        with open(filename, "r") as f:
            contenido = f.read()
    except FileNotFoundError:
        return None

    if not contenido:
        return None

    longitud_contenido = int(len(contenido))
    intentos = 0
    max_intentos = 100  # Para evitar bucles infinitos en archivos muy cortos

    while intentos < max_intentos:
        start = random.randint(0, 10000)
        end = start + random.randint(5, 8)
        password_aleatorio = contenido[start:end]
        longitud_password = len(password_aleatorio)
        if 5 <= longitud_password <= 8:
            print(f"El password elegido fue: {password_aleatorio}")
            return password_aleatorio
        intentos += 1
    return None  # No se pudo encontrar una contraseña válida después de varios intentos


password_correcto = obtener_password_aleatorio_de_archivo()


@app.route("/login", methods=["GET"])
def verificar_password():
    password_ingresado = request.args.get("password")
    global password_correcto
    if not password_ingresado:
        return jsonify({"error": "Se requiere el parámetro 'password' en la URL"}), 400

    acierto = password_ingresado == password_correcto
    return jsonify({"acierto": acierto, "password_correcto": password_correcto})


if __name__ == "__main__":

    app.run(debug=True)
