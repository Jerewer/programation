estudiantes = {
    "A001": {"nombre": "Ana Torres", "edad": 20, "calificaciones": [90, 85, 78]},
    "A002": {"nombre": "Luis Pérez", "edad": 22, "calificaciones": [88, 91, 79]}
}

def mostrar_menu():
    print("\nGestor de Estudiantes")
    print("1. Agregar estudiante")
    print("2. Mostrar estudiantes")
    print("3. Calcular promedio")
    print("4. Eliminar estudiante")
    print("5. Salir")

def agregar_estudiante():
    id_est = input("ID: ").upper()
    if id_est in estudiantes:
        print("ID ya existe")
        return
    
    nombre = input("Nombre: ")
    
    try:
        edad = int(input("Edad: "))
    except:
        print("Edad debe ser número")
        return
    
    califs = []
    print("Calificaciones (enter para terminar):")
    while True:
        calif = input("Calificación: ")
        if not calif:
            break
        try:
            califs.append(float(calif))
        except:
            print("Calificación debe ser número")
    
    estudiantes[id_est] = {
        "nombre": nombre,
        "edad": edad,
        "calificaciones": califs
    }
    print("Estudiante agregado")

def mostrar_estudiantes():
    if not estudiantes:
        print("No hay estudiantes")
        return
    
    for id_est, datos in estudiantes.items():
        califs = datos["calificaciones"]
        promedio = sum(califs) / len(califs) if califs else 0
        print(f"{id_est} - {datos['nombre']} - Promedio: {promedio:.1f}")

def calcular_promedio():
    id_est = input("ID del estudiante: ").upper()
    if id_est not in estudiantes:
        print("Estudiante no encontrado")
        return
    
    califs = estudiantes[id_est]["calificaciones"]
    if not califs:
        print("No tiene calificaciones")
        return
    
    promedio = sum(califs) / len(califs)
    print(f"Promedio: {promedio:.1f}")

def eliminar_estudiante():
    id_est = input("ID del estudiante a eliminar: ").upper()
    if id_est not in estudiantes:
        print("Estudiante no encontrado")
        return
    
    del estudiantes[id_est]
    print("Estudiante eliminado")

while True:
    mostrar_menu()
    opcion = input("Opción: ")
    
    if opcion == "1":
        agregar_estudiante()
    elif opcion == "2":
        mostrar_estudiantes()
    elif opcion == "3":
        calcular_promedio()
    elif opcion == "4":
        eliminar_estudiante()
    elif opcion == "5":
        print("Adiós")
        break
    else:
        print("Opción no válida")
