
try:
  import usocket as socket
except Exception:
  import socket

from machine import Pin
import network
import gc

def configWifi(ssid :str,password :str):
  gc.collect()
  led = Pin("LED", Pin.OUT)
  led.off()
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  while not station.isconnected():
    pass
  print('Connection successful')
  print(station.ifconfig())
  led.on()

def crearSocket():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)
  return s

def EsperaPeticion(s : socket.socket):
  conn, addr = s.accept()
  #print('Got a connection from %s' % str(addr))
  return conn

def ObtenerRequest(conn: socket.socket):
  request = conn.recv(1024)
  request = str(request)
  return request

def CerrarPeticion(conn: socket.socket,response:str):
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Access-Control-Allow-Origin: *\r\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
