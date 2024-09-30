from machine import Pin, PWM

#TypeAxis = Enum('TypeAxis',['EjeX','EjeY','EjeZ'])

class Driver:
  def __init__(self) -> None:
    self.type = type
  def set_velocity(self, velocity):
    pass

class AM6807(Driver):
  def __init__(self, acc: PWM, dec: Pin, for_rev: Pin):
    super().__init__()
    self.acc = acc
    self.dec = dec
    self.for_rev = for_rev

  def set_velocity(self, velocity):
    if abs(velocity) <= 4000:
      self.acc.duty_u16(int(abs(velocity)*16.25))
      if velocity > 0:
        self.for_rev.on()
      else:
        self.for_rev.off()
  """ Con Velocidad 0 se produce un short brake
      La velocidad máxima es 4000 
      El signo de la velocidad indica el sentido de giro"""

class Sensor:
  def __init__(self, encoder: Pin, interrupt) -> None:
    self.encoder = encoder

class Motor:
  def __init__(self, axis , driver :Driver):
    self.axis = axis
    self.driver = driver



