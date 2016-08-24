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
import xlwt
import json
import time
import codecs # Utilizada para la lectura del csv
import os, sys
from .models import *
from .listas import *


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
    origen_destino = []
    tablas = t
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


# La funcion encontrarJoins recibe una lista de las tablas para la consulta, luego
# busca y crea los join necesarios entre esas tablas para realizar la consulta.
def encontrarJoins(t):

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
        if tipo == "dependiente": # Caso Particular: Ubicacion Demografica. 
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
        elif tipo == "multiple": # Select Multiple: estrato, estado civil, ipp, operadora, etc.
                                 # Tambien aplica para el Caso Particular: Centros Especificos.
            disj_or = ""
            print elem[1]
            for e in elem[1][1:]:
                if e:
                    if disj_or == "":
                        if not elem[1][0][0]: # caso funcion operadora.
                            disj_or = "(" + elem[1][0][1] + " = " + e + ")"
                        else:
                            disj_or = "(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + e + ")"
                    else:
                        if not elem[1][0][0]: # caso funcion operadora.
                            disj_or = disj_or + " OR " "(" + elem[1][0][1] + " = " + e + ")"
                        else:
                            disj_or = disj_or + " OR " "(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + e + ")"
            if disj_or:
                where_items.append("(" + disj_or + ")")
        elif tipo == "simple":  # Select Simple: sexo, validacion, etc.
            if len(elem[1]) == 2:
                if elem[1][1]:
                    where_items.append("(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + elem[1][1] + ")")
        elif tipo == "rango": # # Dos Input de Tipo Rango: edad, isei, score, score_rr, etc.
            mini, maxi, minimo_abs, maximo_abs = elem[1][1], elem[2][1], '-1000000', '1000000'
            if ((not mini) and maxi):
                mini = minimo_abs
            if (mini and (not maxi)):
                maxi = maximo_abs
            if (mini and maxi):
                if not elem[1][0][0]: # caso funcion edad.
                    where_items.append("(" + elem[1][0][1] + " BETWEEN " + mini + " AND " + maxi + ")")
                else:
                    where_items.append("(" + elem[1][0][0] + "." + elem[1][0][1] + " BETWEEN " + mini + " AND " + maxi + ")")
        elif tipo == "doble": # Caso Particular: Nacionalidad y Cedula de Identidad.
            if len(elem[1]) == 2: 
                if elem[1][1]:
                    where_items.append("(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + elem[1][1] + ")")
            if len(elem[2]) == 2: 
                if elem[2][1]:
                    where_items.append("(" + elem[2][0][0] + "." + elem[2][0][1] + " = " + elem[2][1] + ")")
        elif tipo == "cuadruple": # Caso Particular: Nombres y Apellidos.
            for i in range(1,5):
                if len(elem[i]) == 2:  
                    if elem[i][1]:
                        where_items.append("(" + elem[i][0][0] + "." + elem[i][0][1] + " = '" + elem[i][1] + "')")
        elif tipo == "dependiente2": # Caso Particular: Ubicacion por Circuitos.
            disj_or = ""
            for e, c in zip(elem[1][1:], elem[2][1:]): 
                if (e and c):
                    if disj_or == "": 
                        disj_or = "(" + elem[1][0][0] + "." + elem[1][0][1] + " = " + e + " AND " + elem[2][0][0] + "." + elem[2][0][1] + " = " + c + ")"
                    else:
                        disj_or = disj_or + " OR (" + elem[1][0][0] + "." + elem[1][0][1] + " = " + e + " AND " + elem[2][0][0] + "." + elem[2][0][1] + " = " + c + ")"
            if disj_or:
                where_items.append("(" + disj_or + ")") 
    # Union de todos los casos. 
    for elem in where_items:
        if where_items_2 == "":
            where_items_2 = elem
        else:
            where_items_2 = where_items_2 + " AND " + elem
    return where_items_2


