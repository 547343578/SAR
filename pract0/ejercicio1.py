
#ejercicio 1
import string
cadena = input("Introduce la cadena: ")
def IsPangrama(cadena):
    x = set(cadena.lower())
    y = set(string.ascii_lowercase)
    return True if x >= y else False

print(IsPangrama(cadena))



    