################################################################################
# DHTlib example
#
# Created: 2016-03-10 11:00:30.630615
#
################################################################################

from community.andib.DHTlib import DHTlib as DHT


# import the streams module for USB serial port.
import streams
# open the default serial port
streams.serial()

#import timers
import timers

sleep(2000)
print("starting")
sleep(500)
sleep(2000)
print("starting")
sleep(500)


sensor = DHT.DHT22(D3.ICU,D3)

timer2 = timers.timer()
timer2.start()

while True:
    if timer2.get()>2500:
        sensor.read()
        DHT22_hum_2 =  sensor.hum_22()
        DHT22_temp_2 = sensor.temp_22()
        print(DHT22_temp_2,DHT22_hum_2)
        timer2.reset()
