import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta


def fecha_actual():
    fecha = datetime.now()
    fecha_str = fecha.strftime("%Y-%m-%d")
             
    hora_str = str(fecha.strftime("%H:%M").replace(':', '.'))
    hora_float = float(hora_str)

    return hora_float

class RegistrosVentas:
    def __init__(self,document,sheet_name):
        self.file_name = 'registro_venta/credentials-service-account.json'
        self.gc = gspread.service_account(filename=self.file_name)
        self.sh = self.gc.open(document)
        self.sheet = self.sh.worksheet(sheet_name)

    def access(self):
        ruta_credenciales = self.file_name    
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        return ruta_credenciales, scopes
    
    def delete_row_by_uid(self, uid):
        try:
            # Buscar el UID en la hoja
            cell = self.sheet.find(uid)
            row_index = cell.row
            # Borrar la fila
            self.sheet.delete_rows(row_index)
            print(f"Fila con UID {uid} borrada exitosamente.")
        except gspread.exceptions.CellNotFound:
            print(f"UID {uid} no encontrado.")

    def update_cell_by_id(self, id_registro_venta, column_name, new_value):
        try:
            # Buscar la fila del UID
            data = self.sheet.get_all_records()
            df = pd.DataFrame(data)
            
            # Encontrar el índice de la columna
            col_index = df.columns.get_loc(column_name) + 1  # +1 porque las columnas empiezan desde 1 en Google Sheets

            # Buscar el UID en la hoja
            cell = self.sheet.find(id_registro_venta)
            row_index = cell.row

            # Actualizar el valor en la celda específica
            self.sheet.update_cell(row_index, col_index, new_value)
            print(f"Celda en la fila {row_index}, columna '{column_name}' actualizada a '{new_value}'.")
        except gspread.exceptions.CellNotFound:
            print(f"id {id_registro_venta} no encontrado.")
        except KeyError:
            print(f"Columna '{column_name}' no encontrada.")
    

    def confirmacion_registro_ventas(self, registro_ventas, id_registro_venta, telefono):
        ruta_credenciales, scopes = self.access()

        ##  CREDENCIALES
        credenciales = Credentials.from_service_account_file(ruta_credenciales, scopes=scopes)
        cliente = gspread.authorize(credenciales)

        ## CONFIRMACIÓN REGISTRO DE LA VENTA
        hoja1 = cliente.open(registro_ventas).sheet1
        hoja1 = hoja1.get_all_values()
        df = pd.DataFrame(hoja1[1:], columns=hoja1[0])

        df = df[ (df["telefono"] == telefono) & (df["id_registro_venta"] == id_registro_venta) ][["id_registro_venta", "numero_registro", "nombre", "telefono", "fecha_registro", "hora_registro"]]
        nombre = df['nombre'].iloc[0] if not df.empty else None
        id_registro_venta =  df['id_registro_venta'].iloc[0] if not df.empty else None

        print(nombre)

        return nombre, id_registro_venta
    


if __name__=="__main__":
    clase = RegistrosVentas("registro_ventas", "Sheet1")

    nombre, id_registro_venta = clase.confirmacion_registro_ventas("registro_ventas", '822', "521204375825")

    if nombre != None:
        clase.update_cell_by_id(id_registro_venta, "hora_confirmacion", fecha_actual())
        clase.update_cell_by_id(id_registro_venta, "status_confirmacion", 1)

