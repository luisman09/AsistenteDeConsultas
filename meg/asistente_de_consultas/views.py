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
import json
import codecs # Utilizada para la lectura del csv
from .models import *
from .listas import *


# Variables globales.
attos_select = []           # Lista de elementos que seran mostrados en el SELECT.
conds_where = []            # Lista de elementos que seran condicionados en el WHERE.
consulta_final = ""         # String que guarda la consulta final cuando se ejecuta.
resultados_consulta = []    # Lista que guarda todos los resultados de la consulta.
attos_muestreo = []         # Lista que guarda los elementos a mostrar junto con el elemento de muestreo.
consulta_final_muestras = ""         # String que guarda la consulta final de muestreo cuando se ejecuta.
resultados_consulta_muestras = []    # Lista que guarda todos los resultados de la consulta de muestreo.
es_muestra = 0


# La funcion buscarElementoIndice devuelve el valor del diccionario correspondiente al indice. 
def buscarElementoIndice(a, lista, indice):
    for elem in lista:
        if a == elem[0]:
            return elem[indice]


# La funcion buscarElementoCompleto devuelve el valor del diccionario completo.
# que contiene como clave a la clave dada. 
def buscarElementoCompleto(a, lista):
    for elem in lista:
        if a == elem[0]:
            return elem


# La funcion encontrarOD recibe una lista de las tablas necesarias para la consulta,
# y devuelve una lista de origenes y destinos que seran tomados para encontrar 
# los joins de la consulta principal.
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
    if 'fijo' in t:
        contacto.append('fijo')
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
    

# La funcion buscarJoin recibe un origen, un destino y procede buscar a ver si existe 
# un join entre esos elementos en la lista lista. 
def buscarJoin(origen,destino,lista):

    for elem in lista:
        if origen == elem[0] and destino == elem[1]:
            return elem[2]
    return "No existe el elemento"


# La funcion encontrarJoins recibe una lista de las tablas necesarias para la consulta, 
# y busca los join necesarios entre esas tablas para realizar la consulta.
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
        # Si solo es necesaria una hilera de joins. Ej: estado-persona
        if where_joins == "":
            where_joins = condicion
        # Si se necesita mas de una hilera de joins. Ej: email-persona y celular-estado
        else:
            where_joins = where_joins + " AND " + condicion
    tablas_joins = [from_joins, where_joins]
    return tablas_joins


# La funcion agregarCondiciones devuelve un String con todas las condiciones (del WHERE)
# que se indicaron a traves de la interfaz. Lo hace a traves del tipo de la condicion.
def agregarCondiciones(attos_where):

    where_items = []
    where_items_2 = ""
    for elem in attos_where:
        tipo = elem[0]
        if tipo == "dependiente": # Ubicacion demografica. 
            i = 4
            parrs, muns, edos = [], [], []
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
        elif tipo == "multiple": # estrato, estado civil, ipp, etc.
            disj_or = ""
            for e in elem[1][1:]:
                if e:
                    if disj_or == "":
                        disj_or = "(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + e + ")"
                    else:
                        disj_or = disj_or + " OR " "(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + e + ")"
            where_items.append("(" + disj_or + ")")
        elif tipo == "simple":  # sexo, etc.
            if len(elem[1]) == 2:
                if elem[1][1]:
                    where_items.append("(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + elem[1][1] + ")")
        elif tipo == "rango": # edad e isei de la persona.
            mini, maxi, minimo_abs, maximo_abs = elem[1][1], elem[2][1], '0', '1000000'
            if ((not mini) and maxi):
                mini = minimo_abs
            if (mini and (not maxi)):
                maxi = maximo_abs
            if (mini and maxi):
                if not elem[1][0][0]: # caso funcion edad.
                    where_items.append("(" + elem[1][0][1] + " BETWEEN " + mini + " AND " + maxi + ")")
                else:
                    where_items.append("(" + elem[1][0][0] + "." + elem[1][0][1] + " BETWEEN " + mini + " AND " + maxi + ")")
        elif tipo == "doble": # Cedula de identidad.
            if len(elem[1]) == 2: 
                if elem[1][1]:
                    where_items.append("(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + elem[1][1] + ")")
            if len(elem[2]) == 2: 
                if elem[2][1]:
                    where_items.append("(" + elem[2][0][0] + "." + elem[2][0][1] + " = " + elem[2][1] + ")")
        elif tipo == "cuadruple": # Nombre de la persona.
            for i in range(1,5):
                if len(elem[i]) == 2:  
                    if elem[i][1]:
                        where_items.append("(" + elem[i][0][0] + "." + elem[i][0][1] + " = '" + elem[i][1] + "')")
        elif tipo == "dependiente2": # Ubicacion por circuitos.
            disj_or = ""
            for e, c in zip(elem[1][1:], elem[2][1:]): 
                if (e and c):
                    if disj_or == "": 
                        disj_or = "(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + e + " AND " + elem[2][0][0] + "." + elem[2][0][1] + " = " + c + ")"
                    else:
                        disj_or = disj_or + " OR (" + elem[1][0][0] + "." + elem[1][0][1] + " = " + e + " AND " + elem[2][0][0] + "." + elem[2][0][1] + " = " + c + ")"
            if disj_or:
                where_items.append("(" + disj_or + ")") 
    for elem in where_items:
        if where_items_2 == "":
            where_items_2 = elem
        else:
            where_items_2 = where_items_2 + " AND " + elem
    return where_items_2


