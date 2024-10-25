# from googleapiclient.discovery import build
# from google.oauth2 import service_account
# from googleapiclient.http import MediaIoBaseDownload
# import io



# SCOPES = ['https://www.googleapis.com/auth/drive.radonly']

# SERVICE_ACCOUNT_FILE = 'service_account.json'

# PARENT_FOLDER_ID = "1QP4a8P4Y01Xg3NvgY5XjUxAp-lnSFP9K"

# def authenticate():
#     creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#     return creds

# def upload_photo(file_path):
#     creds = authenticate()
#     service = build('drive', 'v3', credentials=creds)

#     file_metadata = {
#         'name' : "Demonstration",
#         'parents' : [PARENT_FOLDER_ID]
#     }

#     file = service.files().create(
#         body=file_metadata,
#         media_body=file_path
#     ).execute()




# # def download_file(file_id, destination):
# #     # Autenticarse y crear el servicio
# #     creds = authenticate()
# #     service = build('drive', 'v3', credentials=creds)
    
# #     # Obtener el archivo del Drive
# #     request = service.files().get_media(fileId=file_id)
    
# #     # Crear un buffer para el archivo descargado
# #     fh = io.FileIO(destination, 'wb')
    
# #     # Descargar el archivo
# #     downloader = MediaIoBaseDownload(fh, request)
# #     done = False
# #     while not done:
# #         status, done = downloader.next_chunk()
# #         print(f"Download {int(status.progress() * 100)}%.")
    
# #     print(f"File downloaded to {destination}")


# def get_file_mimetype(file_id):
#     creds = authenticate()
#     service = build('drive', 'v3', credentials=creds)
#     file = service.files().get(fileId=file_id, fields='mimeType').execute()
#     return file['mimeType']



#-----------------------------------------------------------------------------------------

import mysql.connector


def agregar_clientes(id, name, telefono, correo):
    id = id
    nombre = name
    telefono = telefono
    correo = correo
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Marmansanico12345$$",
        database="tory_cafe",
        port="3306")

    cursor = db.cursor()

    insert_query = "INSERT INTO clientes (id_cliente, nombre, telefono, correo) VALUES (%s, %s, %s, %s)"
    data = (id, nombre, telefono, correo)
    cursor.execute(insert_query, data)

    db.commit()
    db.close()


def run2():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Marmansanico12345$$",
            database="tory_cafe")

        cursor = db.cursor()

        select_query = "SELECT id_cliente, nombre, telefono, correo FROM clientes"
        cursor.execute(select_query)

        data = cursor.fetchall()
        db.close()

        if data:
            entries = "\n".join([f"(name: {row[0]}, email: {row[1]})" for row in data])
            response = f"Sure, these are the details of the database:\n{entries}"
        else:
            response = "The database is empty."

    except Exception as e:
        print("Error:", e)
    return []



if __name__=="__main__":

    run('Angel Uriel-10', "'Angel Clavellina", "5565637294", "angel.chave.clavellina@gmail.com")
