#!/usr/bin/env python
# ! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys


## Nombres: Zhuqing Wang

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################


def sort_index(d):
    for k in d:
        d[k][1] = sorted(d[k][1], key=lambda x: x[0], reverse=True)  # aqui he modificado el sorted


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[^.;?!]+')  # con findall, divide la frase por signos
        self.r2 = re.compile('\w+')

    def index_sentence(self, sentence, tri):
        #############
        # COMPLETAR #
        #############

        for i in range(len(sentence) - 1):                              # para cada palabra de la frase, miro si esta en
            if sentence[i].lower() not in self.index['bi']:             # el dict index, si no esta, creo una lista y en
                self.index['bi'][sentence[i].lower()] = [1, [
                    [1, sentence[i + 1].lower()]]]                      # la posicion 0 pongo el numero total de veces que aparece
                                                                        # la posicion 1 pongo la palabra que le sigue con su numero
            else:
                self.index['bi'][sentence[i].lower()][0] += 1           # si esta en el dict index, en la posicion 0 de su lista sumo 1
                listWord = self.index['bi'][sentence[i].lower()][1]     # y ahora miro si la palabra que le sigue aparece en su lista
                check = False
                for j in listWord:
                    if sentence[i + 1].lower() == j[1]:                 # si lo encuentra
                        j[0] += 1                                       # suma 1
                        check = True
                if not check:                                           # si no estaba en la lista
                    self.index['bi'][sentence[i].lower()][1].append(
                        [1, sentence[i + 1].lower()])                   # en la lista de la palabra actual
                                                                        # creo esta palabra y la inicio a 1
        pass

    def compute_index(self, filename, tri):
        self.index = {'name': filename, "bi": {}}
        if tri:
            self.index["tri"] = {}
        raw_sentence = ""
        #############
        # COMPLETAR #
        #############
        f = open(filename, "r")
        texto = f.readlines()
        for line in texto:                          # para cada linea del fichero le quito todos los signos
            palabras = self.r2.findall(line)        # y añado un $ al principio y al final de la linea
            palabras.insert(0, '$')
            palabras.append('$')
            if line != "\n":                        # si no es una linea vacia, llamo al metodo index_sentece para meter los datos
                self.index_sentence(palabras, tri)

        sort_index(self.index['bi'])                # ordeno el diccionario
        if tri:
            sort_index(self.index['tri'])

        for clave, valor in self.index['bi'].items():  # convierto los valores del diccionario en tuplas
            for i in range(len(valor[1])):
                valor[1][i] = tuple(valor[1][i])
            self.index['bi'][clave] = tuple(self.index['bi'][clave])


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
                    print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])),
                          file=fh)

    def generate_sentences(self, n=10):
        #############
        # COMPLETAR #
        #############
        listFrases = []
        for i in range(n):
            listFrases.append('$')               # creo una lista de frases para guardar cada linea
            wordActual = "$"                     # al principio de cada linea añado un $
            frase = 0
            while frase < 25:                    # la frase no puede superar 25 cinco letras
                nextwords = []
                nextwordsPorcentaje = []
                nextwordsTuples = self.index['bi'][wordActual][1]        # en esta variable guardo las palabras que le sigue a la palabra actual
                for word in nextwordsTuples:
                    nextwords.append(word[1])                            # guardo todas las palabras que le sigue en una lista
                    nextwordsPorcentaje.append(float(word[0]) / float(self.index['bi'][wordActual][0]))    # guardo las proporciones en una lista
                nextword = random.choices(nextwords, weights=nextwordsPorcentaje, k=1)      # calculo la siguiente palabra utilizando choices
                nextword = nextword[0]                                   # saco la siguiente palabra de la lista
                listFrases[i] += " " + str(nextword)                     # la concadeno con la palabra actual
                wordActual = nextword                                    # la palabra siguiente se convierte en la palabra actual
                if nextword == '$':                                      # si la siguiente palabra es $, se acaba la frase
                    break
                frase += 1                                               # el contador de las palabras suma 1

        for j in listFrases:                                             # muestro las frases que se ha generado
            print(j)

        pass


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")
