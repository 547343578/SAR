#! -*- encoding: utf8 -*-

## Nombres: Zhuqing Wang

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import re
import sys
import os


def sort_dic_by_values(d, asc=True):
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))

class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile(r'\W+')
        self.clean_re2 = re.compile(r'\w+')

    def write_stats(self, filename, stats, use_stopwords, full,bigrams):     # he añadido el boolean bigrams
        """
        Este método escribe en fichero las estadísticas de un texto
            
        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas

        :return: None
        """

        with open(filename, 'w',encoding='utf-8') as fh:
            ## completar
            
            # ordeno el dict word alfabeticamente y los meto en en un string  
            wordAlpha = ""
            count = 0
            aux = sorted(stats['word'].items(),key=lambda x:x[0], reverse=False)
            while full == False:                                                                  # si no es full, muestro los primeros 20 palabras con su valor
                if count < 20 and count < len(aux):                                               # o menor si no llega
                    wordAlpha += "\t" + str(aux[count][0]) + ": " + str(aux[count][1]) + "\n" 
                    count += 1
                else:
                    break
            else:
                for i in aux:
                    wordAlpha += "\t" + str(i[0]) + ": " + str(i[1]) + "\n"                       # hago lo mismo pero en el caso de si es full
            
            # ordeno el dict word frecuencialmente y los meto en un string
            wordFre = ""
            count = 0
            aux = sort_dic_by_values(stats['word'])
            while full == False:                                                                  # lo mismo que anterior
                if count < 20 and count < len(aux):
                    wordFre += "\t" + str(aux[count][0]) + ": " + str(aux[count][1]) + "\n"
                    count += 1
                else:
                    break
            else:
                for i in aux:
                    wordFre += "\t" + str(i[0]) + ": " + str(i[1]) + "\n"
            
            # ordeno el dict symbol alfabeticamente y los meto en un string 
            symAlpha = ""
            count = 0
            aux = sorted(stats['symbol'].items(),key=lambda x:x[0], reverse=False)
            while full == False:                                                                   # lo mismo que anterior
                if count < 20 and count < len(aux):
                    symAlpha += "\t" + str(aux[count][0]) + ": " + str(aux[count][1]) + "\n"
                    count += 1
                else:
                    break
            else:
                for i in aux:
                    symAlpha+= "\t" + str(i[0]) + ": " + str(i[1]) + "\n"
            
            # ordeno el dict symbol frecuencialmente y los meto en un string
            symFre = ""
            count = 0
            aux = sort_dic_by_values(stats['symbol'])
            while full == False:                                                                   # lo mismo que anterior
                if count < 20 and count < len(aux):
                    symFre += "\t" + str(aux[count][0]) + ": " + str(aux[count][1]) + "\n"
                    count += 1
                else:
                    break
            else:
                for i in aux:
                    symFre += "\t" + str(i[0]) + ": " + str(i[1]) + "\n"
                    
            if bigrams:
                
            # ordeno el dict biword alfabeticamente y los meto en un string
                biAlpha = ""
                count = 0
                aux = sorted(stats['biword'].items(),key=lambda x:x[0], reverse=False)
                while full == False:                                                                   # lo mismo que anterior
                    if count < 20 and count < len(aux):
                        biAlpha += "\t" + str(aux[count][0]) + ": " + str(aux[count][1]) + "\n"
                        count += 1
                    else:
                        break
                else:
                    for i in aux:
                        biAlpha += "\t" + str(i[0]) + ": " + str(i[1]) + "\n"
            
            # ordeno el dict biword frecuencialmente y los meto en un string    
                biFre = ""
                count = 0
                aux = sort_dic_by_values(stats['biword'])
                while full == False:                                                                   # lo mismo que anterior
                    if count < 20 and count < len(aux):
                        biFre += "\t" + str(aux[count][0]) + ": " + str(aux[count][1]) + "\n"
                        count += 1
                    else:
                        break
                else:
                    for i in aux:
                        biFre += "\t" + str(i[0]) + ": " + str(i[1]) + "\n"
            
            # ordeno el dict bisymbol alfabeticamente y los meto en un string
                biSymAlpha = ""
                count = 0
                aux = sorted(stats['bisymbol'].items(),key=lambda x:x[0], reverse=False)
                while full == False:                                                                   # lo mismo que anterior
                    if count < 20 and count < len(aux):
                        biSymAlpha += "\t" + str(aux[count][0]) + ": " + str(aux[count][1]) + "\n"
                        count += 1
                    else:
                        break
                else:
                    for i in aux:
                        biSymAlpha += "\t" + str(i[0]) + ": " + str(i[1]) + "\n"
            
            # ordeno el dict bisymbol frecuencialmente y los meto en un string        
                biSymFre = ""
                count = 0
                aux = sort_dic_by_values(stats['bisymbol'])
                while full == False:                                                                   # lo mismo que anterior
                    if count < 20 and count < len(aux):
                        biSymFre += "\t" + str(aux[count][0]) + ": " + str(aux[count][1]) + "\n"
                        count += 1
                    else:
                        break
                else:
                    for i in aux:
                        biSymFre += "\t" + str(i[0]) + ": " + str(i[1]) + "\n"
                
                
            
            # creo la cadena que quiero escribir en el nuevo fichero
            contenido = ["Lines: " + str(stats['nlines']) + "\n",
                         "Number words(including stopwords): " + str(stats['nwords']) + "\n",
                         "Vocabulario size: " + str(len(stats['word'])) + "\n",
                         "Number of symbols: " + str(stats['nsymbol']) + "\n",
                         "Number of different symbols: " + str(len(stats['symbol'])) + "\n",
                         "Words (alphabetical order): " + "\n" + wordAlpha,
                         "Words (by frequency): " + "\n" + wordFre,
                         "Symbols (alphabetical order): " + "\n" + symAlpha,
                         "Symbols (by frequency): " + "\n" +  symFre]
            
            # si se usa stopwords, inserto en la posicion 2 de la cadena una frase con el valor de numero sin stopwords - numero de stopwords
            if use_stopwords == True:
                contenido.insert(2, "Number words(without stopwords): " + str(stats['nwords'] - stats['nwordNo']) + "\n")
            
            # si bigrams es True, inserto al final del contenido las frases sobre el biword y bisymbol    
            if bigrams == True:
                contenido.insert(len(contenido), "Word pairs (alphabetical order): " + "\n" + biAlpha)
                contenido.insert(len(contenido), "Word pairs (by frequency): " + "\n" + biFre)
                contenido.insert(len(contenido), "Symbol pairs (alphabetical order): " + "\n" + biSymAlpha)
                contenido.insert(len(contenido), "Symbol pairs (by frequency): " + "\n" + biSymFre)
            
            # escribo contenido al fichero nuevo    
            fh.writelines(contenido)
            
            pass


    def file_stats(self, filename, lower, stopwordsfile, bigrams, full):
        """
        Este método calcula las estadísticas de un fichero de texto

        :param 
            filename: el nombre del fichero.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?

        :return: None
        """

        stopwords = [] if stopwordsfile is None else open(stopwordsfile).read().split()

        # variables for results

        sts = {
                'nwords': 0,
                'nlines': 0,
                'word': {},
                'symbol': {}
                }

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        # completar
        cad = '_'
        if lower == True:           # si es -l, añado 'l' al nombre de fichero
            cad += 'l'
        if stopwords != []:         # si es -s, añado 's' al nombre de fichero
            cad += 's'
        if bigrams == True:         # si es -b, añado 'b' al nombre de fichero
            cad += 'b'
        if full == True:            # si es -f, añado 'f' al nombre de fichero
            cad += 'f'
        if cad == '_':              # si no se añade nada, se borra la cadena
            cad = ''
            
        # creo el fichero destino, lo meto en la direccion donde esta el fichero original y lo concadeno con las letras que hace falta
        f = open(filename,"r")
        new_filename = os.path.dirname(os.path.realpath(f.name)) + "\\" + f.name.split('.')[0] + cad + '_stats.txt'
        
        # declaro una vaiable para guarda el numero de lineas
        countlines = 0
        
        # declaro dos keys para guardar el numero de simbolos y numero de palabras de stopwords
        sts['nsymbol'] = 0
        sts['nwordNo'] = 0
        
        readlines = f.readlines()    
        
        for lines in readlines:
            countlines += 1                                               # contador de lineas
            sts['nwords'] += len(self.clean_re2.findall(lines))           # calculo los words quitando los signos
            
            wor = self.clean_re2.findall(lines)                           # una lista de words
            for word in wor:
                if lower == True:                                         # para cada palabra de la lista, primero miro si es lower
                    if word.lower() not in sts['word']:                   # en el caso de si, si el word.lower() no esta en la lista
                        if word.lower() not in stopwords:                 # y tampoco esta en la lista de stopwords
                            sts['word'][word.lower()] = 1                 # en el dict de palabras creo la nueva key dandole valor de 1
                        else:        
                            sts['nwordNo'] += 1                           # si esta en la lista de stopwords, en el contador de stopwords sumo 1
                    else:                                            
                        if word.lower() not in stopwords:                 # en el caso de que la palabra esta en el dict de words, primero miro si esta en la lista de stopwords
                            sts['word'][word.lower()] += 1                # en el caso de no esta, el valor del key suma 1        
                        else:
                            sts['nwordNo'] += 1                           # si esta en la lista de stopwords, el contador suma 1
                else:
                    if word not in sts['word']:                           # pasa lo mismo que antes pero en el caso de que no es lower
                        if word.lower() not in stopwords:
                            sts['word'][word] = 1
                        else:
                            sts['nwordNo'] += 1 
                    else:                                            
                        if word.lower() not in stopwords:
                            sts['word'][word] += 1                       
                        else:
                            sts['nwordNo'] += 1
                for letra in word:                                        # para cada letra de la palabra en donde estamos, 
                    if word.lower() not in stopwords:                     # miro si la palabra esta en el stopwords, porque si esta, esta palabra no contara
                        if lower == True:                                 # a continuacion hago lo mismo como lo que he hecho en la palabra
                            if letra.lower() in sts['symbol']:                   
                                sts['symbol'][letra.lower()] += 1
                            else:
                                sts['symbol'][letra.lower()] = 1 
                        else:                                        
                            if letra in sts['symbol']:                   
                                sts['symbol'][letra] += 1
                            else:
                                sts['symbol'][letra] = 1
                        sts['nsymbol'] += 1 
        
        sts['nlines'] = countlines                                        # asigno valor al key de numero de lineas
        
        if bigrams:                                                       # si es bigrama, primero ignoro las lineas vacias
            for line in readlines:                                        # y inserto '$' al principio y al final de la linea
                if line != "\n":                                          # en cada iteracion
                    wor = self.clean_re2.findall(line)
                    wor.insert(0,'$')
                    wor.append('$')
                    bigrama = ""
                    
                    for i in range(len(wor)-1):                           # para concadenar las bigramas, primero miro si la palabra en la posicion i 
                        if wor[i].lower() not in stopwords:               # y la palabra que esta de tras de el i+1 esta en la lista de stopwords
                            if wor[i+1].lower() not in stopwords:
                                if lower == True:                                          # en segundo lugar miro si es lower y concadeno las dos palabras
                                    bigrama = wor[i].lower() + " " + wor[i+1].lower()
                                    if bigrama not in sts['biword']:                       # aqui hago lo mismo que en sts['word'], si no estaba, lo creo y lo igualo a 1
                                        sts['biword'][bigrama] = 1                         
                                    else:
                                        sts['biword'][bigrama] += 1                        # si esta, lo sumo 1
                                else:
                                    bigrama = wor[i] + " " + wor[i+1]
                                    if bigrama not in sts['biword']:
                                        sts['biword'][bigrama] = 1
                                    else:
                                        sts['biword'][bigrama] += 1
                                
                    lineAux = self.clean_re2.findall(line)
                    for word in lineAux:                                                   # para los simbolos primero hago un for para cada palabra de la linea 
                        if word.lower() not in stopwords:                                  # y miro si la palabra esta en la lista de stopwords
                            for i in range(len(word)-1):                                   # a continuacion los concadeno y los inserto en el diccionario
                                if lower == True:
                                    bigrama = word[i].lower() + word[i+1].lower()
                                    if bigrama not in sts['bisymbol']:
                                        sts['bisymbol'][bigrama] = 1
                                    else:
                                        sts['bisymbol'][bigrama] += 1
                                else:
                                    bigrama = word[i] + word[i+1]
                                    if bigrama not in sts['bisymbol']:
                                        sts['bisymbol'][bigrama] = 1
                                    else:
                                        sts['bisymbol'][bigrama] += 1
                                    
                
                
        self.write_stats(new_filename, sts, stopwordsfile is not None, full,bigrams)       # he añadido el boolean bigrams


    def compute_files(self, filenames, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower',
                        action='store_true', default=False, 
                        help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                        help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram',
                        action='store_true', default=False, 
                        help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full',
                        action='store_true', default=False, 
                        help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file,
                     lower=args.lower,
                     stopwordsfile=args.stopwords,
                     bigrams=args.bigram,
                     full=args.full)


