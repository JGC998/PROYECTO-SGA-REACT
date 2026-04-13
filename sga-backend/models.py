"""
models.py — Modelos SQLAlchemy mapeados a las tablas REALES de la base de datos LIN (esquema dbo).

Convención de alias:
  Cada columna legacy (en MAYÚSCULAS) se expone con un nombre pythónico limpio
  usando el parámetro de nombre en Column('NOMBRE_COLUMNA', ...).
"""

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    ForeignKey, PrimaryKeyConstraint, Text
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# ==============================================================================
# USUARIOS WEB (tabla propia del SGA, no existe en LIN)
# Mantenemos esta tabla en el esquema dbo pero es propia.
# ==============================================================================

class Usuario(Base):
    """Usuario del API REST (login web con JWT). No es SGAUSUARIO."""
    __tablename__ = "sga_usuarios"
    __table_args__ = {'schema': 'sga'}

    id             = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre         = Column(String(100), nullable=False)
    email          = Column(String(150), unique=True, nullable=False, index=True)
    password_hash  = Column(String(255), nullable=False)
    rol            = Column(String(20), nullable=False)   # 'admin' | 'supervisor' | 'operario'
    activo         = Column(Boolean, default=True)
    ultimo_acceso  = Column(DateTime, nullable=True)
    creado_en      = Column(DateTime, default=datetime.utcnow)


class AuditoriaLog(Base):
    """Log de auditoría del SGA web (tabla propia)."""
    __tablename__ = "sga_auditoria_log"
    __table_args__ = {'schema': 'sga'}

    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id    = Column(Integer, nullable=True)
    accion        = Column(String(50), nullable=False)
    entidad       = Column(String(50), nullable=False)
    entidad_id    = Column(String(50), nullable=True)  # str porque ahora los IDs son string
    datos_antes   = Column(Text, nullable=True)
    datos_despues = Column(Text, nullable=True)
    ip            = Column(String(45), nullable=True)
    fecha         = Column(DateTime, default=datetime.utcnow)


# ==============================================================================
# TABLAS DE LA BASE DE DATOS LIN (esquema dbo — tablas heredadas de la empresa)
# ==============================================================================

class Articulo(Base):
    """
    Artículos del almacén — tabla ARTICULO de LIN.
    PK: ARTCOD (código alfanumérico, ej. 'A0001')
    """
    __tablename__ = 'ARTICULO'
    __table_args__ = {'schema': 'dbo'}

    sku           = Column('ARTCOD',      String(10), primary_key=True)
    nombre        = Column('ARTNOM',      String(50),  nullable=True, default='')
    codigo2       = Column('ARTCOD2',     String(30),  nullable=True)
    barcode       = Column('ARTBARCOD',   String(30),  nullable=True)
    barcode_caja  = Column('ARTCAJBARCOD',String(30),  nullable=True)
    barcode_palet = Column('ARTPALBARCOD',String(14),  nullable=True)
    codigo_largo  = Column('ARTLARCOD',   String(50),  nullable=True)
    peso_uni      = Column('ARTPESUNI',   Float,       nullable=True, default=0)
    stock_min     = Column('ARTSTOMIN',   Float,       nullable=True, default=0)
    stock_max     = Column('ARTSTOMAX',   Float,       nullable=True, default=0)
    precio_coste  = Column('ARTCOS',      Float,       nullable=True, default=0)
    grupo         = Column('ARTGRUCOD',   String(5),   nullable=True)
    unidad_medida = Column('ARTMEDCOD',   String(20),  nullable=True)
    material      = Column('ARTMAT',      String(20),  nullable=True)
    color         = Column('ARTCOL',      String(20),  nullable=True)
    imagen_url    = Column('ARTIMA',      String(255), nullable=True)
    # ARTMOS: 0 = mostrar, 1 = ocultar
    oculto        = Column('ARTMOS',      Integer,     nullable=True, default=0)
    usa_lote      = Column('ARTLOTMER',   Integer,     nullable=True, default=0)
    fecha_inv     = Column('ARTFECINV',   DateTime,    nullable=True)
    asin          = Column('ARTASIN',     String(11),  nullable=True)

    @property
    def activo(self):
        return self.oculto == 0

    @property
    def id(self):
        """Alias para compatibilidad con el frontend: devuelve el SKU como id."""
        return self.sku


class Almacen(Base):
    """
    Almacenes — tabla ALMACENES de LIN.
    PK: ALMCOD (código de 2 caracteres, ej. 'A1')
    """
    __tablename__ = 'ALMACENES'
    __table_args__ = {'schema': 'dbo'}

    codigo = Column('ALMCOD', String(2), primary_key=True)
    nombre = Column('ALMNOM', String(50), nullable=True)

    @property
    def id(self):
        return self.codigo

    @property
    def activo(self):
        return True


