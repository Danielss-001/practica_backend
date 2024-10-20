from sqlalchemy import Table, Column, ForeignKey, ARRAY, JSON
from sqlalchemy.sql.sqltypes import Integer, String, NUMERIC
from config.base_control import engine, meta_data

# Modelo tabla ususarios 
users = Table(
    "users",meta_data,
    Column("id", Integer, primary_key=True),
    Column("username",String(255),nullable=False, unique=True),
    Column("password",String(255),nullable=False),
    Column("name",String(255),nullable=False),
    Column("perfil",String(255),nullable=False)
)

# Modelo tabla modulos pilares de estudio
calificaciones = Table(
    "calificaciones",meta_data, 
    Column("id",Integer, primary_key=True),
    Column("user_id",Integer, ForeignKey('users.id'),nullable=False),
    Column("estructura",NUMERIC(3,2),nullable=False),         # pilar_1
    Column("competencias",NUMERIC(3,2),nullable=False),       # pilar_2
    Column("comportamientos",NUMERIC(3,2), nullable=False),   # pilar_3
    Column("objetividad",NUMERIC(3,2), nullable=False),       # pilar_4
    Column("preguntas",NUMERIC(3,2),nullable=False),          # pilar_5
    Column("feedback",NUMERIC(3,2), nullable=False),          # pilar_6
    Column("total",NUMERIC(3,2),nullable=False)               # total calificacion
)

# Modelo de chats de AI
chats = Table(
    "chats", meta_data,
    Column("id",Integer, primary_key=True),
    Column("user_id",Integer, ForeignKey("users.id"),nullable=False),
    Column("estructura",JSON),                 # pilar_1
    Column("competencias",JSON),               # pilar_2
    Column("comportamientos",JSON),            # pilar_3
    Column("objetividad",JSON),                # pilar_4
    Column("preguntas",JSON),                  # pilar_5
    Column("feedback",JSON)                    # pilar_6
)

# Limpimamos la base de datos
#meta_data.drop_all(engine)

# Creacion de base de datos
meta_data.create_all(engine)

#Column("estructura",ARRAY(String)),