def funcion_grep(path,cadena):
    return [line.rstrip('\n') for line in open(path,'r',encoding='utf8') if cadena in line]

print(funcion_grep('D:\prueba.txt','la'))