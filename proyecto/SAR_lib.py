import json
from nltk.stem.snowball import SnowballStemmer
import os
import re


class SAR_Project:
    """
    Prototipo de la clase para realizar la indexacion y la recuperacion de noticias
        
        Preparada para todas las ampliaciones:
          parentesis + multiples indices + posicionales + stemming + permuterm + ranking de resultado

    Se deben completar los metodos que se indica.
    Se pueden añadir nuevas variables y nuevos metodos
    Los metodos que se añadan se deberan documentar en el codigo y explicar en la memoria
    """

    # lista de campos, el booleano indica si se debe tokenizar el campo
    # NECESARIO PARA LA AMPLIACION MULTIFIELD
    fields = [("title", True), ("date", False),
              ("keywords", True), ("article", True),
              ("summary", True)]

    # numero maximo de documento a mostrar cuando self.show_all es False
    SHOW_MAX = 10

    def __init__(self):
        """
        Constructor de la classe SAR_Indexer.
        NECESARIO PARA LA VERSION MINIMA

        Incluye todas las variables necesaria para todas las ampliaciones.
        Puedes añadir más variables si las necesitas 

        """
        self.docId = 0
        self.newsId = 0
        self.index = {'title': {},
                      'date': {},
                      'keywords': {},
                      'summary': {},
                      'article': {}}  # hash para el indice invertido de terminos --> clave: termino, valor: posting list.
        # Si se hace la implementacion multifield, se pude hacer un segundo nivel de hashing de tal forma que:
        # self.index['title'] seria el indice invertido del campo 'title'.
        self.sindex = {'title': {},
                       'date': {},
                       'keywords': {},
                       'summary': {},
                       'article': {}}  # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.ptindex = {
                           'title': {},
                           'date': {},
                           'keywords': {},
                           'summary': {},
                           'article': {}
                       },  # hash para el indice p}  # hash para el indice permuterm.
        self.docs = {}  # diccionario de documentos --> clave: entero(docid),  valor: ruta del fichero.
        self.weight = {}  # hash de terminos para el pesado, ranking de resultados. puede no utilizarse
        self.news = {}  # hash de noticias --> clave entero (newid), valor: la info necesaria para diferenciar la noticia dentro de su fichero (doc_id y posición dentro del documento)
        self.tokenizer = re.compile("\W+")  # expresion regular para hacer la tokenizacion
        self.stemmer = SnowballStemmer('spanish')  # stemmer en castellano
        self.show_all = False  # valor por defecto, se cambia con self.set_showall()
        self.show_snippet = False  # valor por defecto, se cambia con self.set_snippet()
        self.use_stemming = False  # valor por defecto, se cambia con self.set_stemming()
        self.use_ranking = False  # valor por defecto, se cambia con self.set_ranking()

    ###############################
    ###                         ###
    ###      CONFIGURACION      ###
    ###                         ###
    ###############################

    def set_showall(self, v):
        """

        Cambia el modo de mostrar los resultados.
        
        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_all es True se mostraran todos los resultados el lugar de un maximo de self.SHOW_MAX, no aplicable a la opcion -C

        """
        self.show_all = v

    def set_snippet(self, v):
        """

        Cambia el modo de mostrar snippet.
        
        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_snippet es True se mostrara un snippet de cada noticia, no aplicable a la opcion -C

        """
        self.show_snippet = v

    def set_stemming(self, v):
        """

        Cambia el modo de stemming por defecto.
        
        input: "v" booleano.

        UTIL PARA LA VERSION CON STEMMING

        si self.use_stemming es True las consultas se resolveran aplicando stemming por defecto.

        """
        self.use_stemming = v

    def set_ranking(self, v):
        """

        Cambia el modo de ranking por defecto.
        
        input: "v" booleano.

        UTIL PARA LA VERSION CON RANKING DE NOTICIAS

        si self.use_ranking es True las consultas se mostraran ordenadas, no aplicable a la opcion -C

        """
        self.use_ranking = v

    ###############################
    ###                         ###
    ###   PARTE 1: INDEXACION   ###
    ###                         ###
    ###############################

    def index_dir(self, root, **args):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        
        Recorre recursivamente el directorio "root" e indexa su contenido
        los argumentos adicionales "**args" solo son necesarios para las funcionalidades ampliadas

        """

        self.multifield = args['multifield']
        self.positional = args['positional']
        self.stemming = args['stem']
        self.permuterm = args['permuterm']

        for dir, subdirs, files in os.walk(root):
            for filename in files:
                if filename.endswith('.json'):
                    fullname = os.path.join(dir, filename)

                    self.index_file(fullname)

    def index_file(self, filename):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Indexa el contenido de un fichero.

        Para tokenizar la noticia se debe llamar a "self.tokenize"

        Dependiendo del valor de "self.multifield" y "self.positional" se debe ampliar el indexado.
        En estos casos, se recomienda crear nuevos metodos para hacer mas sencilla la implementacion

        input: "filename" es el nombre de un fichero en formato JSON Arrays (https://www.w3schools.com/js/js_json_arrays.asp).
                Una vez parseado con json.load tendremos una lista de diccionarios, cada diccionario se corresponde a una noticia

        """

        with open(filename) as fh:
            jlist = json.load(fh)

        if self.positional:
            self.index_file_positional(filename)
        else:
            self.docs[str(self.docId)] = filename
            for new in jlist:
                for field in self.fields:
                    if field[1]:
                        a = new[field[0]]
                        article = self.tokenize(a)
                        for word in article:
                            if self.index[field[0]].get(word) is None:
                                self.index[field[0]][word] = [self.newsId]
                            else:
                                if self.newsId not in self.index[field[0]][word]:
                                    self.index[field[0]][word].append(self.newsId)

                    else:
                        token = new[field[0]]
                        if self.index[field[0]].get(token) is None:
                            self.index[field[0]][token] = []
                        if (self.docId, self.newsId) not in self.index[field[0]][token]:
                            self.index[field[0]][token].append((self.docId, self.newsId))

                self.news[self.newsId] = (self.docId, id)
                self.newsId += 1
            self.docId += 1

    def tokenize(self, text):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Tokeniza la cadena "texto" eliminando simbolos no alfanumericos y dividientola por espacios.
        Puedes utilizar la expresion regular 'self.tokenizer'.

        params: 'text': texto a tokenizar

        return: lista de tokens

        """
        return self.tokenizer.sub(' ', text.lower()).split()

    def make_stemming(self):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING.

        Crea el indice de stemming (self.sindex) para los terminos de todos los indices.

        self.stemmer.stem(token) devuelve el stem del token

        """
        if self.multifield:
            multifield = ['title', 'date', 'keywords', 'article', 'summary']
        else:
            multifield = ['article']
        for field in multifield:
            for token in self.index[field].keys():
                tokenAux = self.stemmer.stem(token)
                if self.sindex[field].get(tokenAux) is None:
                    self.sindex[field][tokenAux] = [token]
                else:
                    if token not in self.sindex[field][tokenAux]:
                        self.sindex[field][tokenAux] += [token]

    def make_permuterm(self):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM
        Crea el indice permuterm (self.ptindex) para los terminos de todos los indices.
        """
        fields = ['article']
        if self.multifield:
            fields = ['title', 'date', 'keywords', 'article', 'summary']

        if self.multifield:
            for field in range(len(fields)):
                for term in self.index[fields[field]].keys():
                    backupterm = term
                    term += '$'
                    permutations = []
                    for _ in range(len(term)):
                        term = term[1:] + term[0]
                        permutations.append(term)
                    self.ptindex[fields[field]][backupterm] = len(permutations) if self.ptindex[fields[field]].get(
                        backupterm) is None else self.ptindex[fields[field]][backupterm] + len(permutations)
        else:
            for t in self.index['article'].keys():
                t += '$'
                permutations = []
                for _ in range(len(t) - 1):
                    t = t[1:] + t[0]
                    permutations.append(t)

                self.ptindex['article'][t] = len(permutations) + 1

    def show_stats(self):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Muestra estadisticas de los indices

        """
        self.ptindex = {'title': {}, 'date': {}, 'keywords': {}, 'summary': {}, 'article': {}}
        print("=" * 40)
        print("Number of indexed news: " + str(len(self.news)))
        print("-" * 40)
        print("TOKENS:")
        # ------------------------------- If multified option is active ----------------------
        if self.multifield:
            print("\t# of tokens in \'title\': " + str(len(self.index['title'])))
            print("\t# of tokens in \'date\': " + str(len(self.index['date'])))
            print("\t# of tokens in \'keywords\': " + str(len(self.index['keywords'])))
            print("\t# of tokens in \'article\': " + str(len(self.index['article'])))
            print("\t# of tokens in \'summary\': " + str(len(self.index['summary'])))
            print("-" * 40)

        # ------------------------------- If permuterm option is active ----------------------
        if self.permuterm:
            self.make_permuterm()  # lanzamos el make permuterm
            print('PERMUTERMS: ')

            fields = [i[0] for i in self.fields] if self.multifield else ['article']
            for f in fields:
                i = 0
                for termino in self.ptindex[f].keys():
                    i += self.ptindex[f][termino]
                print(f"\t# of tokens in \'{f}\': {i}")
            print("-" * 40)

            if self.stemming:
                self.make_stemming()
                print('STEMMING: ')
                print("\t# of tokens in \'title\': " + str(len(self.sindex['title'])))
                print("\t# of tokens in \'date\': " + str(len(self.sindex['date'])))
                print("\t# of tokens in \'keywords\': " + str(len(self.sindex['keywords'])))
                print("\t# of tokens in \'article\': " + str(len(self.sindex['article'])))
                print("\t# of tokens in \'summary\': " + str(len(self.sindex['summary'])))
                print("-" * 40)

            print('Positional queries are NOT allowed. \n========================================')

    ###################################
    ###                             ###
    ###   PARTE 2.1: RECUPERACION   ###
    ###                             ###
    ###################################
    def solve_query(self, query, prev={}):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una query.
        Debe realizar el parsing de consulta que sera mas o menos complicado en funcion de la ampliacion que se implementen


        param:  "query": cadena con la query
                "prev": incluido por si se quiere hacer una version recursiva. No es necesario utilizarlo.


        return: posting list con el resultado de la query

        """

        if query is None or len(query) == 0:
            return []

        # sacar postiing list de cada palabra y hacer su query (and or or)

        query = str(query).split(' ')
        i = 0
        res = []
        while len(query) > i:
            if query[i] == 'NOT':  # FIRST TERM
                res = self.reverse_posting(self.get_posting(query[i + 1]))
                i += 2
            elif query[i] == 'AND':
                if query[i + 1] == 'NOT':
                    res = self.and_posting(res, self.reverse_posting(self.get_posting(query[i + 2])))
                    i += 3
                else:
                    res = self.and_posting(res, self.get_posting(query[i + 1]))
                    i += 2
            elif query[i] == 'OR':
                if query[i + 1] == 'NOT':
                    res = self.or_posting(res, self.reverse_posting(self.get_posting(query[i + 2])))
                    i += 3
                else:
                    res = self.or_posting(res, self.get_posting(query[i + 1]))
                    i += 2
            else:
                res = self.get_posting(query[i])
                i += 1
        return res

    def get_posting(self, term, field='article'):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve la posting list asociada a un termino. 
        Dependiendo de las ampliaciones implementadas "get_posting" puede llamar a:
            - self.get_positionals: para la ampliacion de posicionales
            - self.get_permuterm: para la ampliacion de permuterms
            - self.get_stemming: para la amplaicion de stemming


        param:  "term": termino del que se debe recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list
        """
        if self.permuterm:
            return self.get_permuterm(term=term, field=field)
        if self.stemming:
            return self.get_stemming(term=term, field=field)
        # if self.positional:
        #     return self.get_positionals(terms=term, field=field)
        return self.index[field].get(term, [])

    def get_positionals(self, terms, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE POSICIONALES
        Devuelve la posting list asociada a una secuencia de terminos consecutivos.
        param:  "terms": lista con los terminos consecutivos para recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices
        return: posting list
        """
        sols = self.index[terms[0]]
        i = 1
        while i < len(terms):
            newsols = self.index[terms[i]]
            auxsols = []
            for sol in sols:
                for newsol in newsols:
                    if (sol[0] == newsol[0] and sol[1] + 1 == newsol[1]):
                        auxsols.append(newsol)

            sols = auxsols
        return sols

    def get_stemming(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING

        Devuelve la posting list asociada al stem de un termino.

        param:  "term": termino para recuperar la posting list de su stem.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list
        """
        stem = self.stemmer.stem(term)
        res = []
        if stem in self.sindex[field]:
            for token in self.sindex[field][stem]:
                res = self.or_posting(res, list(self.index[field][token].keys()))
        return res

    def get_permuterm(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Devuelve la posting list asociada a un termino utilizando el indice permuterm.

        param:  "term": termino para recuperar la posting list, "term" incluye un comodin (* o ?).
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """

        query = self.get_permuterm_query(term=term)
        questionMark = '?' in term
        if query:
            self.ptindex = {'title': {}, 'date': {}, 'keywords': {}, 'summary': {}, 'article': {}}
            self.make_permuterm()
            res = []
            for t in self.ptindex[field].keys():
                empezar = query.split('$')[1][:-1]
                acabar = query.split('$')[0]
                if t.startswith(empezar) and t.endswith(acabar) and not questionMark:
                    res += [i for i in self.index[field].get(t, []) if i not in res]

                elif questionMark and t.startswith(empezar) and t.endswith(acabar) and len(empezar) + len(acabar) + 1 == len(t):
                    res += [i for i in self.index[field].get(t, []) if i not in res]
                else:
                    continue
            return res
        else:
            return self.index[field].get(term, [])

    def get_permuterm_query(self, term):
        if not ('*' in term or '?' in term):
            return False
        else:
            term = term.replace('?', '*')
            return term[term.index('*') + 1:] + '$' + term[:term.index('*')] + '*'

    def reverse_posting(self, p):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Devuelve una posting list con todas las noticias excepto las contenidas en p.
        Util para resolver las queries con NOT.
        param:  "p": posting list
        return: posting list con todos los newid exceptos los contenidos en p
        """

        return [res for res in list(self.news.keys()) if res not in p]

    def and_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Calcula el AND de dos posting list de forma EFICIENTE

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos en p1 y p2

        """

        res = []
        i = 0
        j = 0
        p1.sort()
        p2.sort()
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                res.append(p1[i])
                i += 1
                j += 1
            elif p1[i] < p2[j]:
                i += 1
            else:
                j += 1
        return res

    def or_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Calcula el OR de dos posting list de forma EFICIENTE
        param:  "p1", "p2": posting lists sobre las que calcular
        return: posting list con los newid incluidos de p1 o p2
        """

        res = []
        i = 0
        j = 0
        p1.sort()
        p2.sort()
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                res.append(p1[i])
                i += 1
                j += 1
            elif p1[i] < p2[j]:
                res.append(p1[i])
                i += 1
            else:
                res.append(p2[j])
                j += 1

        while i < len(p1):
            res.append(p1[i])
            i += 1

        while j < len(p2):
            res.append(p2[j])
            j += 1

        return res

    def minus_posting(self, p1, p2):
        """
        OPCIONAL PARA TODAS LAS VERSIONES
        Calcula el except de dos posting list de forma EFICIENTE.
        Esta funcion se propone por si os es util, no es necesario utilizarla.
        param:  "p1", "p2": posting lists sobre las que calcular
        return: posting list con los newid incluidos de p1 y no en p2
        """

        pass

    def solve_and_count(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Resuelve una consulta y la muestra junto al numero de resultados
        param:  "query": query que se debe resolver.
        return: el numero de noticias recuperadas, para la opcion -T
        """
        result = self.solve_query(query)
        print("%s\t%d" % (query, len(result)))
        return len(result)

    def solve_and_show(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra informacion de las noticias recuperadas.
        Consideraciones:

        - En funcion del valor de "self.show_snippet" se mostrara una informacion u otra.
        - Si se implementa la opcion de ranking y en funcion del valor de self.use_ranking debera llamar a self.rank_result

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T
        
        """
        result = self.solve_query(query)
        print('=' * 40)
        print(f'Query: "{query}"')
        print(f'Number of results: {len(result)}')
        if self.use_ranking:
            result_ranked = self.rank_result(result, query)
            i = 1
            for res in result_ranked:

                with open(self.docs.get(str(self.news[res[1]][0]))) as fh:
                    document = json.load(fh)
                    document = document[0]
                    if self.show_snippet:
                        snippet = self.get_snippet(number=i, id=res[1], date=document['date'], title=document['title'],
                                                   keywords=document['keywords'],
                                                   score=result_ranked[i][0])
                        print(snippet)
                    else:
                        text = self.get_without_snippet(number=i, id=res[1], date=document['date'], title=document['title'],
                                                   keywords=document['keywords'],
                                                   score=result_ranked[i][0])
                        print(text)
                i += 1
        else:
            i = 1
            for elem in result:

                with open(self.docs.get(str(self.news[elem][0]))) as fh:
                    document = json.load(fh)
                    document = document[0]
                    if self.show_snippet:
                        snippet = self.get_snippet(number=i, id=elem, date=document['date'], title=document['title'],
                                                   keywords=document['keywords'])
                        print(snippet)
                    else:
                        text = self.get_without_snippet(number=i, id=elem, date=document['date'], title=document['title'],
                                                   keywords=document['keywords'])
                        print(text)
                i += 1

    def get_snippet(self, number, id, date, title, keywords, score=0):
        return f'#{number}\n' \
                f'{id}\n' \
               f'Score: {score}\n' \
               f'Date: {date}\n' \
               f'Title: {title}\n' \
               f'Keywords: {keywords}\n'
    def get_without_snippet(self, number, id, date, title, keywords, score=0):
        return f'#{number} \t ({id}) ({date}) {title} ({keywords}) '
    def rank_result(self, result, query):
        """
        NECESARIO PARA LA AMPLIACION DE RANKING
        Ordena los resultados de una query.
        param:  "result": lista de resultados sin ordenar
                "query": query, puede ser la query original, la query procesada o una lista de terminos
        return: la lista de resultados ordenada
        """
        # Se eliminan los elementos de la query que no son términos. Puesto que se eliminará los términos después de un NOT, este se reemplaza por nnoott para evitar que se pueda confundir con un término tras pasarlo a minúsculas.
        query = query.replace('AND', '')
        query = query.replace('OR', '')
        query = query.replace('NOT', 'nnoott')
        query = self.tokenize(query)
        i = 0
        while i < len(query):
            if query[i] == 'nnoott':
                del query[i:i + 2]
                i += 1
            i += 1

        rank = []

        # Se calcula la distancia de jaccard para cada noticia devuelta por la query
        for elem in result:
            with open(self.docs.get(str(self.news[elem][0]))) as fh:
                document = json.load(fh)
                document = document[0]['article']
            # Se guardan los resultados en una tupla formada por el identificador la noticia y su ranking con respecto a la query.
            rank.append([self.jaccard(query, self.tokenize(document)), elem])

        rank.sort(key=lambda tup: tup[0], reverse=True)
        return rank

    def jaccard(self, query, article):
        '''
        Computa la metrica de jaccard el documento enviado.
        J(A,B) = |A ∧ B| / |A ∨ B|
        '''

        intr = [value for value in query if value in article]
        union = article + [value for value in query if value not in intr]
        # DEvolvemos el cociente entre las longitudes de la intersección y la union de los conjuntos.
        return len(intr) / len(union)

    def index_file_positional(self, filename):
        with open(filename) as fh:
            jlist = json.load(fh)
            # "jlist" es una lista con tantos elementos como noticias hay en el fichero,
            # cada noticia es un diccionario con los campos:
            #      "title", "date", "keywords", "article", "summary"
            #
            # En la version basica solo se debe indexar el contenido "article"
            self.docs[str(self.docId)] = filename
            id = 0
            for new in jlist:
                article = new['article']
                article = self.tokenize(article)
                idWord = 0
                for word in article:
                    if self.index.get(word) is None:
                        self.index[word] = [(self.newsId, idWord)]
                    else:
                        self.index[word].append((self.newsId, idWord))
                    idWord += 1
                idWord = 0
                self.news[self.newsId] = (self.docId, id)
                self.newsId += 1
                id += 1
            self.docId += 1
