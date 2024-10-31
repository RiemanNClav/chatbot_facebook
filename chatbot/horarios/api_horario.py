import requests
from api_google_drive import GoogleDrive

api = GoogleDrive()
get_horario = api.action_get_horario()
acotar_ubicacion = api.action_acotar_ubicacion()

dicc = get_horario | acotar_ubicacion

# Define la URL del servicio `chatbot`
chatbot_url = "http://localhost:5001/receive_data"

# Envía los datos al endpoint
response = requests.post(chatbot_url, json={"response": dicc})

# Verifica la respuesta del servidor
if response.status_code == 200:
    print("Datos enviados exitosamente:", response.json())
else:
    print("Error al enviar datos:", response.status_code)