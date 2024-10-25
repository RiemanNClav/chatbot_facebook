
import qrcode
from PIL import Image

imagen = qrcode.make("https://www.google.com")

nombre_archivo = 'imagen_codigo.png'

imagen.save(nombre_archivo)

Image.open(nombre_archivo).show()