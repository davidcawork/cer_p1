import re, requests
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return re.compile('\d*\.?\d*<br>').findall(requests.get('https://www.numeroalazar.com.ar/').text)[0][:-4]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
