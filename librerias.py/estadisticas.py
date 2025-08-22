def total_libros(biblioteca):
    return len(biblioteca["libros"])

def libros_leidos(biblioteca):
    contador = 0
    for libro in biblioteca["libros"]:
        if libro["leido"]:
            contador += 1
    return contador

def porcentaje_leidos(biblioteca):
    total = total_libros(biblioteca)
    if total == 0:
        return 0
    leidos = libros_leidos(biblioteca)
    return (leidos / total) * 100

def generos_comunes(biblioteca):
    generos = {}
    for libro in biblioteca["libros"]:
        if libro["genero"] in generos:
            generos[libro["genero"]] += 1
        else:
            generos[libro["genero"]] = 1
    
    
    generos_ordenados = sorted(generos.items(), key=lambda x: x[1], reverse=True)
    return generos_ordenados[:3]  

def mostrar_estadisticas(biblioteca):
    if not biblioteca["libros"]:
        return "No hay libros en la biblioteca para mostrar estadísticas"
    
    stats = "ESTADÍSTICAS DE LA BIBLIOTECA:\n"
    stats += f"Total de libros: {total_libros(biblioteca)}\n"
    stats += f"Libros leídos: {libros_leidos(biblioteca)}\n"
    stats += f"Porcentaje leído: {porcentaje_leidos(biblioteca):.1f}%\n"
    
    top_generos = generos_comunes(biblioteca)
    stats += "Géneros más comunes:\n"
    for genero, cantidad in top_generos:
        stats += f"- {genero}: {cantidad} libro(s)\n"
    
    return stats