# -*- coding: utf-8 -*-

# La lista lista_demografica contiene los elementos mostrables correspondientes a las tablas 
# centro, parroquia, municipio y estado.
lista_demografica = [("Estado",["estado","nombre"]),
                     ("Municipio",["municipio","nombre"]),
                     ("Parroquia",["parroquia","nombre"]),
                     ("Centro Id",["centro","id"]),
       # centro, parroquia, municipio y estado.
              ("Centro",["centro","nombre"]),
                     ("Direccion Centro",["centro","direccion"]),
                     ("Circuitos 15",["centro","circuitos_15"]),
                     ("Latitud",["centro","latitud"]),
                     ("Longitud",["centro","longitud"])
                    ]


# La lista lista_personas contiene todos los elementos mostrables correspondientes a los
# datos personales y de contacto de cada una de las personas de la bd.
lista_personas = [("Nacionalidad",["persona","nac"]),
                  ("Cedula",["persona","ci"]),
                  ("Primer Nombre",["persona","nombre1"]),
                  ("Segundo Nombre",["persona","nombre2"]),
                  ("Primer Apellido",["persona","apellido1"]),
                  ("Segundo Apellido",["persona","apellido2"]),
                  ("Fecha Nacimiento",["persona","fecha_nac"]),
                  ("Edad",["persona","date_part('year',age(persona.fecha_nac))::integer","f"]),
                  ("Sexo",["persona","sexo"]),
                  ("Estado Civil",["persona","ecivil"]),
                  ("Estrato",["persona","estrato"]),
                  ("ISEI",["persona","isei"]),
                  ("IPP",["persona","ipp"]),
                  ("Score",["persona","score"]),
                  ("Etiqueta Score", ["persona", "etiqueta_score"]),
                  ("Score_rr",["persona","score_rr"]),
                  ("Etiqueta_score_rr",["persona","etiqueta_score_rr"]),
                  ("Validacion", ["persona", "validacion"]),
                  ("Telefono Celular", ["persona", "celular_prioritario"]),
                  ("Correo Electronico", ["persona", "email_prioritario"]),
                  ("Telefono Fijo", ["persona", "fijo_prioritario"])
                 ]


# La lista lista_attos contiene todos los elementos mostrables de las tres listas anteriores.
lista_attos = lista_demografica + lista_personas 


# La lista lista_agrupados contiene todas las posibles agrupaciones de elementos que permitiran
# agrupaciones sobre si mismos. 
lista_agrupados = [("Cantidad de Estados",["estado","count(estado.id)","f"]),
                   ("Cantidad de Municipios",["municipio","count(municipio.id)","f"]),
                   ("Cantidad de Parroquias",["parroquia","count(parroquia.id)","f"]),
                   ("Cantidad de Centros",["centro","count(centro.id)","f"]),
                   ("Cantidad de Personas (Electores)",["persona","count(distinct (persona.nac, persona.ci))","f"]),
                   ("Cantidad de Telefonos Celulares",["persona","count(celular_prioritario)","f"]),
                   ("Cantidad de Correos Electronicos",["persona","count(email_prioritario)","f"]),
                   ("Cantidad de Telefonos Fijos",["persona","count(distinct (fijo_prioritario))","f"])
                  ]


# La lista lista_agrupados_select contiene todos los elementos mostrables sobre
# los cuales el usuario puede agrupar una consulta con GROUP BY.
lista_agrupados_select = [("Estado",["estado","nombre"]),
                          ("Municipio",["municipio","nombre"]),
                          ("Parroquia",["parroquia","nombre"]),
                          ("Circuitos 15",["centro","circuitos_15"]),
                          ("Centro",["centro","id"]),
                          ("Nacionalidad",["persona","nac"]),
                          ("Sexo",["persona","sexo"]),
                          ("Edad",["persona","date_part('year',age(persona.fecha_nac))::integer","f"]),
                          ("Estado Civil",["persona","ecivil"]),
                          ("Estrato",["persona","estrato"]),
                          ("IPP",["persona","ipp"]),
                          ("Etiqueta Score",["persona","etiqueta_score"]),
                          ("Etiqueta Score RR",["persona","etiqueta_score_rr"])
                         ]


# La lista lista_muestreo_select contiene todos los elementos mostrables sobre los cuales
# se puede realizar una generacion de muestras.
lista_muestreo_select = lista_demografica[0:7] + lista_personas[:-3]


# La lista lista_muestreo contiene todos los elementos sobre los cuales se puede sacar muestras.
lista_muestreo = lista_personas[-3:-1]


# La lista lista_join contiene todos los posibles join que puede haber en la base de datos. 
# Desde una tabla origen hasta una tabla destino.
lista_join = [('persona', 'centro', 'persona.id_centro = centro.id'),
              ('persona', 'parroquia', 'persona.id_centro = centro.id AND centro.id_parr = parroquia.id'),
              ('persona', 'municipio', 'persona.id_centro = centro.id AND centro.id_parr = parroquia.id AND parroquia.id_mun = municipio.id'),
              ('persona', 'estado', 
                'persona.id_centro = centro.id AND centro.id_parr = parroquia.id AND parroquia.id_mun = municipio.id AND municipio.id_edo = estado.id'),
              ('centro', 'parroquia', 'centro.id_parr = parroquia.id'),
              ('centro', 'municipio', 'centro.id_parr = parroquia.id AND parroquia.id_mun = municipio.id'),
              ('centro', 'estado', 'centro.id_parr = parroquia.id AND parroquia.id_mun = municipio.id AND municipio.id_edo = estado.id'),
              ('parroquia', 'municipio', 'parroquia.id_mun = municipio.id'),
              ('parroquia', 'estado', 'parroquia.id_mun = municipio.id AND municipio.id_edo = estado.id'),
              ('municipio', 'estado', 'municipio.id_edo = estado.id')
             ]


