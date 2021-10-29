#!/usr/bin/python3

from elasticsearch import Elasticsearch
import os, logging, requests, uuid, time

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
        self.es = Elasticsearch([{'host': self.host, 'port': self.port}])
        
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

        #settings_num_table = {"properties": {"number": {"type": "float", "fielddata": "true"}}}
        
        settings = {
            "numbers": {
                "properties": {
                    "number": {
                        "type": "float"
                    }
                }
            }
        }        

        # Vamos a empezar por la tabla de numeros rng
        if self.es.indices.exists(index=self.num_table):
            logging.debug('Se ha encontrado index ' + self.num_table +' creado... regenerando')
            
            # Primero eliminamos
            self.es.indices.delete(index=self.num_table)

            # Despues regeneramos la tabla 
            self.es.indices.create(index= self.num_table, ignore=400, mappings = settings)

        else:
            # Si no existe la creamos y ya
            logging.debug('Generando index ' + self.num_table + ' ...')
            self.es.indices.create(index= self.num_table, ignore=400, mappings = settings)


        # Ahora vamos a ver si existe la base de datos del ususario 
        if self.es.indices.exists(index=self.usr_table):
            logging.debug('Se ha encontrado index ' + self.usr_table +' creado... regenerando')

            # Primero eliminamos
            self.es.indices.delete(index=self.usr_table)

            # Despues regeneramos la tabla
            self.es.indices.create(index= self.usr_table)
        
        else:
            # Si no existe la creamos y ya
            logging.debug('Generando index ' + self.usr_table + ' ...')
            self.es.indices.create(index= self.usr_table)
            
            
    def storeNumber(self, data):
        """
            Metodo para añadir datos a la base de datos
        """
        self.es.index(index = self.num_table, id = uuid.uuid4().int, document= {'number': float(data)})        


    def getMean(self):
        """
            Metodo para obtener la media de la base de datos
        """
        return self.es.search(index= self.num_table, aggs= {'avg_number':{'avg':{ 'field': 'number'}}})

        

    def getNumberByID(self, _id):
        """
            Metodo para conseguir un numero de la base de datos por ID
        """
        return self.es.get(index =  self.num_table, id = _id)
        

    def storeUser(self, _usr):
        """
            Metodo para añadir un usuario a la base de datos 
        """
        self.es.index(index = self.usr_table, id = uuid.uuid4().int, document = _usr)


    def getNumberOfUsersByEmail(self, email):
        """
            Metodo para obtener el numero de ususarios con un email dado
        """
        return self.es.search(index = self.usr_table, query = {'match': { 'mail': email}})['hits']['total']['value']


    def getNumberOfUsersByName(self, name):
        """
            Metodo para obtener el numero de ususarios con un nombre dado
        """
        return self.es.search(index = self.usr_table, query = {'match': { 'username': name}})['hits']['total']['value']


    def getIDByUsername(self, name):
        """
            Metodo para obtener el ID asociado a un usuario por su nombre
        """
        return self.es.search(index = self.usr_table, query = {'match': { 'username': name}})['hits']['hits'][0]['_id']


    def getUserByID(self, _id):
        """
            Obtenemos un usuario por ID
        """
        return self.es.get(index = self.usr_table, id = _id)


    def updatePets(self, _id, _pet):
        """
            Metodo para actualziar las peticiones de un ususario 
        """
        
        # Primero sacamos la info del user 
        usr_data = self.getUserByID(_id)
        
        # Hacemos el update delos datos
        new_usr_data = usr_data['_source']
        new_usr_data['peticiones'] = new_usr_data['peticiones'] + _pet

        # Actualizamos al ususario
        self.es.index(index = self.usr_table, id = _id, document = new_usr_data)


    def getSearch(self, _index):
        """
            Metodo para realizar una busqueda en la base de datos por index 
        """
        return self.es.search(index= _index)



logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
test = ElastiClient('localhost', 9200)
test.checkElasticsearch()
test.initDataTables()

for i in range(1,10):
    test.storeNumber(i)

time.sleep(2)
test.getMean()
test.storeUser({"username": "karrax", "mail": "davidcawork@gmail.com","password": "asdlkjasoñdhnoñas","peticiones":0})
time.sleep(2)
test.getNumberOfUsersByEmail('davidcawork@gmail.com')
id_ = test.getIDByUsername('karrax')
print(str(id_))
test.updatePets(id_, 2)
test.getUserByID(id_)
