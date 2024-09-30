import network 
import socket
import time
from machine import Pin 
import asyncio
led = Pin(15, Pin.OUT) 
onboard = Pin("LED", Pin.OUT, value=0)   
ssid = 'redpucp'  
password = 'C9AA28BA93'   
html = """<!DOCTYPE html>  <html>      <head> <title>Pico W</title> </head>      <body> <h1>Pico W</h1>          <p>%s</p>      </body>  </html>  """   
wlan = network.WLAN(network.STA_IF)  

def connect_to_network() :
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
async def serve_client(reader: asyncio.StreamReader, writer):
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
  writer.write('HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-type: text/html\r\n\r\n') 
  writer.write(response) 
  await writer.drain() 
  await writer.wait_closed() 
  print("Client disconnected") 

async def main():
  print('Connecting to Network...') 
  connect_to_network() 
  print('Setting up webserver...') 
  asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))  # type: ignore
  while True: 
    onboard.on() 
    await asyncio.sleep(0.25) 
    onboard.off() 
    await asyncio.sleep(0.8)

try:      
  asyncio.run(main()) 
finally: 
  asyncio.new_event_loop()