# La lista lista_attos_where contiene los nombres de los values de las opciones a condicionar, 
# el tipo de opcion que corresponde y una lista de todo lo que contiene, es decir, valor del 
# elemento(s) y nombre de la tabla y atributo que referencia a nivel de la base de datos.
# Los tipos son:    dependiente: input dependiente de 4 niveles. (listas desplegables dependientes).
#                   dependiente2: input dependiente de 2 niveles.
#                   simple: input simple, sea por texto o por seleccion.
#                   doble: input doble, dos inputs simples juntos.
#                   multiple: input multiple, seleccion multiple.
#                   cuadruple: input cuadruple, cuatro inputs simples juntos.
#                   rango: input doble en forma de rango (para usar between)
lista_attos_where = [["ubicacion","dependiente",[("edos",("estado","id")),("muns",("municipio","id")),("parrs",("parroquia","id")),
                                                 ("ctros",("centro","id"))], "Ubicación (Edo-Mun-Parr-Centro)", "Edo-Mun-Parr"],
                     ["ubicacion-circs","dependiente2",[("edos-circs",("estado","id")),("circs",("centro","circuitos_15"))], "Ubicación (Edo-Circuito)", "Edo-Circuito"],
                     ["centro-esp","multiple",[("centro-id",("centro","id"))],"Centro Específico"],
                     ["cedula-esp","doble",[("nac",("persona","nac")),("ci",("persona","ci"))], "Cédula de Identidad"],
                     ["nombre-completo","cuadruple",[("primer-nombre",("persona","nombre1")),("segundo-nombre",("persona","nombre2")),
                                                     ("primer-apellido",("persona","apellido1")),("segundo-apellido",("persona","apellido2"))], "Nombre Completo (Persona)"],
                     ["edad","rango",[("min-edad",("","date_part('year',age(fecha_nac))::integer")),
                                      ("max-edad",("","date_part('year',age(fecha_nac))::integer"))], "Edad", "Edad"],
                     ["genero","simple",[("sexo",("persona","sexo"))], "Sexo", "Sexo"],
                     ["estrato-soc","multiple",[("estratos",("persona","estrato"))], "Estrato Socioeconómico", "Estrato"],
                     ["estado-civil","multiple",[("estados-civiles",("persona","ecivil"))], "Estado Civil", "E. Civil"],
                     ["ipp","multiple",[("ipps",("persona","ipp"))], "Índice de Preferencia Política (IPP)", "IPP"],
                     ["isei","rango",[("min-isei",("persona","isei")),("max-isei",("persona","isei"))], "Índice Socioeconómico Inferido (ISEI)", "ISEI"],
                     ["score","rango",[("min-score",("persona","score")),("max-score",("persona","score"))], "Score", "Score"],
                     ["etiqueta-score","multiple",[("etiquetas-score",("persona","etiqueta_score"))], "Etiqueta Score", "Etq. Score"],
                     ["score-rr","rango",[("min-score-rr",("persona","score_rr")),("max-score-rr",("persona","score_rr"))], "Score RR", "Score RR"],
                     ["etiqueta-score-rr","multiple",[("etiquetas-score-rr",("persona","etiqueta_score_rr"))], "Etiqueta Score RR", "Etq. Score RR"],
                     ["operadora","multiple",[("operadoras",("","substring(celular_prioritario::text,1,3)::integer"))], "Operadora", "Operadora"],
                     ["validacion","simple",[("validaciones",("persona","validacion"))], "Validacion", "Validacion"]
                    ]


# Las listas lista_attos_matriz_cols y lista_attos_matriz_fils contienen subconjuntos
# de la lista anterior que son necesarios para las condiciones de creacion de la matriz.
lista_attos_matriz_cols = lista_attos_where[5:16] 
lista_attos_matriz_fils = lista_attos_where[0:2] + lista_attos_where[5:16]


# Lista de posibles Nacionalidades.
lista_nacionalidades = ['V','E']

# Lista de posibles Sexos.
lista_sexo = ['F','M']

# Lista de posibles Estratos.
lista_estratos = ['A','B','C','D','E']

# Lista de posibles Estados Civiles.
lista_edos_civiles = [1,2,3,4,5,6,7,8]

# Lista de posibles IPP's.
lista_ipps = [0,1,2,3,4,5,6,7,8,9]

# Lista de posibles Etiquetas Score
lista_etq_score = ['CHAVISTA', 'CHAVISTA LIGHT', 'OPOSITOR LIGHT', 'OPOSITOR']

# Lista de posibles Etiquetas Score RR
lista_etq_score_rr = ['FIRMANTES', 'GEMELOS', 'HERMANOS', 'PRIMOS', 'OTROS AZULES', 'NO AZULES']

# Lista de operadoras
lista_operadoras = [412,414,424,416,426]

# Lista validacion
lista_validacion = [0,1]

# Listas de pruebas para la dimension de la matriz.
#lista_3 = ['1','2','3']
#lista_5 = ['1','2','3','4','5']
lista_10 = ['1','2','3','4','5','6','7','8','9','10']
#lista_25 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']     


