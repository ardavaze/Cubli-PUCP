import machine
import utime
import time
import Wifi_servidor
import _thread

def encoder_handler(pin):
    global paso
    paso += 1

def set_duty(timer):
    global acc, dec, bandera, duty, div_duty, contador2,paso,bandera2,rpm,rpm_ant,rpm_deseado,pul_sub_baj_vuelta,tiempo, start
    if start:
      if freno:
          acc_valor = 0; dec_valor = 0
      else:
          acc_valor = 65535; dec_valor = 65535
          if bandera == 0:
              if duty>0:
                  dec_valor = 65535-duty #acelera
              else:
                  acc_valor = 65535+duty  #desacelera
              bandera+=1
          elif bandera == div_duty-1 :
              bandera = 0
          else:
              bandera += 1
      acc.duty_u16(acc_valor); dec.duty_u16(dec_valor)
      if contador2==149:
          contador2=0
          rpm = paso*1000*60/(tm_encoder*pul_sub_baj_vuelta)
          rpm_deseado = max(0, rpm_deseado); rpm_deseado = min(4000, rpm_deseado)
          if (rpm_deseado-rpm)>290 :
              duty=int(((rpm_deseado-rpm)-228.8)/1.38)
          else:
              duty=int(((rpm_deseado-rpm)-9.736)/8)
          if rpm==0: 
              if rpm_ant==0 and bandera2==0 :
                  duty=2200
                  bandera2=1
          else:
              bandera2=0
          tiempo += tm_encoder
          paso = 0; bandera=0; rpm_ant=rpm
      else:
          contador2+=1
    else:
       paso=0;acc.duty_u16(0); dec.duty_u16(0)


def AnalizarRequest(request:str):
  global rpm_deseado, rpm, angulo_deseado,angulo, start,freno
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
      response = str(rpm_deseado)
    if req=="angulo":
      response = str(angulo)
  
  return response

def main():
#configuraciones-------------------------------
    global div_duty, duty, paso, contador2,tm_encoder,bandera2,rpm_ant,tiempo,rpm_deseado,rpm \
    ,acc, dec, bandera, freno,pul_sub_baj_vuelta, tiempo, angulo_deseado,angulo,start
    #datos---------------------------------
    pul_sub_baj_vuelta = 40 #subidas y bajadas de nivel por vuelta en el sensor
    div_duty = 8 #divisiones del dutycycle
    tm_encoder = 100
    #------------------------------------
    bandera = 0; paso = 0; freno = 0; rpm = 0; rpm_deseado=0
    rpm_ant = 0; tiempo = 0; bandera2 = 0; duty =0; contador2=0
    angulo_deseado=0; angulo=0; start=False

    encoder = machine.Pin(22, machine.Pin.IN)
    encoder.irq(trigger=machine.Pin.IRQ_FALLING, handler=encoder_handler)
    encoder.irq(trigger=machine.Pin.IRQ_RISING, handler=encoder_handler)

    acc = machine.PWM(machine.Pin(0))
    acc.freq(3000); acc.duty_u16(0)
    dec = machine.PWM(machine.Pin(2))
    dec.freq(3000); dec.duty_u16(0)
    F_R= machine.Pin(4,machine.Pin.OUT)

    time.sleep_ms(1000)

    tim = machine.Timer()
    tim.init(freq = 1500, mode = machine.Timer.PERIODIC, callback = set_duty)
    time_start =utime.ticks_ms()
    Wifi_servidor.configWifi('CasaVZ','23060507')
    s=Wifi_servidor.crearSocket()
    while True:
        try:
            conn= Wifi_servidor.EsperaPeticion(s)
            request = Wifi_servidor.ObtenerRequest(conn)
            response = AnalizarRequest(request)
            Wifi_servidor.CerrarPeticion(conn,response)
        except Exception as e:
            print(e)
            conn.close()         

main()
    