class Ubicacion(Base):
    """
    Ubicaciones físicas del almacén — tabla UBICACION de LIN.
    PK: UBICON (número secuencial Float)
    """
    __tablename__ = 'UBICACION'
    __table_args__ = {'schema': 'dbo'}

    id          = Column('UBICON',       Float,    primary_key=True)
    codigo      = Column('UBICODUBI',    String(20), nullable=True, default='')
    nombre      = Column('UBINOM',       String(50), nullable=True, default='')
    almacen_cod = Column('UBIALMCOD',    String(2),  nullable=True, default='')
    alto        = Column('UBIALT',       Float,    nullable=True, default=0)
    ancho       = Column('UBIANC',       Float,    nullable=True, default=0)
    num_palets  = Column('UBINUMPAL',    Integer,  nullable=True, default=1)
    # UBILIB: 1 = libre/activa, 0 = bloqueada
    libre       = Column('UBILIB',       Integer,  nullable=True, default=0)
    multi_art   = Column('UBIMUL',       Integer,  nullable=True, default=0)

    @property
    def activo(self):
        return True

    @property
    def descripcion(self):
        return self.nombre


class Stock(Base):
    """
    Stock por artículo, ubicación y lote — tabla STOCK de LIN.
    PK compuesta: (STOARTCOD, STOUBI, STOLOT)
    NO tiene id autoincremental — usar la PK compuesta.
    """
    __tablename__ = 'STOCK'
    __table_args__ = (
        PrimaryKeyConstraint('STOARTCOD', 'STOUBI', 'STOLOT', name='IDSTO1'),
        {'schema': 'dbo'}
    )

    articulo_cod = Column('STOARTCOD', String(10), primary_key=True)
    ubicacion    = Column('STOUBI',    String(20), primary_key=True)
    lote         = Column('STOLOT',    String(10), primary_key=True)
    cantidad     = Column('STOCAN',    Float,      nullable=True)


class Proveedor(Base):
    """
    Proveedores — tabla PROVEEDOR de LIN (misma estructura que CLIENTE).
    PK compuesta: (CLICOD, CLICENCOD). Usamos CLICOD como identificador principal en la API.
    """
    __tablename__ = 'PROVEEDOR'
    __table_args__ = (
        PrimaryKeyConstraint('CLICOD', 'CLICENCOD', name='IDPROVEEDOR1'),
        {'schema': 'dbo'}
    )

    cod       = Column('CLICOD',    String(15), primary_key=True)
    cen_cod   = Column('CLICENCOD', String(4),  primary_key=True, default='')
    razon     = Column('CLIRAZ',    String(50), nullable=True, default='')
    nombre    = Column('CLINOM',    String(50), nullable=True, default='')
    direccion = Column('CLIDIR',    String(100),nullable=True, default='')
    cp        = Column('CLIPOSCOD', String(10), nullable=True, default='')
    ciudad    = Column('CLIPOSCIU', String(30), nullable=True, default='')
    provincia = Column('CLIPOSPRO', String(15), nullable=True, default='')
    nif       = Column('CLINIF',    String(15), nullable=True, default='')
    telefono  = Column('CLITEL',    String(40), nullable=True, default='')
    pais      = Column('CLIPAICOD', String(3),  nullable=True, default='')
    contacto  = Column('CLIPERCON', String(50), nullable=True, default='')
    email     = Column('CLIEMA',    String(50), nullable=True, default='')
    cargo     = Column('CLICAR',    String(50), nullable=True, default='')

    @property
    def id(self):
        return self.cod

    @property
    def activo(self):
        return True

    @property
    def cif(self):
        return self.nif


class Cliente(Base):
    """
    Clientes — tabla CLIENTE de LIN.
    PK compuesta: (CLICOD, CLICENCOD).
    """
    __tablename__ = 'CLIENTE'
    __table_args__ = (
        PrimaryKeyConstraint('CLICOD', 'CLICENCOD', name='IDCLIENTE1'),
        {'schema': 'dbo'}
    )

    cod       = Column('CLICOD',    String(15), primary_key=True)
    cen_cod   = Column('CLICENCOD', String(4),  primary_key=True, default='')
    razon     = Column('CLIRAZ',    String(50), nullable=True, default='')
    nombre    = Column('CLINOM',    String(50), nullable=True, default='')
    direccion = Column('CLIDIR',    String(100),nullable=True, default='')
    cp        = Column('CLIPOSCOD', String(10), nullable=True, default='')
    ciudad    = Column('CLIPOSCIU', String(30), nullable=True, default='')
    provincia = Column('CLIPOSPRO', String(15), nullable=True, default='')
    nif       = Column('CLINIF',    String(15), nullable=True, default='')
    telefono  = Column('CLITEL',    String(40), nullable=True, default='')
    pais      = Column('CLIPAICOD', String(3),  nullable=True, default='')
    contacto  = Column('CLIPERCON', String(50), nullable=True, default='')
    email     = Column('CLIEMA',    String(50), nullable=True, default='')
    cargo     = Column('CLICAR',    String(50), nullable=True, default='')
    idioma    = Column('CLIIDICOD', String(3),  nullable=True, default='')

    @property
    def id(self):
        return self.cod


