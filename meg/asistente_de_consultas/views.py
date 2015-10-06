# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views import generic
from django.apps import apps
from django.db import connection
from django.core import serializers

from .models import *
from .listas import *


    #class IndexView(generic.ListView):
    #    template_name = 'asistente_de_consultas/index.html'
    #    context_object_name = 'parroquia_list'
    #
    #    def get_queryset(self):
    #        return Parroquia.objects.order_by('id')


    #class DetailView(generic.DetailView):
    #    model = Parroquia
    #    template_name = 'asistente_de_consultas/detail.html'


    #def vote(request, parroquia_id):
    #    p = get_object_or_404(Parroquia, pk=parroquia_id)
    #    try:
    #        c = p.centro_set.get(pk=request.POST['centro'])
    #    except (KeyError, Centro.DoesNotExist):
    #        return render(request, 'asistente_de_consultas/detail.html', {'parroquia': p, 'error_message': "NO SELECCIONASTE NINGUN CENTRO.",})
    #    else:
    #        return render(request, 'asistente_de_consultas/vote.html', {'parroquia': p, 'centro': c,})


# La funcion lista_attos retorna una lista que devuelve tuplas, en donde los primeros elementos
# son los nombres visibles de los atributos que puede escoger el usuario y los segundos elementos 
# son a su vez tuplas, que representan el nombre de la tabla y el nombre del 
# atributo (o funcion) tal cual como aparecen (o se ejecutan) a nivel de base de datos.
def listaAttos():
    lista = lista_demografica + lista_personas + lista_contactos
    return lista


# La funcion demografico devuelve una lista de un elemento que representa al origen
# y al destino de de la hilera de joins: estado-persona
# DE MOMENTO ESTA ES LA FUNCION QUE ESTA CABLEADAAAAAAA JUNTO A ENCONTRAROD. OJOOOOOOOOOOOOOO
def demografico(t, x):
    y = []
    if 'estado' in t:
        y.append((x,'estado'))
    #elif 'municipio' in t and not y:
    #    y.append((x,'municipio'))
    #elif 'parroquia' in t and not y:
    #    y.append((x,'parroquia'))
    elif 'centro' in t and not y:
        y.append((x,'centro'))
    return y


# La funcion encontrarOD devuelve una lista de origenes y destinos que seran tomados
# para encontrar los joins de la consulta principal.
# DE MOMENTO ESTA ES LA FUNCION QUE ESTA CABLEADAAAAAAA JUNTO A DEMOGRAFICO. OJOOOOOOOOOOOOOO
def encontrarOD(t):
    x = False
    contacto = []
    origen_destino = []
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
        elif 'centro' in t:
            x = True
            origen_destino.append(('persona','centro'))
    if not x and 'centro' in t:
        if 'estado' in t:
            origen_destino.append(('centro','estado'))
    #if not x and 'parroquia' in t:
    #    x = demografico(t, 'parroquia')
    #    origen_destino.append(x[0])
    #if not x and 'municipio' in t:
    #    x = demografico(t, 'municipio')
    #    origen_destino.append(x[0]) 

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

    #print attos_where

    for elem in attos_where:
        tipo = elem[0]
        if tipo == "dependiente":
            listo = False
            i = 4
            while not listo and i > 0:
                #print elem[i]
                if len(elem[i]) >= 2: # Esto verifica que se tengan dos elementos (aunque el segundo sea vacio) o mas de dos en el caso de centro.
                    if elem[i][1]: # Se especifico un centro o parr o mun o edo [4,3,2,1]
                        if i == 4:
                            disj_or = ""
                            for e in elem[i][1:]:
                                if disj_or == "":
                                    disj_or = "(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + e + ")"
                                else:
                                    disj_or = disj_or + " OR " "(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + e + ")"
                            where_items.append("(" + disj_or + ")")
                        else:
                            #print elem[i][1]
                            where_items.append("(" + elem[i][0][0] + "." + elem[i][0][1] + " = " + elem[i][1] + ")")
                        listo = True
                i -= 1
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
    

# la funcion buscarTupla devuelve la tupla de la base de datos dado un atributo visible al usuario
# usando el diccionario listaAttos. 
def buscarLista(a,lista,index):
    for elem in lista:
        if a == elem[0]:
            return elem[index]
    return "No existe el elemento"


