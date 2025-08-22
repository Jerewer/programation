import biblioteca as gestor
import buscador as buscador
import estadisticas as stats

def main():
    
    mi_biblioteca = gestor.crear_biblioteca()
    
   
    print(gestor.agregar_libro(mi_biblioteca, "Cien años de soledad", "Gabriel García Márquez", 1967, "Realismo mágico"))
    print(gestor.agregar_libro(mi_biblioteca, "1984", "George Orwell", 1949, "Ciencia ficción"))
    print(gestor.agregar_libro(mi_biblioteca, "El principito", "Antoine de Saint-Exupéry", 1943, "Fábula"))
    print(gestor.agregar_libro(mi_biblioteca, "Crimen y castigo", "Fiódor Dostoyevski", 1866, "Novela psicológica"))
    
    
    print(gestor.marcar_leido(mi_biblioteca, 1))
    print(gestor.marcar_leido(mi_biblioteca, 3))
    
    
    print("\n" + gestor.mostrar_libros(mi_biblioteca))
    
    
    print(buscador.mostrar_resultados(buscador.buscar_por_autor(mi_biblioteca, "Orwell")))
    
    
    print(stats.mostrar_estadisticas(mi_biblioteca))
    
    
    while True:
        print("\n--- GESTIÓN DE BIBLIOTECA PERSONAL ---")
        print("1. Agregar libro")
        print("2. Marcar libro como leído")
        print("3. Buscar por título")
        print("4. Buscar por autor")
        print("5. Ver todos los libros")
        print("6. Ver estadísticas")
        print("7. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            año = input("Año: ")
            genero = input("Género: ")
            print(gestor.agregar_libro(mi_biblioteca, titulo, autor, año, genero))
        
        elif opcion == "2":
            print(gestor.mostrar_libros(mi_biblioteca))
            try:
                id_libro = int(input("ID del libro a marcar como leído: "))
                print(gestor.marcar_leido(mi_biblioteca, id_libro))
            except:
                print("ID inválido")
        
        elif opcion == "3":
            titulo = input("Título a buscar: ")
            resultados = buscador.buscar_por_titulo(mi_biblioteca, titulo)
            print(buscador.mostrar_resultados(resultados))
        
        elif opcion == "4":
            autor = input("Autor a buscar: ")
            resultados = buscador.buscar_por_autor(mi_biblioteca, autor)
            print(buscador.mostrar_resultados(resultados))
        
        elif opcion == "5":
            print(gestor.mostrar_libros(mi_biblioteca))
        
        elif opcion == "6":
            print(stats.mostrar_estadisticas(mi_biblioteca))
        
        elif opcion == "7":
            print("¡Hasta pronto!")
            break
        
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()