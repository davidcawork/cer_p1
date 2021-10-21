from elasticsearch import Elasticsearch
import re, requests

# Iniciamos el cliente para hablar con la base de datos local
es = Elasticsearch([{'host':'localhost','port':9200}])



def getData():
    return re.compile('\d*\.?\d*<br>').findall(requests.get('https://www.numeroalazar.com.ar/').text)[0][:-4]

for i in range(1,10):
    res = es.index(index="test", id=i, document= {'number': float(getData())})


#res = es.get(index="test-index", id=1)
res = es.search(index="test", aggs= {"avg_value": { "avg": { "field": "number" }}}, size = 0)

print(str(res['aggregations']['avg_grade']['number']))


