def IsEquilibrado(cadena):
    contador = 0
    for letra in cadena:
        if letra == '[': contador += 1
        elif letra == ']': contador -= 1
    
    print( "OK" ) if contador == 0 else print("NOT OK")

IsEquilibrado(input("Introduce la cadena: "))