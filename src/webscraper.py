#!/usr/bin/python3


import re, requets

class WebScraper(object):
    """
        Clase para recolectar los datos de la página web
    """

    @staticmethod
    def getRandomNumber(self):
        """
            Método para obtener un numero aleatorio
        """
        return re.compile('\d*\.?\d*<br>').findall(requests.get('https://www.numeroalazar.com.ar/').text)[0][:-4]