class SgaUsuarioLegacy(Base):
    """
    Usuarios del SGA legacy (Windows app) — tabla SGAUSUARIO de LIN.
    Diferente de la tabla sga.usuarios (que es para el API REST web).
    """
    __tablename__ = 'SGAUSUARIO'
    __table_args__ = {'schema': 'dbo'}

    codigo  = Column('USUCOD',  String(10), primary_key=True)
    nombre  = Column('USUNOM',  String(50),  nullable=True, default='')
    nivel   = Column('USUNIV',  Integer,     nullable=True, default=0)
    tipo    = Column('USUTIP',  Integer,     nullable=True, default=0)
    # Contraseñas del sistema legacy (no usadas para JWT)
    clave1  = Column('USUCONENT', String(10), nullable=True)
    clave2  = Column('USUCONENT2', String(10), nullable=True)


class Picking(Base):
    """
    Órdenes de picking — tabla PICKING de LIN.
    PK: PICCOD (Float, secuencial)
    """
    __tablename__ = 'PICKING'
    __table_args__ = {'schema': 'dbo'}

    id           = Column('PICCOD',    Float,    primary_key=True)
    loaser       = Column('PICLOASER', String(5),  nullable=False)
    loacod       = Column('PICLOACOD', Float,    nullable=False)
    recuento     = Column('PICREC',    Integer,  nullable=True)
    operario_cod = Column('PICREPCOD', String(15), nullable=True)
    fecha_ini    = Column('PICFECINI', DateTime, nullable=True)
    hora_ini     = Column('PICHORINI', DateTime, nullable=True)
    fecha_fin    = Column('PICFECFIN', DateTime, nullable=True)
    hora_fin     = Column('PICHORFIN', DateTime, nullable=True)


class MovimientoStock(Base):
    """
    Movimientos de almacén (entradas/salidas) — tabla ALBARANCS de LIN.
    Cada fila es un movimiento de stock de un artículo en una ubicación.
    PK compuesta de 6 campos.
    """
    __tablename__ = 'ALBARANCS'
    __table_args__ = (
        PrimaryKeyConstraint(
            'ACSSER', 'ACSEJE', 'ACSNUM', 'ACSMOV', 'ACSACLCOD', 'ACSCOD',
            name='IDACS1'
        ),
        {'schema': 'dbo'}
    )

    serie       = Column('ACSSER',    String(5),  primary_key=True)
    ejercicio   = Column('ACSEJE',    String(4),  primary_key=True)
    numero      = Column('ACSNUM',    Float,      primary_key=True)
    mov         = Column('ACSMOV',    String(2),  primary_key=True)
    aclcod      = Column('ACSACLCOD', Float,      primary_key=True)
    cod         = Column('ACSCOD',    Float,      primary_key=True)
    fecha       = Column('ACSFEC',    DateTime,   nullable=True)
    cliente_cod = Column('ACSCLICOD', String(9),  nullable=True)
    articulo_cod= Column('ACSARTCOD', String(10), nullable=True)
    cantidad_pal= Column('ACSPAL',    Float,      nullable=True)
    cantidad_caj= Column('ACSCAJ',    Float,      nullable=True)
    cantidad_uni= Column('ACSUNI',    Float,      nullable=True)
    cantidad    = Column('ACSCAN',    Float,      nullable=True)
    lote        = Column('ACSLOT',    String(10), nullable=True)
    ubicacion   = Column('ACSUBI',    String(20), nullable=True)
    tipo_mov    = Column('ACSTIPMOV', String(16), nullable=True)
    almacen_cod = Column('ACSALMCOD', String(2),  nullable=True)
    hora        = Column('ACSHOR',    DateTime,   nullable=True)
    manual      = Column('ACSMAN',    Integer,    nullable=True)
    cliente_nom = Column('ACSCLINOM', String(50), nullable=True)
    num_alb     = Column('ACSNUMALB', String(10), nullable=True)


class SubFamilia(Base):
    """
    Subfamilias/Categorías de artículos — tabla SUBFAMILIA de LIN.
    """
    __tablename__ = 'SUBFAMILIA'
    __table_args__ = {'schema': 'dbo'}

    codigo  = Column('SUBFAMCOD', String(5), primary_key=True)
    nombre  = Column('SUBFAMNOM', String(50), nullable=True, default='')

    @property
    def id(self):
        return self.codigo