#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys

## Nombres: ZhuQing Wang

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################



def sort_index(d):
    for k in d:
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]')
        self.r2 = re.compile('\W+')


    def index_sentence(self, sentence, tri):
        #############
        # COMPLETAR #
        #############
        frase = self.r2.sub(' ', sentence).split()                      # separo todas las palabras
        if frase is not []:
            frase = ['$'] + frase + ['$']                               # inserto $ al principio y al final de la lista
            if not tri:                                                 # en el caso de bigramas
                for palabra in range(len(frase) - 1):                   # analizo cada 2 palabras y lo envio al metodo contador
                    palabraAux = frase[palabra:palabra + 2]
                    self.contador(palabraAux, 'bi')
            else:                                                       # en el caso de si que se analiza trigramas
                for palabra in range(len(frase) - 2):                   # analizo por cada 2 y cada 3 palabras y lo envio al metodo contador
                    palabraAux = frase[palabra:palabra + 3]
                    self.contador((palabraAux[0], palabraAux[1]), 'bi')
                    self.contador(((palabraAux[0], palabraAux[1]), palabraAux[2]), 'tri')

    def contador(self, palabraAux: slice, tipo: str):

        primerPalabra = self.index[tipo].get(palabraAux[0])             # saco la primera palabra
        if not primerPalabra:
            self.index[tipo][palabraAux[0]] = {palabraAux[1]: 1}        # si la palabra que le sigue no existia en el dict, lo inicio a 1
        else:                                                           # si existe, sumo por 1
            self.index[tipo][palabraAux[0]][palabraAux[1]] = self.index[tipo][palabraAux[0]].get(palabraAux[1], 0) + 1

    def compute_index(self, filename, tri):
        self.index = {'name': filename, "bi": {}}
        if tri:
            self.index["tri"] = {}
        raw_sentence = ""
        #############
        # COMPLETAR #
        #############

        with open(filename, 'r') as f:
            lineaAnt = ""
            for line in f:                                      # para cada linea del fichero le quito los espacios por la derecha y lo convierto en minuscula
                line = line.rstrip().lower()
                frase = []
                indexAux = 0

                if not line and lineaAnt:                       # si es una linea vacia y la linea anterior no se ha acabado
                    frase = [lineaAnt]                          # lo meto en la lista
                    indexAux = 1                                # indexAux lo pongo a 1
                else:
                    frase = self.r1.split(lineaAnt + " " + line)  # quito los signos de la concatenacion de linea anterior y la linea actual

                lineaAnt = ""

                if frase:                                       # si la frase no es vacia
                    index = len(frase) - 1 or indexAux
                    for i in range(index):
                        self.index_sentence(frase[i], tri)      # analizo la cadena
                    if not indexAux:                            # si la frase no se ha acabado aun
                        fraseAnt = frase[len(frase) - 1]        # lo guardo en la variable fraseAnt
                        if fraseAnt and not indexAux:           # si hay frase que no se ha acabado aun
                            lineaAnt += " " + fraseAnt          # la concateno con la linea anterior
                        else:
                            lineaAnt = ""

            if lineaAnt:                                        # analizo la ultima linea
                self.index_sentence(lineaAnt, tri)

        sort_index(self.index['bi'])
        if tri:
            sort_index(self.index['tri'])
        

    def load_index(self, filename):
        with open(filename, "rb") as fh:
            self.index = pickle.load(fh)


    def save_index(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.index, fh)


    def save_info(self, filename):
        with open(filename, "w") as fh:
            print("#" * 20, file=fh)
            print("#" + "INFO".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            print("filename: '%s'\n" % self.index['name'], file=fh)
            print("#" * 20, file=fh)
            print("#" + "BIGRAMS".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for word in sorted(self.index['bi'].keys()):
                wl = self.index['bi'][word]
                print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)
            if 'tri' in self.index:
                print(file=fh)
                print("#" * 20, file=fh)
                print("#" + "TRIGRAMS".center(18) + "#", file=fh)
                print("#" * 20, file=fh)
                for word in sorted(self.index['tri'].keys()):
                    wl = self.index['tri'][word]
                    print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)


    def generate_sentences(self, n=10):
        #############
        # COMPLETAR #
        #############
        listFrases = []
        for i in range(n):
            listFrases.append('$')                      # creo una lista de frases para guardar cada linea
            wordActual = "$"                            # al principio de cada linea añado un $
            frase = 0
            while frase < 25:                           # la frase no puede superar 25 cinco letras
                nextwords = []
                nextwordsPorcentaje = []
                nextwordsTuples = self.index['bi'][wordActual][
                    1]                                  # en esta variable guardo las palabras que le sigue a la palabra actual
                for word in nextwordsTuples:
                    nextwords.append(word[1])           # guardo todas las palabras que le sigue en una lista
                    nextwordsPorcentaje.append(
                        float(word[0]) / float(self.index['bi'][wordActual][0]))  # guardo las proporciones en una lista
                nextword = random.choices(nextwords, weights=nextwordsPorcentaje,
                                          k=1)          # calculo la siguiente palabra utilizando choices
                nextword = nextword[0]                  # saco la siguiente palabra de la lista
                listFrases[i] += " " + str(nextword)    # la concadeno con la palabra actual
                wordActual = nextword                   # la palabra siguiente se convierte en la palabra actual
                if nextword == '$':                     # si la siguiente palabra es $, se acaba la frase
                    break
                frase += 1                              # el contador de las palabras suma 1

        for j in listFrases:                            # muestro las frases que se ha generado
            print(j)


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")


