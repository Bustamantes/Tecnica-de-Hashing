# -*- coding: utf-8 -*-
"""
Demostración práctica de:
- Funciones hash
- Hashing abierto (encadenamiento)
- Hashing cerrado (open addressing)
- Manejo de colisiones
- Comparación simple y conclusiones
"""


# ===========================================================
#   1. FUNCIÓN HASH SENCILLA
# ===========================================================

def simple_hash(key: str, size: int) -> int:
    h = 0
    p = 31
    power = 1
    for ch in key:
        h += ord(ch) * power
        power *= p
    return h % size


# ===========================================================
#   2. HASHING ABIERTO (ENCADENAMIENTO)
# ===========================================================

class HashOpen:  # separate chaining
    def __init__(self, size=7):
        self.size = size
        self.table = [[] for _ in range(size)]

    def insert(self, key, value):
        idx = simple_hash(key, self.size)
        self.table[idx].append((key, value))

    def __str__(self):
        return "\n".join([f"{i}: {bucket}" for i, bucket in enumerate(self.table)])


# ===========================================================
#   3. HASHING CERRADO (OPEN ADDRESSING – LINEAR PROBING)
# ===========================================================

class HashClosed:
    def __init__(self, size=7):
        self.size = size
        self.table = [None] * size

    def insert(self, key, value):
        idx = simple_hash(key, self.size)
        start = idx

        while self.table[idx] is not None:
            idx = (idx + 1) % self.size
            if idx == start:  # tabla llena
                return False

        self.table[idx] = (key, value)
        return True

    def __str__(self):
        return "\n".join([f"{i}: {slot}" for i, slot in enumerate(self.table)])


# ===========================================================
#   4. DEMOSTRACIÓN DE COLISIONES
# ===========================================================

def demo_collisions():
    print("\n=== DEMO: Colisiones Prácticas ===")

    keys = ["Ana", "Aña", "Anb"]  # Fuerzan colisiones pequeñas
    size = 7

    open_table = HashOpen(size)
    closed_table = HashClosed(size)

    for k in keys:
        open_table.insert(k, f"valor_{k}")
        closed_table.insert(k, f"valor_{k}")

    print("\nHashing ABIERTO (encadenamiento):")
    print(open_table)

    print("\nHashing CERRADO (linear probing):")
    print(closed_table)


# ===========================================================
#   5. MINI DEMO INTERACTIVA
# ===========================================================

def demo_usuario():
    print("\n=== DEMO INTERACTIVA HASH ===")
    name = input("Nombre: ")
    password = input("Contraseña: ")

    key = f"{name}|{password}"
    size = 7
    h = simple_hash(key, size)

    print(f"\nHash generado: {h}  (dentro de una tabla de tamaño {size})")
    print("Esto determina la posición donde se almacenaría la clave.")


# ===========================================================
#   6. CONCLUSIONES PRÁCTICAS (IMPRIMIBLES)
# ===========================================================

def conclusiones():
    print("\n=== CONCLUSIONES PRÁCTICAS ===")
    print("- Hash abierto guarda colisiones dentro de listas.")
    print("- Hash cerrado busca la siguiente casilla libre.")
    print("- Una buena función hash reduce colisiones.")
    print("- Complejidad promedio de ambas: O(1).")
    print("- Peor caso: muchas colisiones → O(n).")


# ===========================================================
#   MAIN
# ===========================================================

def main():
    demo_collisions()
    demo_usuario()
    conclusiones()


if __name__ == "__main__":
    main()
