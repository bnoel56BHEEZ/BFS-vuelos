import collections

# --- CLASE NODO (Original modificada ligeramente para mayor eficiencia) ---
class Nodo:
    def __init__(self, datos, padre=None):
        self.datos = datos
        self.padre = padre
        # En una implementación real de grafos, los hijos se calculan
        # dinámicamente, no se guardan en el nodo necesariamente.

    def get_datos(self):
        return self.datos
    
    def get_padre(self):
        return self.padre

    def __str__(self):
        return str(self.datos)

    # Definimos __eq__ y __hash__ para poder usar sets() en visitados
    # Esto hace la búsqueda mucho más rápida que buscar en una lista.
    def __eq__(self, otro):
        if not isinstance(otro, Nodo):
            return False
        return self.datos == otro.datos

    def __hash__(self):
        return hash(self.datos)

# --- DEFINICIÓN DEL PROBLEMA (Grafo de Vuelos) ---
# Un diccionario que representa las conexiones directas entre ciudades.
conexiones = {
    'CDMX': {'Guadalajara', 'Monterrey', 'Cancún', 'Mérida'},
    'Guadalajara': {'CDMX', 'Puerto Vallarta', 'Tijuana'},
    'Monterrey': {'CDMX', 'Cancún', 'Tijuana'},
    'Cancún': {'CDMX', 'Monterrey', 'Mérida'},
    'Mérida': {'CDMX', 'Cancún'},
    'Puerto Vallarta': {'Guadalajara'},
    'Tijuana': {'Guadalajara', 'Monterrey'}
}

# --- ALGORITMO BFS MODIFICADO ---
def buscar_solucion_BFS_vuelos(origen, destino):
    origen = origen.strip()
    destino = destino.strip()

    # Validaciones iniciales
    if origen not in conexiones or destino not in conexiones:
        return None, "Una o ambas ciudades no existen en la red de vuelos."
    
    if origen == destino:
        return [origen], "Ya estás en el destino."

    nodo_inicial = Nodo(origen)
    
    # Usamos collections.deque para una cola eficiente (O(1) popleft)
    nodos_frontera = collections.deque([nodo_inicial])
    
    # Usamos un set para visitados (búsqueda O(1) en promedio)
    # En tu código original usabas .en_lista() que es O(N), muy lento.
    nodos_visitados = set()
    nodos_visitados.add(origen)

    while nodos_frontera:
        # Tomamos el primer nodo (FIFO)
        nodo_actual = nodos_frontera.popleft()
        ciudad_actual = nodo_actual.get_datos()

        #--- TEST DE OBJETIVO ---
        if ciudad_actual == destino:
            # Reconstruir ruta
            ruta = []
            temp = nodo_actual
            while temp is not None:
                ruta.append(temp.get_datos())
                temp = temp.get_padre()
            ruta.reverse()
            return ruta, "Ruta encontrada"

        #--- EXPANDIR HIJOS (Usando el grafo) ---
        # Obtenemos los vecinos de la ciudad actual
        vecinos = conexiones.get(ciudad_actual, [])
        
        for vecino in vecinos:
            # Si no ha sido visitado, lo añadimos a frontera y visitados
            if vecino not in nodos_visitados:
                nodos_visitados.add(vecino)
                nuevo_hijo = Nodo(vecino, padre=nodo_actual)
                nodos_frontera.append(nuevo_hijo)

    return None, "No existe conexión entre estas ciudades."

# --- FUNCIÓN DE VISUALIZACIÓN ---
def visualizar_ruta(ruta, mensaje):
    print("\n" + "="*40)
    print(f"RESULTADO: {mensaje}")
    print("="*40)
    if ruta:
        print(" -> ".join(ruta))
        print(f"Total de escalas: {len(ruta) - 2}")
    print("="*40 + "\n")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    # Ciudades disponibles: CDMX, Guadalajara, Monterrey, Cancún, Mérida, Puerto Vallarta, Tijuana
    
    print("--- Buscador de Vuelos (BFS) ---")
    inicio = input("Ingrese ciudad de Origen: ").strip()
    fin = input("Ingrese ciudad de Destino: ").strip()
    
    ruta_res, msg = buscar_solucion_BFS_vuelos(inicio, fin)
    visualizar_ruta(ruta_res, msg)