# La funcion crearConsulta crea la consulta en forma de STRING, que sera ejecutada a nivel de la
# base de datos a partir de los elementos escogidos por el usuario a traves del formulario.
# Recibe los atributos a mostrar, y tambien, si los hay, las condiciones, el agrupado y el limite.
def crearConsulta(attos_select, attos_where, agrupado, orden, limite):

    select_items, from_items, where_items = "", "", ""
    group_by_items, order_by_items, elem_agr_ord = "", "", ""
    condiciones, limit = "", ""
    tablas = []
    lista = lista_attos
    # Si hay agrupado, entonces la lista cambia de lista_attos a lista_agrupados y ademas
    # agrega al agrupado a los atributos seleccionados
    if agrupado[0]:
        attos_select = agrupado + attos_select
        elem_agr = buscarElementoCompleto(agrupado[0],lista_agrupados)
        elem_agr_ord = elem_agr[1][1]
        lista = lista_agrupados_select + [elem_agr]

    # Se va formando la consulta en las clausulas SELECT y GROUP BY.
    # Tambien se van agregando las tablas correspondientes para el FROM. 
    for elem in attos_select:
        x = buscarElementoIndice(elem, lista, 1)
        if select_items == "":

            if len(x) >= 3:  
                select_items = x[1]
            else:
                select_items = x[0] + "." + x[1]
            tablas.append(x[0])
        else:
            if len(x) >= 3:
                select_items = select_items + ", " + x[1]
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
        group_by_items = " GROUP BY " + group_by_items 
    # Se busca las condiciones del WHERE (no joins) de la consulta y se continua 
    # agregando a la lista de tablas, mas tablas participantes en la consulta
    # (solo en caso de ser necesario).
    condiciones = agregarCondiciones(attos_where)
    for elem in attos_where:
        for tabla_atto in elem[1:]:
            tabla = tabla_atto[0][0]
            for e in tabla_atto[1:]:
                if e:
                    # Agrego las tablas que no se agregaron por los campos a mostrar.
                    if tabla not in tablas:
                        if tabla:
                            tablas.append(tabla)   

    # Agregar tablas intermedias, en caso de ser necesarias:
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
    # Se agrega el orden y/o el limite, si los hay.
    if orden:
        if ("'3'" in orden):
            order_by_items = " ORDER BY random()"
        elif ("'1'" in orden):
            order_by_items = " ORDER BY " + elem_agr_ord + " DESC" 
        elif ("'2'" in orden):
            order_by_items = " ORDER BY " + elem_agr_ord
        print orden
        print order_by_items
    if limite[0]:
        limit = " LIMIT " + limite[0];
    # Se crea la consulta completa.
    consulta = "SELECT " + select_items + " FROM " + from_items + where_items + group_by_items + order_by_items + limit +";"
    return consulta


# La funcion obtenerCOndicionesWhere obtiene la lista de los atributos que seran 
# condicionados y sus valores introducidos por el usuario mediante el formulario.
def obtenerCondicionesWhere(request, elems_where):

    conds_where = []
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


# La funcion escribirRegisto escribe en un archivo txt del servidor, las consultas realizadas 
# por el usuario, con el objetivo de poder comprobar consultas erroneas o el mal uso de los datos.
# Los archivos se encuentran en la carpeta: home/administrador/Documentos/Logs_Users_ADC_MEG/
# Una vez en esa carpeta, abra una caperta por cada usuario, y dentro de cada carpeta de usuario, 
# archivos txt mensuales con las consultas realizadas y descargadas por el usuario.
def escribirRegistro(consulta, user, formato_descarga):

    mes = time.strftime("%B")
    anio = time.strftime("%Y")
    path = "/home/administrador/Documentos/Logs_Users_ADC_MEG/" + user
    try:
        os.stat(path)
    except:
        os.mkdir(path, 0777)
    nombre_archivo = path + "/" + user + "_" + anio + "_" + mes + ".txt"
    archivo = open(nombre_archivo, 'a')
    archivo.write(time.strftime("\nDia: %d, Hora %I:%M %p \n"))
    if not formato_descarga:
        archivo.write(consulta + "\n")
    else:
        archivo.write("La consulta previa fue descargada en formato " + formato_descarga + "\n")
    archivo.close()


