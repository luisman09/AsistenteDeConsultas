# -*- coding: utf-8 -*-

# La lista lista_demografica contiene los elementos mostrables correspondientes a las tablas 
# centro, parroquia, municipio y estado.
lista_demografica = [("Edo Id",["estado","id"]),("Estado",["estado","nombre"]),
                     ("Mun Id",["municipio","id - (id_edo*100)"]),("Municipio",["municipio","nombre"]),
                     ("Parr Id",["parroquia","id - (id_mun*100)"]),("Parroquia",["parroquia","nombre"]),
                     ("Centro Id",["centro","id"]),("Centro",["centro","nombre"]),
                     ("Direccion Centro",["centro","direccion"]),("# Mesas",["centro","mesas"]),
                     ("# Electores",["centro","electores"]),("# Venezolanos",["centro","venezolanos"]),
                     ("# Extranjeros",["centro","extranjeros"]),("Circuitos 15",["centro","circuitos_15"]),
                     ("Focal",["centro","focal"]),("Latitud",["centro","latitud"]),
                     ("Longitud",["centro","longitud"])
                    ]


# La lista lista_personas contiene todos los elementos mostrables correspondientes a los
# datos personales de cada una de las personas de la bd.
lista_personas = [("Nacionalidad",["persona","nac"]),("Cedula",["persona","ci"]),
                  ("Primer Nombre",["persona","nombre1"]),("Segundo Nombre",["persona","nombre2"]),
                  ("Primer Apellido",["persona","apellido1"]),("Segundo Apellido",["persona","apellido2"]),
                  ("Fecha Nacimiento",["persona","fecha_nac"]),("Edad",["persona","date_part('year',age(persona.fecha_nac))::integer","f"]),
                  ("Sexo",["persona","sexo"]),("Estado Civil",["persona","ecivil"]),
                  ("Estrato",["persona","estrato"]),("ISEI",["persona","isei"]),
                  ("IPP",["persona","ipp"])
                 ]


# La lista lista_contactos contiene todos los elementos mostrables referentes a los datos
# de contacto de las personas.
lista_contactos = [("Celular 1",["celular as c1","c1.numero","c1","1"]),("Celular 2",["celular as c2","c2.numero","c2","2"]),
                   ("Celular 3",["celular as c5","c5.numero","c5","5"]),("Email 1",["email as e1","e1.direccion","e1","1"]),
                   ("Email 2",["email as e2","e2.direccion","e2","2"]),("Email 3",["email as e5","e5.direccion","e5","5"]),
                   ("Telefono Fijo 1",["fijo as f2","f2.numero","f2","2"]),("Telefono Fijo 2",["fijo as f4","f4.numero","f4","4"]),
                   ("Telefono Fijo 3",["fijo as f5","f5.numero","f5","5"])
                  ]


# La lista lista_attos contiene todos los elementos mostrables de las tres listas anteriores.
lista_attos = lista_demografica + lista_personas + lista_contactos


# La lista lista_agrupados contiene todas las posibles agrupaciones de elementos que permitiran
# agrupaciones sobre si mismos. 
lista_agrupados = [("Cantidad de Estados",["estado","count(estado.id)","f"]),
                   ("Cantidad de Municipios",["municipio","count(municipio.id)","f"]),
                   ("Cantidad de Parroquias",["parroquia","count(parroquia.id)","f"]),
                   ("Cantidad de Centros",["centro","count(centro.id)","f"]),
                   ("Cantidad de Electores (Centro)", ["centro","sum(centro.electores)","f"]),
                   ("Cantidad de Elecs Venezolanos",["centro","sum(centro.venezolanos)","f"]),
                   ("Cantidad de Elecs Extranjeros",["centro","sum(centro.extranjeros)","f"]),
                   ("Cantidad de Mesas Electorales",["centro","sum(centro.mesas)","f"]),
                   ("Cantidad de Personas",["persona","count(persona.id)","f"]),
                   ("Cantidad de Celulares Tipo 1",["celular as c1","count(c1.numero)","c1","1"]),
                   ("Cantidad de Celulares Tipo 2",["celular as c2","count(c2.numero)","c2","2"]),
                   ("Cantidad de Celulares Tipo 3",["celular as c3","count(c3.numero)","c3","3"]),
                   ("Cantidad de Emails Tipo 1",["email as e1","count(e1.direccion)","e1","1"]),
                   ("Cantidad de Emails Tipo 2",["email as e2","count(e2.direccion)","e2","2"]),
                   ("Cantidad de Emails Tipo 3",["email as e3","count(e3.direccion)","e3","3"]),
                   ("Cantidad de Telefonos Fijos",["fijo","count(distinct (fijo.numero))","f"])
                  ]


