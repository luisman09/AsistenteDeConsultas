

class AseguradoPor(models.Model):
    nac_asegurado = models.ForeignKey('Persona', db_column='nac_asegurado')
    ci_asegurado = models.IntegerField()
    nac_titular = models.ForeignKey('Persona', db_column='nac_titular')
    ci_titular = models.IntegerField()
    id_asegurado = models.ForeignKey('Persona', db_column='id_asegurado')
    id_titular = models.ForeignKey('Persona', db_column='id_titular')
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'asegurado_por'


class CaracteristicasElectorales(models.Model):
    id_persona = models.ForeignKey('Persona', db_column='id_persona', primary_key=True)
    nac = models.ForeignKey('Persona', db_column='nac')
    ci = models.IntegerField()
    tipo_mov = models.CharField(max_length=64, blank=True, null=True)
    vota_aqui = models.NullBooleanField()
    fallecido_mud = models.NullBooleanField()
    homonimo_mud = models.NullBooleanField()
    cambio_datos = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'caracteristicas_electorales'
        unique_together = (('nac', 'ci'),)


class CaracteristicasSocioeconomicas(models.Model):
    id_persona = models.ForeignKey('Persona', db_column='id_persona', primary_key=True)
    nac = models.ForeignKey('Persona', db_column='nac')
    ci = models.IntegerField()
    hijos = models.NullBooleanField()
    oficio = models.NullBooleanField()
    trabajo = models.NullBooleanField()
    profesion = models.NullBooleanField()
    familiares = models.NullBooleanField()
    info_bancaria = models.NullBooleanField()
    nse = models.NullBooleanField()
    empresa = models.NullBooleanField()
    tarjeta = models.NullBooleanField()
    cuenta = models.NullBooleanField()
    dolares = models.NullBooleanField()
    votantes = models.NullBooleanField()
    tendencia = models.NullBooleanField()
    politico = models.NullBooleanField()
    abstencion = models.NullBooleanField()
    mision = models.NullBooleanField()
    jubilado = models.NullBooleanField()
    inversionista = models.NullBooleanField()
    inmueble = models.NullBooleanField()
    vehiculo = models.NullBooleanField()
    marca = models.NullBooleanField()
    cable = models.NullBooleanField()
    viaja = models.NullBooleanField()
    seguro = models.NullBooleanField()
    deportista = models.NullBooleanField()
    club = models.NullBooleanField()
    gse = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'caracteristicas_socioeconomicas'
        unique_together = (('nac', 'ci'),)


class Celular(models.Model):
    numero = models.BigIntegerField(primary_key=True)
    nac = models.ForeignKey('Persona', db_column='nac')
    ci = models.IntegerField()
    prioridad = models.ForeignKey('Origen', db_column='prioridad')
    id_persona = models.ForeignKey('Persona', db_column='id_persona')

    class Meta:
        managed = False
        db_table = 'celular'


class Centro(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=256)
    direccion = models.CharField(max_length=256)
    mesas = models.IntegerField(blank=True, null=True)
    electores = models.IntegerField(blank=True, null=True)
    venezolanos = models.IntegerField(blank=True, null=True)
    extranjeros = models.IntegerField(blank=True, null=True)
    circuitos_15 = models.IntegerField(blank=True, null=True)
    focal = models.NullBooleanField()
    latitud = models.CharField(max_length=32, blank=True, null=True)
    longitud = models.CharField(max_length=32, blank=True, null=True)
    id_parr = models.ForeignKey('Parroquia', db_column='id_parr')

    class Meta:
        managed = False
        db_table = 'centro'


class CentroFull(models.Model):
    id = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=256, blank=True, null=True)
    direccion = models.CharField(max_length=256, blank=True, null=True)
    mesas = models.IntegerField(blank=True, null=True)
    electores = models.IntegerField(blank=True, null=True)
    venezolanos = models.IntegerField(blank=True, null=True)
    extranjeros = models.IntegerField(blank=True, null=True)
    circuitos_15 = models.IntegerField(blank=True, null=True)
    focal = models.NullBooleanField()
    latitud = models.CharField(max_length=32, blank=True, null=True)
    longitud = models.CharField(max_length=32, blank=True, null=True)
    id_parr = models.IntegerField(blank=True, null=True)
    id_mun = models.IntegerField(blank=True, null=True)
    id_edo = models.IntegerField(blank=True, null=True)
    parroquia = models.CharField(max_length=64, blank=True, null=True)
    municipio = models.CharField(max_length=64, blank=True, null=True)
    estado = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'centro_full'


