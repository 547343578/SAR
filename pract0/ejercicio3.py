#ejercicio 3
import string
cadena = input("Introduce la cadena: ")
cadena2 = input("Introduce la cadena2 : ")

def IsAnagrama(cadena,cadena2):
    x = list(cadena.lower())
    y = list(cadena2.lower())
    xNuevo = list()
    yNuevo = list()
    
    for i in x:
        if i in string.ascii_lowercase:
            xNuevo.append(i)
    for j in y:
        if j in string.ascii_lowercase:
            yNuevo.append(j)        
    xNuevo.sort()
    yNuevo.sort()
    print(xNuevo,yNuevo)
    pos = 0
    matches = True
    if(len(xNuevo) != len(yNuevo)): return False
    while pos < len(xNuevo) and matches:
        if xNuevo[pos] == yNuevo[pos]:
            pos = pos + 1
        else :
            matches = False
    return matches

print(IsAnagrama(cadena,cadena2))
