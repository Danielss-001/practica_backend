from fastapi import FastAPI,status
from routers import router_interview, router_user, router_evaluations
from ai.welcome_ai import message_context_welcome, chat, conversation_base_data,conversation_history
from fastapi.middleware.cors import CORSMiddleware 
from dotenv import load_dotenv
import os

load_dotenv('.env')
url_front = os.getenv('URL_FRONTEND')

app = FastAPI()
app.title = 'AIProject_API'

app.include_router(router_interview.router,tags=['interview'],prefix='/interview') # Incluir api de usuarios
app.include_router(router_user.router,tags=['user'],prefix='/user') # Incluimos el routr de usuario
app.include_router(router_evaluations.router,tags=['modules'],prefix='/modules')

#   ////////////////////////////////////////////
#   ////////////////////////////////////////////
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",url_front],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#   ////////////////////////////////////////////
#   ////////////////////////////////////////////


@app.get('/',tags=['home'],status_code=status.HTTP_200_OK)
async def root():
    #conversation_history.append(message_context_welcome) # Anexamos a local data chat AI
    #conversation_base_data.append(message_context_welcome.content) # Anexamos a local base de datos AI

    #response = chat.invoke(conversation_history)

    return {"message":"Bienvenido a SOFIA"}



# Local Host
#   http://127.0.0.1:8000/
