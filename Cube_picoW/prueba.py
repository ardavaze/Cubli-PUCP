import uasyncio as asyncio
import socket
import network
import time
# Configuración de la conexión Wi-Fi
ssid = 'CasaVZ'
password = '23060507'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Conectando a Wi-Fi...')
        time.sleep(1)
    
    print('Conexión establecida:', wlan.ifconfig())

async def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        print('Solicitud recibida:\n', request)

        response = 'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: text/plain\r\n\r\nHola, mundo!'
        client_socket.send(response.encode())
    except Exception as e:
        print('Error al manejar la conexión:', e)
    finally:
        client_socket.close()

async def main():
    connect_wifi()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        client_socket, _ = s.accept()
        print('Conexión aceptada.')
        asyncio.create_task(await handle_client(client_socket))  # Maneja la conexión en una tarea asíncrona

# Ejecuta el servidor
try:
    asyncio.run(main())
except Exception as e:
    print('Error en el servidor:', e)
