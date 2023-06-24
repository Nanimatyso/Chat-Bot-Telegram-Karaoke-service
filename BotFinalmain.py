import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode
import json
import traceback
import html
import googleapiclient.discovery  #google ya que es la api oficial de youtube y la key se obtiene por medio de google
import requests


logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO)

# defino el objeto para que me ayude a loggear lo que sucede con el bot
logger = logging.getLogger(__name__)


######MANEJO DE ERRORES######
# funcion que hace catch de los errores que se puede llegar a dar n el bot
# y los devuelve en la misma conversacion, ordenado para que podamos debuggear
async def error_handler(update: object,
                        context: ContextTypes.DEFAULT_TYPE) -> None:
  """Log the error and send a telegram message to notify the developer."""
  logger.error(msg="Exception while handling an update:",
               exc_info=context.error)
  tb_list = traceback.format_exception(None, context.error,
                                       context.error.__traceback__)
  tb_string = "".join(tb_list)
  update_str = update.to_dict() if isinstance(update, Update) else str(update)
  message = (
    f"An exception was raised while handling an update\n"
    f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
    "</pre>\n\n"
    f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
    f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
    f"<pre>{html.escape(tb_string)}</pre>")
  # Finally, send the message
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=message,
                                 parse_mode=ParseMode.HTML)


#############################################################

####DEFINO FUNCIONES####

# Comando de start del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.effective_user
  await update.message.reply_html(
    rf"Hola {user.mention_html()}!, escribe /help para ver las funciones del bot",
  )


#Comando de help donde detallo las opciones del bot
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="""
/help - mensaje de ayuda\n\
/youtube + canción que deseas buscar - Me dices una canción y te devuelvo la pista de karaoke sobre la que puedes cantar \n\
/letras - Me dirás la canción, luego el artista y te daré la letra de la canción. 
""")


#API Youtube (definición de mi api_key y argumentos que requiere la documentación)
api_service_name = "youtube"
api_version = "v3"
# API key
DEVELOPER_KEY = "AIzaSyBVcvf-gYcInkzBESLPpCkOwdsbt7crXw4"
# API client
youtube = googleapiclient.discovery.build(api_service_name,
                                          api_version,
                                          developerKey=DEVELOPER_KEY,
                                          static_discovery=False)

#Función para obtener url de Youtube
def get_karaoke(cancion):
  query = cancion + " Karaoke" #busca la versión karaoke de la cancion ingresada
  request = youtube.search().list(part="id",
                                  type='video',
                                  regionCode="US",
                                  order="relevance",
                                  q=query,
                                  maxResults=5,
                                  fields="items(id(videoId))")
  response = request.execute()

  video_id = response['items'][0]['id']['videoId']

  url = f"https://www.youtube.com/watch?v={video_id}" #Union de url base con ID
  return url


#Función comando Youtube en el bot
async def search_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
  song = ' '.join(context.args)  #Lo que escriba el usuario al lado de /youtube
  response = get_karaoke(song) #Ejecución de la función fuera del bot
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=response) #Bot devuelve el response (url)

###################################################################################

#api_key de Musixmatch lyrics
musixmatch_apikey = "4ebe29117cd088bb2a108bffa684aab2"

#Función fuera del bot para obtener la letra de la canción según el ID encontrado
def get_lyrics(track_id):
  # Conectarse al servicio de la API para obtener las letras de la canción
  response = requests.get(
    f'http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey={musixmatch_apikey}&track_id={track_id}'
  )
  results = response.json()

  # Verificar si se encontraron resultados
  if results['message']['header']['status_code'] == 200:
    lyrics = results['message']['body']['lyrics']['lyrics_body']
    return (lyrics)
  else:
    return ("No se encontraron letras para esta canción.")

#Función fuera del bot para recibir mensajes del usuario y devolverle lo escrito
def receive_text(update, context):
  text = update.message.text
  return text
  
# comando que hace start de /letras
async def letras(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # user = update.effective_user
  context.user_data['step'] = 'song' #se establece primer step es = song
  await update.message.reply_html(
    'Ingrese el nombre de la canción:') #Pedido de ingreso de la canción

#Función donde se termina de obtener variable Cancion y Artista, se ejecuta una request a la api de Musixmatch y devuelve la letra de la canción ingresada usando la funciones previamente definidas.
async def search_lyrics(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if context.user_data.get("step") == "song":   #si step es = a song (que lo es)
    cancion = update.message.text            #escucho todo cuando se ejecuta /letras y lo meto en variable "song" 
    context.user_data['song'] = cancion
    await update.message.reply_html('Ingrese el nombre del artista:') #Pregunto artista
    # await update.message.reply_text(context.user_data['song']) #era para comprobar
    context.user_data['step'] = "artist" #Cambio el step a = artist
    return #Return corta
  if context.user_data.get("step") == "artist":  #si step es = a artist (que lo es)
    artist = update.message.text                #escucho todo cuando se ejecuta /letras y lo meto en variable "artist" 
    context.user_data['artist'] = artist
    await update.message.reply_text(f"La canción {context.user_data['song']} de {context.user_data['artist']}") #Prueba de que tengo en cada variable.
    cancion = context.user_data['song'] #Buenas practicas
    artist= context.user_data['artist'] #Buenas practicas
    #Hago el request
    response = requests.get(
    f'http://api.musixmatch.com/ws/1.1/track.search?apikey={musixmatch_apikey}&q_track={cancion}&q_artist={artist}&s_track_rating=desc&page=1&page_size=3'
  )
    results = response.json()
  # Verificar si se encontraron resultados
    if results['message']['header']['available'] > 0:
      track_id = results['message']['body']['track_list'][0]['track']['track_id']
      lyrics = get_lyrics(track_id)
      await update.message.reply_text(lyrics)
    else:
      await update.message.reply_text("No se encontraron resultados.")


#Creo el bot y sus handles
if __name__ == '__main__':
  application = ApplicationBuilder().token(
    '6014908534:AAFnVWfibyBhV3Ij8qGTu9e8yfeuEJj4sb8').build()
  #debes agregar pass_args=True para habilitar la captura de argumentos en los comandos:
  # creo los handlers
  start_handler = CommandHandler('start', start)
  help_handler = CommandHandler('help', help)
  youtube_handler = CommandHandler('youtube', search_youtube)
  lyrics_handler = CommandHandler('letras', letras)
  search_lyrics_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND),
                                           search_lyrics)
  
  #message handler escucha todo lo que digas al ejecutar search lyrics

  # le agrego los handlers al bot
  application.add_handler(start_handler)
  application.add_handler(help_handler)
  application.add_handler(youtube_handler)
  application.add_handler(lyrics_handler)
  application.add_handler(search_lyrics_message_handler)
  

  # le agrego un handler de error al bot que estoy importando
  application.add_error_handler(error_handler)

  application.run_polling()
