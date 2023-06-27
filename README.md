# Chat-Bot-Telegram-Karaoke-service

# Resumen del proyecto:
Somos un grupo de jóvenes interesados en crear un servicio para facilitarle la vida a alguien. Por eso creamos este proyecto que trata de un chatbot de Telegram con una nueva idea divertida para renovar nuestros encuentros. El bot te solicitará una canción para devolverte la pista de la canción versión karaoke. También se te solicitara el artista de la canción para devolverte la letra de la misma. Así podrás revitalizar tus encuentros con amigos y crear memorias y momentos únicos. 

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
