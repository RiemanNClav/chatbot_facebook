import gspread
import pandas as pd
import uuid


class GoogleSheet:
    def __init__(self,file_name,document,sheet_name):
        self.gc = gspread.service_account(filename=file_name)
        self.sh = self.gc.open(document)
        self.sheet = self.sh.worksheet(sheet_name)

    def read_data(self, range): #range = "A1:E1". Data devolvera un array de la fila 1 desde la columna A hasta la E
        data = self.sheet.get(range)
        return data

    def read_data_by_uid(self, uid):
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        print(df)
        filtered_data = df[df['uid'] == uid]
        return filtered_data #devuelve un data frame de una tabla, de dos filas siendo la primera las cabeceras de las columnas y la segunda los valores filtrados para acceder a un valor en concreto df["nombre"].to_string()
    
    def write_data(self, range, values): #range ej "A1:V1". values must be a list of list
        self.sheet.update(range, values)

    def write_data_by_uid(self, uid, values): 
        # Find the row index based on the UID
        cell = self.sheet.find(uid)
        row_index = cell.row
        # Update the row with the specified values
        self.sheet.update(f"A{row_index}:E{row_index}", values)

    def get_last_row_range(self):   
        last_row = len(self.sheet.get_all_values()) + 1
        deta = self.sheet.get_values()
        range_start = f"A{last_row}"
        range_end = f"{chr(ord('A') + len(deta[0]) - 1)}{last_row}"
        return f"{range_start}:{range_end}"
    
    def get_all_values(self):
        #self.sheet.get_all_values () # this return a list of list, so the get all records is easier to get values filtering
        return self.sheet.get_all_records() # thislar colum
    
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
            print(f"UID {id_registro_venta} no encontrado.")
        except KeyError:
            print(f"Columna '{column_name}' no encontrada.")
    

class InsertData:
    def __init__(self, file_name):
        self.file_name = file_name

    def convertir_telefono_id(self, numero_telefono):
        numero_str = str(numero_telefono)
        id_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, numero_str))
        return id_uuid

    def insert_data(self, telefono, token_sesion, numero_secreto, fecha_registro, hora_registro):
        clase = GoogleSheet('registro_venta/credentials-service-account.json', self.file_name, "Sheet1")

        id_registro_venta = str(numero_secreto) + "-" + telefono[-4:] + '-' + str(hora_registro).replace('.', '')
        id_cliente = self.convertir_telefono_id(telefono)

        values = [id_registro_venta, id_cliente, token_sesion, numero_secreto, 
                " ", telefono, " ", fecha_registro, 
                hora_registro, " ", 1, " ", " ", " ", " ", " "]
        
        value = [values]
        range = clase.get_last_row_range()
        clase.write_data(range, value)

        return id_registro_venta
        

if __name__=="__main__":
    clase = InsertData("registro_ventas")
    clase.insert_data("5565637294", "54345", "1006", "2024-10-01", 10.14)
    # value = [
    #     [
    #         "512-4662-2216",
    #         "f1c528fc-09e3-596f-8de4-3dd39edc93e4",
    #         "512",
    #         "Angel Prueba 3",
    #         "526968144662",
    #         "En desarrollo",
    #         "2024-10-21",
    #         22.16,
    #         None,
    #         1,
    #         None
    #     ]
    # ]
    # range = clase.get_last_row_range()  
    # clase.write_data(range, value)