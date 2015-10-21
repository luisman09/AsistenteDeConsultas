# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views import generic
from django.apps import apps
from django.db import connection
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import csv

from .models import *
from .listas import *


# Variable global que me guarda todos las opciones deshabilitadas para el WHERE.
# OJOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO00000000 NECESITA SER GLOBAL PORQUE DE NO SERLO AL HACER LA CONSULTA LA LISTA PASA VACIA.
conds_where = []
consulta_final = ""
resultados_consulta = []
attos_select = []


# la funcion buscarElementoIndice recibe una clave, una lista en forma de diccionario (clave, valor(es))
# y un indice, y devuelve el valor del diccionario correspondiente al indice. 
def buscarElementoIndice(a, lista, indice):
    for elem in lista:
        if a == elem[0]:
            return elem[indice]


# la funcion buscarElementoCompleto recibe una clave y una lista en forma de diccionario (clave, valor(es)),
# y devuelve el valor del diccionario completo del diccionario que contiene como clave a la clave dada. 
def buscarElementoCompleto(a, lista):
    for elem in lista:
        if a == elem[0]:
            return elem


# La funcion encontrarOD devuelve una lista de origenes y destinos que seran tomados
# para encontrar los joins de la consulta principal.
# OJOOOOOOOOOOOOOOO DE MOMENTO ESTA ES LA FUNCION QUE ESTA CABLEADAAAAAAA.
def encontrarOD(t):
    x = False
    contacto = []
    origen_destino = []
    tablas = t
    if 'celular as c1' in t:
        contacto.append('celular as c1')
    if 'celular as c2' in t:
        contacto.append('celular as c2')
    if 'celular as c5' in t:
        contacto.append('celular as c5')
    if 'email as e1' in t:
        contacto.append('email as e1')
    if 'email as e2' in t:
        contacto.append('email as e2')
    if 'email as e5' in t:
        contacto.append('email as e5')
    if 'fijo as f2' in t:
        contacto.append('fijo as f2')
    if 'fijo as f4' in t:
        contacto.append('fijo as f4')
    if 'fijo as f5' in t:
        contacto.append('fijo as f5')
    for elem in contacto:
        if 'persona' in t:
            origen_destino.append((elem, 'persona'))
    if 'persona' in t:
        if 'estado' in t:
            x = True
            origen_destino.append(('persona','estado'))
        else:
            if 'municipio' in t:
                x = True
                origen_destino.append(('persona','municipio'))
            else:
                if 'parroquia' in t:
                    x = True
                    origen_destino.append(('persona','parroquia'))
                else:
                    if 'centro' in t:
                        x = True
                        origen_destino.append(('persona','centro'))
    if not x and 'centro' in t:
        if 'estado' in t:
            x = True
            origen_destino.append(('centro','estado'))
        else:
            if 'municipio' in t:
                x = True
                origen_destino.append(('centro','municipio'))
            else:
                if 'parroquia' in t:
                    x = True
                    origen_destino.append(('centro','parroquia'))
    if not x and 'parroquia' in t:
        if 'estado' in t:
            x = True
            origen_destino.append(('parroquia','estado'))
        else:
            if 'municipio' in t:
                x = True
                origen_destino.append(('parroquia','municipio'))
    if not x and 'municipio' in t:
        if 'estado' in t:
            origen_destino.append(('municipio','estado'))
    return origen_destino
    

def buscarJoin(origen,destino,lista):

    for elem in lista:
        if origen == elem[0] and destino == elem[1]:
            return elem[2]
    return "No existe el elemento"