# La funcion ejecutarConsulta ejecuta la consulta prediseñada en la base de datos
# a traves de un cursor. Si la consulta viene por un query directo, se agregan los 
# nombres de las columnas como cabeceras de tabla de los resultados que se obtendran.
def ejecutarConsulta(consulta, esQueryDirecto, user):

    if user:
        escribirRegistro(consulta, user, '')
        print user + " ejecuto la consulta: " + consulta

    cursor = connection.cursor()
    cursor.execute(consulta)
    if esQueryDirecto:
        attos_select = [s[0] for s in cursor.description]
    resultados = cursor.fetchall()
    if esQueryDirecto:
        return [attos_select, resultados]
    return resultados
    

# La funcion exportar_csv permite la descarga de un archivo csv desde el asistente de consultas
# con los resultados de haber ejecutado alguna consulta.
def exportar_csv(request):

    usuario = request.user.get_username()
    sesion_usuario = "sesion_" + usuario
    sesion_usuario = request.session[sesion_usuario]
    resultados = sesion_usuario[1]
    cabecera = sesion_usuario[0]

    escribirRegistro('', usuario, 'CSV')

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


# La funcion exportar_xls permite la descarga de un archivo excel (xlsx) desde el asistente de consultas
# con los resultados de haber ejecutado alguna consulta.
def exportar_xls(request):

    usuario = request.user.get_username()
    sesion_usuario = "sesion_" + usuario
    sesion_usuario = request.session[sesion_usuario]
    resultados = sesion_usuario[1]
    cabecera = sesion_usuario[0]

    escribirRegistro('', usuario, 'XLS')

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="consulta.xls"'

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("consulta")

    num_fil = 0
    num_col = 0
    for elem in cabecera:
        worksheet.write(num_fil,num_col,unicode(elem).encode("utf-8"))
        num_col = num_col + 1
    num_fil = 1
    num_col = 0
    for elem in resultados:
        for e in elem:
            if isinstance(e, basestring):
                worksheet.write(num_fil,num_col,e)
            else:
                worksheet.write(num_fil,num_col,unicode(e).encode("utf-8"))
            num_col = num_col + 1
        num_fil = num_fil + 1
        num_col = 0

    workbook.save(response)

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
        data = ejecutarConsulta(consulta, False, '')
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
        context['etiquetas_score'] = lista_etq_score
        context['etiquetas_score_rr'] = lista_etq_score_rr
        context['operadoras'] = lista_operadoras
        context['validacion'] = lista_validacion
        context['orden_simple'] = lista_orden_simple
        context['orden_agrupados'] = lista_orden_agrupados
        return context


