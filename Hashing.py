import sys

def simple_hash(text: str, base: int = 257, mod: int = 1_000_000_007) -> int:
    """Función de hash polinómico, típico en algoritmos como Rabin-Karp"""
    h = 0
    for c in text:
        h = (h * base + ord(c)) % mod
    return h

def collide_hash(text: str) -> int:
    """Hash simplificado para demostrar colisiones fácilmente"""
    if len(text) < 2:
        return ord(text[0]) % 50
    return (ord(text[0]) + ord(text[1])) % 50

class OpenHashTable:
    """Hashing abierto (encadenamiento) para manejo de colisiones"""
    def __init__(self, size=5):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        if len(key) < 2:
            return ord(key[0]) % self.size
        return (ord(key[0]) + ord(key[1])) % self.size

    def insert(self, key):
        idx = self._hash(key)
        if self.table[idx]:
            print(f" Colisión detectada: '{key}' entra donde ya está {self.table[idx]}")
        self.table[idx].append(key)

    def __repr__(self):
        return "\n".join(f"{i}: {bucket}" for i, bucket in enumerate(self.table))

class ClosedHashTable:
    """Hashing cerrado (dir. abierta, sondeo lineal) para manejo de colisiones"""
    def __init__(self, size=5):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        if len(key) < 2:
            return ord(key[0]) % self.size
        return (ord(key[0]) + ord(key[1])) % self.size

    def insert(self, key):
        idx = self._hash(key)
        start = idx
        if self.table[idx] is not None:
            print(f"Colisión: '{key}' no puede ir en {idx} porque ya está '{self.table[idx]}'")
        while self.table[idx] is not None:
            idx = (idx + 1) % self.size
            if idx == start:
                raise Exception("Tabla llena")
        print(f"'{key}' almacenado en posición {idx}")
        self.table[idx] = key

    def __repr__(self):
        return "\n".join(f"{i}: {val}" for i, val in enumerate(self.table))

class HashDemo:
    """Demo comparativa de funciones hash y su efecto"""
    def __init__(self, size=10, hash_func=None):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.hash_func = hash_func

    def insert(self, key):
        idx = self.hash_func(key) % self.size
        self.table[idx].append(key)

    def __repr__(self):
        return "\n".join(f"{i}: {bucket}" for i, bucket in enumerate(self.table))

def bad_hash(key: str) -> int:
    return ord(key[0])

def better_hash(key: str) -> int:
    h = 5381
    for c in key:
        h = (h * 33) ^ ord(c)
    return h


def menu():
    while True:
        print("\n▁▁▁▁▁▁▁▁▁ MENÚ DE HASHING ▁▁▁▁▁▁▁▁▁")
        print("1. Concepto de hashing y función hash")
        print("2. Demostración de colisión")
        print("3. Hashing abierto (Open Hash)")
        print("4. Hashing cerrado (Closed Hash/Open Addressing)")
        print("5. Comparativa de funciones hash + tabla")
        print("0. Salir")

        try:
            opc = int(input("Opción: "))
        except ValueError:
            print("Opción inválida.")
            continue

        if opc == 0:
            print("¡Saliendo!")
            sys.exit()
        elif opc == 1:
            print("\n--- CONCEPTO DE HASH ---")
            print("Ingrese nombres para ver su valor hash (0 para volver):")
            while True:
                name = input("  Nombre: ").strip()
                if name == "0":
                    break
                raw_hash = simple_hash(name)
                print(f"    Hash: {raw_hash}\n")
                
        elif opc == 2:
            print("\n--- DEMOSTRACIÓN DE COLISIÓN ---")
            for w in ["cama", "casa"]:
                print(f"  Hash('{w}'): {collide_hash(w)}")
            print("Observa que ambas palabras producen el mismo hash (colisión).")
            
        elif opc == 3:
            print("\n--- HASHING ABIERTO ---")
            ht_open = OpenHashTable()
            for w in ["casa", "cama"]:
                ht_open.insert(w)
            print("\nTabla Hash:")
            print(ht_open)
            
        elif opc == 4:
            print("\n--- HASHING CERRADO ---")
            ht_closed = ClosedHashTable()
            for w in ["casa", "cama"]:
                ht_closed.insert(w)
            print("\nTabla Hash:")
            print(ht_closed)

        elif opc == 5:
            print("\n--- COMPARATIVA DE FUNCIONES HASH ---")
            words = ["cama", "casa", "canto", "sol", "sal", "silla", "mesa", "misa", "museo"]
            ht_bad = HashDemo(hash_func=bad_hash)
            ht_better = HashDemo(hash_func=better_hash)
            for w in words:
                ht_bad.insert(w)
                ht_better.insert(w)
            print("Hash pésimo (muchas colisiones):")
            print(ht_bad)
            print("\nHash mejorado (colisiones mucho menos frecuentes):")
            print(ht_better)

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
