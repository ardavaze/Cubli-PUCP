from machine import Pin, PWM 
import uasyncio as asyncio
import Wifi_servidor
import motor

def encoder_handler(pin):
    global paso
    paso += 1
encoder=Pin(22, Pin.IN,Pin.PULL_UP)
encoder.irq(trigger=Pin.IRQ_FALLING,handler=encoder_handler)
encoder.irq(trigger=Pin.IRQ_RISING,handler=encoder_handler)

onboard = Pin("LED", Pin.OUT, value=0)

def controlMotor():
#configuraciones-------------------------------
  global paso, cambio, motor1, rpm_deseado, angulo_deseado, angulo, rpm, start, freno
  rpm_deseado = 0
  angulo_deseado = 0
  paso = 0
  cambio = False
  rpm = 0
  angulo = 0
  start =False
  freno = False
  #------------------------------------
  motor1 = motor.Motor("EjeX", 
                       motor.AM6807(machine.PWM(machine.Pin(1, machine.Pin.OUT),
                                                20000),
                                    machine.Pin(2, machine.Pin.OUT),
                                    machine.Pin(3, machine.Pin.OUT)))
  #datos---------------------------------
  pul_sub_baj_vuelta = 40 #subidas y bajadas de nivel por vuelta en el sensor
  tm_encoder = 100
  timerStart = utime.ticks_ms()
  while True:
    if cambio:
      if start and not freno:
        motor1.driver.set_velocity(rpm_deseado)
      else:
        motor1.driver.set_velocity(0)
      cambio = False

    time_elapsed = utime.ticks_diff(utime.ticks_ms(),timerStart)
    if time_elapsed >= tm_encoder:
      state = machine.disable_irq()
      rpm = paso*1000*60/(tm_encoder*pul_sub_baj_vuelta)
      paso = 0
      machine.enable_irq(state)
      timerStart = utime.ticks_ms()


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

def AnalizarRequest(request:str):
  global rpm_deseado, rpm, angulo_deseado, angulo, start, freno
  if '/set_' in request:
    req=request.split("/set_")[1].split(" ")[0]
    if req=="velocidad":
      rpm_deseado = int(request.split('velocidad=')[1].split('\'')[0])
      response = str(rpm_deseado)
    if req=="angulo":
      angulo_deseado = int(request.split('angulo=')[1].split('\'')[0])
      response = str(angulo_deseado)
    if req=="start":
      start = int(request.split('start=')[1].split('\'')[0])
      response = str(start)
    if req=="freno":
      freno = int(request.split('freno=')[1].split('\'')[0])
      response = str(freno)
    print(response)
  elif '/get_' in request:
    req=request.split("/get_")[1].split(" ")[0]
    if req=="velocidad":
      response = str(rpm)
    if req=="angulo":
      response = str(angulo_deseado)
  response="1"
  return response
