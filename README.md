# Backend SOFIA | Primera version para MVP
## Aqui implemento el backend utilizando Python y FastAPI para servir la aplicacion de Inteligencia Artificial para entrenamiento de analistas de seleccion para realizar entrevistas por competencias.
## Se usa LangChain para conectar la API de OpenAI y poder crear el chat con el usuario.
## La base de datos que se usa es relacional(PostgreSQL), para guardar datos de usuario, y los prompt de la IA, asi como las conversaciones y notas de cada usuario.  
## Gracias a la modularidad del framework y las llamadas asincronicas, se puede realizar peticiones HTTP de manera fluida sin interrupcion ademas de estas se usan WebSockets para el chat con la IA sin necesidad de cerrar la conexion con el servidor.
