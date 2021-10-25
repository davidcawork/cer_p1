#!/usr/bin/env python3

from flask import Flask
import threading, time, re, requests

app = Flask(__name__)

# Thread A: Flask Operations
@app.route("/")
def hello():
    return re.compile('\d*\.?\d*<br>').findall(requests.get('https://www.numeroalazar.com.ar/').text)[0][:-4]

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