# La funcion crearConsulta crea la consulta en forma de STRING, que sera ejecutada a nivel de la
# base de datos a partir de los elementos escogidos por el usuario a traves del formulario.
# Recibe los atributos a mostrar, y tambien, si los hay, las condiciones, el agrupado y el limite.
def crearConsulta(attos_select, attos_where, agrupado, limite):

    select_items, from_items, where_items, group_by_items = "", "", "", ""
    condiciones, limit = "", ""
    condiciones_contacto, tablas = [], []
    lista = lista_attos
    # Si hay agrupado, entonces la lista cambia de lista_attos a lista_agrupados y ademas
    # agrega al agrupado a los atributos seleccionados
    if agrupado[0]:
        attos_select = agrupado + attos_select;
        lista = lista_agrupados_select + [buscarElementoCompleto(agrupado[0],lista_agrupados)]

    # Se va formando la consulta en las clausulas SELECT y GROUP BY.
    # Tambien se van agregando las tablas correspondientes para el FROM. 
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
                            tablas.append(tabla)     # Agrego las tablas que no se agregaron por los campos a mostrar.

    # Agregar tablas intermedias, en caso de ser necesarias:
    if ('celular as c1' in tablas) or ('celular as c2' in tablas) or ('celular as c5' in tablas) or ('email as e1' in tablas) or ('email as e2' in tablas) or ('email as e5' in tablas) or ('fijo as f2' in tablas) or ('fijo as f4' in tablas) or ('fijo as f5' in tablas) or ('fijo' in tablas):
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

    # Se crean las partes FROM y WHERE (joins y condiciones) de la consulta.
    if len(tablas) == 1:
        from_items = tablas[0]
        if condiciones:
            where_items = " WHERE (" + condiciones + ")"
    else:
        joins = encontrarJoins(tablas)

        from_items = joins[0]
        if condiciones:
            where_items = " WHERE " + joins[1] + " AND (" + condiciones + ")"
        else:
            where_items = " WHERE " + joins[1]
    # Se crea la consulta completa y se toma en cuenta si hay o no numeros fijos, ya que ellos implican
    # que la consulta agregue un DISTINCT.
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


# La funcion obtenerCOndicionesWhere obtiene la lista de los atributos que seran 
# condicionados y sus valores introducidos por el usuario mediante el formulario.
def obtenerCondicionesWhere(request, elems_where):

    # El ultimo elems_where que se recibe en consultas es el del boton final, en ese caso
    # la lista de condiciones se recibe vacia, por lo cual, nos debemos quedar con el penultimo
    # elems_where recibido que tendria todos las opciones que se quieren condicionar.
    # Se reciben tantos elems_where como cambios en la lista de condiciones haya. por ello
    # con cada cambio recibido se elimina la lista de condiciones anterior.
    global conds_where
    if elems_where:
        del conds_where[:]
        for elem in elems_where:
            x = buscarElementoCompleto(elem,lista_attos_where)
            conds_where.append(x)
    # attos_where agrega los valores introducidos a las condiciones establecidas en conds_where.
    attos_where = []
    for atto in conds_where:
        temp, temp4 = [], []
        valores = buscarElementoIndice(atto[0], conds_where, 2)     # valores: [("value interfaz",("tabla","atto"))]        
        tipo = buscarElementoIndice(atto[0], conds_where, 1)        # tipo: "tipo"
        temp.append(tipo)                           # temp: ["tipo"]
        for elem in valores:
            temp2 = []
            temp2.append(elem[1])                   # temp2: [("tabla","atto")]
            temp3 = request.POST.getlist(elem[0])   # temp3: [val1, val2, ... , valN]
            temp2 = temp2 + temp3       # temp2: [("tabla","atto"), val1, val2, ... , valN]
            temp4.append(temp2)         # temp4: [ [("tabla","atto"), val1, val2, ... , valN], ... ]
        temp = temp + temp4             # temp: ["tipo", [("tabla","atto"), val1, val2, ... , valN], ...]
        attos_where.append(temp)        # attos_where: [ ["tipo", [("tabla","atto"), val1, val2, ... , valN], ...], ... ]
    return attos_where