# La funcion encontrarJoins busca a traves de otra consulta en la base de datos los join 
# necesarios para realizar la consulta, dados los atributos seleccionados por el usuario.
# Esa consulta se ejecuta a traves de un cursor y a nivel de la base de datos.
def encontrarJoins(t):

    contacto = []
    origen_destino = encontrarOD(t)
    from_joins = ""
    where_joins = ""

    for elem in t:
        if elem:
            if from_joins == "":
                from_joins = elem
            else:
                from_joins = from_joins + ", " + elem


      
    lista = lista_join
    for elem in origen_destino:

        condicion = buscarJoin(elem[0],elem[1],lista)

        #consulta = """WITH RECURSIVE joins(origen, destino, joins_where, tablas_from) AS (
        #                SELECT origen, destino, '' || arco, origen || ', ' || destino 
        #                FROM grafo 
        #              UNION ALL 
        #                SELECT j.origen, g.destino, 
        #                       g.arco || ' AND ' || j.joins_where, tablas_from || ', ' || g.destino 
        #                FROM joins j, grafo g 
        #                WHERE j.destino = g.origen
        #              ) SELECT joins_where, tablas_from
        #                FROM joins 
        #                WHERE origen = '""" + elem[0] + "' and destino = '" + elem[1] + "' LIMIT 1;"
        #c = connection.cursor()
        #c.execute(consulta)
        #resultados_consulta = c.fetchall()

        # Si solo es necesaria una hilera de joins. Ej: estado-persona
        if where_joins == "":
            where_joins = condicion
        # Si se necesita mas de una hilera de joins. Ej: email-persona y celular-estado
        else:
            where_joins = where_joins + " AND " + condicion
    tablas_joins = [from_joins, where_joins]
    return tablas_joins


# La funcion agregarCondiciones devuelve un String con todas las condiciones (del WHERE)
# que se indicaron a traves de la interfaz.
def agregarCondiciones(attos_where):
    where_items = []
    where_items_2 = ""

    for elem in attos_where:

        tipo = elem[0]
        if tipo == "dependiente":
            i = 4
            parrs = []
            muns = []
            edos = []
            disj_or = ""
            while i > 0:
                if len(elem[i]) >= 2: # Esto verifica que se tengan dos elementos (aunque el segundo sea vacio) o mas de dos en el caso de centro.
                    #if elem[i][1]: # Se especifico un centro o parr o mun o edo [4,3,2,1]
                    if i == 4:
                        for e in elem[i][1:]:   # e es el codigo del centro
                            if e:
                                if disj_or == "":
                                    disj_or = "(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + e + ")"
                                else:
                                    disj_or = disj_or + " OR " "(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + e + ")"
                                # Se guardan las parroquias correspondientes de estos centros
                                # para que no se tomen en cuenta al revisar las parroquias.
                                if e[:-3] not in parrs: 
                                    parrs.append(e[:-3])
                                if e[:-5] not in muns:
                                    muns.append(e[:-5])
                                if e[:-7] not in edos:
                                    edos.append(e[:-7])
                    elif i == 3:
                        for e in elem[i][1:]:
                            if e:
                                if e not in parrs: 
                                    if disj_or == "":
                                        disj_or = "(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + e + ")"
                                    else:
                                        disj_or = disj_or + " OR " "(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + e + ")"
                                    if e[:-2] not in muns:
                                        muns.append(e[:-2])
                                    if e[:-4] not in edos:
                                        edos.append(e[:-4])
                    elif i == 2:
                        for e in elem[i][1:]:
                            if e:
                                if e not in muns: 
                                    if disj_or == "":
                                        disj_or = "(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + e + ")"
                                    else:
                                        disj_or = disj_or + " OR " "(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + e + ")"
                                    if e[:-2] not in edos:
                                        edos.append(e[:-2])
                    elif i == 1:
                        for e in elem[i][1:]:
                            if e:
                                if e not in edos: 
                                    if disj_or == "":
                                        disj_or = "(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + e + ")"
                                    else:
                                        disj_or = disj_or + " OR " "(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + e + ")"
                i -= 1
            if disj_or:
                where_items.append("(" + disj_or + ")")
        elif tipo == "multiple":
            if elem[1][1]:
                disj_or = ""
                for e in elem[1][1:]:
                    if disj_or == "":
                        disj_or = "(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + e + ")"
                    else:
                        disj_or = disj_or + " OR " "(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + e + ")"
                where_items.append("(" + disj_or + ")")
        elif tipo == "simple":
            if len(elem[1]) == 2:
                if elem[1][1]:
                    where_items.append("(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + elem[1][1] + ")")
        elif tipo == "rango":
            if len(elem[1]) == 2:
                if elem[1][1] and elem[2][1]:
                    if not elem[1][0][0]: # caso funcion edad
                        where_items.append("(" + elem[1][0][1] + " BETWEEN " + elem[1][1] + " AND " + elem[2][1] + ")")
                    else:
                        where_items.append("(" + elem[1][0][0] + "." + elem[1][0][1] + " BETWEEN " + elem[1][1] + " AND " + elem[2][1] + ")")
        elif tipo == "doble": 
            if len(elem[1]) == 2: 
                if elem[1][1]:
                    where_items.append("(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + elem[1][1] + ")")
            if len(elem[2]) == 2: 
                if elem[2][1]:
                    where_items.append("(" + elem[2][0][0] + "." + elem[2][0][1] + " = " + elem[2][1] + ")")
        elif tipo == "cuadruple": 
            for i in range(1,5):
                if len(elem[i]) == 2:  
                    if elem[i][1]:
                        where_items.append("(" + elem[i][0][0] + "." + elem[i][0][1] + " = '" + elem[i][1] + "')")
                                                                                         
    for elem in where_items:
        if where_items_2 == "":
            where_items_2 = elem
        else:
            where_items_2 = where_items_2 + " AND " + elem
    #print where_items_2
    return where_items_2

