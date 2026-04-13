from typing import Optional
import datetime

from sqlalchemy import CHAR, Column, DateTime, Float, Identity, Index, Integer, PrimaryKeyConstraint, String, TEXT, Table, Unicode, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class ALBARANCJ(Base):
    __tablename__ = 'ALBARANCJ'
    __table_args__ = (
        PrimaryKeyConstraint('ACJSER', 'ACJEJE', 'ACJNUM', 'ACJMOV', 'ACJCOD', name='IDACJ1'),
        Index('IDACJ2', 'ACJSER', 'ACJEJE', 'ACJNUM', 'ACJMOV', mssql_clustered=False),
        {'schema': 'dbo'}
    )

    ACJSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACJEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACJNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACJMOV: Mapped[str] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACJCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACJCER: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


class ALBARANCL(Base):
    __tablename__ = 'ALBARANCL'
    __table_args__ = (
        PrimaryKeyConstraint('ACLACCSER', 'ACLACCEJE', 'ACLACCNUM', 'ACLMOV', 'ACLCOD', name='IDACL1'),
        Index('IDalbarancl25092023', 'ACLCANSER', 'ACLCAN', 'ACLLINSER', 'ACLREPCOD', 'ACLACCSER', 'ACLACCEJE', 'ACLACCNUM', 'ACLMOV', 'ACLCOD', mssql_clustered=False),
        {'schema': 'dbo'}
    )

    ACLACCSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACLACCEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACLACCNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACLMOV: Mapped[str] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACLCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACLARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACLCAN: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLCANCAJ: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLALBOBS: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'))
    ACLMOTCOD: Mapped[Optional[str]] = mapped_column(CHAR(3, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACLCANSER: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACLLINPRO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACLACCFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    ACLUBI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    ACLREPCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACLLINSER: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACLPRE: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLDES1: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLLOTINI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    ACLCLIDES: Mapped[Optional[str]] = mapped_column(CHAR(11, 'Modern_Spanish_CI_AS'))
    ACLPEDORI: Mapped[Optional[str]] = mapped_column(CHAR(7, 'Modern_Spanish_CI_AS'))
    ACLCANINI: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLCANCOMP: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLEMPCOD: Mapped[Optional[str]] = mapped_column(CHAR(12, 'Modern_Spanish_CI_AS'), server_default=text("('LIN')"))
    ACLUTI: Mapped[Optional[int]] = mapped_column(Integer)
    ACLCANREC: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text("('0')"))


t_ALBARANCL05022024 = Table(
    'ALBARANCL05022024', Base.metadata,
    Column('ACLACCSER', CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACLACCEJE', CHAR(4, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACLACCNUM', Float(53), nullable=False),
    Column('ACLMOV', CHAR(2, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACLCOD', Float(53), nullable=False),
    Column('ACLARTCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACLCAN', Float(53)),
    Column('ACLCANCAJ', Float(53)),
    Column('ACLALBOBS', CHAR(255, 'Modern_Spanish_CI_AS')),
    Column('ACLMOTCOD', CHAR(3, 'Modern_Spanish_CI_AS')),
    Column('ACLCANSER', Float(53)),
    Column('ACLLINPRO', Integer),
    Column('ACLACCFEC', DateTime),
    Column('ACLUBI', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACLREPCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACLLINSER', Integer),
    Column('ACLPRE', Float(53)),
    Column('ACLDES1', Float(53)),
    Column('ACLLOTINI', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACLCLIDES', CHAR(11, 'Modern_Spanish_CI_AS')),
    Column('ACLPEDORI', CHAR(7, 'Modern_Spanish_CI_AS')),
    Column('ACLCANINI', Float(53)),
    Column('ACLCANCOMP', Float(53)),
    Column('ACLEMPCOD', CHAR(12, 'Modern_Spanish_CI_AS')),
    Column('ACLUTI', Integer),
    schema='dbo'
)


t_ALBARANCL050220242 = Table(
    'ALBARANCL050220242', Base.metadata,
    Column('ACLACCSER', CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACLACCEJE', CHAR(4, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACLACCNUM', Float(53), nullable=False),
    Column('ACLMOV', CHAR(2, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACLCOD', Float(53), nullable=False),
    Column('ACLARTCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACLCAN', Float(53)),
    Column('ACLCANCAJ', Float(53)),
    Column('ACLALBOBS', CHAR(255, 'Modern_Spanish_CI_AS')),
    Column('ACLMOTCOD', CHAR(3, 'Modern_Spanish_CI_AS')),
    Column('ACLCANSER', Float(53)),
    Column('ACLLINPRO', Integer),
    Column('ACLACCFEC', DateTime),
    Column('ACLUBI', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACLREPCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACLLINSER', Integer),
    Column('ACLPRE', Float(53)),
    Column('ACLDES1', Float(53)),
    Column('ACLLOTINI', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACLCLIDES', CHAR(11, 'Modern_Spanish_CI_AS')),
    Column('ACLPEDORI', CHAR(7, 'Modern_Spanish_CI_AS')),
    Column('ACLCANINI', Float(53)),
    Column('ACLCANCOMP', Float(53)),
    Column('ACLEMPCOD', CHAR(12, 'Modern_Spanish_CI_AS')),
    Column('ACLUTI', Integer),
    schema='dbo'
)


class ALBARANCS(Base):
    __tablename__ = 'ALBARANCS'
    __table_args__ = (
        PrimaryKeyConstraint('ACSSER', 'ACSEJE', 'ACSNUM', 'ACSMOV', 'ACSACLCOD', 'ACSCOD', name='IDACS1'),
        Index('IDACS08102023', 'ACSSER', 'ACSMOV', 'ACSCAN', 'ACSFEC', mssql_clustered=False, mssql_include=['ACSEJE', 'ACSNUM', 'ACSACLCOD', 'ACSCOD']),
        Index('IDACS2', 'ACSLOT', 'ACSUBI', 'ACSARTCOD', mssql_clustered=False),
        Index('IDACS20', 'ACSFEC', 'ACSLOT', mssql_clustered=False, mssql_include=['ACSSER', 'ACSEJE', 'ACSNUM', 'ACSMOV', 'ACSACLCOD', 'ACSCOD', 'ACSCLICOD', 'ACSARTCOD', 'ACSPAL', 'ACSCAJ', 'ACSUNI', 'ACSCAN', 'ACSUBI', 'ACSNUMPAL', 'ACSNUMCAJ', 'ACSREPCOD', 'ACSENV', 'ACSREGFEC', 'ACSREGSER', 'ACSREGEJE', 'ACSREGNUM', 'ACSALBOBS', 'ACSCANREA', 'ACSHOR', 'ACSMAN', 'ACS2LOT', 'ACSALMCOD', 'ACSNUMALB', 'ACSCLINOM', 'ACSTIPMOV', 'ACSSIGCAN', 'ACSUBITXT', 'ACSCENCOD', 'ACSNOMOS', 'ACSPOS', 'ACSEMPCOD', 'ACSNUEPRO']),
        Index('IDACS3', 'ACSFEC', 'ACSHOR', 'ACSSER', 'ACSEJE', 'ACSNUM', 'ACSMOV', 'ACSACLCOD', 'ACSCOD', mssql_clustered=False),
        Index('IDACS4', 'ACSFEC', mssql_clustered=False),
        Index('IDACS5', 'ACSMOV', 'ACSARTCOD', 'ACSLOT', mssql_clustered=False),
        Index('IDACS6', 'ACSMOV', 'ACSARTCOD', 'ACSCAN', mssql_clustered=False),
        Index('IDACS7', 'ACSCAN', 'ACSARTCOD', mssql_clustered=False),
        Index('IDACS8', 'ACSALMCOD', 'ACSSER', 'ACSEJE', 'ACSNUM', 'ACSMOV', mssql_clustered=False),
        Index('IDACS9', 'ACSMOV', 'ACSSER', 'ACSEJE', 'ACSNUM', 'ACSNUMCAJ', mssql_clustered=False),
        Index('IDALBARANCS231', 'ACSARTCOD', 'ACSALMCOD', 'ACSFEC', 'ACSUBI', mssql_clustered=False, mssql_include=['ACSSER', 'ACSEJE', 'ACSNUM', 'ACSMOV', 'ACSACLCOD', 'ACSCOD', 'ACSCLICOD', 'ACSPAL', 'ACSCAJ', 'ACSUNI', 'ACSCAN', 'ACSLOT', 'ACSNUMPAL', 'ACSNUMCAJ', 'ACSREPCOD', 'ACSENV', 'ACSREGFEC', 'ACSREGSER', 'ACSREGEJE', 'ACSREGNUM', 'ACSALBOBS', 'ACSCANREA', 'ACSHOR', 'ACSMAN', 'ACS2LOT', 'ACSNUMALB', 'ACSCLINOM', 'ACSTIPMOV', 'ACSSIGCAN', 'ACSUBITXT', 'ACSCENCOD', 'ACSNOMOS', 'ACSPOS', 'ACSEMPCOD']),
        Index('IDALBARANCS232', 'ACSALMCOD', 'ACSFEC', mssql_clustered=False, mssql_include=['ACSARTCOD', 'ACSLOT', 'ACSUBI', 'ACSCANREA']),
        {'schema': 'dbo'}
    )

    ACSSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSMOV: Mapped[str] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSACLCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ACSCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(9, 'Modern_Spanish_CI_AS'))
    ACSARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSPAL: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSCAJ: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSUNI: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSCAN: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSLOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSUBI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    ACSNUMPAL: Mapped[Optional[int]] = mapped_column(Integer)
    ACSNUMCAJ: Mapped[Optional[int]] = mapped_column(Integer)
    ACSREPCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSENV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACSREGFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    ACSREGSER: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSREGEJE: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSREGNUM: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACSALBOBS: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSCANREA: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACSHOR: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    ACSMAN: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACS2LOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSALMCOD: Mapped[Optional[str]] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSNUMALB: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSCLINOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    ACSTIPMOV: Mapped[Optional[str]] = mapped_column(CHAR(16, 'Modern_Spanish_CI_AS'))
    ACSSIGCAN: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSUBITXT: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    ACSCENCOD: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))
    ACSNOMOS: Mapped[Optional[int]] = mapped_column(Integer)
    ACSPOS: Mapped[Optional[int]] = mapped_column(Integer)
    ACSEMPCOD: Mapped[Optional[str]] = mapped_column(CHAR(12, 'Modern_Spanish_CI_AS'), server_default=text("('LIN')"))
    ACSNUEPRO: Mapped[Optional[int]] = mapped_column(Integer)
    ACSNUMPIC: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSCANREC: Mapped[Optional[float]] = mapped_column(Float(53))


t_ALBARANCS050220242 = Table(
    'ALBARANCS050220242', Base.metadata,
    Column('ACSSER', CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSEJE', CHAR(4, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSNUM', Float(53), nullable=False),
    Column('ACSMOV', CHAR(2, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSACLCOD', Float(53), nullable=False),
    Column('ACSCOD', Float(53), nullable=False),
    Column('ACSFEC', DateTime),
    Column('ACSCLICOD', CHAR(9, 'Modern_Spanish_CI_AS')),
    Column('ACSARTCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSPAL', Float(53)),
    Column('ACSCAJ', Float(53)),
    Column('ACSUNI', Float(53)),
    Column('ACSCAN', Float(53)),
    Column('ACSLOT', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSUBI', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACSNUMPAL', Integer),
    Column('ACSNUMCAJ', Integer),
    Column('ACSREPCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSENV', Integer),
    Column('ACSREGFEC', DateTime),
    Column('ACSREGSER', CHAR(5, 'Modern_Spanish_CI_AS')),
    Column('ACSREGEJE', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('ACSREGNUM', Float(53)),
    Column('ACSALBOBS', CHAR(255, 'Modern_Spanish_CI_AS')),
    Column('ACSCANREA', Float(53)),
    Column('ACSHOR', DateTime),
    Column('ACSMAN', Integer),
    Column('ACS2LOT', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSALMCOD', CHAR(2, 'Modern_Spanish_CI_AS')),
    Column('ACSNUMALB', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSCLINOM', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('ACSTIPMOV', CHAR(16, 'Modern_Spanish_CI_AS')),
    Column('ACSSIGCAN', Float(53)),
    Column('ACSUBITXT', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACSCENCOD', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('ACSNOMOS', Integer),
    Column('ACSPOS', Integer),
    Column('ACSEMPCOD', CHAR(12, 'Modern_Spanish_CI_AS')),
    Column('ACSNUEPRO', Integer),
    schema='dbo'
)


t_ALBARANCS_110324 = Table(
    'ALBARANCS_110324', Base.metadata,
    Column('ACSSER', CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSEJE', CHAR(4, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSNUM', Float(53), nullable=False),
    Column('ACSMOV', CHAR(2, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSACLCOD', Float(53), nullable=False),
    Column('ACSCOD', Float(53), nullable=False),
    Column('ACSFEC', DateTime),
    Column('ACSCLICOD', CHAR(9, 'Modern_Spanish_CI_AS')),
    Column('ACSARTCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSPAL', Float(53)),
    Column('ACSCAJ', Float(53)),
    Column('ACSUNI', Float(53)),
    Column('ACSCAN', Float(53)),
    Column('ACSLOT', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSUBI', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACSNUMPAL', Integer),
    Column('ACSNUMCAJ', Integer),
    Column('ACSREPCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSENV', Integer),
    Column('ACSREGFEC', DateTime),
    Column('ACSREGSER', CHAR(5, 'Modern_Spanish_CI_AS')),
    Column('ACSREGEJE', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('ACSREGNUM', Float(53)),
    Column('ACSALBOBS', CHAR(255, 'Modern_Spanish_CI_AS')),
    Column('ACSCANREA', Float(53)),
    Column('ACSHOR', DateTime),
    Column('ACSMAN', Integer),
    Column('ACS2LOT', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSALMCOD', CHAR(2, 'Modern_Spanish_CI_AS')),
    Column('ACSNUMALB', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSCLINOM', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('ACSTIPMOV', CHAR(16, 'Modern_Spanish_CI_AS')),
    Column('ACSSIGCAN', Float(53)),
    Column('ACSUBITXT', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACSCENCOD', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('ACSNOMOS', Integer),
    Column('ACSPOS', Integer),
    Column('ACSEMPCOD', CHAR(12, 'Modern_Spanish_CI_AS')),
    Column('ACSNUEPRO', Integer),
    schema='dbo'
)


t_ALBARANCS_110324_PICKING = Table(
    'ALBARANCS_110324_PICKING', Base.metadata,
    Column('ACSSER', CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSEJE', CHAR(4, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSNUM', Float(53), nullable=False),
    Column('ACSMOV', CHAR(2, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSACLCOD', Float(53), nullable=False),
    Column('ACSCOD', Float(53), nullable=False),
    Column('ACSFEC', DateTime),
    Column('ACSCLICOD', CHAR(9, 'Modern_Spanish_CI_AS')),
    Column('ACSARTCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSPAL', Float(53)),
    Column('ACSCAJ', Float(53)),
    Column('ACSUNI', Float(53)),
    Column('ACSCAN', Float(53)),
    Column('ACSLOT', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSUBI', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACSNUMPAL', Integer),
    Column('ACSNUMCAJ', Integer),
    Column('ACSREPCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSENV', Integer),
    Column('ACSREGFEC', DateTime),
    Column('ACSREGSER', CHAR(5, 'Modern_Spanish_CI_AS')),
    Column('ACSREGEJE', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('ACSREGNUM', Float(53)),
    Column('ACSALBOBS', CHAR(255, 'Modern_Spanish_CI_AS')),
    Column('ACSCANREA', Float(53)),
    Column('ACSHOR', DateTime),
    Column('ACSMAN', Integer),
    Column('ACS2LOT', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSALMCOD', CHAR(2, 'Modern_Spanish_CI_AS')),
    Column('ACSNUMALB', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSCLINOM', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('ACSTIPMOV', CHAR(16, 'Modern_Spanish_CI_AS')),
    Column('ACSSIGCAN', Float(53)),
    Column('ACSUBITXT', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACSCENCOD', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('ACSNOMOS', Integer),
    Column('ACSPOS', Integer),
    Column('ACSEMPCOD', CHAR(12, 'Modern_Spanish_CI_AS')),
    Column('ACSNUEPRO', Integer),
    Column('ACCTIP', CHAR(1, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACCSER', CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACCEJE', CHAR(4, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACCNUM', Float(53), nullable=False),
    Column('ACCCLICOD', CHAR(15, 'Modern_Spanish_CI_AS')),
    Column('ACCCENCOD', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('ACCSIT', CHAR(1, 'Modern_Spanish_CI_AS')),
    Column('ACCCON', Float(53)),
    Column('ACCPEDDIA', Float(53)),
    Column('ACCSAL', Integer),
    Column('REGENV', Integer),
    Column('ACCFEC', DateTime),
    Column('ACCALBOBS', CHAR(200, 'Modern_Spanish_CI_AS')),
    Column('ACCLOASER', CHAR(5, 'Modern_Spanish_CI_AS')),
    Column('ACCLOACOD', Float(53)),
    Column('ACCFORALB', Integer),
    Column('ACCREPCOD', CHAR(15, 'Modern_Spanish_CI_AS')),
    Column('ACCPESTOT', Float(53)),
    Column('ACCCOMREC', Integer),
    Column('ACCENVAS', Integer),
    Column('ACCTIPINV', Integer),
    Column('ACCFECCIE', DateTime),
    Column('ACCNUMBUL', Float(53)),
    Column('ACCALMCOD', CHAR(2, 'Modern_Spanish_CI_AS')),
    Column('ACCREPCOD2', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACCREPCOD3', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACCGRUCOD', Integer),
    Column('ACCNUMLIN2', Integer),
    Column('ACCPROALB', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('ACCNUMEXP', Integer),
    Column('ACCNUMEXP2', CHAR(7, 'Modern_Spanish_CI_AS')),
    Column('ACCFECENT', DateTime),
    Column('ACCNUMFAS', CHAR(7, 'Modern_Spanish_CI_AS')),
    Column('ACCALMDESCOD', CHAR(12, 'Modern_Spanish_CI_AS')),
    Column('ACCFICREC', Float(53)),
    Column('ACCNUMFAC', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACCESAGE', Integer),
    Column('ACCREPCOD4', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACCREPCOD5', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACCGRUPED', Float(53)),
    Column('ACCPALNUMSER', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('ACCNUEPIC', Integer),
    Column('ACCRECCLI', Integer),
    schema='dbo'
)


t_ALBARANCS_120324 = Table(
    'ALBARANCS_120324', Base.metadata,
    Column('ACSSER', CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSEJE', CHAR(4, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSNUM', Float(53), nullable=False),
    Column('ACSMOV', CHAR(2, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACSACLCOD', Float(53), nullable=False),
    Column('ACSCOD', Float(53), nullable=False),
    Column('ACSFEC', DateTime),
    Column('ACSCLICOD', CHAR(9, 'Modern_Spanish_CI_AS')),
    Column('ACSARTCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSPAL', Float(53)),
    Column('ACSCAJ', Float(53)),
    Column('ACSUNI', Float(53)),
    Column('ACSCAN', Float(53)),
    Column('ACSLOT', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSUBI', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACSNUMPAL', Integer),
    Column('ACSNUMCAJ', Integer),
    Column('ACSREPCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSENV', Integer),
    Column('ACSREGFEC', DateTime),
    Column('ACSREGSER', CHAR(5, 'Modern_Spanish_CI_AS')),
    Column('ACSREGEJE', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('ACSREGNUM', Float(53)),
    Column('ACSALBOBS', CHAR(255, 'Modern_Spanish_CI_AS')),
    Column('ACSCANREA', Float(53)),
    Column('ACSHOR', DateTime),
    Column('ACSMAN', Integer),
    Column('ACS2LOT', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSALMCOD', CHAR(2, 'Modern_Spanish_CI_AS')),
    Column('ACSNUMALB', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACSCLINOM', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('ACSTIPMOV', CHAR(16, 'Modern_Spanish_CI_AS')),
    Column('ACSSIGCAN', Float(53)),
    Column('ACSUBITXT', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('ACSCENCOD', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('ACSNOMOS', Integer),
    Column('ACSPOS', Integer),
    Column('ACSEMPCOD', CHAR(12, 'Modern_Spanish_CI_AS')),
    Column('ACSNUEPRO', Integer),
    schema='dbo'
)


class ALBARANPALET(Base):
    __tablename__ = 'ALBARANPALET'
    __table_args__ = (
        PrimaryKeyConstraint('PALSER', 'PALEJE', 'PALNUM', 'PALMOV', 'PALCOD', name='IDPAL1'),
        {'schema': 'dbo'}
    )

    PALSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    PALEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    PALNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    PALMOV: Mapped[str] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), primary_key=True)
    PALCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    PALPES: Mapped[Optional[float]] = mapped_column(Float(53))
    PALOBS: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'))
    UBITIP: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'))
    UBISER: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'))
    UBIEJE: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))
    UBINUM: Mapped[Optional[float]] = mapped_column(Float(53))
    UBICOD: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    UBIARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    UBILOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    UBICAN: Mapped[Optional[float]] = mapped_column(Float(53))
    PALNUMSER: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    PALLAR: Mapped[Optional[float]] = mapped_column(Float(53))
    PALANC: Mapped[Optional[float]] = mapped_column(Float(53))
    PALALT: Mapped[Optional[float]] = mapped_column(Float(53))


class ALBARANUSU(Base):
    __tablename__ = 'ALBARANUSU'
    __table_args__ = (
        PrimaryKeyConstraint('USUSER', 'USUEJE', 'USUNUM', 'USUTIP', 'USUCOD', name='IDALBUSU1'),
        {'schema': 'dbo'}
    )

    USUSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    USUEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    USUNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    USUTIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    USUCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    USUFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    USUHOR: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))


class ALMACENES(Base):
    __tablename__ = 'ALMACENES'
    __table_args__ = (
        PrimaryKeyConstraint('ALMCOD', name='IDALM1'),
        {'schema': 'dbo'}
    )

    ALMCOD: Mapped[str] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), primary_key=True)
    ALMNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    REGMOD: Mapped[Optional[int]] = mapped_column(Integer)


class ARTICULO(Base):
    __tablename__ = 'ARTICULO'
    __table_args__ = (
        PrimaryKeyConstraint('ARTCOD', name='IDARTICULO1'),
        Index('IDARTICULO2', 'ARTCOD2', mssql_clustered=False),
        Index('IDARTICULO3', 'ARTBARCOD', mssql_clustered=False),
        Index('IDARTICULO4', 'ARTCAJBARCOD', mssql_clustered=False),
        Index('IDARTICULO5', 'ARTPALBARCOD', mssql_clustered=False),
        Index('IDARTICULO6', 'ARTLARCOD', mssql_clustered=False),
        Index('IDARTICULO7', 'ARTNOM', mssql_clustered=False),
        {'schema': 'dbo'}
    )

    ARTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    ARTNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTPESUNI: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTEST1: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTEST2: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTEST3: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTCOD2: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTBARCOD: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTCAJBARCOD: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTCAJRELDIR: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTINV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ARTPALBARCOD: Mapped[Optional[str]] = mapped_column(CHAR(14, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTPALRELDIR: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTFECINV: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    ARTLOTMER: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ARTGRUCOD: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTSTO400: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTMOS: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ARTIMA: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTMEDCOD: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTMAT: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTCOL: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTCOS: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTDES1: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTPEDFEC: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), server_default=text("('N')"))
    ARTSTOMIN: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTSTOMAX: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTPORENT: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTPARARA: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    ARTLARCOD: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    ARTPESUN2: Mapped[Optional[float]] = mapped_column(Float(53))
    ARTVOL: Mapped[Optional[float]] = mapped_column(Float(53))
    ARTNOLOTUNI: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((1))'))
    ARTCHI: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ARTPIE: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ARTUBIPIC: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTULTUBI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTSUBCAJ: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTCOSUNI: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTASIN: Mapped[Optional[str]] = mapped_column(CHAR(11, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class ARTICULOAUX(Base):
    __tablename__ = 'ARTICULOAUX'
    __table_args__ = (
        PrimaryKeyConstraint('ARTCON', name='IDARTIULOAUX1'),
        {'schema': 'dbo'}
    )

    ARTCON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTCOD2: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    REGENV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    REGMOD: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


class ARTICULOEXCLOTCLI(Base):
    __tablename__ = 'ARTICULOEXCLOTCLI'
    __table_args__ = (
        PrimaryKeyConstraint('HISCON', name='IDARTEXCLOTCLI1'),
        {'schema': 'dbo'}
    )

    HISCON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    HISCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HISARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HISLOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class ARTICULOIDI(Base):
    __tablename__ = 'ARTICULOIDI'
    __table_args__ = (
        PrimaryKeyConstraint('IDIARTCOD', 'IDICOD', name='IDARTICULOIDI1'),
        {'schema': 'dbo'}
    )

    IDIARTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    IDICOD: Mapped[str] = mapped_column(CHAR(3, 'Modern_Spanish_CI_AS'), primary_key=True)
    IDIARTNOM: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class ARTICULOLOTCLI(Base):
    __tablename__ = 'ARTICULOLOTCLI'
    __table_args__ = (
        PrimaryKeyConstraint('HISCON', name='IDARTICULOLOTCLI1'),
        {'schema': 'dbo'}
    )

    HISCON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    HISCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HISARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HISLOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HISTIP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    HISDIA: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    HISOBS: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class ARTICULOLOTOBS(Base):
    __tablename__ = 'ARTICULOLOTOBS'
    __table_args__ = (
        PrimaryKeyConstraint('HISCON', name='IDARTICULOLOTOBS1'),
        {'schema': 'dbo'}
    )

    HISCON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    HISARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HISLOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HISOBS: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class ARTICULOSINREP(Base):
    __tablename__ = 'ARTICULOSINREP'
    __table_args__ = (
        PrimaryKeyConstraint('HISCON', name='IDARTICULOSINREP1'),
        {'schema': 'dbo'}
    )

    HISCON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    HISARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class ARTICULOSTOMIN(Base):
    __tablename__ = 'ARTICULOSTOMIN'
    __table_args__ = (
        PrimaryKeyConstraint('MINARTCOD', name='IDARTICULOSTOMIN1'),
        {'schema': 'dbo'}
    )

    MINARTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    MINSTOMIN: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    MINSTOMAX: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))


class ARTICULOUBI(Base):
    __tablename__ = 'ARTICULOUBI'
    __table_args__ = (
        PrimaryKeyConstraint('ARTUBICON', name='IDARTICULOUBI1'),
        {'schema': 'dbo'}
    )

    ARTUBICON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ARTUBIARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTUBICODUBI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    REGENV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    REGMOD: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ARTUBIMIN: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTUBIALMCOD: Mapped[Optional[str]] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ARTUBIMAX: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ARTUBIEXC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


class BARRA(Base):
    __tablename__ = 'BARRA'
    __table_args__ = (
        PrimaryKeyConstraint('BARCOD', name='IDBARRA1'),
        {'schema': 'dbo'}
    )

    BARCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    BARARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    BARCAJCOD: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    BARPALCOD: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    BARCANCAJ: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    BARCANPAL: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))


class CABECERA(Base):
    __tablename__ = 'CABECERA'
    __table_args__ = (
        PrimaryKeyConstraint('ACCEMPCOD', 'ACCPRCCOD', 'ACCSER', 'ACCEJE', 'ACCNUM', name='IDCAB1'),
        {'schema': 'dbo'}
    )

    ACCEMPCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACCPRCCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACCSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACCEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACCNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACCALBOBS: Mapped[Optional[str]] = mapped_column(CHAR(200, 'Modern_Spanish_CI_AS'))
    accFec: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    AccCliCod: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    AccCenCod: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))
    AccCliNom: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    AccCliRaz: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    AccCliDir: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    accCliPob: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    accCliPro: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    ACCCLITEL: Mapped[Optional[str]] = mapped_column(CHAR(40, 'Modern_Spanish_CI_AS'))
    ACCPESTOT: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    accempraz: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    accempdir: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    accEmpPob: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    accempnif: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    accemptel: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    ACCEMPWEB: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    accempcor: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    ACCPEDGEN: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'))
    ACCPIC: Mapped[Optional[str]] = mapped_column(CHAR(1000, 'Modern_Spanish_CI_AS'))
    ACCPALPESV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACCALMDESCOD: Mapped[Optional[str]] = mapped_column(CHAR(12, 'Modern_Spanish_CI_AS'))


class CANTIDADSERVIDA(Base):
    __tablename__ = 'CANTIDADSERVIDA'
    __table_args__ = (
        PrimaryKeyConstraint('STOARTCOD', 'STOFEC', name='IDCANSER1'),
        {'schema': 'dbo'}
    )

    STOARTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    STOFEC: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    STOCAN: Mapped[Optional[float]] = mapped_column(Float(53))


class CLIENTE(Base):
    __tablename__ = 'CLIENTE'
    __table_args__ = (
        PrimaryKeyConstraint('CLICOD', 'CLICENCOD', name='IDCLIENTE1'),
        {'schema': 'dbo'}
    )

    CLICOD: Mapped[str] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), primary_key=True)
    CLICENCOD: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    CLIRAZ: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLINOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIDIR: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIPOSCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIPOSCIU: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIPOSPRO: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLINIF: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIRUTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLITEL: Mapped[Optional[str]] = mapped_column(CHAR(40, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIPAICOD: Mapped[Optional[str]] = mapped_column(CHAR(3, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIPERCON: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIEMA: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLICAR: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIIDICOD: Mapped[Optional[str]] = mapped_column(CHAR(3, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class CLIENTEENVIO(Base):
    __tablename__ = 'CLIENTEENVIO'
    __table_args__ = (
        PrimaryKeyConstraint('CLICOD', 'CLICENCOD', name='IDCLIENTEENVIO1'),
        {'schema': 'dbo'}
    )

    CLICOD: Mapped[str] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), primary_key=True)
    CLICENCOD: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    CLIPOSCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    CLIPOSCIU: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'))
    CLIPOSPRO: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'))
    CLITEL: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    CLIVIANOM: Mapped[Optional[str]] = mapped_column(CHAR(45, 'Modern_Spanish_CI_AS'))
    CLIALBOBS: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))


class CONTADOR(Base):
    __tablename__ = 'CONTADOR'
    __table_args__ = (
        PrimaryKeyConstraint('CONCOD', 'CONSER', 'CONEJE', name='IDCON1'),
        Index('IDCON2', 'CONNOM', mssql_clustered=False),
        {'schema': 'dbo'}
    )

    CONCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    CONSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    CONEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    CONNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    CONNUM: Mapped[Optional[float]] = mapped_column(Float(53))
    REGMOD: Mapped[Optional[int]] = mapped_column(Integer)
    REGENV: Mapped[Optional[int]] = mapped_column(Integer)


class DOCUMENTO(Base):
    __tablename__ = 'DOCUMENTO'
    __table_args__ = (
        PrimaryKeyConstraint('DOCPRO', 'DOCCON', name='IDDOC1'),
        {'schema': 'dbo'}
    )

    DOCPRO: Mapped[float] = mapped_column(Float(53), primary_key=True)
    DOCCON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    DOCSER: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'))
    DOCEJE: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))
    DOCNUM: Mapped[Optional[float]] = mapped_column(Float(53))
    DOCTIP: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'))
    DOCFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DOCCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    DOCCENCOD: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))


class EJECUTABLEIDI(Base):
    __tablename__ = 'EJECUTABLEIDI'
    __table_args__ = (
        PrimaryKeyConstraint('EJECOD', name='IDEJECUTABLEIDI'),
        {'schema': 'dbo'}
    )

    EJECOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    EJENOMAPL: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EJEEMPCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EJENOMFOR: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EJENOMOBJ: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EJEIDICOD: Mapped[Optional[str]] = mapped_column(CHAR(3, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EJETRA: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EJEELE: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EJETIP: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EJENUMCOL: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("('')"))
    EJEVALCOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EJEIND: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


class ETIQUETAZ(Base):
    __tablename__ = 'ETIQUETAZ'
    __table_args__ = (
        PrimaryKeyConstraint('ETIPRO', 'ETICON', name='IDETIZ1'),
        {'schema': 'dbo'}
    )

    ETIPRO: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ETICON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ETITEX1: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX2: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX3: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX4: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX5: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX6: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX7: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX8: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX9: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX10: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX11: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX12: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX13: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX14: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX15: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX16: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX17: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX18: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX19: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX20: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX21: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX22: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX23: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX24: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX25: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX26: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX27: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX28: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX29: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX30: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX31: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX32: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX33: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX34: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX35: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX36: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX37: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX38: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX39: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ETITEX40: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class FAMILIANOLOTE(Base):
    __tablename__ = 'FAMILIANOLOTE'
    __table_args__ = (
        PrimaryKeyConstraint('FAMCON', name='IDFAMILIANOLOTE1'),
        {'schema': 'dbo'}
    )

    FAMCON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    FAMCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))


class GENERICOC(Base):
    __tablename__ = 'GENERICOC'
    __table_args__ = (
        PrimaryKeyConstraint('GECPROCOD', name='IDGENERICOC1'),
        {'schema': 'dbo'}
    )

    GECPROCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    GECEMP: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GECTIT: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GECPET: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    IVCFAMNOM: Mapped[Optional[str]] = mapped_column(CHAR(500, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class GENERICOL(Base):
    __tablename__ = 'GENERICOL'
    __table_args__ = (
        PrimaryKeyConstraint('GELPROCOD', 'GELNUM', name='IDGENERICOL1'),
        {'schema': 'dbo'}
    )

    GELPROCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    GELNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    GELCODIRE: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELCOD: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELNOM: Mapped[Optional[str]] = mapped_column(CHAR(500, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HILCAB1T: Mapped[Optional[str]] = mapped_column(CHAR(75, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HILCAB2T: Mapped[Optional[str]] = mapped_column(CHAR(75, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HILCAB3T: Mapped[Optional[str]] = mapped_column(CHAR(75, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HILCAB4T: Mapped[Optional[str]] = mapped_column(CHAR(75, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELFES: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    GELFUN: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    GELCOR: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    GELLIN: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    GELPULMAN: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    GELTAP: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    GELPEDCER: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELPEDCERV: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    GELPEDPEN: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELPEDPENV: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    GELPASREA: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELPASREAV: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    GELPASPEN: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELPASPENV: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    GELMES: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    HILCAB5T: Mapped[Optional[str]] = mapped_column(CHAR(75, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELCENCOD: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELTERCOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    GELPALV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    GELPAL: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class INFOESTADISTICA(Base):
    __tablename__ = 'INFOESTADISTICA'
    __table_args__ = (
        PrimaryKeyConstraint('ACSSER', 'ACSEJE', 'ACSNUM', 'ACSMOV', 'ACSACLCOD', 'ACSCOD', name='IDINFOESTADISTICA'),
        {'schema': 'dbo'}
    )

    ACSSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSMOV: Mapped[str] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSACLCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ACSPAL: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSCAJ: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSUNI: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSCAN: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSREPCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSHOR: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


t_INFORMEPEDIDOS = Table(
    'INFORMEPEDIDOS', Base.metadata,
    Column('ACCSER', CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACCEJE', CHAR(4, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACCNUM', Float(53), nullable=False),
    Column('ACCCLICOD', CHAR(15, 'Modern_Spanish_CI_AS')),
    Column('ACCCENCOD', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('CLIRUTCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('CLIRAZ', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('CLINOM', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('ACCFEC', DateTime),
    Column('ACCFECCIE', DateTime),
    Column('ACCREPCOD', CHAR(15, 'Modern_Spanish_CI_AS')),
    Column('UNIDADESSERVIDAS', Integer),
    Column('CAJASFISICAS', Integer),
    schema='dbo'
)


class INVENTARIOC3(Base):
    __tablename__ = 'INVENTARIOC3'
    __table_args__ = (
        PrimaryKeyConstraint('UBI3USU', 'UBI3TIP', 'UBI3SER', 'UBI3EJE', 'UBI3NUM', name='IDINVC3'),
        {'schema': 'dbo'}
    )

    UBI3USU: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI3TIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI3SER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI3EJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI3NUM: Mapped[float] = mapped_column(Float(53), primary_key=True)


class INVENTARIOC32(Base):
    __tablename__ = 'INVENTARIOC32'
    __table_args__ = (
        PrimaryKeyConstraint('UBI3USU', 'UBI3TIP', 'UBI3SER', 'UBI3EJE', 'UBI3NUM', 'UBI3CON', name='IDINVC32'),
        {'schema': 'dbo'}
    )

    UBI3USU: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI3TIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI3SER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI3EJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI3NUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    UBI3CON: Mapped[int] = mapped_column(Integer, primary_key=True)


class INVENTARIOC4(Base):
    __tablename__ = 'INVENTARIOC4'
    __table_args__ = (
        PrimaryKeyConstraint('UBI4USU', 'UBI4TIP', 'UBI4SER', 'UBI4EJE', 'UBI4NUM', 'UBI4ARTCOD', name='IDINVC4'),
        {'schema': 'dbo'}
    )

    UBI4USU: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI4TIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI4SER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI4EJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI4NUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    UBI4ARTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)


class INVENTARIOC42(Base):
    __tablename__ = 'INVENTARIOC42'
    __table_args__ = (
        PrimaryKeyConstraint('UBI4USU', 'UBI4TIP', 'UBI4SER', 'UBI4EJE', 'UBI4NUM', 'UBI4ARTCOD', 'UBI4CON', name='IDINVC42'),
        {'schema': 'dbo'}
    )

    UBI4USU: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI4TIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI4SER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI4EJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI4NUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    UBI4ARTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI4CON: Mapped[int] = mapped_column(Integer, primary_key=True)


class INVENTARIOCS(Base):
    __tablename__ = 'INVENTARIOCS'
    __table_args__ = (
        PrimaryKeyConstraint('ACSSER', 'ACSEJE', 'ACSNUM', 'ACSMOV', 'ACSACLCOD', 'ACSCOD', name='IDICS1'),
        {'schema': 'dbo'}
    )

    ACSSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSMOV: Mapped[str] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSACLCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ACSCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(9, 'Modern_Spanish_CI_AS'))
    ACSARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSPAL: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSCAJ: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSUNI: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSCAN: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSLOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSUBI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    ACSNUMPAL: Mapped[Optional[int]] = mapped_column(Integer)
    ACSNUMCAJ: Mapped[Optional[int]] = mapped_column(Integer)
    ACSREPCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSMAN: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACSHOR: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    ACS2LOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSUSUINV: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSRECPAR: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


class InventarioContador(Base):
    __tablename__ = 'InventarioContador'
    __table_args__ = (
        PrimaryKeyConstraint('INV5SER', 'INV5EJE', 'INV5NUM', 'INV5ARTCOD', 'Contador', name='PK__Inventar__B6F1BA26AB3F59F5'),
        {'schema': 'dbo'}
    )

    INV5SER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    INV5EJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    INV5NUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    INV5ARTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    Contador: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)


class KIMPRESION(Base):
    __tablename__ = 'KIMPRESION'
    __table_args__ = (
        PrimaryKeyConstraint('IMPSER', 'IMPEJE', 'IMPNUM', 'IMPMOV', 'IMPTIP', name='IDKIMP1'),
        {'schema': 'dbo'}
    )

    IMPSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    IMPEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    IMPNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    IMPMOV: Mapped[str] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), primary_key=True)
    IMPTIP: Mapped[str] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), primary_key=True)
    IMPTER: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    IMPIMPNOM: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'))
    IMPEMP: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    IMPFECHOR: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    IMPETI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    IMPTIPETI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    IMPNUMCAJ: Mapped[Optional[int]] = mapped_column(Integer)
    IMPCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    IMPCLICENCOD: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))
    IMPPROCESADO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


class KIMPRESION2(Base):
    __tablename__ = 'KIMPRESION2'
    __table_args__ = (
        PrimaryKeyConstraint('IMPID', name='PK_KIMPRESION2'),
        {'schema': 'dbo'}
    )

    IMPID: Mapped[float] = mapped_column(Float(53), primary_key=True)
    IMPSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False)
    IMPEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), nullable=False)
    IMPNUM: Mapped[float] = mapped_column(Float(53), nullable=False)
    IMPMOV: Mapped[str] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), nullable=False)
    IMPTIP: Mapped[str] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), nullable=False)
    IMPTER: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    IMPIMPNOM: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'))
    IMPEMP: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    IMPFECHOR: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    IMPETI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    IMPTIPETI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    IMPNUMCAJ: Mapped[Optional[int]] = mapped_column(Integer)
    IMPCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    IMPCLICENCOD: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))
    IMPPROCESADO: Mapped[Optional[int]] = mapped_column(Integer)
    IMPTIPOPROCESO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


class LINEA(Base):
    __tablename__ = 'LINEA'
    __table_args__ = (
        PrimaryKeyConstraint('ACLEMPCOD', 'ACLPRCCOD', 'ACLSER', 'ACLEJE', 'ACLNUM', 'ACLNUMLIN', name='IDLIN1'),
        {'schema': 'dbo'}
    )

    ACLEMPCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACLPRCCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACLSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACLEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACLNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACLNUMLIN: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACLTIPLIN: Mapped[Optional[int]] = mapped_column(Integer)
    ACLARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACLARTNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    AclBARCod: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Modern_Spanish_CI_AS'))
    aclartCod2: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Modern_Spanish_CI_AS'))
    ACLARTGRUCOD: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'))
    AclArtEST1: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    AclArtEST2: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    AclArtEST3: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACLPALV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLCAJV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLUNIV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLCANV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLCAN: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    ACLCANSERV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLPESLINV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLPESLIN: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    ACLCANVOLV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLCANVOL: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    ACLMOTCOD: Mapped[Optional[str]] = mapped_column(CHAR(3, 'Modern_Spanish_CI_AS'))
    ACLNUMPAL: Mapped[Optional[int]] = mapped_column(Integer)
    ACLNUMCAJ: Mapped[Optional[int]] = mapped_column(Integer)
    ACLLOT: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    ACLCANCAJV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLARTCANCAJV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLARTCANPALV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLCANCAJ: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACLSIGNO: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'))
    ACLARTCOD2LOT: Mapped[Optional[str]] = mapped_column(CHAR(51, 'Modern_Spanish_CI_AS'))
    ACLPALPESV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLPALOBS: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'))
    ACLPALNUMSER: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    ACLLAR: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACLANC: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACLALT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACLPARARA: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    ACLPESLIN2V: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLLARV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLANCV: Mapped[Optional[float]] = mapped_column(Float(53))
    ACLALTV: Mapped[Optional[float]] = mapped_column(Float(53))


class LOG(Base):
    __tablename__ = 'LOG'
    __table_args__ = (
        PrimaryKeyConstraint('LOGCOD', name='IDLOG1'),
        {'schema': 'dbo'}
    )

    LOGCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    LOGACC: Mapped[Optional[str]] = mapped_column(CHAR(40, 'Modern_Spanish_CI_AS'))
    LOGNOM: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'))
    LOGIMP1: Mapped[Optional[float]] = mapped_column(Float(53))
    LOGIMP2: Mapped[Optional[float]] = mapped_column(Float(53))
    LOGUSU: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    LOGTER: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    LOGFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LOGFECREA: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LOGHORREA: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LOGCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    LOGCENCOD: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))
    LOGARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Modern_Spanish_CI_AS'))
    LOGLOT: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    LOGUBI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))


class LOG2(Base):
    __tablename__ = 'LOG2'
    __table_args__ = (
        PrimaryKeyConstraint('LOGCOD', name='IDLOG2'),
        {'schema': 'dbo'}
    )

    LOGCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    LOGEMP: Mapped[str] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), nullable=False)
    LOGTER: Mapped[str] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), nullable=False)
    LOGFECREA: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    LOGHORREA: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    LOGTEX: Mapped[Optional[str]] = mapped_column(TEXT(16, 'Modern_Spanish_CI_AS'))


class PEDIDOCC(Base):
    __tablename__ = 'PEDIDOCC'
    __table_args__ = (
        PrimaryKeyConstraint('ACCTIP', 'ACCSER', 'ACCEJE', 'ACCNUM', name='IDXCC1'),
        Index('IDACCGRUPED1', 'ACCGRUPED', mssql_clustered=False),
        Index('IDPCC2', 'ACCLOASER', 'ACCLOACOD', 'ACCTIPINV', mssql_clustered=False),
        Index('IDPCCPALNUMSER1', 'ACCPALNUMSER', mssql_clustered=False),
        Index('IDPEDIDOCC02', 'ACCTIP', 'ACCTIPINV', 'ACCSIT', 'ACCFEC', mssql_clustered=False),
        Index('IDWXC2', 'ACCCLICOD', 'ACCCENCOD', mssql_clustered=False),
        {'schema': 'dbo'}
    )

    ACCTIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACCSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACCEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACCNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACCCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACCCENCOD: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACCSIT: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACCCON: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACCPEDDIA: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACCSAL: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    REGENV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACCFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    ACCALBOBS: Mapped[Optional[str]] = mapped_column(CHAR(200, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACCLOASER: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACCLOACOD: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACCFORALB: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACCREPCOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACCPESTOT: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACCCOMREC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACCENVAS: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACCTIPINV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACCFECCIE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    ACCNUMBUL: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACCALMCOD: Mapped[Optional[str]] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACCREPCOD2: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACCREPCOD3: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACCGRUCOD: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACCNUMLIN2: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((-1))'))
    ACCPROALB: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    ACCNUMEXP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACCNUMEXP2: Mapped[Optional[str]] = mapped_column(CHAR(7, 'Modern_Spanish_CI_AS'))
    ACCFECENT: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    ACCNUMFAS: Mapped[Optional[str]] = mapped_column(CHAR(7, 'Modern_Spanish_CI_AS'))
    ACCALMDESCOD: Mapped[Optional[str]] = mapped_column(CHAR(12, 'Modern_Spanish_CI_AS'))
    ACCFICREC: Mapped[Optional[float]] = mapped_column(Float(53))
    ACCNUMFAC: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACCESAGE: Mapped[Optional[int]] = mapped_column(Integer)
    ACCREPCOD4: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACCREPCOD5: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACCGRUPED: Mapped[Optional[float]] = mapped_column(Float(53))
    ACCPALNUMSER: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    ACCNUEPIC: Mapped[Optional[int]] = mapped_column(Integer)
    ACCRECCLI: Mapped[Optional[int]] = mapped_column(Integer)
    ACCESAGE1: Mapped[Optional[int]] = mapped_column(Integer)
    ACCRUTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACCENPROCESO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACCPICCOMPRA: Mapped[Optional[int]] = mapped_column(Integer)
    ACCRPRCOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    ACCFECEXP: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ACCPRFNUM: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACCRECART: Mapped[Optional[int]] = mapped_column(Integer)
    ACCMANIFIESTO: Mapped[Optional[float]] = mapped_column(Float(53))
    ACCSUPED: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))


class PEDIDOCCENVIO(Base):
    __tablename__ = 'PEDIDOCCENVIO'
    __table_args__ = (
        PrimaryKeyConstraint('ACCTIP', 'ACCSER', 'ACCEJE', 'ACCNUM', name='IDPEDIDOCCENVIO1'),
        {'schema': 'dbo'}
    )

    ACCTIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACCSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACCEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACCNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACCALBOBS: Mapped[Optional[str]] = mapped_column(CHAR(200, 'Modern_Spanish_CI_AS'))
    ACCPOSCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACCPOSCIU: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'))
    ACCPOSPRO: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'))
    ACCTEL: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    ACCIMPREEMBOLSO: Mapped[Optional[float]] = mapped_column(Float(53))
    ACCVIANOM: Mapped[Optional[str]] = mapped_column(CHAR(45, 'Modern_Spanish_CI_AS'))
    ACCRETORNO: Mapped[Optional[int]] = mapped_column(Integer)


class PEDIDOCCUSU(Base):
    __tablename__ = 'PEDIDOCCUSU'
    __table_args__ = (
        PrimaryKeyConstraint('USUSER', 'USUEJE', 'USUNUM', 'USUTIP', 'USUCOD', name='IDPEDIDOCCUSU1'),
        {'schema': 'dbo'}
    )

    USUSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    USUEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    USUNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    USUTIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    USUCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    USUFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    USUHOR: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    USUUBI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


t_PEDIDOSSINASIGNAR = Table(
    'PEDIDOSSINASIGNAR', Base.metadata,
    Column('CANTIDAD', Float(53)),
    schema='dbo'
)


class PICKING(Base):
    __tablename__ = 'PICKING'
    __table_args__ = (
        PrimaryKeyConstraint('PICCOD', name='IDPIC1'),
        {'schema': 'dbo'}
    )

    PICCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    PICLOASER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False)
    PICLOACOD: Mapped[float] = mapped_column(Float(53), nullable=False)
    PICREC: Mapped[Optional[int]] = mapped_column(Integer)
    PICREPCOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    PICFECINI: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PICHORINI: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PICFECFIN: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PICHORFIN: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class PROCESO(Base):
    __tablename__ = 'PROCESO'
    __table_args__ = (
        PrimaryKeyConstraint('PRCCOD', 'PRCLINCOD', name='IDPRC1'),
        {'schema': 'dbo'}
    )

    PRCCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    PRCLINCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    PRCNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    PRCACCTIP: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'))
    PRCACCSER: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'))
    PRCACCEJE: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))
    PRCACCNUM: Mapped[Optional[float]] = mapped_column(Float(53))
    PRCCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'))
    PRCCENCOD: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))
    REGMOD: Mapped[Optional[int]] = mapped_column(Integer)
    REGENV: Mapped[Optional[int]] = mapped_column(Integer)
    PRCDIVCOD: Mapped[Optional[str]] = mapped_column(CHAR(3, 'Modern_Spanish_CI_AS'))
    PRCEMPCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))


class PROVEEDOR(Base):
    __tablename__ = 'PROVEEDOR'
    __table_args__ = (
        PrimaryKeyConstraint('CLICOD', 'CLICENCOD', name='IDPROVEEDOR1'),
        {'schema': 'dbo'}
    )

    CLICOD: Mapped[str] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), primary_key=True)
    CLICENCOD: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    CLIRAZ: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLINOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIDIR: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIPOSCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIPOSCIU: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIPOSPRO: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLINIF: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIRUTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLITEL: Mapped[Optional[str]] = mapped_column(CHAR(40, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIPAICOD: Mapped[Optional[str]] = mapped_column(CHAR(3, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIPERCON: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLIEMA: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    CLICAR: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class REPOSICIONCS(Base):
    __tablename__ = 'REPOSICIONCS'
    __table_args__ = (
        PrimaryKeyConstraint('ACSSER', 'ACSEJE', 'ACSNUM', 'ACSMOV', 'ACSACLCOD', 'ACSCOD', name='IDRES1'),
        Index('IDRES2', 'ACSLOT', 'ACSUBI', 'ACSARTCOD', mssql_clustered=False),
        {'schema': 'dbo'}
    )

    ACSSER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSNUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSMOV: Mapped[str] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), primary_key=True)
    ACSACLCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ACSFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ACSCLICOD: Mapped[Optional[str]] = mapped_column(CHAR(9, 'Modern_Spanish_CI_AS'))
    ACSARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSPAL: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSCAJ: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSUNI: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSCAN: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSLOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSUBI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    ACSNUMPAL: Mapped[Optional[int]] = mapped_column(Integer)
    ACSNUMCAJ: Mapped[Optional[int]] = mapped_column(Integer)
    ACSREPCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSENV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACSREGFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    ACSREGSER: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSREGEJE: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSREGNUM: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACSALBOBS: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSCANREA: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACSHOR: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    ACSMAN: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ACS2LOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    ACSALMCOD: Mapped[Optional[str]] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    ACSPOS: Mapped[Optional[int]] = mapped_column(Integer)
    ACSEMPCOD: Mapped[Optional[str]] = mapped_column(CHAR(12, 'Modern_Spanish_CI_AS'), server_default=text("('LIN')"))
    ACSNUEPRO: Mapped[Optional[int]] = mapped_column(Integer)
    ACSNUMPIC: Mapped[Optional[float]] = mapped_column(Float(53))
    ACSCANREC: Mapped[Optional[float]] = mapped_column(Float(53))


class REPRESENTANTE(Base):
    __tablename__ = 'REPRESENTANTE'
    __table_args__ = (
        PrimaryKeyConstraint('RPRCOD', name='IDRPR1'),
        {'schema': 'dbo'}
    )

    RPRCOD: Mapped[str] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), primary_key=True)
    RPRNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))