# La funcion ejecutarConsulta ejecuta la consulta prediseñada en la base de datos
# a traves de un cursor. Si la consulta viene por un query directo, se agregan los 
# nombres de las columnas como cabeceras de tabla de los resultados que se obtendran.
def ejecutarConsulta(consulta, esQueryDirecto):

    print consulta
    cursor = connection.cursor()
    cursor.execute(consulta)
    if esQueryDirecto:
        global attos_select
        attos_select = [s[0] for s in cursor.description]
    resultados = cursor.fetchall()
    return resultados


# La funcion limpiarGlobales reinicia las variables globales que se utilizaron para hacer
# la consulta anterior con el asistente. 
def limpiarGlobales(request):

    global conds_where, consulta_final, resultados_consulta, attos_select
    conds_where = []
    consulta_final = ""
    resultados_consulta = []
    attos_select = []
    print "Se limpiaron las Globales"
    return render(request, 'asistente_de_consultas/consultas.html')
    

# La funcion exportar_csv permite la descarga de un archivo csv desde el asistente de consultas
# con los resultados de haber ejecutado alguna consulta.
def exportar_csv(request):

    if es_muestra == 0:
        cabecera = attos_select
        resultados = resultados_consulta
    else:
        cabecera = attos_muestreo
        resultados = resultados_consulta_muestras

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="consulta.csv"'
    writer = csv.writer(response)
    row = []
    for elem in cabecera:
        row.append(elem)
    writer.writerow([unicode(s).encode("utf-8") for s in row])
    for elem in resultados:
        row = []
        for e in elem:
            row.append(e)
        writer.writerow([unicode(s).encode("utf-8") for s in row])
    return response


# La clase BusquedaAjaxView busca el estado seleccionado y devuelve sus municipios.
class BusquedaAjaxView(generic.TemplateView):
    
    def get(self, request, *args, **kwargs):
        x = request.GET['edo']
        municipios = Municipio.objects.filter(id_edo=x).order_by('nombre')
        data = serializers.serialize('json', municipios, fields=('nombre'))
        return HttpResponse(data, content_type='application/json')


# La clase BusquedaAjax2View busca el municipio seleccionado y devuelve sus parroquias.
class BusquedaAjax2View(generic.TemplateView):
    
    def get(self, request, *args, **kwargs):
        x = request.GET['mun']
        parroquias = Parroquia.objects.filter(id_mun=x).order_by('nombre')
        data = serializers.serialize('json', parroquias, fields=('nombre'))
        return HttpResponse(data, content_type='application/json')


# La clase BusquedaAjax3View busca la parroquia seleccionada y devuelve sus centros.
class BusquedaAjax3View(generic.TemplateView):
    
    def get(self, request, *args, **kwargs):
        x = request.GET['parr']
        centros = Centro.objects.filter(id_parr=x).order_by('nombre')
        data = serializers.serialize('json', centros)
        return HttpResponse(data, content_type='application/json')


# La clase BusquedaAjax4View busca los posibles circuitos de un estado y los devuelve.
class BusquedaAjax4View(generic.TemplateView):
    
    def get(self, request, *args, **kwargs):
        x = request.GET['edo']
        consulta = """SELECT DISTINCT(circuitos_15) AS circuitos
                      FROM estado e, municipio m, parroquia p, centro c
                      WHERE e.id = m.id_edo AND m.id = p.id_mun AND
                            p.id = c.id_parr AND e.id = """ + x + ";"            
        data = ejecutarConsulta(consulta, False)
        circuitos = []
        for elem in data:
            if elem[0]:
                circuitos.append(elem[0])
        circuitos.sort()
        return JsonResponse(circuitos, safe=False)