# La funcion crearConsulta crea la consulta que sera ejecutada a nivel de la base de datos
# a partir de los elementos escogidos por el usuario a traves del formulario.
# Recibe los atributos a mostrar 
def crearConsulta(attos_select, attos_where, agrupado, limite):

    lista = lista_attos
    select_items = ""
    from_items = ""
    where_items = ""
    group_by_items = ""
    condiciones = ""
    condiciones_contacto = []
    limit = ""
    tablas = []
    # Si hay agrupado, entonces la lista cambia de lista_attos a lista_agrupados y ademas
    # agrega al agrupado a los atributos seleccionados
    if agrupado[0]:
        attos_select = agrupado + attos_select;
        lista = lista_agrupados_nivel_5 + [buscarElementoCompleto(agrupado[0],lista_agrupados)]

    for elem in attos_select:
        x = buscarElementoIndice(elem, lista, 1)
        if select_items == "":

            if len(x) >= 3:  
                if x[2] == "f":             # Es una funcion, por ejem Edad.
                    select_items = x[1]
                else:                       # Es una prioridad de algun dato de contacto.
                    select_items = x[1]
                    condiciones_contacto.append(["(" + x[2] + ".prioridad = " + x[3] + ")",x[0]])
            else:
                select_items = x[0] + "." + x[1]
            tablas.append(x[0])
        else:
            if len(x) >= 3:
                if x[2] == "f":             # Es una funcion, por ejem Edad.
                    select_items = select_items + ", " + x[1]
                else:                       # Es una prioridad de algun dato de contacto.
                    select_items = select_items + ", " + x[1]
                    condiciones_contacto.append(["(" + x[2] + ".prioridad = " + x[3] + ")",x[0]])
                if agrupado[0]:
                    if group_by_items == "":
                        group_by_items = x[1]
                    else:
                        group_by_items = group_by_items + ", " + x[1]
            else:
                select_items = select_items + ", " + x[0] + "." + x[1]
                if agrupado[0]:
                    if group_by_items == "":
                        group_by_items = x[0] + "." + x[1]
                    else:
                        group_by_items = group_by_items + ", " + x[0] + "." + x[1]
            if x[0] not in tablas:
                tablas.append(x[0])
    if group_by_items:
        group_by_items = " GROUP BY " + group_by_items + " ORDER BY " + group_by_items
    #else:
    #    group_by_items = " ORDER BY " + select_items
    # Se busca las condiciones del WHERE (no joins) de la consulta y se continua 
    # agregando a la lista de tablas, mas tablas participantes en la consulta
    # (solo en caso de ser necesario).
    condiciones = agregarCondiciones(attos_where)

    if condiciones_contacto:
        for elem in condiciones_contacto:
            if condiciones == "":
                condiciones = elem[0]
            else:
                condiciones = condiciones + " AND " + elem[0]

    for elem in attos_where:
        for tabla_atto in elem[1:]:
            tabla = tabla_atto[0][0]
            for e in tabla_atto[1:]:
                if e:
                    if tabla not in tablas:
                        if tabla:
                            tablas.append(tabla)                # Agrego las tablas que no se agregaron por los campos seleccionados.

    # Agregar tablas intermedias, en caso de ser necesarias:
    if ('celular as c1' in tablas) or ('celular as c2' in tablas) or ('celular as c3' in tablas) or ('email as e1' in tablas) or ('email as e2' in tablas) or ('email as e3' in tablas) or ('fijo as f1' in tablas) or ('fijo as f2' in tablas) or ('fijo as f3' in tablas):
        if ('estado' in tablas) or ('centro' in tablas):
            if not 'persona' in tablas:
                tablas.append('persona')

    if 'estado' in tablas:
        if ('persona' in tablas) or ('centro' in tablas) or ('parroquia' in tablas):
            if not 'municipio' in tablas:
                tablas.append('municipio')
        if ('persona' in tablas) or ('centro' in tablas):
            if not 'parroquia' in tablas:
                tablas.append('parroquia')
        if ('persona' in tablas):
            if not 'centro' in tablas:
                tablas.append('centro')
    if ('municipio' in tablas) and not ('estado' in tablas):
        if ('persona' in tablas) or ('centro' in tablas):
            if not 'parroquia' in tablas:
                tablas.append('parroquia')
        if ('persona' in tablas):
            if not 'centro' in tablas:
                tablas.append('centro')
    if ('parroquia' in tablas) and not ('municipio' in tablas):
        if ('persona' in tablas):
            if not 'centro' in tablas:
                tablas.append('centro')


    # Se crean las partes FROM y WHERE (joins y condiciones) de la consulta
    # Cuando la consulta es sobre una sola tabla de la base de datos.

    if len(tablas) == 1:
        from_items = tablas[0]
        if condiciones:
            where_items = " WHERE (" + condiciones + ")"
    # Cuando la consulta requiere mas de una tabla de la base de datos.
    else:
        joins = encontrarJoins(tablas)

        from_items = joins[0]
        if condiciones:
            where_items = " WHERE " + joins[1] + " AND (" + condiciones + ")"
        else:
            where_items = " WHERE " + joins[1]
    # Se crea la consulta completa
    hay_fijos = ""
    if 'fijo as f2' in tablas:
        hay_fijos = 'f2.numero'
    if 'fijo as f4' in tablas:
        if not hay_fijos:
            hay_fijos = 'f4.numero'
        else:
            hay_fijos = hay_fijos + ', f4.numero'
    if 'fijo as f5' in tablas:
        if not hay_fijos:
            hay_fijos = 'f5.numero'
        else:
            hay_fijos = hay_fijos + ', f5.numero'
    
    if limite[0]:
        limit = " LIMIT " + limite[0];
    if hay_fijos:
        consulta = "SELECT DISTINCT ON (" + hay_fijos + ") " + select_items + " FROM " + from_items + where_items + group_by_items + limit +";"
    else:
        consulta = "SELECT " + select_items + " FROM " + from_items + where_items + group_by_items + limit +";"
    return consulta


