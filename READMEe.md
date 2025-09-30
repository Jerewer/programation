# Codigo de Pokem0n
Pokémon Terminal: es un juego de combate por turnos inspirado en Pokémon, ejecutándose completamente en terminal/consola. Los jugadores pueden explorar un mapa, encontrar Pokémon salvajes y combatir con ellos usando un sistema de tipos y estados.
Características Principales:
- 6 tipos de Pokémon: Fuego, Agua, Planta, Normal, Metal, Tierra
- Sistema de combate por turnos con efectividad de tipos
- Estados alterados (quemado, envenenado, etc.)
- Sistema de guardado automático
- Mapa aleatorio con eventos
- Evoluciones y habilidades especiales

Clases:
1) Movimiento: ataques(invalido, basico, doble, turno perdido) el tipo de ataque depende del efecto random que toque al utilizar el ataque
2) Pokemon: en estas clases tenemos los tipos y aptitudes de cada pokemon, tambien se calculara el daño que puede hacer un pokemon a otro por su tipo de elemento ya que algunos dependiendo su elemento puedes ser ineficaces o muy eficaces.
dependiendo el elemento se le añadira un efecto como por ejemplo (Quemado, Mojado, Etc...) 
3) Tipo de pokemon: se creo una class para cada pokemon este caso 6 para especificar su tipo y aptitudes, ademas de añadirle su arte ASCII a cada pokemon.
4) Juego: en esta clase se crea el personaje que jugara nuestro juego se tiene que añadir (nombre del personaje, pokemon inicial e historial de combate)
Se muestra el menu de juego para cargar una partida anterior o iniciar una nueva, se genera el mapa y al mostrar el mapa en la parte de abajo te muestra las teclas de movimiento para avanzar por el mapa.
al interactuar con los pokemon que salen en el mapa te sale un menu para decidir si pelear o huir(no siempre se puede uir es random)
despues de la pelea te dejara continuar o guardar datos de la partida para continuarla despues ya que se guarda en un archivo JSON.