# La funcion consultas tiene dos funciones en particular:
# 1- recibir todos los request introducidos por el usuario a traves del formulario,
#    formular la consulta y mostrar la primera pagina de los resultados. 
# 2- simplemente navegar por las paginas de los resultados.
def consultas(request):

    resultados_pag = []
    page = request.GET.get('page')
    usuario = request.user.get_username()
    if not page:
        no_null= ''
        # Se obtiene los atributos a mostrar (SELECT), cuando la consulta es simple
        attos_select = request.POST.getlist('attos')
        # Se obtiene el agrupado y los campos a agrupar (SELECT), cuando la consulta es por agrupados.
        agrupado = request.POST.getlist('agrupados')
        if not attos_select:
            attos_select = request.POST.getlist('ag_attos')
        else: # La consulta es simple por lo tanto puede tener restricciones de nulidad en datos de c
            celular_null = request.POST.getlist('celular-null')
            email_null = request.POST.getlist('email-null')
            fijo_null = request.POST.getlist('fijo-null')
            if celular_null:
                no_null = 'persona.celular_prioritario IS NOT NULL'
            if email_null:
                if not no_null:
                    no_null = 'persona.email_prioritario IS NOT NULL'
                else:
                    no_null = no_null + ' AND persona.email_prioritario IS NOT NULL'
            if fijo_null:
                if not no_null:
                    no_null = 'persona.fijo_prioritario IS NOT NULL'
                else:
                    no_null = no_null + ' AND persona.fijo_prioritario IS NOT NULL'
        # Se obtiene los atributos a condicionar (WHERE) con sus valores del formulario, si existen.
        elems_where = request.POST.getlist('conds')
        attos_where = obtenerCondicionesWhere(request, elems_where)
        # Se obtiene el valor del orden y/o del limite, si existen.
        orden = request.POST.getlist('orden')
        limite = request.POST.getlist('limite')
        consulta_final = crearConsulta(attos_select, attos_where, agrupado, orden, limite)
        if no_null:
            if 'GROUP BY' not in consulta_final:
                if 'WHERE' not in consulta_final:
                    if 'LIMIT' not in consulta_final:
                        c = consulta_final.partition(';')
                        consulta_final = c[0] + ' WHERE ' + no_null + c[1]
                    else:
                        c = consulta_final.partition('LIMIT')
                        consulta_final = c[0] + 'WHERE ' + no_null + ' ' + c[1] + c[2]
                else:
                    c = consulta_final.partition('WHERE')
                    consulta_final = c[0] + c[1] + ' ' + no_null + ' AND' + c[2]
        resultados_consulta = ejecutarConsulta(consulta_final, False, usuario)
        # Si hay un agrupado se agrega a los atributos a mostrar
        if agrupado[0]:
            attos_select = agrupado + attos_select

        # Para el manejo de la sesion y los resultados sin variables globales
        sesion_usuario = "sesion_" + usuario
        if sesion_usuario in request.session:
            del request.session[sesion_usuario]
        request.session[sesion_usuario] = [attos_select, resultados_consulta]
        sesion_usuario = request.session[sesion_usuario]
    else:
        sesion_usuario = "sesion_" + usuario
        sesion_usuario = request.session[sesion_usuario]
        resultados_consulta = sesion_usuario[1]
        attos_select = sesion_usuario[0]
    # Paginacion.
    paginator = Paginator(resultados_consulta, 10) # Muestra 10 elementos por pagina.
    try:
        resultados_pag = paginator.page(page)
    except PageNotAnInteger:
        resultados_pag = paginator.page(1)
    except EmptyPage:
        resultados_pag = paginator.page(paginator.num_pages)
    context = {'atributos': attos_select, 'resultados_pag': resultados_pag, 'total_rows': len(resultados_consulta)}
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

    resultados_pag = []
    resultados_consulta = []
    page = request.GET.get('page')
    usuario = request.user.get_username()
    if not page:
        query = request.POST.get('query')
        consulta_final = query
        resultados = ejecutarConsulta(consulta_final, True, usuario)
        print resultados_consulta
        attos_select = resultados[0]
        resultados_consulta = resultados[1]

        # Para el manejo de la sesion y los resultados sin variables globales
        sesion_usuario = "sesion_" + usuario
        if sesion_usuario in request.session:
            del request.session[sesion_usuario]
        request.session[sesion_usuario] = [attos_select, resultados_consulta]
        sesion_usuario = request.session[sesion_usuario]
    else:
        sesion_usuario = "sesion_" + usuario
        sesion_usuario = request.session[sesion_usuario]
        resultados_consulta = sesion_usuario[1]
        attos_select = sesion_usuario[0]

    # Paginacion.
    paginator = Paginator(resultados_consulta, 10) # Muestra 10 elementos por pagina.
    try:
        resultados_pag = paginator.page(page)
    except PageNotAnInteger:
        resultados_pag = paginator.page(1)
    except EmptyPage:
        resultados_pag = paginator.page(paginator.num_pages)
    context = {'atributos': attos_select, 'resultados_pag': resultados_pag, 'total_rows': len(resultados_consulta)}
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
        context['lista_10'] = lista_10
        context['estados'] = Estado.objects.order_by('nombre')
        context['municipios'] = Municipio.objects.order_by('nombre')
        context['parroquias'] = Parroquia.objects.order_by('nombre')
        context['sexo'] = lista_sexo
        context['estratos'] = lista_estratos
        context['edos_civiles'] = lista_edos_civiles
        context['ipps'] = lista_ipps
        context['etiquetas_score'] = lista_etq_score
        context['etiquetas_score_rr'] = lista_etq_score_rr
        context['operadoras'] = lista_operadoras
        return context


