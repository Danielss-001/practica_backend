from fastapi import APIRouter, WebSocket, Depends, status, WebSocketDisconnect, HTTPException
from config.db import User_Chats, Update_chat_structure, Update_Structure_Calification,Update_chat_competencias, Update_competencias_Calification, Update_chat_comportamientos, Update_comportamientos_calificacion, Update_chat_objetividad, Update_objetividad_calificacion, Update_chat_preguntas, Update_preguntas_calificacion, Update_chat_feedback, Update_feedback_calificacion,Update_test_calificacion
from .router_user import CurrentUser
from ai.modules_ai import  chat, HumanMessage, Update_Name_to_Structure, Update_Name_to_Competencias, Update_Name_to_Comportamientos, Update_Name_to_Objetividad, Update_Name_to_Preguntas, Update_Name_to_Feedback, Test
import json


router = APIRouter()

user = {
    "calification": None,
    "name_user":None
}

interview_history_chat = []
conversation_base_data_chat = []

#   Enviamos data al backend AI :: name por medio de una Query
@router.get('/data_send/')
async def Send_Data_AI(name:str):
    """
        1. Paso uno: es enviar los datos del nombre a la IA | Enviaras por medio de una Query
    """
    user["name_user"] = name
    if user["name_user"] != None:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED)
    else:
        raise HTTPException(status_code=status.HTTP_510_NOT_EXTENDED)
    

#
#
#
#   Aqui estan los chats de los modulos 
#
#   Obtenemos los chats de modulo estructura si la funcion Send_data_AI le dice correcto al frontend de que fue actualizada la variable
@router.get('/chat_structure')
async def Structure_Get_Chat(id_user:int = Depends(CurrentUser)):
    """
        2. Paso dos: obtenemos el chat de la base de datos para usarlos 
    """
    try:
        
        # Obtenemos los chats
        data = User_Chats(id_user) # Cambiar la clave aqui y en el historial 

        # Verifica si no se encontraron datos
        if data is None or "estructura" not in data:
            raise HTTPException(status_code=404, detail="No chats found for user")
        
        chat_data = data["estructura"]
        
        global interview_history_chat
        global conversation_base_data_chat

        # Limpiamos los chat antes de asignar algo nuevo
        interview_history_chat.clear()
        conversation_base_data_chat.clear()
        
        # Asignamos nuevos valores a la lista de control de chats
        interview_history_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "estructura" and item["message"].get("fase") == "interview"]
        
        conversation_base_data_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "estructura" and item["message"].get("fase") == "interview"]
        
        #   Agregamos el prompt a la lista del historial
        interview_history_chat.append({"fase":"interview","message":Update_Name_to_Structure(user["name_user"])})
        conversation_base_data_chat.append({"fase":"interview","message":Update_Name_to_Structure(user["name_user"]).content})
     

    except:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Hay un eeror al conectar con la base de datos")
    
#   Metodo chats competencias
@router.get('/chat_competencias')
async def Competencias_Get_Chat(id_user:int = Depends(CurrentUser)):
    """
        2. Paso dos: obtenemos el chat de la base de datos para usarlos 
    """
    try:
        
        # Obtenemos los chats
        data = User_Chats(id_user) # Cambiar la clave aqui y en el historial 

        # Verifica si no se encontraron datos
        if data is None or "competencias" not in data:
            raise HTTPException(status_code=404, detail="No chats found for user")
        
        chat_data = data["competencias"]
        
        global interview_history_chat
        global conversation_base_data_chat

        # Limpiamos los chat antes de asignar algo nuevo
        interview_history_chat.clear()
        conversation_base_data_chat.clear()
        
        # Asignamos nuevos valores a la lista de control de chats
        interview_history_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "competencias" and item["message"].get("fase") == "interview"]
        
        conversation_base_data_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "competencias" and item["message"].get("fase") == "interview"]
        
        #   Agregamos el prompt a la lista del historial
        interview_history_chat.append({"fase":"interview","message":Update_Name_to_Competencias(user["name_user"])})
        conversation_base_data_chat.append({"fase":"interview","message":Update_Name_to_Competencias(user["name_user"]).content})
     

    except:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Hay un eeror al conectar con la base de datos")

