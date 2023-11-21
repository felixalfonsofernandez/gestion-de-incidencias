# models.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Crea una conexión a SQL Server usando sqlalchemy
conn_str = (
    r"mssql+pyodbc://sa:Andromeda257@DESKTOP-CKOF5F5/proyecto_eficiencia_trabajadores?"
    r"driver=SQL Server"
)
engine = create_engine(conn_str)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Usuario(Base):
    __tablename__ = 'Usuario'
    Id = Column(Integer, primary_key=True)
    Nombres = Column(String)
    Telefono = Column(String)
    Correo = Column(String)
    Usuario = Column(String)
    Contraseña = Column(String)

class Jefe(Base):
    __tablename__ = 'Jefe'
    
    Id = Column(Integer, primary_key=True)
    Nombres = Column(String(100))
    Cargo = Column(String(100))
    Correo = Column(String(100))
    Area = Column(String(100))
    Direccion = Column(String(100))
    Telefono = Column(String(20))
    Usuario = Column(String(50))
    Contraseña = Column(String(50))  # Recuerda, deberías considerar hashear las contraseñas

    def __repr__(self):
        return f'<Jefe {self.Nombres} - {self.Cargo}>'


class Tareas(Base):
    __tablename__ = 'Tareas'
    Id = Column(Integer, primary_key=True)
    Creador = Column(String)
    Contenido = Column(String)
    Realizado = Column(Boolean)
    EnProgreso = Column(Boolean)
    creacion = Column(DateTime, default=datetime.datetime.now)  # fecha y hora de creación
    fecha_termino = Column(DateTime)  # fecha y hora de terminación, no tiene valor predeterminado
    Designado = Column(Integer, ForeignKey('Usuario.Id'))  # Esto crea una relación con la tabla Usuario
    Dificultad = Column(String)  # Cadena de texto para describir la dificultad
    NUMERO_TRABAJADORES = Column(Integer)  # Esto crea una relación con la tabla Usuario

    usuario_designado = relationship("Usuario", foreign_keys=[Designado])
    
# ... (otros modelos)

class DataSynLab(Base):
    __tablename__ = 'datasynlab'
    Ticket = Column(Float, primary_key=True)
    Tipo_Ticket = Column(String(255), nullable=True, name='Tipo Ticket')
    Area = Column(String(255), nullable=True)
    Id_Solicitante = Column(Float, nullable=True, name='Id Solicitante')
    Mail_Solicitante = Column(String(255), nullable=True, name='Mail Solicitante')
    Solicitante = Column(String(255), nullable=True)
    Cargo = Column(String(255), nullable=True)
    Centro_de_costos = Column(Float, nullable=True, name='Centro de costos')
    Area1 = Column(String(255), nullable=True)
    Gerencia = Column(String(255), nullable=True)
    Local = Column(String(255), nullable=True)
    Titulo = Column(String(255), nullable=True)
    Categoría = Column(String(255), nullable=True)
    Sub_Categoria = Column(String(255), nullable=True, name='Sub-Categoria')
    Aplicacion_Servicio = Column(String(255), nullable=True, name='Aplicacion Servicio')
    Prioridad = Column(String(255), nullable=True)
    Fecha_Registro = Column(String(255), nullable=True, name='Fecha Registro')  # Considera usar DateTime
    Fecha_Estado = Column(String(255), nullable=True, name='Fecha Estado')  # Considera usar DateTime
    Dias_Espera = Column(Float, nullable=True, name='Dias Espera')
    Dias_Laborales = Column(Float, nullable=True, name='Dias Laborales')
    Estado = Column(String(255), nullable=True)
    Id_Ejecutor = Column(Float, nullable=True, name='Id Ejecutor')
    Cta_Ejecutor = Column(String(255), nullable=True, name='Cta Ejecutor')
    Ejecutor = Column(String(255), nullable=True)

# Inicializa la base de datos
def init_db():
    Base.metadata.create_all(bind=engine)

# No olvides llamar a init_db() cuando inicies tu aplicación para crear las tablas.
