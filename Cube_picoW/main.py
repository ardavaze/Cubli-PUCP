from machine import Pin, PWM, disable_irq, enable_irq
import uasyncio as asyncio
import utime
import Wifi_servidor
import motor

paso = 0
def encoder_handler(pin):
    global paso
    paso += 1
encoder=Pin(22, Pin.IN,Pin.PULL_UP)
encoder.irq(trigger=Pin.IRQ_FALLING,handler=encoder_handler)
encoder.irq(trigger=Pin.IRQ_RISING,handler=encoder_handler)

onboard = Pin("LED", Pin.OUT, value=0)

async def main():
  #configuraciones-------------------------------

  #------------------------------------
  motor1 = motor.Motor("EjeX", 
                       motor.AM6807(PWM(Pin(1, Pin.OUT),
                                                20000),
                                    Pin(2, Pin.OUT),
                                    Pin(3, Pin.OUT)))
  #datos---------------------------------
  pul_sub_baj_vuelta = 40 #subidas y bajadas de nivel por vuelta en el sensor
  tm_encoder = 100
  timerStart = utime.ticks_ms()
  print('Connecting to Network...') 
  Wifi_servidor.connect_to_network('redpucp', 'C9AA28BA93') 
  print('Setting up webserver...') 
  asyncio.create_task(asyncio.start_server(Wifi_servidor.serve_client, "0.0.0.0", 80))  # type: ignore
  timerStart = utime.ticks_ms
  while True: 
    if Wifi_servidor.start and not Wifi_servidor.freno:
      motor1.driver.set_velocity(Wifi_servidor.rpm_deseado)
    else:
      motor1.driver.set_velocity(0)
    time_elapsed = utime.ticks_diff(utime.ticks_ms(),timerStart)
    state = disable_irq()
    Wifi_servidor.rpm = paso*1000*60/(tm_encoder*pul_sub_baj_vuelta)
    paso = 0
    enable_irq(state)
    timerStart = utime.ticks_ms()
    print(time_elapsed)
    await asyncio.sleep_ms(tm_encoder)
try:      
  asyncio.run(main()) 
finally: 
  asyncio.new_event_loop()
