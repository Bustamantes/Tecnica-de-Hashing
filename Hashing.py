# -*- coding: utf-8 -*-
"""Hashing simple interactivo:
Permite al usuario ingresar nombre y gmail, calcula un hash sencillo y muestra el
resultado (entero, hexadecimal y el índice en la tabla hash).
Incluye validación básica de email y opción para guardar el resultado en JSON.
"""

from typing import Any, List, Tuple, Optional
import re
import json


class SimpleHashTable:
    """Tabla hash con encadenamiento y una función hash sencilla (polynomial rolling)."""

    def __init__(self, size: int = 101) -> None:
        if size <= 0:
            raise ValueError("size debe ser un entero positivo")
        self.size: int = size
        self.table: List[List[Tuple[str, Any]]] = [[] for _ in range(self.size)]

    def _simple_hash(self, key: str) -> int:
        """Polinomial rolling hash simple.
        h = sum_{i}( ord(key[i]) * p^i ) mod M
        Usamos p = 31 y devolvemos un entero grande (sin modular) y el índice modular.
        """
        p = 31
        h = 0
        power = 1
        for ch in key:
            h += ord(ch) * power
            power *= p
        return h

    def _index_for(self, key: str) -> int:
        return self._simple_hash(key) % self.size

    def insert(self, key: str, value: Any) -> None:
        """Inserta o actualiza la clave en la tabla (encadenamiento)."""
        idx = self._index_for(key)
        bucket = self.table[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key: str) -> Optional[Any]:
        """Obtiene el valor asociado a la clave, o None si no existe."""
        idx = self._index_for(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None

    def delete(self, key: str) -> bool:
        """Elimina la clave si existe; retorna True si se eliminó."""
        idx = self._index_for(key)
        bucket = self.table[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False

    def __str__(self) -> str:
        """Representación breve por claves almacenadas."""
        items = []
        for bucket in self.table:
            items.extend(bucket)
        return "{" + ", ".join(f"{k}: {v}" for k, v in items) + "}"

    def bucket_info(self, key: str) -> Tuple[int, int]:
        """Devuelve (index, chain_length) para la clave."""
        idx = self._index_for(key)
        return idx, len(self.table[idx])


def is_valid_email(email: str) -> bool:
    """Validación simple y robusta para emails (no perfecta, pero útil)."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def prompt_input() -> Tuple[str, str]:
    """Solicita al usuario nombre y gmail con validación."""
    name = input("Ingrese su nombre: ").strip()
    while not name:
        print("El nombre no puede estar vacío. Intente nuevamente.")
        name = input("Ingrese su nombre: ").strip()

    email = input("Ingrese su Gmail (ej: usuario@gmail.com): ").strip()
    while not is_valid_email(email):
        print("Formato de email inválido. Asegúrese de ingresar un correo válido.")
        email = input("Ingrese su Gmail (ej: usuario@gmail.com): ").strip()

    return name, email


def save_result(path: str, data: dict) -> None:
    """Guarda el resultado en formato JSON (sobrescribe si existe)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> None:
    print("Hashing sencillo - ingrese nombre y gmail para obtener el hash resultante.")
    name, email = prompt_input()

    combined_key = f"{name}|{email}"
    ht = SimpleHashTable(size=101)

    # Calcula hash entero (raw) y el índice
    raw_hash = ht._simple_hash(combined_key)
    index = ht._index_for(combined_key)
    hex_hash = hex(raw_hash & ((1 << 64) - 1))  # mostrar menor representación hex (64-bit view)

    # Guardamos el resultado en la tabla con la clave (email) y datos
    value = {"name": name, "email": email, "raw_hash": raw_hash}
    ht.insert(email, value)

    # Mostrar resultados al usuario
    print("\nResultado:")
    print(f"  Nombre: {name}")
    print(f"  Email:  {email}")
    print(f"  Clave combinada: {combined_key}")
    print(f"  Hash (entero): {raw_hash}")
    print(f"  Hash (hex, 64-bit view): {hex_hash}")
    print(f"  Índice en tabla (size={ht.size}): {index}")
    idx, chain_len = ht.bucket_info(email)
    print(f"  Longitud de la cadena en ese bucket: {chain_len}")
    print(f"\nContenido de la tabla hash (resumen): {ht}")

    # Opción para guardar
    guardar = input("\n¿Desea guardar este resultado en 'hash_result.json'? (s/n): ").strip().lower()
    if guardar in {"s", "si", "y", "yes"}:
        data = {
            "name": name,
            "email": email,
            "combined_key": combined_key,
            "raw_hash": raw_hash,
            "hex_hash": hex_hash,
            "index": index,
            "table_size": ht.size,
        }
        save_result("hash_result.json", data)
        print("Guardado en 'hash_result.json'.")

    print("\nProceso finalizado.")


if __name__ == "__main__":
    main()
