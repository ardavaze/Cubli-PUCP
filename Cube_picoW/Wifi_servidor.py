import network 
import time
from machine import Pin 
import asyncio

onboard = Pin("LED", Pin.OUT, value=0)
serverQueue = asyncio.Queue()
POST : int = 0
GET : int = 1
VELOCIDAD: int = 0
ANGULO: int = 1
 
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
    print('connected') 
    status = wlan.ifconfig() 
    print('ip = ' + status[0])

async def serve_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
  print("Client connected") 
  method_line = await reader.readline() 
  print(method_line)
# We are not interested in HTTP request headers, skip them 
  while await reader.readline() != b"\r\n": 
    pass
  if method_line.decode('utf-8').startswith("POST"):
    request_line = await reader.readline()
    print(request_line)
  response = "1"
  writer.write(b'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-type: text/html\r\n\r\n') 
  writer.write(response.encode()) 
  await writer.drain() 
  await writer.wait_closed() 
  print("Client disconnected") 