class Email(models.Model):
    direccion = models.CharField(primary_key=True, max_length=256)
    nac = models.ForeignKey('Persona', db_column='nac')
    ci = models.IntegerField()
    prioridad = models.ForeignKey('Origen', db_column='prioridad')
    id_persona = models.ForeignKey('Persona', db_column='id_persona')

    class Meta:
        managed = False
        db_table = 'email'


class Empresa(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'empresa'


class Estado(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'estado'


class Fijo(models.Model):
    numero = models.BigIntegerField()
    nac = models.ForeignKey('Persona', db_column='nac')
    ci = models.IntegerField()
    prioridad = models.ForeignKey('Origen', db_column='prioridad')
    id_persona = models.ForeignKey('Persona', db_column='id_persona')
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'fijo'
        unique_together = (('numero', 'nac', 'ci'),)


class HuboCambio(models.Model):
    nac = models.ForeignKey('Persona', db_column='nac')
    ci = models.IntegerField()
    centro_viejo = models.IntegerField()
    centro_nuevo = models.ForeignKey(Centro, db_column='centro_nuevo')
    tipo_mov = models.CharField(max_length=64)
    periodo_viejo = models.IntegerField()
    periodo_nuevo = models.IntegerField()
    id_persona = models.ForeignKey('Persona', db_column='id_persona')
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'hubo_cambio'


class Municipio(models.Model):
    nombre = models.CharField(max_length=64)
    id_edo = models.ForeignKey(Estado, db_column='id_edo')
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'municipio'


class Origen(models.Model):
    prioridad = models.IntegerField(primary_key=True)
    bd_fuente = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'origen'


class Parroquia(models.Model):
    nombre = models.CharField(max_length=64)
    id = models.IntegerField(primary_key=True)
    id_mun = models.ForeignKey(Municipio, db_column='id_mun')

    class Meta:
        managed = False
        db_table = 'parroquia'


class Persona(models.Model):
    nac = models.CharField(max_length=1)
    ci = models.IntegerField()
    id_centro = models.ForeignKey(Centro, db_column='id_centro')
    nombre1 = models.CharField(max_length=64)
    nombre2 = models.CharField(max_length=64, blank=True, null=True)
    apellido1 = models.CharField(max_length=64)
    apellido2 = models.CharField(max_length=64, blank=True, null=True)
    fecha_nac = models.DateField()
    sexo = models.CharField(max_length=1)
    ecivil = models.IntegerField()
    ipp = models.IntegerField(blank=True, null=True)
    estrato = models.CharField(max_length=1, blank=True, null=True)
    isei = models.FloatField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'persona'
        unique_together = (('nac', 'ci'),)


class Producto(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    id_categoria = models.IntegerField(blank=True, null=True)
    departamento = models.IntegerField(blank=True, null=True)
    linea = models.IntegerField(blank=True, null=True)
    seccion = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=256, blank=True, null=True)
    categoria = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto'


class RefAgregados(models.Model):
    codigo = models.IntegerField(blank=True, null=True)
    referencia = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ref_agregados'


class Transaccion(models.Model):
    nac = models.ForeignKey(Persona, db_column='nac')
    ci = models.IntegerField()
    id_producto = models.ForeignKey(Producto, db_column='id_producto')
    sucursal = models.IntegerField(blank=True, null=True)
    id_empresa = models.ForeignKey(Empresa, db_column='id_empresa')
    fecha = models.DateField()
    precio = models.FloatField(blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=16)
    id_persona = models.ForeignKey(Persona, db_column='id_persona')

    class Meta:
        managed = False
        db_table = 'transaccion'


