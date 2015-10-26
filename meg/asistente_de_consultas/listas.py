# -*- coding: utf-8 -*-

# Las siguientes listas contienen elementos de la forma: (elem1,(elem2,elem3)), 
# donde elem1 es el nombre del atributo que se le presentara al usuario, 
# elem2 es el nombre de la tabla en postgresql y elem3 el nombre del atributo
# en postgresql. 


# La lista demografica contiene los datos de las tablas centro, parroquia, municipio y estado.
# Representa los centros de votacion actuales con sus caracteristicas y sus ubicaciones.
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


lista_personas = [("Nacionalidad",["persona","nac"]),("Cedula",["persona","ci"]),
                  ("Primer Nombre",["persona","nombre1"]),("Segundo Nombre",["persona","nombre2"]),
                  ("Primer Apellido",["persona","apellido1"]),("Segundo Apellido",["persona","apellido2"]),
                  ("Fecha Nacimiento",["persona","fecha_nac"]),("Edad",["persona","date_part('year',age(persona.fecha_nac))::integer","f"]),
                  ("Sexo",["persona","sexo"]),("Estado Civil",["persona","ecivil"]),
                  ("Estrato",["persona","estrato"]),("ISEI",["persona","isei"]),
                  ("IPP",["persona","ipp"])
                 ]


lista_contactos = [("Celular 1",["celular as c1","c1.numero","c1","1"]),("Celular 2",["celular as c2","c2.numero","c2","2"]),
                   ("Celular 3",["celular as c5","c5.numero","c5","5"]),("Email 1",["email as e1","e1.direccion","e1","1"]),
                   ("Email 2",["email as e2","e2.direccion","e2","2"]),("Email 3",["email as e5","e5.direccion","e5","5"]),
                   ("Telefono Fijo 1",["fijo as f2","f2.numero","f2","2"]),("Telefono Fijo 2",["fijo as f4","f4.numero","f4","4"]),
                   ("Telefono Fijo 3",["fijo as f5","f5.numero","f5","5"])
                  ]


# La funcion lista_attos retorna una lista que devuelve tuplas, en donde los primeros elementos
# son los nombres visibles de los atributos que puede escoger el usuario y los segundos elementos 
# son a su vez tuplas, que representan el nombre de la tabla y el nombre del 
# atributo (o funcion) tal cual como aparecen (o se ejecutan) a nivel de base de datos.
lista_attos = lista_demografica + lista_personas + lista_contactos