# La clase BuscarCentroAjaxView busca y verifica que el centro exista en la base de datos.
class BuscarCentroAjaxView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        x = request.GET['centroId']
        centro = Centro.objects.filter(id=int(x))
        if centro:
            data = serializers.serialize('json', centro, fields=('nombre'))
        return HttpResponse(data, content_type='application/json')


# La clase AtributosView muestra el formulario completo para hacer una consulta (simple o 
# con agrupado) usando al asistente. Requiere pasar todos los contextos y listas necesarias al html.
# Esta ligada al uso de la funcion consultas.
class AtributosView(generic.ListView):
    template_name = 'asistente_de_consultas/atributos.html'
    context_object_name = 'attos_select'
    queryset = lista_attos

    def get_context_data(self, **kwargs):
        context = super(AtributosView, self).get_context_data(**kwargs)
        context['attos_where'] = lista_attos_where
        context['agrupados'] = lista_agrupados
        context['agrupados_select'] = lista_agrupados_select
        context['estados'] = Estado.objects.order_by('nombre')
        context['municipios'] = Municipio.objects.order_by('nombre')
        context['parroquias'] = Parroquia.objects.order_by('nombre')
        context['nacionalidades'] = lista_nacionalidades
        context['sexo'] = lista_sexo
        context['estratos'] = lista_estratos
        context['edos_civiles'] = lista_edos_civiles
        context['ipps'] = lista_ipps
        return context


# La funcion consultas tiene dos funciones en particular:
# 1- recibir todos los request introducidos por el usuario a traves del formulario,
#    formular la consulta y mostrar la primera pagina de los resultados. 
# 2- simplemente navegar por las paginas de los resultados.
def consultas(request):

    global consulta_final, resultados_consulta, conds_where, attos_select, es_muestra
    resultados_pag = []

    es_muestra = 0

    page = request.GET.get('page')
    if not page:
        # Se obtiene los atributos a mostrar (SELECT), cuando la consulta es simple
        attos_select = request.POST.getlist('attos')
        # Se obtiene el agrupado y los campos a agrupar (SELECT), cuando la consulta es por agrupados.
        agrupado = request.POST.getlist('agrupados')
        if not attos_select:
            attos_select = request.POST.getlist('ag_attos')
        # Se obtiene los atributos a condicionar (WHERE) con sus valores del formulario, si existen.
        elems_where = request.POST.getlist('deshabilitadas[]')
        attos_where = obtenerCondicionesWhere(request, elems_where)
        # Se obtiene el valor del limite, si existe.
        limite = request.POST.getlist('limite')
        consulta_final = crearConsulta(attos_select, attos_where, agrupado, limite)
        resultados_consulta = ejecutarConsulta(consulta_final, False)
        # Si hay un agrupado se agrega a los atributos a mostrar
        if agrupado[0]:
            attos_select = agrupado + attos_select
        #print attos_where

    # Paginacion.
    paginator = Paginator(resultados_consulta, 10) # Muestra 10 elementos por pagina.
    try:
        resultados_pag = paginator.page(page)
    except PageNotAnInteger:
        resultados_pag = paginator.page(1)
    except EmptyPage:
        resultados_pag = paginator.page(paginator.num_pages)
    context = {'atributos': attos_select, 'resultados_pag': resultados_pag}
    return render(request, 'asistente_de_consultas/consultas.html', context)


# La clase QueriesView muestra el formulario completo para hacer una consulta directa
# desde la interfaz. Requiere el contexto query.
# Esta ligada al uso de la funcion consultas_queries.
class QueriesView(generic.TemplateView):
    template_name = 'asistente_de_consultas/queries.html'
    context_object_name = 'query'


# La funcion consultas_queries tiene dos funciones en particular:
# 1- recibir el request introducido por el usuario a traves del query
#    directo y mostrar la primera pagina de los resultados. 
# 2- simplemente navegar por las paginas de los resultados.
def consultas_queries(request):

    global consulta_final, resultados_consulta, conds_where, attos_select, es_muestra
    resultados_pag = []

    es_muestra = 0

    page = request.GET.get('page')
    if not page:
        # Se obtiene el query directo.
        query = request.POST.get('query')
        consulta_final = query
        resultados_consulta = ejecutarConsulta(consulta_final, True)

    # Paginacion.
    paginator = Paginator(resultados_consulta, 10) # Muestra 10 elementos por pagina.
    try:
        resultados_pag = paginator.page(page)
    except PageNotAnInteger:
        resultados_pag = paginator.page(1)
    except EmptyPage:
        resultados_pag = paginator.page(paginator.num_pages)
    context = {'atributos': attos_select, 'resultados_pag': resultados_pag}
    return render(request, 'asistente_de_consultas/consultas.html', context)


