import network 
import time
from machine import Pin 
import uasyncio as asyncio

onboard = Pin("LED", Pin.OUT, value=0)
POST : int = 0
GET : int = 1
VELOCIDAD: int = 0
ANGULO: int = 1

rpm_deseado = 0
angulo_deseado = 0
rpm = 0
angulo = 0
start =False
freno = False
 
def connect_to_network(ssid: str, password: str) :
  onboard.on()
  wlan = network.WLAN(network.STA_IF) 
  wlan.active(True) 
  wlan.config(pm = 0xa11140)  # Disable power-save mode 
  wlan.connect(ssid, password) 
  max_wait = 10 
  while max_wait > 0: 
    if wlan.status() < 0 or wlan.status() >= 3: 
      break 
    max_wait -= 1 
    print('waiting for connection...') 
    time.sleep(1)
  if wlan.status() != 3: 
    raise RuntimeError('network connection failed') 
  else: 
    status = wlan.ifconfig() 
    print('ip = ' + status[0])

async def serve_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
  print("Client connected")
# Leer la línea de solicitud
  request_line = await reader.readline()
  request_line = request_line.decode().strip()
  if request_line.startswith("POST"):
    # Leer los encabezados
    headers = []
    while True:
      header = await reader.readline()
      if header == b'\r\n':  # Fin de los encabezados
          break
      headers.append(header.decode().strip())
    content_length_header = [h for h in headers if h.startswith('Content-Length')]
    content_length = int(content_length_header[0].split(': ')[1]) if content_length_header else None
    if content_length is not None:
      body = await reader.readexactly(content_length)
      body=body.decode().strip()
      print(body)
    else:
      body= ''
    tipo_dato_request=request_line.split("/")[1].split(" ")[0]
    try:
      if tipo_dato_request=="velocidad":
        rpm_deseado=int(body)
      if tipo_dato_request=="angulo":
        angulo_deseado= int(body)
      if tipo_dato_request=="start":
        start = int(body)
      if tipo_dato_request=="freno":
        freno = int(body)
    except:
      print("Error en el dato recibido")
    response = "1".encode()
  else:
    while await reader.readline() != b'\r\n':
      pass
    body= ''  # No hay cuerpo para métodos como GET
    tipo_dato_request=request_line.split("/")[1].split(" ")[0]
    if tipo_dato_request=="velocidad":
      response = rpm.encode()
    if tipo_dato_request=="angulo":
      response = angulo.encode()
    
  writer.write('HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-type: text/html\r\n\r\n') 
  writer.write(response) 
  await writer.drain()  # type: ignore
  await writer.wait_closed()  # type: ignore
  print("Client disconnected")
