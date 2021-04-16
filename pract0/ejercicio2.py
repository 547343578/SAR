#ejercicio 2
import string
cadena = input("Introduce la cadena: ")
def IsPangramaPerfecto(cadena):
    x = cadena.lower()
    y = string.ascii_lowercase
    for letra in y:
        contador = 0
        if letra not in x:
            return False
        for letra2 in x:
            if letra == letra2:
                contador += 1
        if contador > 1:
            return False
    return True

print(IsPangramaPerfecto(cadena))