#   Metodo chats comportamientos
@router.get('/chat_comportamientos')
async def Comportamientos_Get_Chat(id_user:int = Depends(CurrentUser)):
    """
        2. Paso dos: obtenemos el chat de la base de datos para usarlos 
    """
    try:
        
        # Obtenemos los chats
        data = User_Chats(id_user) # Cambiar la clave aqui y en el historial 

        # Verifica si no se encontraron datos
        if data is None or "comportamientos" not in data:
            raise HTTPException(status_code=404, detail="No chats found for user")
        
        chat_data = data["comportamientos"]
        
        global interview_history_chat
        global conversation_base_data_chat

        # Limpiamos los chat antes de asignar algo nuevo
        interview_history_chat.clear()
        conversation_base_data_chat.clear()
        
        # Asignamos nuevos valores a la lista de control de chats
        interview_history_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "comportamientos" and item["message"].get("fase") == "interview"]
        
        conversation_base_data_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "comportamientos" and item["message"].get("fase") == "interview"]
        
        #   Agregamos el prompt a la lista del historial
        interview_history_chat.append({"fase":"interview","message":Update_Name_to_Comportamientos(user["name_user"])})
        conversation_base_data_chat.append({"fase":"interview","message":Update_Name_to_Comportamientos(user["name_user"]).content})
     

    except:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Hay un eeror al conectar con la base de datos")
    

#   Metodo chats objetividad
@router.get('/chat_objetividad')
async def objetividad_Get_Chat(id_user:int = Depends(CurrentUser)):
    """
        2. Paso dos: obtenemos el chat de la base de datos para usarlos 
    """
    try:
        
        # Obtenemos los chats
        data = User_Chats(id_user) # Cambiar la clave aqui y en el historial 

        # Verifica si no se encontraron datos
        if data is None or "objetividad" not in data:
            raise HTTPException(status_code=404, detail="No chats found for user")
        
        chat_data = data["objetividad"]
        
        global interview_history_chat
        global conversation_base_data_chat

        # Limpiamos los chat antes de asignar algo nuevo
        interview_history_chat.clear()
        conversation_base_data_chat.clear()
        
        # Asignamos nuevos valores a la lista de control de chats
        interview_history_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "objetividad" and item["message"].get("fase") == "interview"]
        
        conversation_base_data_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "objetividad" and item["message"].get("fase") == "interview"]
        
        #   Agregamos el prompt a la lista del historial
        interview_history_chat.append({"fase":"interview","message":Update_Name_to_Objetividad(user["name_user"])})
        conversation_base_data_chat.append({"fase":"interview","message":Update_Name_to_Objetividad(user["name_user"]).content})
     

    except:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Hay un eeror al conectar con la base de datos")
    
#   Metodo chats preguntas
@router.get('/chat_preguntas')
async def Preguntas_Get_Chat(id_user:int = Depends(CurrentUser)):
    """
        2. Paso dos: obtenemos el chat de la base de datos para usarlos 
    """
    try:
        
        # Obtenemos los chats
        data = User_Chats(id_user) # Cambiar la clave aqui y en el historial 

        # Verifica si no se encontraron datos
        if data is None or "preguntas" not in data:
            raise HTTPException(status_code=404, detail="No chats found for user")
        
        chat_data = data["preguntas"]
        
        global interview_history_chat
        global conversation_base_data_chat

        # Limpiamos los chat antes de asignar algo nuevo
        interview_history_chat.clear()
        conversation_base_data_chat.clear()
        
        # Asignamos nuevos valores a la lista de control de chats
        interview_history_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "preguntas" and item["message"].get("fase") == "interview"]
        
        conversation_base_data_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "preguntas" and item["message"].get("fase") == "interview"]
        
        #   Agregamos el prompt a la lista del historial
        interview_history_chat.append({"fase":"interview","message":Update_Name_to_Preguntas(user["name_user"])})
        conversation_base_data_chat.append({"fase":"interview","message":Update_Name_to_Preguntas(user["name_user"]).content})
     

    except:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Hay un eeror al conectar con la base de datos")


#   Metodo chats feedback
@router.get('/chat_feedback')
async def Feedback_Get_Chat(id_user:int = Depends(CurrentUser)):
    """
        2. Paso dos: obtenemos el chat de la base de datos para usarlos 
    """
    try:
        
        # Obtenemos los chats
        data = User_Chats(id_user) # Cambiar la clave aqui y en el historial 

        # Verifica si no se encontraron datos
        if data is None or "feedback" not in data:
            raise HTTPException(status_code=404, detail="No chats found for user")
        
        chat_data = data["feedback"]
        
        global interview_history_chat
        global conversation_base_data_chat

        # Limpiamos los chat antes de asignar algo nuevo
        interview_history_chat.clear()
        conversation_base_data_chat.clear()
        
        # Asignamos nuevos valores a la lista de control de chats
        interview_history_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "feedback" and item["message"].get("fase") == "interview"]
        
        conversation_base_data_chat = [{"fase":"interview","message":item["message"].get("message")} for item in chat_data if item["fase"] == "feedback" and item["message"].get("fase") == "interview"]
        
        #   Agregamos el prompt a la lista del historial
        interview_history_chat.append({"fase":"interview","message":Update_Name_to_Feedback(user["name_user"])})
        conversation_base_data_chat.append({"fase":"interview","message":Update_Name_to_Feedback(user["name_user"]).content})
     

    except:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Hay un error al conectar con la base de datos")
    
