# -*- coding: utf-8 -*-
"""Hashing
Solicita nombre y Gmail, calcula un hash entero y muestra el resultado.
"""

from typing import Any, List, Tuple
import re


class SimpleHashTable:
    """Tabla hash con encadenamiento y hash polinomial sencillo."""

    def __init__(self, size: int = 101) -> None:
        if size <= 0:
            raise ValueError("El tamaño debe ser un entero positivo.")
        self.size = size
        self.table: List[List[Tuple[str, Any]]] = [[] for _ in range(size)]

    def _simple_hash(self, key: str) -> int:
        """Hash polinomial sin modular (enteros grandes)."""
        h = 0
        p = 31
        power = 1
        for ch in key:
            h += ord(ch) * power
            power *= p
        return h

    def _index_for(self, key: str) -> int:
        return self._simple_hash(key) % self.size

    def insert(self, key: str, value: Any) -> None:
        idx = self._index_for(key)
        bucket = self.table[idx]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def __str__(self) -> str:
        items = [f"{k}: {v}" for bucket in self.table for k, v in bucket]
        return "{" + ", ".join(items) + "}"


def is_valid_email(email: str) -> bool:
    patrón = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(patrón, email) is not None


def prompt_input() -> Tuple[str, str]:
    name = input("Ingrese su nombre: ").strip()
    while not name:
        print("El nombre no puede estar vacío.")
        name = input("Ingrese su nombre: ").strip()

    email = input("Ingrese su Gmail: ").strip()
    while not is_valid_email(email):
        print("Email inválido, intente de nuevo.")
        email = input("Ingrese su Gmail: ").strip()

    return name, email


def main() -> None:
    print("=== Hashing sencillo ===")
    name, email = prompt_input()

    key = f"{name}|{email}"
    ht = SimpleHashTable()

    raw_hash = ht._simple_hash(key)
    ht.insert(email, {"name": name, "email": email, "hash": raw_hash})

    print("\nResultado:")
    print(f"  Nombre: {name}")
    print(f"  Email: {email}")
    print(f"  Hash (entero): {raw_hash}")
    print(f"\nTabla hash (resumen): {ht}")

    print("\nProceso finalizado.")


if __name__ == "__main__":
    main()
