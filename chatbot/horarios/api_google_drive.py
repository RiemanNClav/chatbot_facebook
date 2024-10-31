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

# def download_file(file_id, destination):
#     # Autenticarse y crear el servicio
#     creds = authenticate()
#     service = build('drive', 'v3', credentials=creds)
    
#     # Obtener el archivo del Drive
#     request = service.files().get_media(fileId=file_id)
    
#     # Crear un buffer para el archivo descargado
#     fh = io.FileIO(destination, 'wb')
    
#     # Descargar el archivo
#     downloader = MediaIoBaseDownload(fh, request)
#     done = False
#     while not done:
#         status, done = downloader.next_chunk()
#         print(f"Download {int(status.progress() * 100)}%.")
    
#     print(f"File downloaded to {destination}")


import gspread
from google.oauth2.service_account import Credentials

from horario import Horarios

class GoogleDrive():
    def __init__(self):
        pass

    def access(self):
        ruta_credenciales = "credentials-service-account.json"  # Reemplaza con la ruta a tu archivo JSON de credenciales    
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        return ruta_credenciales, scopes


    def obtener_datos_sheet(self, horario_habitual_hoja, horario_particular_hoja):
        ruta_credenciales, scopes = self.access()

        ##  CREDENCIALES
        credenciales = Credentials.from_service_account_file(ruta_credenciales, scopes=scopes)
        cliente = gspread.authorize(credenciales)

        ## HORARIO HABITUAL
        hoja1 = cliente.open(horario_habitual_hoja).sheet1
        diccionario1 = dict((hoja1.get_all_values()[1:]))

        ## HORARIO PARTICULAR
        hoja2 = cliente.open(horario_particular_hoja).sheet1
        diccionario2 = dict(hoja2.get_all_values()[1:])
        diccionario2 = list(diccionario2.values())

        return diccionario1, diccionario2
    
    def action_acotar_ubicacion(self):
        horario_habitual, horario_particular = self.obtener_datos_sheet("horarios", "horario_particular")
        obj = Horarios()
        dicc = obj.horario(horario_habitual, horario_particular)

        print(dicc)
        return dicc

    def action_get_horario(self):
        horario_habitual, horario_particular = self.obtener_datos_sheet("horarios", "horario_particular")
        obj = Horarios()
        dicc, _, _ = obj.print_horario(horario_habitual, horario_particular)

        print(dicc)
        return dicc
    
if __name__=="__main__":
    clase = GoogleDrive()
    clase.action_acotar_ubicacion()
    clase.action_get_horario()
    
    # def acotar_ubicacion(self):

    #     obj = Horarios()

    #     disponiblidad, botton = obj.horario()


    #     if botton == 1:
    #         disponiblidad += "Perfecto, gracias por tu confianza\n"
    #         disponiblidad += "\n"
    #         disponiblidad += "Antes de comenzar con tu pedido, queremos validar tu dirección, ingresala manualmente:\n"
    #         disponiblidad += "Ej-> alcaldia, colonia, calle"

    #     dispatcher.utter_message(text=disponiblidad)

    #     return [] 

# # Rutas y variables
# ruta_credenciales = "credentials-service-account.json"  # Reemplaza con la ruta a tu archivo JSON de credenciales
# nombre_hoja = "horarios"  # Nombre del archivo de Google Sheets
# nombre_hoja_local = "horarios_prueba.csv"  # Nombre con el que deseas guardar el archivo

# # Autenticación y acceso al archivo
# scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# credenciales = Credentials.from_service_account_file(ruta_credenciales, scopes=scopes)
# cliente = gspread.authorize(credenciales)

# # Abre el archivo de Google Sheets y selecciona la primera hoja
# hoja = cliente.open(nombre_hoja).sheet1

# # Obtén todos los datos de la hoja y guárdalos en un archivo CSV
# with open(nombre_hoja_local, "w", encoding="utf-8") as archivo:
#     for fila in hoja.get_all_values():
#         archivo.write(",".join(fila) + "\n")
# # 
# print(f"Archivo guardado como {nombre_hoja_local}")

# # import gspread
# # import pandas as pd

# class GoogleSheet:
#     def __init__(self,file_name,document,sheet_name):
#         self.gc = gspread.service_account(filename=file_name)
#         self.sh = self.gc.open(document)
#         self.sheet = self.sh.worksheet(sheet_name)

#     def read_data(self, range): #range = "A1:E1". Data devolvera un array de la fila 1 desde la columna A hasta la E
#         data = self.sheet.get(range)
#         return data

#     def read_data_by_uid(self, uid):
#         data = self.sheet.get_all_records()
#         df = pd.DataFrame(data)
#         print(df)
#         filtered_data = df[df['uid'] == uid]
#         return filtered_data #devuelve un data frame de una tabla, de dos filas siendo la primera las cabeceras de las columnas y la segunda los valores filtrados para acceder a un valor en concreto df["nombre"].to_string()
    
#     def write_data(self, range, values): #range ej "A1:V1". values must be a list of list
#         self.sheet.update(range, values)

#     def write_data_by_uid(self, uid, values): 
#         # Find the row index based on the UID
#         cell = self.sheet.find(uid)
#         row_index = cell.row
#         # Update the row with the specified values
#         self.sheet.update(f"A{row_index}:E{row_index}", values)

#     def get_last_row_range(self):   
#         last_row = len(self.sheet.get_all_values()) + 1
#         deta = self.sheet.get_values()
#         range_start = f"A{last_row}"
#         range_end = f"{chr(ord('A') + len(deta[0]) - 1)}{last_row}"
#         return f"{range_start}:{range_end}"
    
#     def get_all_values(self):
#         #self.sheet.get_all_values () # this return a list of list, so the get all records is easier to get values filtering
#         return self.sheet.get_all_records() # this return a list of dictioraies so the key is the name column and the value is the value for that particular column


# if __name__=="__main__":
