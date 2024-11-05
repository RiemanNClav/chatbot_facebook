import requests
from geopy.geocoders import Nominatim
import time
from datetime import datetime
import pandas as pd
import os
import math


 
class ApiAddress():
    def __init__(self):
        self.app = Nominatim(user_agent="tutorial")
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.path_colonias = os.path.join(self.base_dir, 'notebook', 'data', 'colonias_final.csv')
        self.path_alcaldias = os.path.join(self.base_dir, 'notebook', 'data', 'alcaldias_final.csv')



    # def categoria_mas_parecida(self, cadena, lista_categorias):
    #     categoria_parecida = None
    #     distancia_minima = float('inf')
        
    #     for categoria in lista_categorias:
    #         distancia = Levenshtein.distance(cadena, categoria)
            
    #         if distancia < distancia_minima:
    #             distancia_minima = distancia
    #             categoria_parecida = categoria
                
    #     return categoria_parecida
    
    ## ALCALDIA Y COLONIA
    def get_location_by_address(self, address):
        """This function returns a location as raw from an address
        will repeat until success"""
        time.sleep(1)
        try:
            return self.app.geocode(address).raw
        except:
            return 'NO SE ENCONTRO'


    def get_address_by_location(self, latitude, longitude, language="es"):
        """This function returns an address as raw from a location
        will repeat until success"""
        # build coordinates string to pass to reverse() function
        coordinates = f"{latitude}, {longitude}"
        # sleep for a second to respect Usage Policy
        time.sleep(1)
        try:
            return self.app.reverse(coordinates, language=language).raw
        except:
            return 'NO SE ENCONTRO'
        
        
    def get_day_month(self):
        meses = {1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4:'ABRIL',
                5: 'MAYO', 6: 'JUNIO', 7: 'JULIO', 8: 'AGOSTO',
                9: 'SEPTIEMBRE', 10: 'OCTUBRE', 11: 'NOVIEMBRE',
                12: 'DICIEMBRE'}
        
        dia, mes = datetime.now().day, datetime.now().month
        return dia, meses[mes]
    
    
    def api_request_object_1(self, latitud, longitud):


        address = self.get_address_by_location(latitud, longitud)
        alcaldia = address['address']['borough'].upper()
        #alcaldia_inal = self.categoria_mas_parecida(alcaldia, alcaldias)
        colonia = address['address']['neighbourhood'].upper()
        #colonia_final = self.categoria_mas_parecida(colonia, colonias)
        dia, mes = self.get_day_month()


        return alcaldia, colonia, dia, mes
    

    def api_request_object_2(self, complete_address):


        #colonia_final = self.categoria_mas_parecida(colonia, colonias)

        #alcaldia_final = self.categoria_mas_parecida(alcaldia, alcaldias)

        #complete_address= alcaldia + ', ' + colonia + "," + calle
        address = self.get_location_by_address(complete_address)

        latitud = address["lat"]
        longitud = address['lon']
        dia, mes = self.get_day_month()


        return latitud, longitud, dia, mes

    def haversine(self, lat2, lon2, lat1=19.4891421, lon1=-99.153497):
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        distance = R * c
        return distance
        
    def bola_cerrada(self, direccion, radio=100):
        # direccion = direccion.split(',')
        # alcaldia = direccion[0]
        # colonia = direccion[1]
        # calle = direccion[2]
        latitud, longitud, dia, mes = self.api_request_object_2(direccion)
        distancia = self.haversine(float(latitud), float(longitud))

        if distancia <= radio:
            result = 1
        else:
            result = 0

        return result, radio, distancia



if __name__=="__main__":
    # # define your coordinates

    api = ApiAddress()
    
    # # latitude =   19.38065
    # # longitude = -99.18487
    # # address = api.ApiRequestObject(latitude, longitude)
    # # alcaldia, colonia, dia, mes = address

    # # print(f"Alcaldia final: {alcaldia}")
    # # print(f"Colonia final: {colonia} ")
    # # print(f"Dia: {dia} ")
    # # print(f"Mes: {mes} ")

    address = "AZCAPOTZALCO, SANTA CRUZ DE LAS SALINAS, AVENIDA PONIENTE 128 505"

    result, radio, distancia = api.bola_cerrada("Tlalpan, Fuentes Brotantes, Camino a Santa Teresa 1234")
    print(result)

    # location = api.get_location_by_address(address)
    # latitude = location["lat"]
    # longitude = location["lon"]
    # print(f"{latitude}, {longitude}")
    # print('\n')
    # # print all returned data
    # print(location)