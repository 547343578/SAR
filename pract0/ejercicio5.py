from collections import Counter

def char_freq(cadena):
    d = dict(Counter(cadena))
    print(d)


char_freq(input("Introduce la cadena: "))