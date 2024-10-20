from fastapi import APIRouter, status, HTTPException, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from schemes.user import UserEducation
from passlib.context import CryptContext
from config.db import InsertRegister, AllRegisters, VerifyUsername
from ai.welcome_ai import HumanMessage, message_context_input,call_with_name,message_star_interview, chat, conversation_base_data,conversation_history, evaluation_prompt, reload_evaluation
import os
import json


load_dotenv('.env')
router = APIRouter() # Inicializamos el router

# Variablkes necesarias para encriptar crontraseña
crypt = CryptContext(schemes=['bcrypt']) # Encriptado de contraseña y Verificacion 

#///////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////

# Inicializa la variable usuario
new_user = UserEducation(
    username='string',
    password='string',
    name='string',
    perfil='string',
    user_id = 0,
    estructura = 0,
    competencias = 0,
    comportamientos = 0,
    objetividad = 0,
    preguntas = 0,
    feedback = 0,
    total = 0
)
# |                              |
# |  Encryptado y autenticacion  |  
# |                              |
def Hash_password(password:str): # Methodo para encryptar la contraseña
    return crypt.hash(password) 

#
#///////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# 
# Crear Usuario
#
# Empezar entrevista
@router.get('/start')
async def Star_Interview():
    """
        ¡El usuario a dado click en 'Empezar' la IA da la introducion a la entrevista y pide los datos
        de 'nombre' y 'perfil'! 

    """
    conversation_base_data.clear()
    conversation_history.clear()
    conversation_history.append({"fase":"start_interview","message":message_context_input}) # Anexamos nuevo system a la AI
    conversation_base_data.append({"fase":"start_interview","message":message_context_input.content})
    invoke_chat = [msg["message"] for msg in conversation_history if msg["fase"]=="start_interview"]
    
    response = chat.invoke(invoke_chat)

    return {"message":response.content}

# Tomado de datos nombre y perfil por Query
@router.post('/data/')
async def Input_Data(name:str,perfil:str):
    """
        La IA saludara utilizando su nombre y contextualiza el cargo del usuario... animara al usuario a iniciar el chat y entrar en el websocket

    """
    # Toma de datos
    new_user.name = name
    new_user.perfil = perfil
    message = call_with_name(name=name,perfil=perfil)
    conversation_history.append({"fase":"start_interview","message":message})
    conversation_base_data.append({"fase":"start_interview","message":message.content})
    invoke_chat = [msg["message"] for msg in conversation_history if msg["fase"]=="start_interview"]
    response = chat.invoke(invoke_chat)

    return {"message":response.content}  

# Inicio de chat con AI entrevista
@router.websocket('/chat')
async def Start_Chat_Interview(websocket:WebSocket):
    """
        Manejo de chat despues de tomar datos 'name''perfil' inicia la conversacion
    """    
    await websocket.accept()
    # Agregamos contexto de la entrevista a la ia para que esta de la primera pauta
    conversation_history.append({"fase":"interview","message":message_star_interview}) 
    conversation_base_data.append({"fase":"interview","message":message_star_interview.content})
    invoke_chat = [msg["message"] for msg in conversation_history if msg["fase"]=="interview"]
    response_initial = chat.invoke(invoke_chat)
    await websocket.send_text(response_initial.content) # Enviamos la primera respuesta de la IA al front
    try:
        while True:
            data = await websocket.receive_text()
            message = HumanMessage(content=data)
            conversation_history.append({"fase":"interview","message":message})
            conversation_base_data.append({"fase":"interview","message":message.content})
            
            invoke_chat = [msg["message"] for msg in conversation_history if msg["fase"]=="interview"]
            response = chat.invoke(invoke_chat)
            conversation_history.append({"fase":"interview","message":HumanMessage(content=response.content)}) # Añadimos respuesta de IA al historial
            conversation_base_data.append({"fase":"interview","message":response.content})

            await websocket.send_text(response.content)
            
    except WebSocketDisconnect:
        return HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT)

