#!/usr/bin/env python3

from flask import Flask, render_template, redirect, request, session
from src.webscraper import WebScraper
from src.beebotteclient import BeebotteClient
from src.elasticlient import ElastiClient
import threading, time, re, requests, uuid, logging, hashlib

# Iniciamos los objs necesarios de Flask, Elasticsearch y Beebotte
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

elastic = ElastiClient('localhost', 9200)
beebot = BeebotteClient('qCZWxhok0QX7B8jM0AJ9KooM', 'cWRCglPqI6lUsMkkzMBk6tYdgt2cinR7')


# Thread A: Flask Operations
@app.route("/")
def index():
    """
        Página principal de la app
    """
    if 'mail' in session:
        return render_template('index.html', random_num = WebScraper.getRandomNumber(),  msg = session['user'] + 'is online!')
    return render_template('index.html', random_num = WebScraper.getRandomNumber())

@app.route("/register")
def register():
    """
        Página de registro de la app
    """
    if 'email' in session:
        session.clear()
    return render_template('register.html')


@app.route("/success", methods = ['POST'])
def success():
    """
        Página de registro exitoso de la app
    """
  
    session['email'] = request.form['email']
    session['user'] = request.form['name']
    session['pass'] = request.form['pass']
    session['peticiones'] = 0

    # Va mos a comprobar si el user o el mail ya existen 
    if elastic.getNumberOfUsersByEmail(session['email']) == 0 and  elastic.getNumberOfUsersByName(session['user']) == 0:
        
        # Vamos añadir al user a la base datos
        salt = uuid.uuid4().hex
        key = hashlib.sha256(salt.encode() + session['pass'].encode()).hexdigest() + ':' + salt

        elastic.storeUser({"username": session['user'], "mail": session['email'],"password": key,"peticiones":0})

        logging.debug('Ususario ' + session['user']+ 'registrado en la web!')
    else:
        return render_template('register.html', msg = 'Usuario registrado anteriormente, inicie sesion')

    return render_template('success.html', usr = session['user'])

@app.route("/exit")
def logout():
    """
        Página de salida de la app
    """
    if 'email' in session:
        session.clear()
    return render_template('exit.html')

@app.route("/login",  methods = ['POST'])
def login():
    """
        Página de entrada de la app
    """
    if 'email' in session:
        session.clear()
    mail = request.form['email']
    passw = request.form['pass']



    return render_template('login.html')


# Thread B: Get  periodic data
def thread_getData():
    while True:
        
        # Primero solocitamos un nuevo numero
        random_num = WebScraper.getRandomNumber()

        # Loggeamos que numero vamosa meter en ambas bases de datos
        logging.debug('Se va almacenar el numero: '+ str(random_num))

        # Guardamos en la base de datos local
        elastic.storeNumber(random_num)

        # Guardamos en la base de datos externa
        beebot.storeNumber(float(random_num))

        # Esperamos 2 mins
        time.sleep(120)

# Main of our app
if __name__ == '__main__':
    
    # Ponemos el nivel de log deseado 
    logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
    
    # Nos aseguramos que Elasticsearch y beebotte estan OK!
    elastic.checkElasticsearch()
    beebot.checkBeebotte()
    
    # Let's initialize the threads
    t = threading.Thread(target=thread_getData, daemon=True)
    t.start()

    # Then, we have to start out flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