# La clase MuestrasView es la clase principal para el manejo de la generacion de muestras.
# Esta ligada al uso de la funcion consultas_muestras.
class MuestrasView(generic.ListView):
    template_name = 'asistente_de_consultas/muestras.html'
    context_object_name = 'muestreo'
    queryset = lista_muestreo

    def get_context_data(self, **kwargs):
        context = super(MuestrasView, self).get_context_data(**kwargs)
        context['muestreo_select'] = lista_muestreo_select
        context['attos_matriz_cols'] = lista_attos_matriz_cols
        context['attos_matriz_fils'] = lista_attos_matriz_fils
        context['lista_matrices'] = lista_matrices
        context['lista_3'] = lista_3
        context['lista_5'] = lista_5
        context['lista_10'] = lista_10
        context['lista_25'] = lista_25
        context['estados'] = Estado.objects.order_by('nombre')
        context['municipios'] = Municipio.objects.order_by('nombre')
        context['parroquias'] = Parroquia.objects.order_by('nombre')
        context['sexo'] = lista_sexo
        context['estratos'] = lista_estratos
        context['edos_civiles'] = lista_edos_civiles
        context['ipps'] = lista_ipps
        return context


# La funcion consultas_muestras tiene dos funciones en particular:
# 1- recibir todos los request introducidos por el usuario a traves del formulario
#    de muestras, formular la consulta y mostrar la primera pagina de los resultados. 
# 2- simplemente navegar por las paginas de los resultados.
def consultas_muestras(request):

    global consulta_final_muestras, resultados_consulta_muestras, attos_muestreo, es_muestra
    resultados_pag = []

    es_muestra = 1

    page = request.GET.get('page')
    if not page: 

        # Se obtiene el agrupado y los campos a agrupar (SELECT), cuando la consulta es por agrupados.
        elem_muestreo = request.POST.getlist('elems_muestreo')
        attos_muestreo = request.POST.getlist('mst_attos')
        attos_muestreo = elem_muestreo + attos_muestreo
        #print attos_muestreo
        factor = request.POST.getlist('factor')
        #print factor
        elem_cols = request.POST.getlist('elems-cols')
        elem_fils = request.POST.getlist('elems-fils')
        #print elem_cols
        #print elem_fils

        fils = buscarElementoCompleto(elem_fils[0],lista_attos_where)
        cols = []
        for elem in elem_cols:
            if elem != '':
                cols.append(buscarElementoCompleto(elem,lista_attos_where))
        #print fils
        #print cols

        lista_fils = []
        for elem in lista_10:
            casos = []
            for e in fils[2]:
                tabla_atto = e[1]
                val = e[0]+'-'+elem
                valores = request.POST.getlist(val)
                multis = []
                if len(valores) == 2:
                    if not valores[0]:
                        multis.append(valores[1])
                    else:
                        multis.append(valores[0])
                else:
                    if len(valores) == 1:
                        multis.append(valores[0])
                    else:
                        for v in valores:
                            if v != '':
                                multis.append(v)
                if multis:
                    casos.append([tabla_atto] + multis)
            if casos:
                lista_fils.append([fils[1]]+casos)
        #print lista_fils

        lista_cols = []
        for elem in lista_10:
            casos_final = []
            for elemento in cols:
                casos = []
                for e in elemento[2]:
                    tabla_atto = e[1]
                    val = e[0]+'-'+elem
                    # valores casi siempre tiene dos elementos, uno de ellos siempre es vacio
                    # en los casos de ubicacion si tiene un solo valor, y en los casos multiples tiene
                    # la cantidad de valores seleccionados mas uno vacio.
                    valores = request.POST.getlist(val)
                    multis = []
                    if len(valores) == 2:
                        if not valores[0]:
                            multis.append(valores[1])
                        else:
                            multis.append(valores[0])
                    else: 
                        for v in valores:
                            if v != '':
                                multis.append(v)
                    if multis:
                        casos.append([tabla_atto] + multis)
                if casos:
                    casos_final.append([elemento[1]]+casos)
            if casos_final:
                lista_cols.append(casos_final)
        #print lista_cols 

        lista_matriz = []
        for fil in lista_fils:
            casos = []
            for col in lista_cols:
                casos.append([fil] + col)
            lista_matriz.append(casos)
        #print lista_matriz

        matriz_factores = []
        for fil in lista_25[0:len(lista_fils)]:
            fila = []
            for col in lista_25[0:len(lista_cols)]:
                val = 'limite-'+fil+'-'+col
                lim = request.POST.getlist(val)
                fila.append(lim)
            if fila:
                matriz_factores.append(fila)
        #print matriz_factores

        matriz = []
        i = 0
        while i < len(lista_matriz):
            matriz.append(zip (lista_matriz[i],matriz_factores[i]))
            i+=1
        #print matriz

        consulta_list = []
        for limits in matriz:
            for lim in limits:
                if lim[1][0]:
                    limit = int(lim[1][0])*int(factor[0])
                    c = crearConsulta(attos_muestreo, lim[0], [''], [str(limit)])
                    c1 = c[:-1].partition('LIMIT')
                    c2 = c1[0] + "ORDER BY random() " + c1[1] + c1[2]
                    consulta_list.append(c2) 

        consulta = ""
        for elem in consulta_list:
            if consulta == "":
                consulta = "("+elem+")"
            else:
                consulta = consulta + " UNION " + "("+elem+")"
        consulta = consulta+";"
        consulta_final_muestras = consulta
        resultados_consulta_muestras = ejecutarConsulta(consulta_final_muestras, False)

    # Paginacion.
    paginator = Paginator(resultados_consulta_muestras, 10) # Muestra 10 elementos por pagina.
    try:
        resultados_pag = paginator.page(page)
    except PageNotAnInteger:
        resultados_pag = paginator.page(1)
    except EmptyPage:
        resultados_pag = paginator.page(paginator.num_pages)
    context = {'atributos': attos_muestreo, 'resultados_pag': resultados_pag}
    return render(request, 'asistente_de_consultas/consultas.html', context)