# La funcion consultas, a traves de un formulario recibe multiples elementos que el usuario introduce,
# transforma esos elementos mediante varias funciones a una forma de consulta SQL para luego ejecutarla 
# mediante el uso de cursores a nivel de la base de datos y luego redirir a otra pagina mostrando los
# resultados obtenidos de realizar la consulta. 
def consultas(request):

    global consulta_final, resultados_consulta, conds_where, attos_select
    resultados_pag = []

    if not consulta_final:

        query = request.POST.get('query')
        if query:
            
            consulta_final = request.POST.get('query')
            cursor = connection.cursor()
            cursor.execute(consulta_final)
            attos_select = [s[0] for s in cursor.description]
            resultados_consulta = cursor.fetchall()
        else:

            # Si la consulta es simple, aca se tienen todos los atributos a mostrar seleccionados por el usuario.
            attos_select = request.POST.getlist('attos')

            # Si no hay attos_select, es porque la consulta fue por agrupados,
            # y se obtienen el agrupado y los atributos a mostrar por los cuales se agrupa.
            agrupado = request.POST.getlist('agrupados') # campo por el cual se agrupa.
            if not attos_select:
                attos_select = request.POST.getlist('ag_attos') # campos por los cuales se agrupa.
            # Si la consulta tiene condiciones (WHERE), aca se obtienen.
            # EL ULTIMO elems_where QUE SE RECIBE ES EL DEL BOTON FINAL, EN ESE CASO LA LISTA LA 
            # RECIBE VACIA, POR LO CUAL, NOS DEBEMOS QUEDAR CON EL PENULTIMO elems_where RECIBIDO.
            # SE RECIBEN TANTOS elems_where COMO CAMBIOS EN LA LISTA DE CONDICIONES HAYA. POR ELLO
            # CON CADA CAMBIO RECIBIDO SE ELIMINA EL ANTERIOR. OJOOOOOOOOOOOOOOOOOOOOOOOOOOO
            elems_where = request.POST.getlist('deshabilitadas[]')
            if elems_where:
                del conds_where[:]
                for elem in elems_where:
                    x = buscarElementoCompleto(elem,lista_attos_where)
                    # conds_where sera una lista de la forma: Ver lista_attos_where en listas.py.
                    conds_where.append(x)
            # attos_where sera una lista de condiciones que mejora la forma que trae la lista conds_where
            # y a su vez agrega los valores especificos que el usuario introdujo via formulario.
            attos_where = []
            for atto in conds_where:
                temp = []
                temp4 = []
                valores = buscarElementoIndice(atto[0], conds_where, 2)     # ME DA LA LISTA DE VALORES: [("value interfaz",("tabla","atto"))]        
                tipo = buscarElementoIndice(atto[0], conds_where, 1)        # ME DA EL TIPO DEL VALOR: "tipo" ej: "dependiente","simple","rango",etc
                temp.append(tipo)                               # temp = ["tipo"]
                for elem in valores:
                    temp2 = []
                    temp2.append(elem[1])                       # temp2 = [("tabla","atto")]
                    temp3 = request.POST.getlist(elem[0])       # temp3 = [val1, val2, ... , valN]
                    temp2 = temp2 + temp3                       # temp2 = [("tabla","atto"), val1, val2, ... , valN]
                    temp4.append(temp2)                         # temp4 = [ [("tabla","atto"), val1, val2, ... , valN], ... ]
                temp = temp + temp4                             # temp = ["tipo", [("tabla","atto"), val1, val2, ... , valN], ...]
                attos_where.append(temp)                        # attos_where = [ ["tipo", [("tabla","atto"), val1, val2, ... , valN], ...], ... ]
            # Se toma el valor del limite si existe
            limite = request.POST.getlist('limite')
            # Se procede a crear la consulta con los valores recogidos y seguidamente a ejecutarla.
   
            consulta_final = crearConsulta(attos_select, attos_where, agrupado, limite)
            cursor = connection.cursor()
            cursor.execute(consulta_final)
            resultados_consulta = cursor.fetchall()

            #print resultados_consulta

            # Si hay un agrupado se agrega a los atributos a mostrar
            if agrupado[0]:
                attos_select = agrupado + attos_select

    print consulta_final
    #print resultados_consulta[0:10]

    paginator = Paginator(resultados_consulta, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        resultados_pag = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        resultados_pag = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        resultados_pag = paginator.page(paginator.num_pages)

    context = {'atributos': attos_select, 'resultados_pag': resultados_pag}
    #context = {'resultados_pag': resultados_pag}
    return render(request, 'asistente_de_consultas/consultas.html', context)

          
class QueriesView(generic.TemplateView):
    template_name = 'asistente_de_consultas/queries.html'
    context_object_name = 'query'


# La clase AtributosView muestra el formulario completo para hacer una consulta usando al asistente.
# Requiere pasar todos los contextos y listas necesarias al html.
class AtributosView(generic.ListView):
    template_name = 'asistente_de_consultas/atributos.html'
    context_object_name = 'attos_select'
    queryset = lista_attos

    def get_context_data(self, **kwargs):
        context = super(AtributosView, self).get_context_data(**kwargs)
        context['attos_where'] = lista_attos_where
        context['agrupados'] = lista_agrupados
        #context['ag_nivel_1'] = lista_agrupados_nivel_1
        #context['ag_nivel_2'] = lista_agrupados_nivel_2
        #context['ag_nivel_3'] = lista_agrupados_nivel_3
        #context['ag_nivel_4'] = lista_agrupados_nivel_4
        context['ag_nivel_5'] = lista_agrupados_nivel_5
        context['estados'] = Estado.objects.order_by('nombre')
        context['municipios'] = Municipio.objects.order_by('nombre')
        context['parroquias'] = Parroquia.objects.order_by('nombre')
        context['circuitos_15'] = lista_circuitos_15
        context['nacionalidades'] = lista_nacionalidades
        context['sexo'] = lista_sexo
        context['estratos'] = lista_estratos
        context['edos_civiles'] = lista_edos_civiles
        context['ipps'] = lista_ipps
        return context


# Busca el estado seleccionado y devuelve sus municipios.
class BusquedaAjaxView(generic.TemplateView):
    
    def get(self, request, *args, **kwargs):
        x = request.GET['edo']
        municipios = Municipio.objects.filter(id_edo=x).order_by('nombre')
        data = serializers.serialize('json', municipios, fields=('nombre'))
        return HttpResponse(data, content_type='application/json')


# Busca el municipio seleccionado y devuelve sus parroquias.
class BusquedaAjax2View(generic.TemplateView):
    
    def get(self, request, *args, **kwargs):
        x = request.GET['mun']
        parroquias = Parroquia.objects.filter(id_mun=x).order_by('nombre')
        data = serializers.serialize('json', parroquias, fields=('nombre'))
        return HttpResponse(data, content_type='application/json')


# Busca la parroquia seleccionada y devuelve sus centros.
class BusquedaAjax3View(generic.TemplateView):
    
    def get(self, request, *args, **kwargs):
        x = request.GET['parr']
        centros = Centro.objects.filter(id_parr=x).order_by('nombre')
        data = serializers.serialize('json', centros, fields=('nombre'))
        return HttpResponse(data, content_type='application/json')


# Busca y Verifica que el centro exista en la Base de datos.
class BuscarCentroAjaxView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        x = request.GET['centroId']
        centro = Centro.objects.filter(id=int(x))
        if centro:
            data = serializers.serialize('json', centro, fields=('nombre'))
        return HttpResponse(data, content_type='application/json')



def volverAlInicio(request):

    global conds_where, consulta_final, resultados_consulta, attos_select
    conds_where = []
    consulta_final = ""
    resultados_consulta = []
    attos_select = []
    print "Se limpiaron las Globales"
    return render(request, 'asistente_de_consultas/consultas.html')
    

def exportar_csv(request):

    print "aqui llegue"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="consulta.csv"'

    writer = csv.writer(response)
    row = []
    for elem in attos_select:
        row.append(elem)
    writer.writerow([unicode(s).encode("utf-8") for s in row])
    for elem in resultados_consulta:
        row = []
        for e in elem:
            row.append(e)
        writer.writerow([unicode(s).encode("utf-8") for s in row])

    return response