#   Metodo chats test
@router.get('/chat_test')
async def Test_Get_Chat(id_user:int = Depends(CurrentUser)):
    """
        2. Paso dos: obtenemos el chat de la base de datos para usarlos 
    """
    try:
        
        global interview_history_chat
        global conversation_base_data_chat

        # Limpiamos los chat antes de asignar algo nuevo
        interview_history_chat.clear()
        conversation_base_data_chat.clear()
        
        #   Agregamos el prompt a la lista del historial
        interview_history_chat.append({"fase":"interview","message":Test(user["name_user"])})
        conversation_base_data_chat.append({"fase":"interview","message":Test(user["name_user"]).content})
     

    except:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Hay un eeror al conectar con la base de datos")
    










#
#
#
#
#   Aqui encontraras los metodos para actualizar base de datos
#   Solo se actualizara la base de datos una vez finalizada la conversacion
#

#   Estrucutra
#   Guardamos en base de datos la calificacion de estructura
@router.get('/structure_calification')
async def Structure_Base_Calification(id_user:int = Depends(CurrentUser)):
    Update_Structure_Calification(id_user=id_user,new_data=user["calification"]) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   Estrucutra
#   Guardamos la lista del chat de estructura
@router.get('/structure_base_chat')
async def Structure_Base_Chat(id_user:int = Depends(CurrentUser)):
    data = [{"fase":"estructura","message":{"fase":"interview","message":msg["message"]}} for msg in conversation_base_data_chat if msg["fase"]=="interview"]
    Update_chat_structure(id_user=id_user,new_data=data) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   competencias
#   Guardamos en base de datos la calificacion de estructura
@router.get('/competencias_calification')
async def Competencia_Base_Calification(id_user:int = Depends(CurrentUser)):
    Update_competencias_Calification(id_user=id_user,new_data=user["calification"]) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   competencias
#   Guardamos la lista del chat de estructura
@router.get('/competencias_base_chat')
async def Competencia_Base_Chat(id_user:int = Depends(CurrentUser)):
    data = [{"fase":"competencias","message":{"fase":"interview","message":msg["message"]}} for msg in conversation_base_data_chat if msg["fase"]=="interview"]
    Update_chat_competencias(id_user=id_user,new_data=data) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   comportamientos
#   Guardamos en base de datos la calificacion de estructura
@router.get('/comportamientos_calification')
async def comportamientos_Base_Calification(id_user:int = Depends(CurrentUser)):
    Update_comportamientos_calificacion(id_user=id_user,new_data=user["calification"]) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   comportamientos
#   Guardamos la lista del chat de estructura
@router.get('/comportamientos_base_chat')
async def comportamientos_Base_Chat(id_user:int = Depends(CurrentUser)):
    data = [{"fase":"comportamientos","message":{"fase":"interview","message":msg["message"]}} for msg in conversation_base_data_chat if msg["fase"]=="interview"]
    Update_chat_comportamientos(id_user=id_user,new_data=data) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   objetividad
#   Guardamos en base de datos la calificacion de estructura
@router.get('/objetividad_calification')
async def objetividad_Base_Calification(id_user:int = Depends(CurrentUser)):
    Update_objetividad_calificacion(id_user=id_user,new_data=user["calification"]) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   objetividad
#   Guardamos la lista del chat de estructura
@router.get('/objetividad_base_chat')
async def objetividad_Base_Chat(id_user:int = Depends(CurrentUser)):
    data = [{"fase":"objetividad","message":{"fase":"interview","message":msg["message"]}} for msg in conversation_base_data_chat if msg["fase"]=="interview"]
    Update_chat_objetividad(id_user=id_user,new_data=data) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)


#   preguntas
#   Guardamos en base de datos la calificacion de estructura
@router.get('/preguntas_calification')
async def preguntas_Base_Calification(id_user:int = Depends(CurrentUser)):
    Update_preguntas_calificacion(id_user=id_user,new_data=user["calification"]) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   preguntas