# La lista lista_agrupados_select contiene todos los elementos mostrables sobre
# los cuales el usuario puede agrupar una consulta con GROUP BY.
lista_agrupados_select = [("Estado",["estado","nombre"]),("Municipio",["municipio","nombre"]),
                          ("Parroquia",["parroquia","nombre"]),("Circuitos 15",["centro","circuitos_15"]),
                          ("Centro",["centro","id"]),("Nacionalidad",["persona","nac"]),
                          ("Sexo",["persona","sexo"]),("Estado Civil",["persona","ecivil"]),
                          ("Estrato",["persona","estrato"]),("IPP",["persona","ipp"]),("ISEI",["persona","isei"]),
                          ("Edad",["persona","date_part('year',age(persona.fecha_nac))::integer","f"]),
                         ]


# La lista lista_muestreo_select contiene todos los elementos mostrables sobre los cuales
# se puede realizar una generacion de muestras.
lista_muestreo_select = lista_demografica[0:9] + lista_demografica[13:15] + lista_personas


# La lista lista_muestreo contiene todos los elementos sobre los cuales se puede sacar muestras.
lista_muestreo = lista_contactos[0:6]


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
              ('municipio', 'estado', 'municipio.id_edo = estado.id'),
              ('celular as c1', 'persona', 'c1.id_persona = persona.id'),
              ('celular as c2', 'persona', 'c2.id_persona = persona.id'),
              ('celular as c5', 'persona', 'c5.id_persona = persona.id'),
              ('email as e1', 'persona', 'e1.id_persona = persona.id'),
              ('email as e2', 'persona', 'e2.id_persona = persona.id'),
              ('email as e5', 'persona', 'e5.id_persona = persona.id'),
              ('fijo as f2', 'persona', 'f2.id_persona = persona.id'),
              ('fijo as f4', 'persona', 'f4.id_persona = persona.id'),
              ('fijo as f5', 'persona', 'f5.id_persona = persona.id'),
              ('fijo', 'persona', 'fijo.id_persona = persona.id')
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
                     ["cant-mesas","rango",[("min-mesas",("centro","mesas")),("max-mesas",("centro","mesas"))], "Cantidad de Mesas Electorales"],
                     ["cant-elects","rango",[("min-elects",("centro","electores")),("max-elects",("centro","electores"))], "Cantidad de Electores (Centro)"],
                     ["cant-venez","rango",[("min-venez",("centro","venezolanos")),("max-venez",("centro","venezolanos"))], "Cantidad de Elects Venezolanos"],
                     ["cant-extr","rango",[("min-extr",("centro","extranjeros")),("max-extr",("centro","extranjeros"))], "Cantidad de Elects Extranjeros"],
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
                    ]


# Las listas lista_attos_matriz_cols y lista_attos_matriz_fils contienen subconjuntos
# de la lista anterior que son necesarios para las condiciones de creacion de la matriz.
lista_attos_matriz_cols = lista_attos_where[9:15] 
lista_attos_matriz_fils = lista_attos_where[0:2] + lista_attos_where[9:15] 


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


# Listas de pruebas para la dimension de la matriz.
lista_3 = ['1','2','3']
lista_5 = ['1','2','3','4','5']
lista_10 = ['1','2','3','4','5','6','7','8','9','10']
lista_25 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']


# Lista de posibles dimensiones precalculadas de la matriz. 
lista_matrices = [("3 x 3", lista_3, lista_3), ("5 x 3", lista_5, lista_3), ("5 x 5", lista_5, lista_5),
                  ("10 x 5", lista_10, lista_5), ("10 x 10", lista_10, lista_10), ("25 x 10", lista_25, lista_10) 
                 ]         


