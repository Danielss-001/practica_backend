from config.base_control import engine, update
from models.users import users, calificaciones, chats # Modelos de base de datos
from fastapi.encoders import jsonable_encoder


# Insertar un registro nuevo 
def InsertRegister(data_dict:dict):
    with engine.connect() as conn: # Abrir coneccion a base de datos
            
        # insertamos nuevo usuario en la base de datos
        conn.execute(users.insert().values(data_dict['users'])) 

        # obtenemos el id del nuevo usuario
        id_user = conn.execute(users.select().where(users.c.username == data_dict['users']['username'])).scalar()

        # Asignamos valores id al diccionario y guardamos segunda tabla (calificaciones)
        data_dict['calificaciones']['user_id'] = id_user # Asignamos clave foranea(Foreing Key)
        conn.execute(calificaciones.insert().values(data_dict['calificaciones']))

        # Asignamos a tercera tabla
        data_dict['chats']['user_id'] = id_user # Asignamos clave foranea(Foreing Key)
        conn.execute(chats.insert().values(data_dict['chats']))
        
        conn.commit()

# Obtener ID autenticado
def Id_User(username:str):
    id_user:int
    # abrimos coneccion
    with engine.connect() as conn:
        # seleccionamos por nombre de usuario unico
        id_user = conn.execute(users.select().where(users.c.username == username)).scalar()
    return id_user 


# Solo para super usuario
def AllRegisters():
    with engine.connect() as conn:
        # Mostramos datos de tabla users
        usr = conn.execute(users.select()).fetchall()
        # Mostramos datos de tabla calificaciones 
        mdls = conn.execute(calificaciones.select()).fetchall()
        # Mostramos datos de tabla chats
        chts = conn.execute(chats.select()).fetchall()

    usr_dict = [row_to_dict(row, users)for row in usr]
    mdls_dict = [row_to_dict(row, calificaciones)for row in mdls]
    chts_dict = [row_to_dict(row, chats)for row in chts]
    
    return jsonable_encoder({
        "users":usr_dict,
        "calificaciones":mdls_dict,
        "chats":chts_dict
    })
        
# convertir cada fila en un diccionario
def row_to_dict(row,table):
    return {table.columns[i].name: row[i] for i in range(len(row))}

# verificamos si existe el username en la base de datos
def VerifyUsername(name:str):
    
    with engine.connect() as conn:
        # verificamos la existencia del name en base de datos
        if_exist = users.select().where(users.c.username == name)
        # obtenemos el bool de si existe o no 
        verify = conn.execute(if_exist)

        # retornamos si existe
        return verify.scalar() is not None

# Obtenemos datos del ususario ("username" | "password")
def User_data(id_user:int):
    usr:tuple = ()
    # Iniciamos conexion con base de datos
    with engine.connect() as conn:
        # Obtenemos el usuario
        result = users.select().where(users.c.id == id_user)
        usr = conn.execute(result).fetchone()
    return  {
                "username":usr[1],
                "password":usr[2]
            }

# Metodo para acceder a datos de name y username
def User_name(id_user:int):
    usr:tuple = ()
    #   Iniciamos conexion con base de datos
    with engine.connect() as conn:
        #   Obtenemos al usuario
        result = users.select().where(users.c.id == id_user)
        usr = conn.execute(result).fetchone()
    return {
        "username":usr[1],
        "name":usr[3]
    }

# Obtenemos datos del ususario ("calificaciones")
def User_Califications(id_user:int):
    usr:tuple = ()
    # Iniciamos coneccion con base de datos
    with engine.connect() as conn:
        # Obtenemos el usuario
        result = calificaciones.select().where(calificaciones.c.user_id == id_user)
        usr = conn.execute(result).fetchone()
    return {
                "user_id":usr[1],
                "estructura":usr[2],
                "competencias":usr[3],
                "comportamientos":usr[4],
                "objetividad":usr[5],
                "preguntas":usr[6],
                "feedback":usr[7],
                "total":usr[8],
           }

