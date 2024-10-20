from pydantic import BaseModel
from typing import Optional,List

class UserAuth(BaseModel):
    id:Optional[int] = None
    username:str
    password:str

class User(UserAuth):
    name:str
    perfil:str 
    
class UserEducation(User):
    user_id:int = 0
    estructura:float = 0
    competencias:float = 0
    comportamientos:float = 0
    objetividad:float = 0
    preguntas:float = 0
    feedback:float = 0
    total  :float = 0

