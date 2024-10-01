from machine import Pin, PWM 
import asyncio
import Wifi_servidor

onboard = Pin("LED", Pin.OUT, value=0)

async def main():
  print('Connecting to Network...') 
  Wifi_servidor.connect_to_network('redpucp', 'C9AA28BA93') 
  print('Setting up webserver...') 
  asyncio.create_task(asyncio.start_server(Wifi_servidor.serve_client, "0.0.0.0", 80))  # type: ignore
  while True: 
    onboard.on() 
    await asyncio.sleep(0.25) 
    onboard.off() 
    await asyncio.sleep(0.8)
try:      
  asyncio.run(main()) 
finally: 
  asyncio.new_event_loop()