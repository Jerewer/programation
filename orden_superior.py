import sys
import random

def generar_tareas(n):
    tareas = []
    acciones = ["Hacer", "Revisar", "Terminar", "Estudiar"]
    temas = ["informe", "código", "tarea", "proyecto"]
    
    for i in range(n):
        tarea = {
            "id": i + 1,
            "nombre": f"{random.choice(acciones)} {random.choice(temas)}",
            "prioridad": random.choice(["Alta", "Media", "Baja"]),
            "hecha": random.choice([True, False])
        }
        tareas.append(tarea)
    
    return tareas

def mostrar_tareas(tareas, filtro=None):
    if filtro:
        tareas = [t for t in tareas if t["prioridad"] == filtro]
        print(f"\nTareas {filtro}:")
    
    for t in tareas:
        check = "✓" if t["hecha"] else "✗"
        print(f"{t['id']}. [{check}] {t['nombre']}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python tareas.py <cantidad> [alta|media|baja]")
        return
    
    try:
        n = int(sys.argv[1])
        tareas = generar_tareas(n)
        
        if len(sys.argv) > 2:
            filtro = sys.argv[2].capitalize()
            if filtro in ["Alta", "Media", "Baja"]:
                mostrar_tareas(tareas, filtro)
            else:
                mostrar_tareas(tareas)
        else:
            mostrar_tareas(tareas)
            
    except ValueError:
        print("Error: La cantidad debe ser un número")

if __name__ == "__main__":
    main()