class RUTA(Base):
    __tablename__ = 'RUTA'
    __table_args__ = (
        PrimaryKeyConstraint('RUTCOD', name='IDRUT1'),
        {'schema': 'dbo'}
    )

    RUTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    RUTNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))


class SGAEMPRESA(Base):
    __tablename__ = 'SGAEMPRESA'
    __table_args__ = (
        PrimaryKeyConstraint('EMPCOD', name='IDSGAEMPRESA'),
        {'schema': 'dbo'}
    )

    EMPCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    EMPNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPRAZ: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPDIR: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPPOB: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPNIF: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPTEL: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPWEB: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPCOR: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPINTBUSDAT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((2))'))
    EMPRUTFTP: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPUSUFTP: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPCONFTP: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPDIRFTP: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    REGENV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    REGMOD: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPSER: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), server_default=text("('A')"))
    EMPIDICOD: Mapped[Optional[str]] = mapped_column(CHAR(3, 'Modern_Spanish_CI_AS'), server_default=text("('ESP')"))
    EMPNUEFTP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((1))'))
    EMPETIBLO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((15))'))
    EMPTIPEMP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPTIPETI: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPRUTDHL: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPNOLOT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPREPAUT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPFECINI: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("('01/01/1980')"))
    EMPCOM400: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPNOPAL: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPSTO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPETICLI: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPETIPAC: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPNOMOSMENINV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPFAB: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPARTMIN: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPAVIINV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((3))'))
    EMPNOAVIUBIINV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPENVETIEMP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPENVETICLI: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPENVETICUE: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPDOSREP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPRUTWIN: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPETICLI2: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPETIMOV: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPNOSUE001: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPUBIREC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPNUESIS: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPRUTCORREOS: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPRUTMIS: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPVERBD: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPPROVEEDOR: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPNOPICKING: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPDIVDEC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((2))'))
    EMPNOCOMDIR: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPCLIENTE: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPNODIVCAJ: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPMULLOT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPGLSIMPNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPGLSRUTMIS: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPGLSUID: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPPOSCOD: Mapped[Optional[int]] = mapped_column(Integer)
    EMPMONOLOTE: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    empInfCompra: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPETIUBI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    empInfRecepcion: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    empInfCambio: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    empInfManifiesto: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPMRWIMPNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPMRWRUTMIS: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPMRWUSU: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPMRWCON: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPMRWFRA: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPMRWABO: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPMRWURL: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPNOAPP10: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    EMPSERHOS: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPSERUSU: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPSERCON: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPSERIMPNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    EMPSERRUTMIS: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class SGAUSUARIO(Base):
    __tablename__ = 'SGAUSUARIO'
    __table_args__ = (
        PrimaryKeyConstraint('USUCOD', name='IDSGAUSUARIO1'),
        {'schema': 'dbo'}
    )

    USUCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    USUNOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUCONENT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    REGMOD: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    REGENV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    USUTIP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    USUNIV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    USUIMPETI: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUPAN: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((1))'))
    USUIMP1: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUIMP2: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUIMP3: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUIMP4: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUZEB1: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUZEB2: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUZEB3: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUZEB4: Mapped[Optional[str]] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUIDI: Mapped[Optional[str]] = mapped_column(CHAR(3, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUORDPES: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    USUTIPEMP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((-1))'))
    USUCONENT2: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    USUETIQUETAS: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    USUCOMPRAS: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


class SLOG3(Base):
    __tablename__ = 'SLOG3'
    __table_args__ = (
        PrimaryKeyConstraint('LOGCOD', name='IDSLOG31'),
        {'schema': 'dbo'}
    )

    LOGCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    LOGFEC: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LOGHOR: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LOGUSU: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    LOGTEX: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'Modern_Spanish_CI_AS'))
    LOGNUM: Mapped[Optional[float]] = mapped_column(Float(53))