# Al finalizar la Entrevista
@router.get('/finish')
async def Finish_Interview():

    """
        Se finalizara la entrevista y se procede a asignar calificacion a usuario base
    
    """
    conversation_history.append({"fase":"evaluation","message":evaluation_prompt})
    conversation_base_data.append({"fase":"evaluation","message":evaluation_prompt.content})
    invoke_chat = [msg["message"] for msg in conversation_history if msg["fase"] == "interview"]
    invoke_chat.append(evaluation_prompt.content)

    max_attepmts = 4 
    attempt = 0

    while attempt < max_attepmts:

        response = chat.invoke(invoke_chat) # Se obtienen las calificaciones del usuario
        # Se actualiza el historial con las notas
        conversation_history.append({"fase":"evaluation","message":HumanMessage(content=response.content)})
        conversation_base_data.append({"fase":"evaluation","message":response.content})
    
        print(response.content)
        try:
            result = json.loads(response.content) # se transforma en formato json para acceder a los valores
            # Se guardan calificaciones en user temporal
            new_user.estructura = result.get('estructura')
            new_user.competencias = result.get('competencias')
            new_user.comportamientos = result.get('comportamientos')
            new_user.objetividad = result.get('objetividad')
            new_user.preguntas = result.get('preguntas')
            new_user.feedback = result.get('feedback')
            # Devuelve las calificaciones para mostrar al usuario 
            return {
                "estructura":new_user.estructura,
                "competencias":new_user.competencias,
                "comportamientos":new_user.comportamientos,
                "objetividad":new_user.objetividad,
                "preguntas":new_user.preguntas,
                "feedback":new_user.feedback
                }
            # Recuerda dar instruccion al usuario que si desea guardar los datos y mejorar debe crear usuario
            # pedir 'username' y 'password'
        except json.JSONDecodeError:
            invoke_chat.append(reload_evaluation.content)
            attempt += 1 
            print("No es un JSON valido | Reintentando...")
            if attempt >= max_attepmts:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al procesar la respuesta JSON.")
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor: {e}")

# Se piden los datos de 'username' y 'password'
@router.post('/create')
async def Add_Finish_Data(username:str,password:str):
    try:
        new_user.username = username
        new_user.password = password
        raise HTTPException(status_code=status.HTTP_200_OK,detail="Datos asignados ")
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Usuario no asignado")

# Llamado a la API crear usuario
@router.post('/signup')
async def Create_User(data_user:UserEducation):
    if VerifyUsername(data_user.username):
        return HTTPException(status_code=status.HTTP_205_RESET_CONTENT,detail='User already exists')
    else:
        data = TransfomData(data_user) # Transformamos la data en un diccionario valido a la base de datos
        InsertRegister(data) # Insertamos en base de datos
        return HTTPException(status_code=status.HTTP_202_ACCEPTED,detail='User Created Succesful')
    

#/////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////
# Acceder a todos los usuarios de base de datos
@router.get('/data')
async def Get_Users():
    return AllRegisters() # Mostramos en base de datos
#/////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////

#
#   Transformar diccionario
#
def TransfomData(data_user:UserEducation): 
    #hash de la contraseña
    data = dict(data_user)
    password_hash = Hash_password(data['password'])
    data['password'] = password_hash

    # Promedio de nota final
    listNotes = [data.get('estructura'),data.get('competencias'),data.get('comportamientos'),data.get('objetividad'),data.get('preguntas'),data.get('feedback')]
    
    # Se promedian las notas obtenidas
    totalPromedio = sum(listNotes)/len(listNotes)
    promedio = round(totalPromedio,2)

    # Asignar historial de chat 
    list_chats = [{"message":msg} for msg in conversation_base_data if msg["fase"]=="interview"] 
    list_califications = [{"message":msg} for msg in conversation_base_data if msg["fase"]=="evaluation"] 
    history_chat = list_chats + list_califications 
    

    # Asignar a total de notas, en la cracion de data
    new_Data= {
        "users":{
            "username":data.get('username'),
            "password":data.get('password'),
            "name":data.get('name'),
            "perfil":data.get('perfil'),
        },
        "calificaciones":{
            "user_id":data.get('user_id'),
            "estructura":data.get('estructura'),
            "competencias":data.get('competencias'),
            "comportamientos":data.get('comportamientos'),
            "objetividad":data.get('objetividad'),
            "preguntas":data.get('preguntas'),
            "feedback":data.get('feedback'),
            "total":promedio
        },
        "chats":{                   ##### Aqui debes asignar todo el chat de con AI
            "user_id":data.get('user_id'),
            "estructura":[{"fase":"estructura","message":msg["message"]} for msg in history_chat],
            "competencias":[{"fase":"competencias","message":msg["message"]} for msg in history_chat],
            "comportamientos":[{"fase":"comportamientos","message":msg["message"]} for msg in history_chat],
            "objetividad":[{"fase":"objetividad","message":msg["message"]} for msg in history_chat],
            "preguntas":[{"fase":"preguntas","message":msg["message"]} for msg in history_chat],
            "feedback":[{"fase":"feedback","message":msg["message"]} for msg in history_chat],
        },
    }
    return new_Data
    
#


