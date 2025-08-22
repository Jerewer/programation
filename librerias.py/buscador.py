def buscar_por_titulo(biblioteca, titulo):
    resultados = []
    for libro in biblioteca["libros"]:
        if titulo.lower() in libro["titulo"].lower():
            resultados.append(libro)
    return resultados

def buscar_por_autor(biblioteca, autor):
    resultados = []
    for libro in biblioteca["libros"]:
        if autor.lower() in libro["autor"].lower():
            resultados.append(libro)
    return resultados

def buscar_por_genero(biblioteca, genero):
    resultados = []
    for libro in biblioteca["libros"]:
        if genero.lower() in libro["genero"].lower():
            resultados.append(libro)
    return resultados

def mostrar_resultados(resultados):
    if not resultados:
        return "No se encontraron resultados"
    
    texto = "RESULTADOS DE BÚSQUEDA:\n"
    for libro in resultados:
        estado = "Leído" if libro["leido"] else "Por leer"
        texto += f"- {libro['titulo']} por {libro['autor']} ({libro['año']}) - {estado}\n"
    return texto