class STOCK(Base):
    __tablename__ = 'STOCK'
    __table_args__ = (
        PrimaryKeyConstraint('STOARTCOD', 'STOUBI', 'STOLOT', name='IDSTO1'),
        {'schema': 'dbo'}
    )

    STOARTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    STOUBI: Mapped[str] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), primary_key=True)
    STOLOT: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    STOCAN: Mapped[Optional[float]] = mapped_column(Float(53))


class STOCKLOTE(Base):
    __tablename__ = 'STOCKLOTE'
    __table_args__ = (
        PrimaryKeyConstraint('STOARTCOD', 'STOUBI', 'STOLOT', 'STO2LOT', name='IDSTOLOT1'),
        {'schema': 'dbo'}
    )

    STOARTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    STOUBI: Mapped[str] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), primary_key=True)
    STOLOT: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    STO2LOT: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    STOCAN: Mapped[Optional[float]] = mapped_column(Float(53))


class SUBFAMILIA(Base):
    __tablename__ = 'SUBFAMILIA'
    __table_args__ = (
        PrimaryKeyConstraint('SFACOD', name='IDSUBFAMILIA1'),
        {'schema': 'dbo'}
    )

    SFACOD: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    SFANOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    SFANOLOT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("('')"))


t_TABLEAU = Table(
    'TABLEAU', Base.metadata,
    Column('EMPRESA', CHAR(12, 'Modern_Spanish_CI_AS')),
    Column('NÚMERO', Float(53), nullable=False),
    Column('FECHA PEDIDO', DateTime),
    Column('FECHA', DateTime),
    Column('HORA', DateTime),
    Column('TIPO_MOVIMIENTO', CHAR(2, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('MOVIMIENTO', CHAR(16, 'Modern_Spanish_CI_AS')),
    Column('TERCERO', CHAR(9, 'Modern_Spanish_CI_AS')),
    Column('CENTRO', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('NOMBRE DE TERCERO', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('ARTÍCULO', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('CÓDIGO AGRUPADO', CHAR(30, 'Modern_Spanish_CI_AS')),
    Column('NOMBRE DE ARTÍCULO', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('CANTIDAD', Float(53)),
    Column('CANTIDAD CON SIGNO', Float(53)),
    Column('LOTE', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('UBICACIÓN', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('Nº CAJA', Integer),
    Column('Nº PALET', Integer),
    schema='dbo'
)


t_TABLEAU_PENDIENTE = Table(
    'TABLEAU PENDIENTE', Base.metadata,
    Column('EMPRESA', CHAR(12, 'Modern_Spanish_CI_AS')),
    Column('ARTÍCULO', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('CÓDIGO AGRUPADO', CHAR(30, 'Modern_Spanish_CI_AS')),
    Column('NOMBRE DE ARTÍCULO', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('CANTIDAD PENDIENTE', Float(53)),
    schema='dbo'
)


t_TABLEAU_PENDIENTE_INDIVIDUAL = Table(
    'TABLEAU PENDIENTE INDIVIDUAL', Base.metadata,
    Column('EMPRESA', CHAR(12, 'Modern_Spanish_CI_AS')),
    Column('NÚMERO', Float(53), nullable=False),
    Column('FECHA PEDIDO', DateTime),
    Column('CLIENTE', CHAR(15, 'Modern_Spanish_CI_AS')),
    Column('CENTRO', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('NOMBRE DE CLIENTE', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('ARTÍCULO', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('CÓDIGO AGRUPADO', CHAR(30, 'Modern_Spanish_CI_AS')),
    Column('NOMBRE DE ARTÍCULO', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('CANTIDAD PENDIENTE', Float(53)),
    schema='dbo'
)


t_TABLEAUPRUEBAS = Table(
    'TABLEAUPRUEBAS', Base.metadata,
    Column('FECHA', DateTime),
    Column('HORA', DateTime),
    Column('TIPO_MOVIMIENTO', CHAR(2, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('MOVIMIENTO', CHAR(16, 'Modern_Spanish_CI_AS')),
    Column('TERCERO', CHAR(9, 'Modern_Spanish_CI_AS')),
    Column('CENTRO', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('NOMBRE DE TERCERO', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('ARTÍCULO', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('CÓDIGO AGRUPADO', CHAR(30, 'Modern_Spanish_CI_AS')),
    Column('NOMBRE DE ARTÍCULO', CHAR(50, 'Modern_Spanish_CI_AS')),
    Column('CANTIDAD', Float(53)),
    Column('CANTIDAD CON SIGNO', Float(53)),
    Column('LOTE', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('UBICACIÓN', CHAR(20, 'Modern_Spanish_CI_AS')),
    schema='dbo'
)


class TCLIENTEDOC(Base):
    __tablename__ = 'TCLIENTEDOC'
    __table_args__ = (
        PrimaryKeyConstraint('TCLPROCOD', 'TCLCLICOD', 'TCLCENCOD', name='IDTCLIDOC1'),
        {'schema': 'dbo'}
    )

    TCLPROCOD: Mapped[float] = mapped_column(Float(53), primary_key=True)
    TCLCLICOD: Mapped[str] = mapped_column(CHAR(15, 'Modern_Spanish_CI_AS'), primary_key=True)
    TCLCENCOD: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)


class TERMINALFRM(Base):
    __tablename__ = 'TERMINALFRM'
    __table_args__ = (
        PrimaryKeyConstraint('TERCOD', 'TERFORMULARIO', 'TERREJILLA', 'TERINDICE', name='IDTERMINALFRM1'),
        {'schema': 'dbo'}
    )

    TERCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    TERFORMULARIO: Mapped[str] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), primary_key=True)
    TERREJILLA: Mapped[str] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), primary_key=True)
    TERINDICE: Mapped[int] = mapped_column(Integer, primary_key=True)
    TERHEIGHT: Mapped[Optional[float]] = mapped_column(Float(53))
    TERWIDTH: Mapped[Optional[float]] = mapped_column(Float(53))
    TERANCHOREJILLA: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


class TERMINALREJ(Base):
    __tablename__ = 'TERMINALREJ'
    __table_args__ = (
        PrimaryKeyConstraint('TERCOD', 'TERCON', 'TERFORMULARIO', 'TERREJILLA', 'TERINDICE', 'TERCOLUMNA', name='IDTERMINALREJ1'),
        {'schema': 'dbo'}
    )

    TERCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    TERCON: Mapped[int] = mapped_column(Integer, primary_key=True)
    TERFORMULARIO: Mapped[str] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), primary_key=True)
    TERREJILLA: Mapped[str] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), primary_key=True)
    TERINDICE: Mapped[int] = mapped_column(Integer, primary_key=True)
    TERCOLUMNA: Mapped[int] = mapped_column(Integer, primary_key=True)
    TERANCHO: Mapped[Optional[float]] = mapped_column(Float(53))


class UBICACION(Base):
    __tablename__ = 'UBICACION'
    __table_args__ = (
        PrimaryKeyConstraint('UBICON', name='IDUBICACION1'),
        Index('IDUBICACION23', 'UBISUE2', mssql_clustered=False, mssql_include=['UBICODUBI']),
        Index('IDUBICACION231', 'UBICODUBI', 'UBISUE2', mssql_clustered=False),
        {'schema': 'dbo'}
    )

    UBICON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    UBIETI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    UBICODUBI: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    UBIANC: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    UBIALT: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    REGENV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    REGMOD: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    UBICAR: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    UBINUMPAL: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((1))'))
    UBISUE2: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    UBIMUL: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    UBIALMCOD: Mapped[Optional[str]] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    UBINOM: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'), server_default=text("('')"))
    UBINOAVIINV: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    UBILIB: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    UBINOROT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    UBI001: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    UBINORECUENTO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


class UBICACIONC2(Base):
    __tablename__ = 'UBICACIONC2'
    __table_args__ = (
        PrimaryKeyConstraint('UBI2TIP', 'UBI2SER', 'UBI2EJE', 'UBI2NUM', 'UBI2COD', name='IDUBICC2'),
        {'schema': 'dbo'}
    )

    UBI2TIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2SER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2EJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2NUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    UBI2COD: Mapped[str] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2INV: Mapped[Optional[int]] = mapped_column(Integer)
    UBI2REA: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class UBICACIONC22(Base):
    __tablename__ = 'UBICACIONC22'
    __table_args__ = (
        PrimaryKeyConstraint('UBI2TIP', 'UBI2SER', 'UBI2EJE', 'UBI2NUM', 'UBI2COD', 'UBI2CON', name='IDUBICC22'),
        {'schema': 'dbo'}
    )

    UBI2TIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2SER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2EJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2NUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    UBI2COD: Mapped[str] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2CON: Mapped[int] = mapped_column(Integer, primary_key=True)
    UBI2INV: Mapped[Optional[int]] = mapped_column(Integer)
    UBI2REA: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))


class UBICACIONC3(Base):
    __tablename__ = 'UBICACIONC3'
    __table_args__ = (
        PrimaryKeyConstraint('UBI2USU', 'UBI2TIP', 'UBI2SER', 'UBI2EJE', 'UBI2NUM', 'UBI2COD', name='IDUBICC3'),
        {'schema': 'dbo'}
    )

    UBI2USU: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2TIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2SER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2EJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2NUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    UBI2COD: Mapped[str] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2INV: Mapped[Optional[int]] = mapped_column(Integer)
    UBI2REA: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), server_default=text("('')"))


class UBICACIONC32(Base):
    __tablename__ = 'UBICACIONC32'
    __table_args__ = (
        PrimaryKeyConstraint('UBI2USU', 'UBI2TIP', 'UBI2SER', 'UBI2EJE', 'UBI2NUM', 'UBI2COD', 'UBI2CON', name='IDUBICC32'),
        {'schema': 'dbo'}
    )

    UBI2USU: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2TIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2SER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2EJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2NUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    UBI2COD: Mapped[str] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBI2CON: Mapped[int] = mapped_column(Integer, primary_key=True)
    UBI2INV: Mapped[Optional[int]] = mapped_column(Integer)
    UBI2REA: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))


class UBICACIONCC(Base):
    __tablename__ = 'UBICACIONCC'
    __table_args__ = (
        PrimaryKeyConstraint('UBITIP', 'UBISER', 'UBIEJE', 'UBINUM', 'UBIPAS', name='IDUBICC1'),
        {'schema': 'dbo'}
    )

    UBITIP: Mapped[str] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBISER: Mapped[str] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBIEJE: Mapped[str] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'), primary_key=True)
    UBINUM: Mapped[float] = mapped_column(Float(53), primary_key=True)
    UBIPAS: Mapped[str] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), primary_key=True)


class UBICACIONIR(Base):
    __tablename__ = 'UBICACIONIR'
    __table_args__ = (
        PrimaryKeyConstraint('UBICON', name='IDUBIIR1'),
        {'schema': 'dbo'}
    )

    UBICON: Mapped[float] = mapped_column(Float(53), primary_key=True)
    UBITIP: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Modern_Spanish_CI_AS'))
    UBISER: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'))
    UBIEJE: Mapped[Optional[str]] = mapped_column(CHAR(4, 'Modern_Spanish_CI_AS'))
    UBINUM: Mapped[Optional[float]] = mapped_column(Float(53))
    UBICOD: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'))
    UBIARTCOD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    UBILOT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'))
    UBICAN: Mapped[Optional[float]] = mapped_column(Float(53))


class UBICACIONTMP(Base):
    __tablename__ = 'UBICACIONTMP'
    __table_args__ = (
        PrimaryKeyConstraint('UBICOD', name='IDUBITMP1'),
        {'schema': 'dbo'}
    )

    UBICOD: Mapped[str] = mapped_column(CHAR(20, 'Modern_Spanish_CI_AS'), primary_key=True)


class VMVSEMAFOROARTICULO(Base):
    __tablename__ = 'VMVSEMAFOROARTICULO'
    __table_args__ = (
        PrimaryKeyConstraint('ARTCOD', name='IDRVMVSEMART1'),
        {'schema': 'dbo'}
    )

    ARTCOD: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)


t_VPEDIDOCC = Table(
    'VPEDIDOCC', Base.metadata,
    Column('T', String(6, 'Modern_Spanish_CI_AS')),
    Column('ACCNUM', Float(53), nullable=False),
    Column('ACCFEC', DateTime),
    Column('ACCCLICOD', CHAR(15, 'Modern_Spanish_CI_AS')),
    Column('ACCCENCOD', CHAR(4, 'Modern_Spanish_CI_AS')),
    Column('CLIENTE', String(200, 'Modern_Spanish_CI_AS')),
    Column('ACCTIP', String(1, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACCSER', CHAR(5, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACCEJE', CHAR(4, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('ACCTIPINV', Integer),
    Column('ACCLOASER', CHAR(5, 'Modern_Spanish_CI_AS')),
    Column('ACCLOACOD', Float(53)),
    Column('ACCFORALB', Integer),
    Column('ACCALMCOD', CHAR(2, 'Modern_Spanish_CI_AS')),
    Column('ACCPEDDIA', Float(53)),
    Column('ACCTIP2', String(1, 'Modern_Spanish_CI_AS'), nullable=False),
    Column('LINEAS', Integer),
    Column('LINEASSERVIDAS', Integer),
    Column('LINEASPARCIALES', Integer),
    Column('ACCREPCOD', CHAR(15, 'Modern_Spanish_CI_AS')),
    Column('ACCREPCOD2', String(10, 'Modern_Spanish_CI_AS')),
    Column('ACCREPCOD3', String(10, 'Modern_Spanish_CI_AS')),
    Column('ACCNUEPIC', Integer),
    Column('ACCESAGE', Integer),
    Column('ACCUSUCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACCESAGE1', Integer),
    Column('ACCSIT', CHAR(1, 'Modern_Spanish_CI_AS')),
    Column('ACCFECCIE', DateTime),
    Column('ACCREPCOD4', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACCREPCOD5', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('ACCRECART', Integer),
    schema='dbo'
)


t_VSTOCKLOTE = Table(
    'VSTOCKLOTE', Base.metadata,
    Column('STOARTCOD', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('STOUBI', CHAR(20, 'Modern_Spanish_CI_AS')),
    Column('STOLOT', CHAR(10, 'Modern_Spanish_CI_AS')),
    Column('STOCAN', Float(53)),
    Column('STOFECINI', DateTime),
    schema='dbo'
)


class QanetParametro2(Base):
    __tablename__ = 'qanet_parametro2'
    __table_args__ = (
        PrimaryKeyConstraint('connom', name='idqanet_parametro2'),
        {'schema': 'dbo'}
    )

    connom: Mapped[str] = mapped_column(CHAR(100, 'Modern_Spanish_CI_AS'), primary_key=True)
    conentero: Mapped[Optional[int]] = mapped_column(Integer)
    contexto: Mapped[Optional[str]] = mapped_column(CHAR(1000, 'Modern_Spanish_CI_AS'))
    condoble: Mapped[Optional[float]] = mapped_column(Float(53))


class Terminalpda(Base):
    __tablename__ = 'terminalpda'
    __table_args__ = (
        PrimaryKeyConstraint('repcod', name='idterminalpda1'),
        {'schema': 'dbo'}
    )

    repcod: Mapped[str] = mapped_column(CHAR(10, 'Modern_Spanish_CI_AS'), primary_key=True)
    repnom: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Modern_Spanish_CI_AS'))
    repser: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Modern_Spanish_CI_AS'))
    repdat: Mapped[Optional[str]] = mapped_column(CHAR(2, 'Modern_Spanish_CI_AS'))
    reprutsin: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'))
    reprutwifi: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Modern_Spanish_CI_AS'))
    repenv: Mapped[Optional[int]] = mapped_column(Integer)
    regmod: Mapped[Optional[int]] = mapped_column(Integer)
    regenv: Mapped[Optional[int]] = mapped_column(Integer)
    repnoeti: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    repubirec: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    reptipcaj: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    repubirec2: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((-1))'))
