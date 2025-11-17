# -*- coding: utf-8 -*-
"""Hash mínimo: nombre + contraseña → hash entero."""

def simple_hash(text: str) -> int:
    h = 0
    p = 31
    power = 1
    for ch in text:
        h += ord(ch) * power
        power *= p
    return h

def main():
    name = input("Nombre: ").strip()
    password = input("Contraseña: ").strip()

    key = f"{name}|{password}"
    raw_hash = simple_hash(key)

    print("\nResultado:")
    print(f"  Nombre: {name}")
    print(f"  Contraseña: {password}")
    print(f"  Hash: {raw_hash}")

if __name__ == "__main__":
    main()