# La funcion crearConsulta crea la consulta que sera ejecutada a nivel de la base de datos
# a partir de los elementos escogidos por el usuario a traves del formulario.
def crearConsulta(attos_select, attos_where):
    lista = listaAttos()
    select_items = ""
    from_items = ""
    where_items = ""
    condiciones = ""
    condiciones_contacto = []
    conds_cel = ""
    conds_mail = ""
    conds_fijo = ""
    conds_contacto = []
    tablas = []
    # Se crea la parte del SELECT de la consulta y se agregan 
    # las tablas a una lista de tablas participantes en la consulta.
    for elem in attos_select:
        x = buscarLista(elem, lista, 1)
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
            else:
                select_items = select_items + ", " + x[0] + "." + x[1]
            if x[0] not in tablas:
                tablas.append(x[0])
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
            if tabla not in tablas:
                tablas.append(tabla)                # Agrego las tablas que no se agregaron por los campos seleccionados.
    #print "tablas por where"
    #print tablas                                   # Ahorita por el problema del post la consulta agrega todas las tablas. 
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
    if hay_fijos:
        consulta = "SELECT DISTINCT ON (" + hay_fijos + ") " + select_items + " FROM " + from_items + where_items + " limit 50;"
    else:
        consulta = "SELECT " + select_items + " FROM " + from_items + where_items + " limit 50;"
    return consulta


# la funcion consultas, a traves de un formulario recibe una lista con los nombres de los atributos
# a mostrar (SELECT) y otra lista con las condiciones a restringir de una consulta (WHERE), transforma
# esas listas en un string SQL en forma de consulta valida, la ejecuta a nivel de la base de datos, 
# y devuelve los resultados a traves de la interfaz.
def consultas(request):

    attos_select = request.POST.getlist('attos') # lista de atributos a mostrar.
    attos_where = []

    #conds_where = request.POST.getlist('deshabilitadas[]')   # ESTO DA ERROR 403 EN EL POST
    #print "por aca"
    #print conds_where

    conds_where = lista_attos_where         # DE MOMENTO ESTA ES OPCIONAL CON TODAS LAS CONDICIONES (VACIAS las no seleccionadas)

    # attos_where me almacena todas las condiciones seleccionadas por el usuario via html.
    for atto in conds_where:
        temp = []
        temp4 = []
        x = buscarLista(atto[0], conds_where, 2)    # ME DA LA LISTA DE VALORES: [("value interfaz",("tabla","atto"))]        # EN EL CORRECTO QUITAR LOS [0]
        y = buscarLista(atto[0], conds_where, 1)    # ME DA EL TIPO DEL VALOR: "tipo" ej: "dependiente","simple","rango",etc
        temp.append(y)
        for elem in x:
            temp2 = []
            temp2.append(elem[1])
            temp3 = request.POST.getlist(elem[0])
            temp2 = temp2 + temp3
            temp4.append(temp2)
        temp = temp + temp4
        attos_where.append(temp)        # attos_where es de la forma: [ ["tipo", [("tabla","atto"), "valor")], ... ], ... ]


    consulta = crearConsulta(attos_select, attos_where)
    print consulta
    x = connection.cursor()
    x.execute(consulta)
    resultados_consulta = x.fetchall()
    context = {'atributos': attos_select, 'results': resultados_consulta}
    return render(request, 'asistente_de_consultas/consultas.html', context)


# La clase AtributosView muestra el formulario completo para hacer una consulta usando al asistente.
class AtributosView(generic.ListView):
    template_name = 'asistente_de_consultas/atributos.html'
    context_object_name = 'atributos_tupla'
    queryset = listaAttos()

    def get_context_data(self, **kwargs):
        context = super(AtributosView, self).get_context_data(**kwargs)
        context['attos_where'] = lista_attos_where
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
  
  
# ESTA HAY QUE MEJORARLA
def queries(request):
    consulta = request.POST.get('query')
    print consulta
    if consulta:
        x = connection.cursor()
        x.execute(consulta)
        resultados_consulta = x.fetchall()
        return render(request, 'asistente_de_consultas/consultas.html', {'results': resultados_consulta})
    else:
        return render(request, 'asistente_de_consultas/queries.html', {'error_message': 'NO INSERTASTE NADA'})




