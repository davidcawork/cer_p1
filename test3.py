from beebotte import *
import time

_token      = 'token_w3yioZuIvRr4GrBb'
_hostname   = 'api.beebotte.com'

bbt = BBT(token = _token, hostname = _hostname)

# Escribir
for i in range(1,10):
    bbt.write('p1Cer', 'number', i)
    time.sleep(1)

# Leer
records = bbt.read('p1Cer', 'number', limit = 740)
print(str(records))
