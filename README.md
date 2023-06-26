# Chat-Bot-Telegram-Karaoke-service

# Resumen del proyecto:
Un grupo de amigos en búsqueda de una nueva idea divertida para renovar nuestros encuentros se nos ocurrió la idea de crear un chatbot de Telegram que devuelve una pista para realizar un karaoke. Al iniciar el bot, este solicita el nombre de la canción, para devolver la letra de la canción y un video de youtube con la pista de la canción, para poder revitalizar tus encuentros con amigos y crear memorias y momentos únicos.
Somos un grupo de jóvenes interesados en crear un servicio para facilitarle la vida a alguien. Por eso creamos este proyecto que trata de un chatbot de Telegram que al iniciarlo te pide que ingreses el nombre de una canción. Con esa información el servicio te brinda la letra de la misma y un video de youtube con la pista para poder realizar un karaoke. 

# Objetivos:
- Facilitar la búsqueda de elementos para realizar un karaoke
- Proveer mediante un chatbot de telegram un servicio que al introducir el nombre de una canción devuelva la letra y la pista para realizar un karaoke. 

# Instrucciones para utilizar el bot:
- En el buscador de Telegram Buscar KaraokeChat_bot
- Apretar botón /start o escribirlo en el caso de que ya tengas una conversación previa con el chatbot. 
- Siguiendo las instrucciones escribis o clickeas /help
- Si deseas obtener la url correspondiente a la canción deseada en versión Karaoke debés escribir /youtube + la canción deseada.
- Si deseas obtener la letra de la canción clickeas o escribes /letras y el programa te solicitará primero el nombre de la canción y luego el artista y te devolverá la letra de la canción. 


# Buenas prácticas utilizadas: 
- Uso de minúsculas siempre para evitar errores 
- No compartir las Api Keys 
- Facilitar el uso de variables simplificandolas a términos cortos. Ej: 
  cancion = context.user_data['song'] 
  artist= context.user_data['artist']
- Llevar el replit/ el código con anotaciones y comentarios explicando cada paso.
- No utilizar abreviaciones en las variables
- Ir descargando el código como archivo main.py por seguridad. 
- Compartir nuestro proyecto en Github público para que otro lo pueda usar, aportar o ver. 
