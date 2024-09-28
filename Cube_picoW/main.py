import machine
import Wifi_servidor
import motor
import _thread

def encoder_handler(pin):
    global paso
    paso += 1

def controlMotor():
  global cambio, motor1, rpm_deseado,rpm
  rpm = 0
  while True:
    if cambio:
      if start:
        motor1.driver.set_velocity(rpm_deseado)
      else:
        motor1.driver.set_velocity(0)
      cambio = False
    
    
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
  
  return response

def main():
#configuraciones-------------------------------
  global paso, cambio, motor1, rpm_deseado, angulo_deseado
  rpm_deseado = 0
  angulo_deseado = 0
  paso = 0
  cambio = False
  #datos---------------------------------
  pul_sub_baj_vuelta = 40 #subidas y bajadas de nivel por vuelta en el sensor
  tm_encoder = 100
  #------------------------------------
  encoder = machine.Pin(22, machine.Pin.IN)
  encoder.irq(trigger=machine.Pin.IRQ_FALLING, handler=encoder_handler)
  encoder.irq(trigger=machine.Pin.IRQ_RISING, handler=encoder_handler)

  motor1 = motor.Motor(motor.TypeAxis.EjeX, 
                       motor.AM6807(machine.PWM(machine.Pin(1),
                                                1000),
                                        machine.Pin(2),
                                        machine.Pin(3)),
                       motor.Sensor())

  _thread.start_new_thread(controlMotor, ())
  Wifi_servidor.configWifi('CasaVZ','23060507')
  s=Wifi_servidor.crearSocket()
  while True:
    try:
      conn= Wifi_servidor.EsperaPeticion(s)
      request = Wifi_servidor.ObtenerRequest(conn)
      response = AnalizarRequest(request)
      cambio = True
      Wifi_servidor.CerrarPeticion(conn,response)
    except Exception as e:
      print(e)
      conn.close()         

main()
    