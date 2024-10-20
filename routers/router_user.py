from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from schemes.user import UserAuth,UserEducation
from jose import jwt, JWSError
from passlib.context import CryptContext
from config.db import VerifyUsername, User_name,User_data, Id_User, User_Califications, User_Chats
from dotenv import load_dotenv
import os


router = APIRouter()
crypt = CryptContext(schemes=['bcrypt']) # verificar el encriptado de contraseñas
oauth2 = OAuth2PasswordBearer('/login') # Obtenemos token JWT con el "type_token"

load_dotenv('.env')
algorithm = "HS256" # Algoritmo de encriptado
secret_key = os.getenv('SECRET_KEY_BACK') # Secret key para encryptar -hex 32 || PAG: https://codebeautify.org/generate-random-hexadecimal-numbers

# Autenticacion
# obtenemos el ID del usuario autenticado actualmente
# Utilizamos el ID para acceder a los datos de base de datos
async def CurrentUser(token:str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try :
        username = jwt.decode(token=token,key=secret_key,algorithms=[algorithm]).get('username')
        if username is None:
                raise exception
    except JWSError:
         return exception
    
    id = Id_User(username=username)
    return id
    

#//////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////
# Inicio de sesion
@router.post("/login")
async def Login(user:UserAuth):
    user = dict(user)
    if not VerifyUsername(user['username']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='El usuario no existe')
    
    id = Id_User(user['username']) 
    user_auth = User_data(id) # retorna el usuario 

    if not crypt.verify(user['password'],user_auth['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Contraseña incorrecta')
    
    token = {"username":user_auth['username'],"password":user_auth['password']}

    return {"access_token": jwt.encode(claims=token,key=secret_key,algorithm=algorithm),"token_type":"bearer"} # Retoma el token para acceso a base de datos

#    ___________________________________
#   |   _______     _____   _    __    |
#   |  |  __   |   / _   | | |  |  |   |
#   |  | |  |  |  / / |  | | |  |  |   |  
#   |  | |__|  | / /  |  | | |__|  |   |
#   |  |_______|/_/   |__| |_______|   |
#   |__________________________________|
#   .Obtenemos data completa de cursos ('/deshboard')
@router.get('/dashboard/califications')
async def Data_califications_User(id_user:int = Depends(CurrentUser)):
    """
        Una vez autenticado el usuario podra acceder al listado de sus calificaciones
    """
    data_user = User_name(id_user)  # Obtenemos username y name del usuario
    califications = User_Califications(id_user) # Obtenemos las calificaciones 

    data = data_user | califications

    return  data

@router.get('/dashboard/chats')
async def Data_Chats_User(id_user:int = Depends(CurrentUser)):
     """
        Una vez autenticado el usuario podra acceder al listado de los chats de AI
     """
     chats = User_Chats(id_user) # Obtenemos los chats
     return chats
    
#
#
#
#
#
#
#
#
#
#
