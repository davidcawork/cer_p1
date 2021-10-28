#!/usr/bin/python3

from elasticsearch import Elasticsearch
import os

class ElastiClient(object):
    """
        Clase para gestionar la base de datos
    """
    def __init__(self, host = 'localhost', port = 9200, usr_table = 'users', num_table = 'numbers'):
        """
            Constructor de la clase
        """
        self.host = host
        self.port = port
        self.usr_table = usr_table
        self.num_table = num_table
        
    @staticmethod
    def checkElasticsearch():
        """
            Método para asegurarse que el servicio está corriendo
        """
        if 

