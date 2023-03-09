from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Clave de API de YouTube
api_key = 'AIzaSyCGDa0jMvkjc5kYb1J5Qt4Hli6OY19451k'

# ID de canal del usuario
channel_id = 'UCK3hRri53-7lg07cS4890cA'

# Crear objeto de servicio de la API de YouTube
youtube = build('youtube', 'v3', developerKey=api_key)

# Obtener las suscripciones del usuario
subscriptions_response = youtube.subscriptions().list(
    part='snippet',
    channelId=channel_id,
    maxResults=50
).execute()

# Obtener los canales a los que el usuario está suscrito
subscriptions = subscriptions_response['items']

# Categorías de contenido que te interesan
interesting_categories = [
    '/m/02jjt',  # Ciencia y tecnología
    '/m/01k8wb',  # Educación
    '/m/05fw6t',  # Viajes y eventos
]

# Clasificar las suscripciones según las etiquetas de categoría
for subscription in subscriptions:
    channel_name = subscription['snippet']['title']
    channel_id = subscription['snippet']['resourceId']['channelId']
    categories_response = youtube.channels().list(
        part='topicDetails',
        id=channel_id
    ).execute()
    categories = categories_response['items'][0]['topicDetails']['topicCategories']
    interesting_categories_found = [category for category in categories if category in interesting_categories]
    if interesting_categories_found:
        print(f'{channel_name} está clasificado en las siguientes categorías: {interesting_categories_found}')
    else:
        print(f'{channel_name} no está clasificado en ninguna de las categorías de contenido que te interesan.')
