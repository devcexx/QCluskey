# -*- coding: utf-8 -*-
from pybexpp.bexpp import *
import sys

#Antes de nada, comprobar la versión de Python actual (Requerida 2.7)
if sys.version_info[0] != 2 or sys.version_info[1] < 7:
    raise SystemError("This script requires Python 2.7. Current Python version: %d.%d" \
    % (sys.version_info[0], sys.version_info[1]))

class QCluskeyError(Exception):
    pass

"""
Función para comparar elementos de un conjunto de verdad.
Devuelve:
    -1   Si los elementos son iguales.
    -2   Si los elementos no son comparables (tienen más de una diferencia)
    >= 0 La posición de la diferencia entre los dos elementos.
"""
def qcluskey_compare(item1, item2):
    if len(item1) != len(item2):
        raise QCluskeyError("Attempt to compare two elements with different lengths (%s, %s)" \
        % (item1, item2))
    ndiff = 0
    diffindex = 0
    i = 0
    length = len(item1)
    while ndiff < 2 and i < length:
        if item1[i] != item2[i]:
            ndiff += 1
            diffindex = i
        i += 1
    if ndiff == 0:
        return -1
    elif ndiff == 1:
        return diffindex
    else:
        return -2
"""

"""
def qcluskey_is_applicable(item, pattern):
    if len(item) != len(pattern):
        raise QCluskeyError("Attempt to fit an item in a pattern with a different length (%s, %s)" \
        % (item, pattern))
    res = True
    length = len(pattern)
    i = 0
    
    while res and i < length:
        if pattern[i] != '_' and item[i] != pattern[i]:
            res = False
        i += 1
    return res
    
        
def qcluskey_ones(item):
    ones = 0
    for c in item:
        if c == '1':
            ones += 1
    return ones
    
#Forma de los términos [[[a, k], [b]], [[c], [d]]]
def qcluskey_maxterm_multiply(terms):
    length = len(terms)
    if length == 0:
        return []
    if length == 1:
        return terms[0]
    if length == 2:
        result = []
        for fterm in terms[0]:
            for sterm in terms[1]:
                result.append(fterm + sterm)
        return result
    return qcluskey_maxterm_multiply([qcluskey_maxterm_multiply(terms[:2])] + terms[2:])       

def qcluskey_build_operation(minterms, variables):
    string = ""
    first = True
    for minterm in minterms:
        if first:
            first = False
        else:
            string += "+"
        for i in range(0, len(minterm)):
            c = minterm[i]
            var = variables[i]
            if c == '0':
                string += var + '\''
            elif c == '1':
                string += var
    return parse_expr(string)

def qcluskey_simplify(truth_set, variables):
    ilen = 0
    for e in truth_set:
        ilen = len(e)
        break
    
    #Organizar todos los elementos del conjunto de verdad en bloques    
    #Para ello se utilizará una matriz bidimensional (una lista de listas)
    #en la que el primer índice representará el número de ceros de los elementos
    #incluidos en la lista ubicada en ese índice.    
    blocks = []
    
    #Inicializar la lista de listas con el número de bloques requeridos para
    #esta tarea
    for i in range(0, ilen):
        blocks.append(set())
    
    #Incluir todos los elementos en los bloques (y de paso comprobar si todos
    # tienen la misma longitud)
    for e in truth_set:
        if len(e) != ilen:
            raise QCluskeyError("The specified truth set contains items with different sizes!")
        blocks[qcluskey_ones(e)].add(e)
        
    #Ahora, simplificar poquito a poquito los elementos :3
    done = False
    
    #Array que contendrá los elementos que no han podido ser simplificados
    left = set()
    
    #El bloque continúa hasta que se detecta que en la iteración
    #anterior no se pudo simplificar ningún elemento
    while not done:
        done = True
        marked = set() #Los elementos marcados en esta iteración
        original = set() #Los elementos originales presentes en la iteración
        #Iterar los bloques desde el que tiene más unos hasta el que menos.
        for i in range(ilen - 1, -1, -1):
            cblock = blocks[i] #Bloque actual
            nblock = set()
            if i - 1 >= 0:
                nblock = blocks[i - 1] #Bloque siguiente
            sblock = set() #Nuevo bloque generado a partir de la simplificación
            
            #Comparar todos los e del bloque actual con los del siguiente
            for j in cblock:
                original.add(j)
                for k in nblock:
                    cr = qcluskey_compare(j,k)
                    if cr >= 0:
                        newitem = j[:cr] + '_' + j[cr+1:]
                        sblock.add(newitem)
                        marked.add(j)
                        marked.add(k)
                        done = False
            blocks[i] = sblock
        
        #Los elementos que se han dejado sin marcar en este paso
        #será la diferencia entre los marcados y los originales.
        left.update(original.difference(marked))

    """
    Pese a que la tabla de decisión puede ser útil en algunos ámbitos, se pueden
    dar casos en los que la tabla de decisión muestre todas las columnas con
    más de una posible coincidencia con alguno de los elementos tomados
    anteriormente. Es por ello por lo que se ha tenido que utilizar el método
    de Petrick para poder obtener los elementos requeridos por la operación.
    """
    
    #Ahora se genera una "tabla de decisión" en esta variable. Esta variable
    #contendrá listas que contienen las implicaciones que son aplicables a cada
    #uno de los elementos del conjunto de verdad.
    
    dtable = []
    for e in truth_set:
        clist = []
        for pattern in left:
            if qcluskey_is_applicable(e, pattern):
                
                #Se incluye la implicación en otra lista para poder después
                #hacer el método de Petrick
                clist.append([pattern])
        if not clist in dtable:
            dtable.append(clist)
    
    #Ahora, la variable dtable contendría una lista con una forma similar a
    # [[['__00'], ['_00_']], [['_00_']]]. Si cada uno de estos elementos
    #se toma como una variable booleana, según el método de Patrick, la
    #multiplicación de la suma de las implicaciones de cada uno de los elementos
    #debe de ser igual a uno. Es decir, si a las implicaciones anteriores
    #se les da el nombre de a, b y c respectivamente, el método de Petrick dice
    #que (a + b)*c = 1. Ahora se debe operar esa operación para
    #dejarlos en minitérminos
    minterms = qcluskey_maxterm_multiply(dtable)
    
    #Una vez operados los maxitérminos, el resultado debería ser algo tal que
    #[['__00', '_00_'], ['_00_', '_00_']] que, representado de manera matemática
    #con los nombres anteriores, sería algo tal que 'ab + bb = 1'. Como para
    #que el resultado de esa operación sea 1 es suficiente con que uno de los
    #sumandos sea 1, tomamos el de menor longitud (sin contar las repeticiones)
    pickedItems = set()
    pickedItemsLen = 0
    
    for minterm in minterms:
        mset = set(minterm)
        clen = len(mset)
        
        if pickedItemsLen == 0 or clen < pickedItemsLen:
            pickedItems = mset
            pickedItemsLen = clen
            
    #Finalmente, una vez que tenemos los minitérminos cogidos, construimos
    #la operación simplificada
    return qcluskey_build_operation(pickedItems, variables)
    
    
    
    