# La funcion consultas_muestras tiene dos funciones en particular:
# 1- recibir todos los request introducidos por el usuario a traves del formulario
#    de muestras, formular la consulta y mostrar la primera pagina de los resultados. 
# 2- simplemente navegar por las paginas de los resultados.
def consultas_muestras(request):

    resultados_pag = []
    page = request.GET.get('page')
    usuario = request.user.get_username()
    if not page: 

        # Se obtiene el agrupado y los campos a agrupar (SELECT), cuando la consulta es por agrupados.
        elem_muestreo = request.POST.getlist('elems_muestreo')
        attos_select = request.POST.getlist('mst_attos')
        attos_select = elem_muestreo + attos_select
        #print elem_muestreo
        #print attos_select
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
        for fil in lista_10[0:len(lista_fils)]:
            fila = []
            for col in lista_10[0:len(lista_cols)]:
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
                    z = buscarElementoIndice(elem_muestreo[0], lista_muestreo, 1)
                    z1 = z[0] + '.' + z[1]
                    no_null = 'AND ' + z1 + ' IS NOT NULL '
                    c = crearConsulta(attos_select, lim[0], [''], [str(limit)])
                    c1 = c[:-1].partition('LIMIT')
                    c2 = c1[0] + no_null + "ORDER BY random() " + c1[1] + c1[2]
                    consulta_list.append(c2) 

        consulta = ""
        for elem in consulta_list:
            if consulta == "":
                consulta = "("+elem+")"
            else:
                consulta = consulta + " UNION " + "("+elem+")"
        consulta = consulta+";"
        consulta_final = consulta
        resultados_consulta = ejecutarConsulta(consulta_final, False, usuario)

        # Para el manejo de la sesion y los resultados sin variables globales
        sesion_usuario = "sesion_" + usuario
        if sesion_usuario in request.session:
            del request.session[sesion_usuario]
        request.session[sesion_usuario] = [attos_select, resultados_consulta]
        sesion_usuario = request.session[sesion_usuario]
    else:
        sesion_usuario = "sesion_" + usuario
        sesion_usuario = request.session[sesion_usuario]
        resultados_consulta = sesion_usuario[1]
        attos_select = sesion_usuario[0]

    # Paginacion.
    paginator = Paginator(resultados_consulta, 10) # Muestra 10 elementos por pagina.
    try:
        resultados_pag = paginator.page(page)
    except PageNotAnInteger:
        resultados_pag = paginator.page(1)
    except EmptyPage:
        resultados_pag = paginator.page(paginator.num_pages)
    context = {'atributos': attos_select, 'resultados_pag': resultados_pag, 'total_rows': len(resultados_consulta)}
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

    resultados_pag = []
    usuario = request.user.get_username()
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
            #print cedulas

        consulta = crearConsulta(attos_select, [], [u''], [u''])
        #print consulta
        if 'WHERE' not in consulta:
            consulta_final = consulta[:-1] + ' WHERE' + cedulas
        else:
            consulta_final = consulta[:-1] + ' AND' + cedulas
        #print consulta_final
        resultados_consulta = ejecutarConsulta(consulta_final, False, request.user.get_username())

        # Para el manejo de la sesion y los resultados sin variables globales
        sesion_usuario = "sesion_" + usuario
        if sesion_usuario in request.session:
            del request.session[sesion_usuario]
        request.session[sesion_usuario] = [attos_select, resultados_consulta]
        sesion_usuario = request.session[sesion_usuario]
    else:
        sesion_usuario = "sesion_" + usuario
        sesion_usuario = request.session[sesion_usuario]
        resultados_consulta = sesion_usuario[1]
        attos_select = sesion_usuario[0]

    # Paginacion.
    paginator = Paginator(resultados_consulta, 10) # Muestra 10 elementos por pagina.
    try:
        resultados_pag = paginator.page(page)
    except PageNotAnInteger:
        resultados_pag = paginator.page(1)
    except EmptyPage:
        resultados_pag = paginator.page(paginator.num_pages)
    context = {'atributos': attos_select, 'resultados_pag': resultados_pag ,'total_rows': len(resultados_consulta)}
    return render(request, 'asistente_de_consultas/consultas.html', context)


