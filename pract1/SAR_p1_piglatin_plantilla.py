#!/usr/bin/env python
#! -*- encoding: utf8 -*-

# 1.- Pig Latin

import sys
import re
import os

class Translator():

    def __init__(self, punt=None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            punt = ".,;?!"
        self.re = re.compile(r"(\w+)([" + punt + r"]*)")

    def translate_word(self, word):
        """
        Recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """

        #sustituir
        new_word = word

        listVocal = ['A','E','I','O','U','Y','a','e','i','o','u']
        # Creo una lista donde se guarda todos los vocales(inclido y) en mayuscula y en minuscula
        if word[0].isalpha() == False: 
            return word
        # Primero compruebo que es una palabra
        elif word[0] in listVocal:
            if word.isupper():
                new_word = new_word + "YAY"
            else: new_word = new_word + "yay"
            return new_word
        # En segundo compruebo si empieza por un vocal y en el caso de si , le concadeno un "yay" dependiendo si es mayuscula o minuscula
        else:
            for i in range(len(word)):
                if word[i] in listVocal:
                    new_word = word[i:] + word[:i].lower()
                    break
            new_word += "ay"
            if word.isupper():
                new_word = new_word.upper()
            elif word[0].isupper():
                new_word = new_word[0].upper() + new_word[1:]
        # Por ultimo hago una busqueda hasta donde se encuentra primer vocal, cambio la posicion de las palabras siguiendo la regla de PigLatin
        # (aqui los convierto todos en minuscula tambien) y sale del for
        # y luego lo concateno con "ay" y lo convierto en mayuscula dependiendo si el word original empieza por mayuscula o esta todo en mayuscula
        # o en otro caso que no hago nada

                                  
        return new_word

           

    def translate_sentence(self, sentence):
        """
        Recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """

        # sustituir
        new_sentence = ""
        listLetras = self.re.findall(sentence)
        # Aqui creo una lista donde esta todas las palabras con los signos que va de tras de cada palabra
        for i in listLetras:
            new_sentence += self.translate_word(i[0]) + i[1] + " "
        # En el for traduzco cada palabra utilizando el metodo escrito anteriormente y luego la concateno con el signo que le sigue mas un espacio

        return new_sentence

    def translate_file(self, filename):
        """
        Recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: True / False 
        """
        
        try:
            frase = ""
            f = open(filename,"r")
            new_file = open(os.path.dirname(os.path.realpath(f.name)) + "\\" + "resultado.txt","w")  
        # Primero hago un try except para captar excepciones y aqui he creado un new_file donde esta la tradccion del fichero original
            while True:
                line = f.readline()
                if line:
                    frase = self.translate_sentence(line)
                    new_file.write(frase + "\n")
        # Siempre se entra a este while y se lee las lineas una por una, a continuacion se traduce la frase utilizando el metodo anterior 
                else:
                    print("Finalizado!")
                    new_file.close()
                    f.close()
                    break       
        # Si la linea que se lee es vacia, hace un print "Finalizado" y cierra los dos ficheros        
        except Exception:
            print("file not found")
        # Si no se ha encontrado el fichero, hace un print "file not found"
                
        # rellenar

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f'Syntax: python {sys.argv[0]} [filename]')
        exit()
    t = Translator()
    if len(sys.argv) == 2:
        t.translate_file(sys.argv[1])
    else:
        sentence = input("ENGLISH: ")
        while len(sentence) > 1:
            print("PIG LATIN:", t.translate_sentence(sentence))
            sentence = input("ENGLISH: ")
