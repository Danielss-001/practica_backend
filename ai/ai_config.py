from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv('.env') # abrimos variable entorno
ai_key = os.getenv('AI_KEY') # llave de gpt-ai
chat=ChatOpenAI(model='gpt-3.5-turbo',temperature=0.7,api_key=ai_key) # Iniciamos chat

"""
# Convertimos mensaje en string
def MessageRecord(message:HumanMessage) -> str:
    msj = message.content
    return msj

# Convertimos mensaje en HumanMessage
def RestoredMessage(message:str) -> HumanMessage:
    msj = HumanMessage(content=message)
    return msj

# Convertimos mensaje a SystemMessage
def SysMessage(message:str) -> SystemMessage:
    msj = SystemMessage(content=message)
    return msj

# convertimos mensaje a string
def StrMessage(message:SystemMessage) -> str:
    msj = message.content
    return msj
"""
# Historial para base de datos
conversation_base_data = []

# Historial una vez se temine la creacion de usuario
conversation_history = []

# Historial de entrevista
interview_history = []