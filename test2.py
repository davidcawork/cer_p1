from elasticsearch import Elasticsearch
import re, requests

# Iniciamos el cliente para hablar con la base de datos local
es = Elasticsearch([{'host':'localhost','port':9200}])



def getData():
    return re.compile('\d*\.?\d*<br>').findall(requests.get('https://www.numeroalazar.com.ar/').text)[0][:-4]

# Index settings
settings = {
        "numbers": {
            "properties": {
                "number": {
                    "type": "float",
                    "fielddata": "true"
                }
            }
        }
     }

# Create index
es.indices.create(index="test4", ignore=400, mappings=settings)

for i in range(1,10):
    res = es.index(index="test4", id=i, document= {'number': float(getData())})


for i in range(1,10):
    res = es.get(index="test4", id=i)
    print(str(res['_source']))


#res = es.get(index="test-index", id=1)
s = es.search(index="test4", aggs= {'avg_number':{'avg':{ 'field': 'number'}}})

print(str(s['aggregations']['avg_number']['value']))


