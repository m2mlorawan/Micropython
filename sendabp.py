from cayennelpp import CayenneLPP
import utime, time
from ulora import TTN, uLoRa
# Refer to device pinout / schematics diagrams for pin details
LORA_CS = const(5)
LORA_SCK = const(18)
LORA_MOSI = const(23)
LORA_MISO = const(19)
LORA_IRQ = const(12)
LORA_RST = const(26)
#LORA_CS = const(18)
#LORA_SCK = const(5)
#LORA_MOSI = const(27)
#LORA_MISO = const(19)
#LORA_IRQ = const(26)
#LORA_RST = const(14)

LORA_DATARATE = "SF7BW125"  # Choose from several available
# From TTN console for device
DEVADDR = bytearray([0x26, 0x01, 0x15, 0xFF])

NWKEY = bytearray([0xA6, 0xC3, 0x0F, 0xB2, 0x91, 0xDB, 0x55, 0xC5,
                   0x31, 0x82, 0x53, 0xD4, 0x08, 0x08, 0x7A, 0xFF])
APP = bytearray([0x54, 0xBE, 0x2D, 0xE6, 0xB6, 0xB3, 0xF7, 0xC2,
                 0xD0, 0x33, 0x72, 0xB5, 0x27, 0x20, 0xD6, 0xFF ])
				 

TTN_CONFIG = TTN(DEVADDR, NWKEY, APP, country="AS")
FPORT = 1
lora = uLoRa(
    cs=LORA_CS,
    sck=LORA_SCK,
    mosi=LORA_MOSI,
    miso=LORA_MISO,
    irq=LORA_IRQ,
    rst=LORA_RST,
    ttn_config=TTN_CONFIG,
    datarate=LORA_DATARATE,
    fport=FPORT
)
# ...Then send data as bytearray
#data = bytearray([0x01, 0x02, 0x03, 0x04])

#SENSOR 
import machine
import bme280
temp = 0
pa = 0
hum = 0
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21)) #ESP32 Dev Board /myown
#i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

counter = 0
while True:
  bme = bme280.BME280(i2c=i2c)
  temp,pa,hum = bme.values 
  print (temp)
  print(pa)
  print(hum)
  c = CayenneLPP()
#//lpp.addAnalogInput(1, volt / 1000);
#//lpp.addTemperature(2, temp);
#//lpp.addRelativeHumidity(3, humid);
#//lpp.addBarometricPressure(4, pa /100);
#//lpp.addAnalogInput(5, alt);
#//lpp.addAnalogInput(6, distance);
#//lpp.addGPS(7, lat, long,2 );
#//lpp.addLuminosity(8,  lux);
#//lpp.addPresence(9,  value);
#//lpp.addAccelerometer(10, x, y,  z);
#//lpp.addGyrometer(11,  x,  y,  z);
#//lpp.addAnalogInput(12, SAT);
  c.addTemperature(1, float(temp)) # Add temperature read to channel 1 
  c.addRelativeHumidity(2, float(hum)) # Add relative humidity read to channel 2
  c.addBarometricPressure(3, float(pa)) # Add another temperature read to channel 3
  data = c.getBuffer() # Get bytes
  lora.frame_counter=counter
  lora.send_data(data, len(data), lora.frame_counter)
  time.sleep(5)
  counter += 1










