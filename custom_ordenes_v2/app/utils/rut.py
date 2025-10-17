import re

def normalizar_rut(rut: str) -> str:
    """
    Normaliza el RUT: sin puntos, con guión, en mayúscula.
    """
    if not rut:
        return ""
    rut = rut.strip().replace(".", "")
    rut = re.sub(r"[^\dkK\-]", "", rut)
    return rut.upper()
