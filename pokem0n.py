import random
import time
import os
import json
from abc import ABC, abstractmethod

class Movimiento:
    def __init__(self, nombre, poder, tipo):
        self.nombre = nombre
        self.poder = poder
        self.tipo = tipo
    
    def atacar(self):
        efecto = random.randint(1, 100)
        if efecto <= 10:
            return 0, "Sin efecto"
        elif efecto <= 70:
            return self.poder, "Ataque básico"
        elif efecto <= 90:
            return self.poder * 2, "Ataque doble"
        else:
            return self.poder, "Ataque pierde turno"

class Pokemon(ABC):
    def __init__(self, nombre, tipo, ataque, defensa, hp, habilidad, movimientos, arte_ascii):
        self.nombre = nombre
        self.tipo = tipo
        self.ataque = ataque
        self.defensa = defensa
        self.hp_max = hp
        self.hp_actual = hp
        self.habilidad = habilidad
        self.movimientos = movimientos
        self.arte_ascii = arte_ascii
        self.estado = "normal"  # nuevo atributo para estados como quemado, envenenado, etc.
    
    def atacar(self, movimiento_idx, objetivo):
        if movimiento_idx >= len(self.movimientos):
            return 0, "Movimiento no válido"
        
        movimiento = self.movimientos[movimiento_idx]
        danio_base, mensaje = movimiento.atacar()
        
        efectividad = self.calcular_efectividad(movimiento.tipo, objetivo.tipo)
        stab = 1.5 if movimiento.tipo == self.tipo else 1.0
        
        danio_final = int(danio_base * efectividad * stab)
        danio_recibido = objetivo.recibir_danio(danio_final)
        
        # Aplicar efecto de estado basado en el tipo de ataque
        efecto_estado = self.aplicar_efecto_estado(movimiento.tipo, objetivo)
        
        return danio_final, f"{mensaje} - Efectividad: {efectividad}x{efecto_estado}"
    
    def calcular_efectividad(self, tipo_ataque, tipo_defensa):
        tabla_efectividad = {
            'fuego': {'fuego': 0.5, 'agua': 0.5, 'planta': 2.0, 'normal': 1.0, 'metal': 2.0, 'tierra': 1.0},
            'agua': {'fuego': 2.0, 'agua': 0.5, 'planta': 0.5, 'normal': 1.0, 'metal': 1.0, 'tierra': 2.0},
            'planta': {'fuego': 0.5, 'agua': 2.0, 'planta': 0.5, 'normal': 1.0, 'metal': 0.5, 'tierra': 2.0},
            'normal': {'fuego': 1.0, 'agua': 1.0, 'planta': 1.0, 'normal': 1.0, 'metal': 0.5, 'tierra': 1.0},
            'metal': {'fuego': 0.5, 'agua': 0.5, 'planta': 1.0, 'normal': 1.0, 'metal': 0.5, 'tierra': 2.0},
            'tierra': {'fuego': 2.0, 'agua': 1.0, 'planta': 0.5, 'normal': 1.0, 'metal': 2.0, 'tierra': 1.0}
        }
        return tabla_efectividad.get(tipo_ataque, {}).get(tipo_defensa, 1.0)
    
    def aplicar_efecto_estado(self, tipo_ataque, objetivo):
        efectos = {
            'fuego': (0.2, "quemado"),
            'agua': (0.1, "mojado"), 
            'planta': (0.15, "envenenado"),
            'metal': (0.1, "magnetizado"),
            'tierra': (0.25, "atrapado")
        }
        
        if tipo_ataque in efectos and random.random() < efectos[tipo_ataque][0]:
            objetivo.estado = efectos[tipo_ataque][1]
            return f" - ¡{objetivo.nombre} quedó {objetivo.estado}!"
        return ""
    
    def recibir_danio(self, danio):
        # Reducción de daño por estado de defensa
        if self.estado == "magnetizado":
            danio = max(1, danio - 5)  # Metal reduce daño extra
        
        danio_real = max(0, danio - self.defensa)
        self.hp_actual = max(0, self.hp_actual - danio_real)
        
        # Daño por estado después del ataque
        danio_estado = self.aplicar_danio_estado()
        
        return danio_real + danio_estado
    
    def aplicar_danio_estado(self):
        if self.estado == "quemado":
            danio = max(1, self.hp_max // 16)
            self.hp_actual = max(0, self.hp_actual - danio)
            return danio
        elif self.estado == "envenenado":
            danio = max(1, self.hp_max // 8)
            self.hp_actual = max(0, self.hp_actual - danio)
            return danio
        return 0
    
    def usar_habilidad(self):
        if self.habilidad == "Curación":
            curacion = self.hp_max * 0.2
            self.hp_actual = min(self.hp_max, self.hp_actual + curacion)
            self.estado = "normal"  # Curar estado
            return f"{self.nombre} usó {self.habilidad} y recuperó {curacion} HP"
        elif self.habilidad == "Ataque Plus":
            self.ataque += 5
            return f"{self.nombre} usó {self.habilidad} y aumentó su ataque"
        elif self.habilidad == "Defensa Plus":
            self.defensa += 5
            return f"{self.nombre} usó {self.habilidad} y aumentó su defensa"
        else:
            return f"{self.nombre} usó {self.habilidad} pero no tuvo efecto"
    
    def esta_vivo(self):
        return self.hp_actual > 0
    
    @abstractmethod
    def evolucionar(self):
        pass

# POKÉMON DE FUEGO
class Flamigator(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Llamarada", 40, "fuego"),
            Movimiento("Colmillo Ígneo", 35, "fuego"),
            Movimiento("Arañazo", 25, "normal"),
            Movimiento("Gruñido", 0, "normal")
        ]
        arte = """
  /\\_____/\\
 /  o   o  \\
( ==  ^  == )
 )         (
 (         )
 ( (  ) (  )
 (__(__)__)
        """
        super().__init__("Flamigator", "fuego", 55, 40, 100, "Curación", movimientos, arte)
    
    def evolucionar(self):
        return "Flamigator no puede evolucionar aún"

class PyroWing(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Ala de Fuego", 45, "fuego"),
            Movimiento("Picotazo", 30, "normal"),
            Movimiento("Vuelo", 0, "normal"),
            Movimiento("Llamarada", 40, "fuego")
        ]
        arte = """
    /\\
   /  \\
  /o   \\
 /      \\
/________\\
   |  |
        """
        super().__init__("PyroWing", "fuego", 53, 38, 90, "Curación", movimientos, arte)
    
    def evolucionar(self):
        return "PyroWing evoluciona a InfernoBird al nivel 28"

# POKÉMON DE AGUA
class AquaPup(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Chorro", 45, "agua"),
            Movimiento("Burbujas", 30, "agua"),
            Movimiento("Placaje", 20, "normal"),
            Movimiento("Defensa Acuosa", 0, "agua")
        ]
        arte = """
   /\\___/\\
  ( o   o )
 (   =^=   )
 /         \\
(           )
 \\(       )/
  \\_____ /
        """
        super().__init__("AquaPup", "agua", 50, 45, 110, "Ataque Plus", movimientos, arte)
    
    def evolucionar(self):
        return "AquaPup evoluciona a HydroHound al nivel 25"

# POKÉMON DE PLANTA
class LeafKitten(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Hoja Afilada", 40, "planta"),
            Movimiento("Látigo Cepa", 35, "planta"),
            Movimiento("Arañazo", 25, "normal"),
            Movimiento("Síntesis", 0, "planta")
        ]
        arte = """
  /\\___/\\
 ( ^   ^ )
(   \\_/   )
 \\       /
  \\_____/
   |   |
        """
        super().__init__("LeafKitten", "planta", 52, 48, 105, "Curación", movimientos, arte)
    
    def evolucionar(self):
        return "LeafKitten evoluciona a FloraCat al nivel 22"

# POKÉMON NORMAL
class NormalFox(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Hiperrayo", 60, "normal"),
            Movimiento("Ataque Rápido", 30, "normal"),
            Movimiento("Mordisco", 35, "normal"),
            Movimiento("Descanso", 0, "normal")
        ]
        arte = """
  /\\___/\\
 ( -   - )
(   >^<   )
 \\       /
  \\_____/
   |   |
        """
        super().__init__("NormalFox", "normal", 58, 42, 95, "Ataque Plus", movimientos, arte)
    
    def evolucionar(self):
        return "NormalFox no evoluciona"

# POKÉMON DE METAL (NUEVO)
class MetalMite(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Golpe Férreo", 50, "metal"),
            Movimiento("Garrote", 35, "normal"),
            Movimiento("Magnetismo", 0, "metal"),
            Movimiento("Defensa Metálica", 0, "metal")
        ]
        arte = """
    _____
   /     \\
  | [ ] | |
  |_____| |
  /       \\
 /_________\\
        """
        super().__init__("MetalMite", "metal", 48, 60, 120, "Defensa Plus", movimientos, arte)
    
    def evolucionar(self):
        return "MetalMite evoluciona a TitaniumBeetle al nivel 30"

# POKÉMON DE TIERRA (NUEVO)
class TerraTortle(Pokemon):
    def __init__(self):
        movimientos = [
            Movimiento("Terremoto", 55, "tierra"),
            Movimiento("Roca Afilada", 40, "tierra"),
            Movimiento("Excavar", 30, "tierra"),
            Movimiento("Fortificar", 0, "tierra")
        ]
        arte = """
   _______
  /       \\
 /         \\
|    ___    |
|   |   |   |
 \\_________/
        """
        super().__init__("TerraTortle", "tierra", 54, 55, 115, "Defensa Plus", movimientos, arte)
    
    def evolucionar(self):
        return "TerraTortle evoluciona a GeoGiant al nivel 32"

class Juego:
    def __init__(self):
        self.jugador = None
        self.mapa = []
        self.pokemons_disponibles = [Flamigator, AquaPup, LeafKitten, NormalFox, PyroWing, MetalMite, TerraTortle]
        self.historial_combates = []
        self.tamano_mapa = 10
    
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_menu_principal(self):
        while True:
            self.limpiar_pantalla()
            print("=== POKÉMON TERMINAL ===")
            print("1. Crear partida")
            print("2. Continuar partida")
            print("3. Borrar partida")
            print("4. Salir")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.crear_partida()
            elif opcion == "2":
                self.continuar_partida()
            elif opcion == "3":
                self.borrar_partida()
            elif opcion == "4":
                print("¡Hasta pronto!")
                break
            else:
                print("Opción no válida")
                time.sleep(1)
    
    def crear_partida(self):
        self.limpiar_pantalla()
        nombre_jugador = input("Ingresa tu nombre: ")
        
        print("\nElige tu Pokémon inicial:")
        print("1. Flamigator (Fuego)")
        print("2. AquaPup (Agua)")
        print("3. LeafKitten (Planta)")
        print("4. MetalMite (Metal)")
        print("5. TerraTortle (Tierra)")
        
        while True:
            opcion = input("Selecciona (1-5): ")
            if opcion == "1":
                pokemon_inicial = Flamigator()
                break
            elif opcion == "2":
                pokemon_inicial = AquaPup()
                break
            elif opcion == "3":
                pokemon_inicial = LeafKitten()
                break
            elif opcion == "4":
                pokemon_inicial = MetalMite()
                break
            elif opcion == "5":
                pokemon_inicial = TerraTortle()
                break
            else:
                print("Opción no válida")
        
        self.jugador = {
            'nombre': nombre_jugador,
            'equipo': [pokemon_inicial],
            'pokemon_actual': 0,
            'posicion': [self.tamano_mapa//2, self.tamano_mapa//2],
            'combates_ganados': 0,
            'combates_perdidos': 0
        }
        
        self.generar_mapa()
        self.guardar_partida()
        self.menu_exploracion()
    
    def generar_mapa(self):
        self.mapa = [['.' for _ in range(self.tamano_mapa)] for _ in range(self.tamano_mapa)]
        
        for _ in range(5):
            x, y = random.randint(0, self.tamano_mapa-1), random.randint(0, self.tamano_mapa-1)
            self.mapa[y][x] = '🐾'
        
        for _ in range(3):
            x, y = random.randint(0, self.tamano_mapa-1), random.randint(0, self.tamano_mapa-1)
            self.mapa[y][x] = '🌿'
    
    def mostrar_mapa(self):
        self.limpiar_pantalla()
        print("=== MAPA ===")
        for y in range(self.tamano_mapa):
            for x in range(self.tamano_mapa):
                if x == self.jugador['posicion'][0] and y == self.jugador['posicion'][1]:
                    print('😀', end=' ')
                else:
                    print(self.mapa[y][x], end=' ')
            print()
        
        print("\nControles: W-Arriba, A-Izquierda, S-Abajo, D-Derecha")
        print("M - Menú, V - Volver, H - Historial")
    
    def menu_exploracion(self):
        while True:
            self.mostrar_mapa()
            comando = input("\n> ").lower()
            
            if comando == 'm':
                self.menu_estados()
            elif comando == 'v':
                break
            elif comando == 'h':
                self.mostrar_historial()
            elif comando in ['w', 'a', 's', 'd']:
                self.mover_jugador(comando)
                self.verificar_evento()
            else:
                print("Comando no válido")
    
    def mover_jugador(self, direccion):
        x, y = self.jugador['posicion']
        
        if direccion == 'w' and y > 0:
            y -= 1
        elif direccion == 's' and y < self.tamano_mapa - 1:
            y += 1
        elif direccion == 'a' and x > 0:
            x -= 1
        elif direccion == 'd' and x < self.tamano_mapa - 1:
            x += 1
        
        self.jugador['posicion'] = [x, y]
    
    def verificar_evento(self):
        x, y = self.jugador['posicion']
        celda = self.mapa[y][x]
        
        if celda in ['🐾', '🌿']:
            if random.random() < 0.7:
                self.iniciar_combate()
                self.mapa[y][x] = '.'
    
    def iniciar_combate(self):
        pokemon_salvaje_clase = random.choice(self.pokemons_disponibles)
        pokemon_salvaje = pokemon_salvaje_clase()
        
        pokemon_jugador = self.jugador['equipo'][self.jugador['pokemon_actual']]
        
        print(f"¡Un {pokemon_salvaje.nombre} salvaje apareció!")
        time.sleep(1)
        
        while pokemon_jugador.esta_vivo() and pokemon_salvaje.esta_vivo():
            self.limpiar_pantalla()
            print(f"Tu {pokemon_jugador.nombre}: {pokemon_jugador.hp_actual}/{pokemon_jugador.hp_max} HP")
            print(f"Estado: {pokemon_jugador.estado}")
            print(f"{pokemon_salvaje.nombre} salvaje: {pokemon_salvaje.hp_actual}/{pokemon_salvaje.hp_max} HP")
            print(f"Estado: {pokemon_salvaje.estado}")
            print("\n1. Luchar")
            print("2. Estado")
            print("3. Huir")
            
            opcion = input("Selecciona: ")
            
            if opcion == "1":
                self.menu_luchar(pokemon_jugador, pokemon_salvaje)
            elif opcion == "2":
                self.mostrar_estado_pokemon(pokemon_jugador)
                input("Presiona Enter para continuar...")
                continue
            elif opcion == "3":
                if random.random() < 0.5:
                    print("¡Lograste huir!")
                    time.sleep(1)
                    return
                else:
                    print("¡No pudiste huir!")
                    time.sleep(1)
            
            # Aplicar daño por estado antes del ataque del oponente
            if pokemon_jugador.estado != "normal":
                danio_estado = pokemon_jugador.aplicar_danio_estado()
                if danio_estado > 0:
                    print(f"¡{pokemon_jugador.nombre} sufre daño por {pokemon_jugador.estado}!")
                    time.sleep(1)
            
            if pokemon_salvaje.esta_vivo():
                movimiento_salvaje = random.randint(0, len(pokemon_salvaje.movimientos)-1)
                danio, mensaje = pokemon_salvaje.atacar(movimiento_salvaje, pokemon_jugador)
                print(f"¡{pokemon_salvaje.nombre} usó {pokemon_salvaje.movimientos[movimiento_salvaje].nombre}!")
                print(mensaje)
                print(f"Tu {pokemon_jugador.nombre} recibió {danio} de daño")
                time.sleep(2)
        
        if pokemon_jugador.esta_vivo():
            print(f"¡Derrotaste al {pokemon_salvaje.nombre} salvaje!")
            self.jugador['combates_ganados'] += 1
            self.historial_combates.append(f"Victoria contra {pokemon_salvaje.nombre}")
        else:
            print("¡Tu Pokémon fue derrotado!")
            self.jugador['combates_perdidos'] += 1
            self.historial_combates.append(f"Derrota contra {pokemon_salvaje.nombre}")
        
        self.guardar_partida()
        input("Presiona Enter para continuar...")
    
    def menu_luchar(self, pokemon_jugador, pokemon_salvaje):
        print("\nElige un movimiento:")
        for i, movimiento in enumerate(pokemon_jugador.movimientos):
            print(f"{i+1}. {movimiento.nombre} ({movimiento.tipo}) - Poder: {movimiento.poder}")
        
        try:
            opcion = int(input("Selecciona: ")) - 1
            if 0 <= opcion < len(pokemon_jugador.movimientos):
                danio, mensaje = pokemon_jugador.atacar(opcion, pokemon_salvaje)
                print(f"¡{pokemon_jugador.nombre} usó {pokemon_jugador.movimientos[opcion].nombre}!")
                print(mensaje)
                print(f"El {pokemon_salvaje.nombre} salvaje recibió {danio} de daño")
                time.sleep(2)
            else:
                print("Movimiento no válido")
                time.sleep(1)
        except ValueError:
            print("Opción no válida")
            time.sleep(1)
    
    def menu_estados(self):
        while True:
            self.limpiar_pantalla()
            print("=== ESTADO DEL EQUIPO ===")
            for i, pokemon in enumerate(self.jugador['equipo']):
                estado = "✓" if pokemon.esta_vivo() else "✗"
                estado_efecto = f" [{pokemon.estado}]" if pokemon.estado != "normal" else ""
                print(f"{i+1}. {pokemon.nombre} ({pokemon.tipo}) - HP: {pokemon.hp_actual}/{pokemon.hp_max} {estado}{estado_efecto}")
            
            print("\n1. Ver detalles")
            print("2. Usar habilidad")
            print("3. Volver")
            
            opcion = input("Selecciona: ")
            
            if opcion == "1":
                try:
                    idx = int(input("Número del Pokémon: ")) - 1
                    if 0 <= idx < len(self.jugador['equipo']):
                        self.mostrar_estado_pokemon(self.jugador['equipo'][idx])
                        input("Presiona Enter para continuar...")
                except ValueError:
                    print("Opción no válida")
                    time.sleep(1)
            elif opcion == "2":
                try:
                    idx = int(input("Número del Pokémon: ")) - 1
                    if 0 <= idx < len(self.jugador['equipo']):
                        resultado = self.jugador['equipo'][idx].usar_habilidad()
                        print(resultado)
                        time.sleep(1)
                except ValueError:
                    print("Opción no válida")
                    time.sleep(1)
            elif opcion == "3":
                break
            else:
                print("Opción no válida")
                time.sleep(1)
    
    def mostrar_estado_pokemon(self, pokemon):
        print(pokemon.arte_ascii)
        print(f"Nombre: {pokemon.nombre}")
        print(f"Tipo: {pokemon.tipo}")
        print(f"HP: {pokemon.hp_actual}/{pokemon.hp_max}")
        print(f"Ataque: {pokemon.ataque}")
        print(f"Defensa: {pokemon.defensa}")
        print(f"Habilidad: {pokemon.habilidad}")
        print(f"Estado: {pokemon.estado}")
        print("Movimientos:")
        for movimiento in pokemon.movimientos:
            print(f"  - {movimiento.nombre} ({movimiento.tipo}) - Poder: {movimiento.poder}")
        print(pokemon.evolucionar())
    
    def mostrar_historial(self):
        self.limpiar_pantalla()
        print("=== HISTORIAL DE COMBATES ===")
        if not self.historial_combates:
            print("No hay combates registrados")
        else:
            for combate in self.historial_combates[-10:]:
                print(f"- {combate}")
        input("\nPresiona Enter para continuar...")
    
    def guardar_partida(self):
        if self.jugador:
            datos = {
                'jugador': self.jugador,
                'historial': self.historial_combates
            }
            with open('partida_guardada.json', 'w') as f:
                json.dump(datos, f, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else str(o))
    
    def cargar_partida(self):
        try:
            with open('partida_guardada.json', 'r') as f:
                datos = json.load(f)
            
            self.jugador = datos['jugador']
            self.historial_combates = datos['historial']
            
            for i, pokemon_data in enumerate(self.jugador['equipo']):
                clase_pokemon = globals()[pokemon_data['nombre']]
                pokemon = clase_pokemon()
                pokemon.__dict__.update(pokemon_data)
                self.jugador['equipo'][i] = pokemon
            
            self.generar_mapa()
            return True
        except:
            return False
    
    def continuar_partida(self):
        if self.cargar_partida():
            self.menu_exploracion()
        else:
            print("No hay partida guardada")
            time.sleep(1)
    
    def borrar_partida(self):
        try:
            os.remove('partida_guardada.json')
            print("Partida borrada")
        except:
            print("No hay partida para borrar")
        time.sleep(1)

if __name__ == "__main__":
    juego = Juego()
    juego.mostrar_menu_principal()