lista_agrupados = [("Cantidad de Estados",["estado","count(estado.id)","f"]),
                   ("Cantidad de Municipios",["municipio","count(municipio.id)","f"]),
                   ("Cantidad de Parroquias",["parroquia","count(parroquia.id)","f"]),
                   ("Cantidad de Centros",["centro","count(centro.id)","f"]),
                   ("Cantidad de Electores", ["centro","sum(centro.electores)","f"]),
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


lista_agrupados_nivel_1 = [("Estado",["estado","nombre"])]
lista_agrupados_nivel_2 = lista_agrupados_nivel_1 + [("Municipio",["municipio","nombre"])]
lista_agrupados_nivel_3 = lista_agrupados_nivel_2 + [("Parroquia",["parroquia","nombre"])]
lista_agrupados_nivel_4 = lista_agrupados_nivel_3 + [("Circuitos 15",["centro","circuitos_15"])]
lista_agrupados_nivel_5 = lista_agrupados_nivel_4 + [("Centro",["centro","id"]),("Nacionalidad",["persona","nac"]),
                                                     ("Sexo",["persona","sexo"]),("Estado Civil",["persona","ecivil"]),
                                                     ("Estrato",["persona","estrato"]),("IPP",["persona","ipp"]),
                                                     ("Edad",["persona","date_part('year',age(persona.fecha_nac))::integer","f"]),
                                                    ]


# la lista cambios contiene los datos de la tabla hubo_cambios.
# Representa los cambios ocurridos entre diferentes elecciones.
lista_cambios = [("Tipo de Cambio",("hubo_cambio","tipo_mov")),("Centro Anterior",("hubo_cambio","centro_viejo")),
                 ("Centro Vigente",("hubo_cambio","centro_nuevo")),("Valido hasta",("hubo_cambio","periodo_viejo")),
                 ("Vigente desde",("hubo_cambio","periodo_nuevo"))
                ]


# La lista indicadores contiene los datos de la tabla caracteristicas_socioeconomicas.
# Representa algunas caracteristicas socioeconomicas de un grupo de personas.
lista_indicadores = [("Hijos",("caracteristicas_socioeconomicas","hijos")),("Profesion",("caracteristicas_socioeconomicas","profesion")),
                     ("Oficio",("caracteristicas_socioeconomicas","oficio")),("Trabajo",("caracteristicas_socioeconomicas","trabajo")),
                     ("Familiares",("caracteristicas_socioeconomicas","familiares")),("Info Bancaria",("caracteristicas_socioeconomicas","info_bancaria")),
                     ("NSE",("caracteristicas_socioeconomicas","nse")),("Tarjeta",("caracteristicas_socioeconomicas","tarjeta")),
                     ("Empresa",("caracteristicas_socioeconomicas","empresa")),("Cuenta",("caracteristicas_socioeconomicas","cuenta")),
                     ("Dólares",("caracteristicas_socioeconomicas","dolares")),("Votantes",("caracteristicas_socioeconomicas","votantes")),
                     ("Tendencia",("caracteristicas_socioeconomicas","tendencia")),("Politico",("caracteristicas_socioeconomicas","politico")),
                     ("Abstención",("caracteristicas_socioeconomicas","abstencion")),("Mision",("caracteristicas_socioeconomicas","mision")),
                     ("Jubilado",("caracteristicas_socioeconomicas","jubilado")),("Inversionista",("caracteristicas_socioeconomicas","inversionista")),
                     ("Inmueble",("caracteristicas_socioeconomicas","inmueble")),("Vehiculo",("caracteristicas_socioeconomicas","vehiculo")),
                     ("Marca",("caracteristicas_socioeconomicas","marca")),("Cable",("caracteristicas_socioeconomicas","cable")),
                     ("Viaja",("caracteristicas_socioeconomicas","viaja")),("Seguro",("caracteristicas_socioeconomicas","seguro")),
                     ("Deportista",("caracteristicas_socioeconomicas","deportista")),("Club",("caracteristicas_socioeconomicas","club")),
                     ("GSE",("caracteristicas_socioeconomicas","gse"))
                    ]


# La lista sector privado contiene los datos de las tablas empresa, producto y transaccion.
# Representa los datos de adquision de productos o servicios en algunas empresas por parte de algunas personas. 
lista_sector_privado = [("Empresa Id",("empresa","id")),("Empresa",("empresa","nombre")),
                        ("Producto Id",("producto","id")),("Producto",("producto","nombre")),
                        ("Categoria Id",("producto","id_categoria")),("Categoria",("producto","categoria")),
                        ("Departamento",("producto","departamento")),("Linea",("producto","linea")),
                        ("Seccion",("producto","seccion")),("Sucursal",("transaccion","sucursal")),
                        ("Fecha de Adquisicion",("transaccion","fecha")),("Cantidad Adquirida",("transaccion","cantidad")),
                        ("Precio",("transaccion","precio"))
                       ]


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


# La lista attos_where contiene los nombres de los values de las opciones a condicionar, 
# el tipo de opcion que corresponde y una lista de todo lo que contiene, es decir, valor del 
# elemento(s) y nombre de la tabla y atributo que referencia a nivel de la base de datos.
# Los tipos son:    dependiente: input dependiente. (listas desplegables dependientes).
#                   simple: input simple, sea por texto o por seleccion.
#                   doble: input doble, dos inputs simples juntos.
#                   multiple: input multiple, seleccion multiple.
#                   cuadruple: input cuadruple, cuatro inputs simples juntos.
#                   rango: input doble en forma de rango (para usar between)
lista_attos_where = [("ubicacion","dependiente",[("edos",("estado","id")),("muns",("municipio","id")),("parrs",("parroquia","id")),
                                                 ("ctros",("centro","id"))], "Ubicación (Edo-Mun-Parr-Centro)"),
                     ("ubicacion-circs","dependiente2",[("edos-circs",("estado","id")),("circs",("centro","circuitos_15"))], "Ubicación (Edo-Circuito)"),
                     ("centro-esp","multiple",[("centro-id",("centro","id"))],"Centro Específico"),
                     ("cant-mesas","rango",[("min-mesas",("centro","mesas")),("max-mesas",("centro","mesas"))],"Cantidad de Mesas Electorales"),
                     ("cant-elects","rango",[("min-elects",("centro","electores")),("max-elects",("centro","electores"))],"Cantidad de Electores"),
                     ("cant-venez","rango",[("min-venez",("centro","venezolanos")),("max-venez",("centro","venezolanos"))],"Cantidad de Elects Venezolanos"),
                     ("cant-extr","rango",[("min-extr",("centro","extranjeros")),("max-extr",("centro","extranjeros"))],"Cantidad de Elects Extranjeros"),
                     ("cedula-esp","doble",[("nac",("persona","nac")),("ci",("persona","ci"))],"Cédula de Identidad"),
                     ("nombre-completo","cuadruple",[("primer-nombre",("persona","nombre1")),("segundo-nombre",("persona","nombre2")),
                                                     ("primer-apellido",("persona","apellido1")),("segundo-apellido",("persona","apellido2"))],"Nombre Completo"),
                     ("edad","rango",[("min-edad",("","date_part('year',age(fecha_nac))::integer")),
                                      ("max-edad",("","date_part('year',age(fecha_nac))::integer"))],"Edad"),
                     ("genero","simple",[("sexo",("persona","sexo"))],"Sexo"),
                     ("estrato-soc","multiple",[("estratos",("persona","estrato"))],"Estrato Socioeconómico"),
                     ("estado-civil","multiple",[("estados-civiles",("persona","ecivil"))],"Estado Civil"),
                     ("ipp","multiple",[("ipps",("persona","ipp"))],"Índice de Preferencia Política (IPP)"),
                     ("isei","rango",[("min-isei",("persona","isei")),("max-isei",("persona","isei"))],"Índice Socioeconómico Inferido (ISEI)"),
                    ]

lista_circuitos_15 = [1,2,3,4,5,6,7,8,9,10,11,12]

lista_nacionalidades = ['V','E']

lista_sexo = ['F','M']

lista_estratos = ['A','B','C','D','E']

lista_edos_civiles = [0,1,2,3,4,5,6,7,8]

lista_ipps = [0,1,2,3,4,5,6,7,8,9]
