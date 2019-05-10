from cayennelpp import CayenneLPP
import utime, time
from ulora import TTN, uLoRa
# Refer to device pinout / schematics diagrams for pin details
#LORA_CS = const(5)
#LORA_SCK = const(18)
#LORA_MOSI = const(23)
#LORA_MISO = const(19)
#LORA_IRQ = const(12)
#LORA_RST = const(26)
LORA_CS = const(18)
LORA_SCK = const(5)
LORA_MOSI = const(27)
LORA_MISO = const(19)
LORA_IRQ = const(26)
LORA_RST = const(14)

#LORA_CS = const(18)
#LORA_SCK = const(5)
#LORA_MOSI = const(27)
#LORA_MISO = const(19)
#LORA_IRQ = const(26)
#LORA_RST = const(14)
LORA_DATARATE = "SF7BW125"  # Choose from several available
# From TTN console for device
DEVADDR = bytearray([0x26, 0x01, 0x15, 0x6A])

NWKEY = bytearray([0xA6, 0xC3, 0x0F, 0xB2, 0x91, 0xDB, 0x55, 0xC5,
                   0x31, 0x82, 0x53, 0xD4, 0x08, 0x08, 0x7A, 0x4E])
APP = bytearray([0x54, 0xBE, 0x2D, 0xE6, 0xB6, 0xB3, 0xF7, 0xC2,
                 0xD0, 0x33, 0x72, 0xB5, 0x27, 0x20, 0xD6, 0x20 ])
				 

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
data = bytearray([0x01, 0x02, 0x03, 0x04])

c = CayenneLPP()
c.addTemperature(1, 23.5) # Add temperature read to channel 1 
c.addTemperature(2, 22.7) # Add another temperature read to channel 2
c.addRelativeHumidity(3, 88.5) # Add relative humidity read to channel 3
data = c.getBuffer() # Get bytes

counter = 0
while True:
  lora.frame_counter=counter
  lora.send_data(data, len(data), lora.frame_counter)
  time.sleep(5)
  counter += 1