# Obtenemos los chats del susuario ("chats")
def User_Chats(id_user:int):
    usr:tuple = ()
    # Iniciamos coneccion con base de datos
    with engine.connect() as conn:
        # Obtenemos el usuario
        result = chats.select().where(chats.c.user_id == id_user)
        usr = conn.execute(result).fetchone()
        if usr is None:
            print("esta vacia la lista")

    return {
                "user_id":usr[1],
                "estructura":usr[2],
                "competencias":usr[3],
                "comportamientos":usr[4],
                "objetividad":usr[5],
                "preguntas":usr[6],
                "feedback":usr[7]
           }

#
#
#
#
# Reemplazar calificaciones y guardar en base de datos
#
# Estructura
def Update_chat_structure(id_user:int, new_data:list):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt = (
            update(chats)
            .where(chats.c.user_id == id_user)
            .values(estructura=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion del chat

        conn.commit() # Guardamos los cambios en la base de datos
# Estructura
# Reemplazar calificacion 
def Update_Structure_Calification(id_user:int,new_data:float):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt =(
            update(calificaciones)
            .where(calificaciones.c.user_id == id_user)
            .values(estructura=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion de la calificacion

        conn.commit # Guardamos la actualizacion en la base de datos

# competencias
def Update_chat_competencias(id_user:int, new_data:list):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt = (
            update(chats)
            .where(chats.c.user_id == id_user)
            .values(competencias=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion del chat

        conn.commit() # Guardamos los cambios en la base de datos
# competencias
# Reemplazar calificacion 
def Update_competencias_Calification(id_user:int,new_data:float):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt =(
            update(calificaciones)
            .where(calificaciones.c.user_id == id_user)
            .values(competencias=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion de la calificacion

        conn.commit # Guardamos la actualizacion en la base de datos

# comportamientos
def Update_chat_comportamientos(id_user:int, new_data:list):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt = (
            update(chats)
            .where(chats.c.user_id == id_user)
            .values(comportamientos=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion del chat

        conn.commit() # Guardamos los cambios en la base de datos
# comportamientos
# Reemplazar calificacion 
def Update_comportamientos_calificacion(id_user:int,new_data:float):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt =(
            update(calificaciones)
            .where(calificaciones.c.user_id == id_user)
            .values(comportamientos=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion de la calificacion

        conn.commit # Guardamos la actualizacion en la base de datos

# objetividad
def Update_chat_objetividad(id_user:int, new_data:list):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt = (
            update(chats)
            .where(chats.c.user_id == id_user)
            .values(objetividad=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion del chat

        conn.commit() # Guardamos los cambios en la base de datos
# objetividad
# Reemplazar calificacion 
def Update_objetividad_calificacion(id_user:int,new_data:float):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt =(
            update(calificaciones)
            .where(calificaciones.c.user_id == id_user)
            .values(objetividad=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion de la calificacion

        conn.commit # Guardamos la actualizacion en la base de datos

# preguntas
def Update_chat_preguntas(id_user:int, new_data:list):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt = (
            update(chats)
            .where(chats.c.user_id == id_user)
            .values(preguntas=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion del chat

        conn.commit() # Guardamos los cambios en la base de datos
# preguntas
# Reemplazar calificacion 
def Update_preguntas_calificacion(id_user:int,new_data:float):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt =(
            update(calificaciones)
            .where(calificaciones.c.user_id == id_user)
            .values(preguntas=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion de la calificacion

        conn.commit # Guardamos la actualizacion en la base de datos

# feedback
def Update_chat_feedback(id_user:int, new_data:list):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt = (
            update(chats)
            .where(chats.c.user_id == id_user)
            .values(feedback=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion del chat

        conn.commit() # Guardamos los cambios en la base de datos
# feedback
# Reemplazar calificacion 
def Update_feedback_calificacion(id_user:int,new_data:float):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt =(
            update(calificaciones)
            .where(calificaciones.c.user_id == id_user)
            .values(feedback=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion de la calificacion

        conn.commit # Guardamos la actualizacion en la base de datos

# test
# Reemplazar calificacion 
def Update_test_calificacion(id_user:int,new_data:float):
    with engine.connect() as conn:
        # Consulta de actualizacion
        stmt =(
            update(calificaciones)
            .where(calificaciones.c.user_id == id_user)
            .values(total=new_data)
        )
        conn.execute(stmt) # Ejecutamos la actualizacion de la calificacion

        conn.commit # Guardamos la actualizacion en la base de datos