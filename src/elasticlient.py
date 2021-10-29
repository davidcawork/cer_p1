#!/usr/bin/python3

from elasticsearch import Elasticsearch
import os, logging, requests

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
        
    def checkElasticsearch(self):
        """
            Método para asegurarse que el servicio está corriendo
        """

        # Si el servicio esta inactivo lo levantamos
        if os.system('systemctl is-active --quiet elasticsearch.service') != 0:
            logging.debug('Servicio elasticsearch.service inactivo... levantando')
            os.system('systemctl start elasticsearch.service')
        else:
            logging.debug('Servicio elasticsearch.service activo!')

        # Comprobamos que Elasticsearch esté corriendo en el puerto y en el host indicado
        if requests.get('http://' + self.host + ':' + str(self.port)).text is not None:
            logging.debug('Elasticsearch corriendo correctamente en ' + self.host + ':' + str(self.port))
        else:
            logging.error('No se ha encontrado el servicio de Elasticsearch corriendo en ' + self.host + ':' + str(self.port))
    

    def initDataTables(self):
        """
            Metodo para iniciar correctamente las tablas que se van a utilizar
        """
        # Vamos a empezar por la tabla de numeros rng
        if es.indices.exists(index=self.num_table):
            logging.debug('Se ha encontrado index ' + self.num_table +' creado... regenerando')
            es.indices.delete(index=self.num_table)
            



    

logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
ElastiClient('localhost', 9200).checkElasticsearch()