# La clase CargasView muestra el formulario para permitir el cruce de cedulas desde un archivo .csv.
# Esta ligada al uso de la funcion consultas_cargas.
class MapasView(generic.ListView):
    template_name = 'asistente_de_consultas/mapas.html'
    queryset = lista_attos

    def get_context_data(self, **kwargs):
        context = super(MapasView, self).get_context_data(**kwargs)
        context['estados'] = Estado.objects.order_by('nombre')
        context['municipios'] = Municipio.objects.order_by('nombre')
        context['parroquias'] = Parroquia.objects.order_by('nombre')
        return context


# La funcion consultas_cargas tiene dos funciones en particular:
# 1- recibir el request introducido por el usuario a traves del formulario
#    que contiene los elementos a mostrar y el archivo con cedulas para hacer el cruce
#    para luego mostrar la primera pagina de los resultados. 
# 2- simplemente navegar por las paginas de los resultados.
def consultas_mapas(request):

    edo = request.POST.getlist('edos')
    mun = request.POST.getlist('muns')
    parr = request.POST.getlist('parrs')
    ctros = request.POST.getlist('ctros')

    cond = ""
    if ctros[0] or len(ctros) > 1:
        for c in ctros:
            if c:
                if cond == "":
                    cond = cond + c
                else:
                    cond = cond + ',' + c
        cond = 'c.id in (' + cond + ')'
    elif parr[0]:
        cond = 'pa.id = ' + parr[0]
    elif mun[0]:
        cond = 'm.id = ' + mun[0]
    else:
        cond = 'e.id = ' + edo[0]

    consulta = "select distinct on (id) latitud, longitud, score_dominante, id, centro, cant from (select count(p.ci) as cant, c.id, c.nombre as centro, c.latitud, c.longitud, p.etiqueta_score as score_dominante from estado e, municipio m, parroquia pa, centro c, persona p where e.id = m.id_edo and m.id = pa.id_mun and pa.id = c.id_parr and c.id = p.id_centro and p.nac = 'V' and latitud is not null and longitud is not null and " + cond + " group by c.id, c.nombre, c.latitud, c.longitud, p.etiqueta_score order by id, cant desc) as x;"

    resultados = ejecutarConsulta(consulta, False, request.user.get_username())

    print consulta
    print resultados

    coords = []
    datos = []
    for elem in resultados:
        coords.append([float(elem[0]),float(elem[1])])
        datos.append([json.dumps(elem[2]),elem[3],json.dumps(elem[4]),int(elem[5])])

    #coords = [[10.3468,-66.9927],[10.3490,-66.99459839],[10.346,-66.98609924]]

    val = 0.0003
    centro = [0,0]
    coordenadas = []
    for c in coords:
        coordenadas.append([[c[0]-val,c[1]+val],[c[0]+val,c[1]+val],[c[0]+val,c[1]-val],[c[0]-val,c[1]-val]])
        centro[0] = centro[0]+c[0]
        centro[1] = centro[1]+c[1]
    centro[0] = centro[0]/len(coords)
    centro[1] = centro[1]/len(coords)
    context = {'coords': coords, 'coordenadas': coordenadas, 'centro': centro, 'datos': datos}
    return render(request, 'asistente_de_consultas/consultas_mapas.html', context)