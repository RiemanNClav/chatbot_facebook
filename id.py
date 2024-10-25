import uuid

def crear_id_uuid(numero_telefono):
    # Convertir el número en una cadena
    numero_str = str(numero_telefono)
    
    # Crear un UUID basado en el número de teléfono
    id_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, numero_str)
    
    return id_uuid

# Ejemplo de uso
numero_telefono = "5551234567"
id_uuid = crear_id_uuid(numero_telefono)
print(f"UUID para el número {numero_telefono}: {id_uuid}")