#   Guardamos la lista del chat de estructura
@router.get('/preguntas_base_chat')
async def preguntas_Base_Chat(id_user:int = Depends(CurrentUser)):
    data = [{"fase":"preguntas","message":{"fase":"interview","message":msg["message"]}} for msg in conversation_base_data_chat if msg["fase"]=="interview"]
    Update_chat_preguntas(id_user=id_user,new_data=data) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   feedback
#   Guardamos en base de datos la calificacion de estructura
@router.get('/feedback_calification')
async def feedback_Base_Calification(id_user:int = Depends(CurrentUser)):
    Update_feedback_calificacion(id_user=id_user,new_data=user["calification"]) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   feedback
#   Guardamos la lista del chat de estructura
@router.get('/feedback_base_chat')
async def feedback_Base_Chat(id_user:int = Depends(CurrentUser)):
    data = [{"fase":"feedback","message":{"fase":"interview","message":msg["message"]}} for msg in conversation_base_data_chat if msg["fase"]=="interview"]
    Update_chat_feedback(id_user=id_user,new_data=data) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

#   Test
#   Guardamos en base de datos la calificacion de estructura
@router.get('/test_calification')
async def test_Base_Calification(id_user:int = Depends(CurrentUser)):
    Update_test_calificacion(id_user=id_user,new_data=user["calification"]) # Llamamos al metodo de guardar y actualizar base de datos
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)

@router.get('/test_chat')
async def test_data_Chats_clear(id_user:int = Depends(CurrentUser)):
    global conversation_base_data_chat
    global interview_history_chat
    
    conversation_base_data_chat.clear()
    interview_history_chat.clear()

    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)



#
#
#
#   Aqui se encuentra la funcion principal para manejar los chat de los modulos reutilizando una funcion asincronica
#
#
#   Empezamos el seguimiento del modulo estructura
@router.websocket('/module_chat')
async def Module_Chat(websocket:WebSocket):
    """
        3. Paso tres: Conversaremos con el usuario acerca del pilar de Estructura y al finalizar obtendremos la calificacion y se cerrara el websocket
    """
    #   Iniciamos la variable 
    user["calification"] = None
    
    global interview_history_chat
    global conversation_base_data_chat

    invoke_chat = [msg["message"] for msg in interview_history_chat if msg["fase"]=='interview']
    
    await websocket.accept() # Aceptamos la conexion del websocket del frontend
    

    if not invoke_chat:
        await websocket.send_text("Error: No hay mensajes en el historial de la entrevista.")
        await websocket.close()
        return

    response_initial = chat.invoke(invoke_chat)
    await websocket.send_text(response_initial.content)

    try:
        while True:
            # Recibimos el mensaje del usuario
            user_message = await websocket.receive_text()
            message = HumanMessage(content=user_message)
            interview_history_chat.append({"fase":"interview","message":message}) # Actuaizamos el historial de IA
            conversation_base_data_chat.append({"fase":"interview","message":message.content}) # Actualizamos el historial de base de datos
            invoke_chat = [msg["message"] for msg in interview_history_chat if msg["fase"]=="interview"]
            response = chat.invoke(invoke_chat)

            try:
                response_data = json.loads(response.content) # Se intenta transformar la respuesta de la IA en json
                if "calificacion" in response_data:
                    # capturamos el json y cerramos la sesion
                    user["calification"]= response_data["calificacion"]
                    if user["calification"] != None:    
                        await websocket.send_text("Tu calificacion se actualizara pronto, vuelve cuando quieras...")

                        # Enviamos un status code al front para actualizar el boton en el front para actualizar la calificacion y guardar en bases de datos y salir de la pagina
                        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)
                        break
                
            except json.JSONDecodeError:
                #   Si no es un json valido enviamos la respuesta de la ia al websocket, continua la conversacion
                interview_history_chat.append({"fase":"interview","message":response})
                conversation_base_data_chat.append({"fase":"interview","message":response.content})
                await websocket.send_text(response.content)
    except WebSocketDisconnect:
        print("Cliente desconectado")


# Aqui esta el metodo para obtener la calificaion una ves se haya finalizado la conversacion
@router.get('/calification')
async def Get_Calification():
    """
        Obtenemos la calificacion una vez haya finalizado el websocket del chat esta da status_code 1000 al front par hacer la peticion 
    """
    if user["calification"] != None:
        # Guardamos y actualizamos base de datos
        return {"calification":user["calification"]}
    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
    