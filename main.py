#!/usr/bin/env python3

from flask import Flask, render_template, redirect, request, session
from src.webscraper import WebScraper
import threading, time, re, requests, uuid

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

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
    return render_template('success.html', usr = 'Pepe')

@app.route("/exit")
def logout():
    """
        Página de salida de la app
    """
    if 'email' in session:
        session.clear()
    return render_template('exit.html')

@app.route("/login")
def login():
    """
        Página de entrada de la app
    """
    if 'email' in session:
        session.clear()
    return render_template('login.html')


# Thread B: Get  periodic data
def thread_getData():
    while True:
        print('Pido dataaaaaaaaaa')
        time.sleep(2)

# Main of our app
if __name__ == '__main__':
    
    # Let's initialize the threads
    t = threading.Thread(target=thread_getData, daemon=True)
    t.start()

    # Then, we have to start out flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