# La clase CargasView muestra el formulario para permitir el cruce de cedulas desde un archivo .csv.
# Esta ligada al uso de la funcion consultas_cargas.
class CargasView(generic.ListView):
    template_name = 'asistente_de_consultas/cargas.html'
    context_object_name = 'attos_select'
    queryset = lista_attos

    def get_context_data(self, **kwargs):
        context = super(CargasView, self).get_context_data(**kwargs)
        return context


# La funcion consultas_cargas tiene dos funciones en particular:
# 1- recibir el request introducido por el usuario a traves del formulario
#    que contiene los elementos a mostrar y el archivo con cedulas para hacer el cruce
#    para luego mostrar la primera pagina de los resultados. 
# 2- simplemente navegar por las paginas de los resultados.
def consultas_cargas(request):

    global consulta_final, resultados_consulta, conds_where, attos_select, es_muestra, archivo
    resultados_pag = []

    es_muestra = 0

    page = request.GET.get('page')
    if not page:
        # Se obtiene los atributos a mostrar (SELECT), cuando la consulta es simple
        attos_select = request.POST.getlist('attos')
        # Para la lectura del archivo CSV
        if request.POST and request.FILES:
            csvfile = request.FILES['csv_file']
            csvfile.open()
            reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"))
            cedulas = " persona.nac = 'V' AND persona.ci IN ("
            for index,row in enumerate(reader):
                if index == 1:
                    cedulas = cedulas + row[0]
                elif index > 1:
                    cedulas = cedulas + ',' + row[0]
            cedulas = cedulas + ');'
            print cedulas

        consulta = crearConsulta(attos_select, [], [u''], [u''])
        print consulta
        if 'WHERE' not in consulta:
            consulta_final = consulta[:-1] + ' WHERE' + cedulas
        else:
            consulta_final = consulta[:-1] + ' AND' + cedulas
        print consulta_final
        resultados_consulta = ejecutarConsulta(consulta_final, False)

    # Paginacion.
    paginator = Paginator(resultados_consulta, 10) # Muestra 10 elementos por pagina.
    try:
        resultados_pag = paginator.page(page)
    except PageNotAnInteger:
        resultados_pag = paginator.page(1)
    except EmptyPage:
        resultados_pag = paginator.page(paginator.num_pages)
    context = {'atributos': attos_select, 'resultados_pag': resultados_pag}
    return render(request, 'asistente_de_consultas/consultas.html', context)
