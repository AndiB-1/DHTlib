################################################################################
# DHTlib
#
# Created: 2016-03-10 10:47:30.867015

# This software provides data readout from a DHT22 or DHT11 temperature+humidity sensor on any digital pin of an MCU running VIPER python.
# This code was developed and tested on a viperized Photon board (Particle Photon).
# It follows closely the Arduino code by Adafruit (https://github.com/adafruit/DHT-sensor-library).

# Special thanks to Davide who contributed and tested the DHT11 part!
#
# Copyright (c) 2015 A.C. Betz.  All right reserved. Developed using the VIPER IDE. 
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#############################################################################################################################



#import ICU library & timers
import icu
import timers

# USAGE EXAMPLE
#
# from community.andib.DHTlib import DHT22
# 
# import streams
# streams.serial()
#
# sensor = DHT22(D3.ICU,D3)
#
# timer2 = timers.timer()
# timer2.start()
#
# while True:
#     if timer2.get()>2500:
#         sensor.read()
#         DHT22_hum_2 =  sensor.hum()
#         DHT22_temp_2 = sensor.temp()
#         print(DHT22_temp_2,DHT22_hum_2)
#         timer2.reset()

# IMPORTANT
# don't read more than once every 2 seconds!

class DHT22:

    
    def __init__(self,receivePin,receivePinShort):
#         print("init")
        self.receivepin = receivePin
        self.receivepinShort = receivePinShort
        self.DHT22_temp = None
        self.DHT22_hum = None

    def read(self):
        ### don't execute this more than once every 2s!
#         print("read")
        timer1 = timers.timer()
        timer1.start()
        foo = 0

        self.DHT22_temp = 0
        self.DHT22_hum = 0
        BinListDHT22 = []
        timeListDHT22 = []

        #Go into high impedence state to let pull-up raise data line level and start the reading process.
        pinMode(self.receivepinShort,OUTPUT)
        digitalWrite(self.receivepinShort, HIGH)
        #wait 10ms
        timer1.reset()
        while timer1.get()<10: # maybe change this while to one_shot?
            foo+=1 # probably unecessary
        
        #First pull data line low for 10 ms.
        digitalWrite(self.receivepinShort, LOW)
        timer1.reset()
        while timer1.get()<10: # maybe change this while to one_shot?
            foo+=1 # probably unecessary
#         print("ICU")
        #get the data stream via ICU
        #call to ICU seems to take some time, thus call *before* initiation is finished
        tmpICU = icu.capture(self.receivepin,LOW,86,10000,time_unit=MICROS)
#         print(tmpICU)
        # End the start signal by setting data line high.
        digitalWrite(self.receivepinShort, HIGH)
        pinMode(self.receivepinShort,INPUT_PULLUP)
#         print("go to calculus")
        
        # remove all even entries, they're just "start bits", discard 1st two entries
        for i in range(3,len(tmpICU),1):
            if i%2!=0: #these are the odd entries
                timeListDHT22.append(tmpICU[i])
#         print(timeListDHT22)
        # convert to list of binaries
        for i in range(len(timeListDHT22)):
            if timeListDHT22[i] < 35:    # shouldn't be longer than 28us, but allow some wiggle room here
                BinListDHT22.append(0)
            else:
                BinListDHT22.append(1)    
        # extract hum, temp parts (16bits each)
        tmp_hum = BinListDHT22[0:16]    #1st 16 bits are humidity, 2nd 16 bits are temperature
        tmp_temp = BinListDHT22[16:32]
        
        tmp_tempSign = 1
        if tmp_temp[0] == 1:
            tmp_tempSign = -1 # neg temperatures are encoded most significant bit = 1
            tmp_temp[0] = 0
        tmp_temp = tmp_temp[::-1] #invert the list for conversion to decimal
        tmp_hum = tmp_hum[::-1]
#         print(tmp_temp,tmp_hum)

        DHT22_temp_1 = 0
        DHT22_hum_1 = 0
        for i in range(16):
            DHT22_temp_1 += tmp_temp[i]*(2**i)
            DHT22_hum_1 += tmp_hum[i]*(2**i)
            
#         print(DHT22_temp_1/10,DHT22_hum_1/10)
        self.DHT22_temp = DHT22_temp_1/10
        self.DHT22_hum = DHT22_hum_1/10
#         print(self.DHT22_temp, self.DHT22_hum)
        digitalWrite(self.receivepinShort, HIGH)
        timer1.clear()
#         print("read done")

    def temp(self):
        return self.DHT22_temp
    
    def hum(self):
#         print(self.DHT22_hum)
        return self.DHT22_hum

    def getDHTdata(self):
        self.read()
        return(self.DHT22_temp, self.DHT22_hum)

##################################################################################################
##################################################################################################

class DHT11:
    # special thanks to Davide who modified my code to work with the DHT11 sensor

    def __init__(self,receivePin,receivePinShort):
#         print("init")
        self.receivepin = receivePin
        self.receivepinShort = receivePinShort
        self.DHT11_temp = None
        self.DHT11_hum = None

    def read(self):
        ### don't execute this more than once every 2s!
#         print("read")
        timer1 = timers.timer()
        timer1.start()
        foo = 0

        self.DHT11_temp = 0
        self.DHT11_hum = 0
        BinListDHT11 = []
        timeListDHT11 = []

        #Go into high impedence state to let pull-up raise data line level and start the reading process.
        pinMode(self.receivepinShort,OUTPUT)
        digitalWrite(self.receivepinShort, HIGH)
        #wait 10ms
        timer1.reset()
        while timer1.get()<10: # maybe change this while to one_shot?
            foo+=1 # probably unecessary
        
        #First pull data line low for 10 ms.
        digitalWrite(self.receivepinShort, LOW)
        timer1.reset()
        while timer1.get()<10: # maybe change this while to one_shot?
            foo+=1 # probably unecessary
#         print("ICU")
        #get the data stream via ICU
        #call to ICU seems to take some time, thus call *before* initiation is finished
        tmpICU = icu.capture(self.receivepin,LOW,86,10000,time_unit=MICROS)
#         print(tmpICU)
        # End the start signal by setting data line high.
        digitalWrite(self.receivepinShort, HIGH)
        pinMode(self.receivepinShort,INPUT_PULLUP)
#         print("go to calculus")
        
        # remove all even entries, they're just "start bits", discard 1st two entries
        for i in range(3,len(tmpICU),1):
            if i%2!=0: #these are the odd entries
                timeListDHT11.append(tmpICU[i])
#         print(timeListDHT11)
        # convert to list of binaries
        for i in range(len(timeListDHT11)):
            if timeListDHT11[i] < 35:    # shouldn't be longer than 28us, but allow some wiggle room here
                BinListDHT11.append(0)
            else:
                BinListDHT11.append(1)    
        # extract hum, temp parts (16bits each)
        tmp_hum = BinListDHT11[0:8]    #1st 8 bits are humidity, 2nd 8 bits are temperature
        tmp_temp = BinListDHT11[8:24]
        
        tmp_tempSign = 1
        if tmp_temp[0] == 1:
            tmp_tempSign = -1 # neg temperatures are encoded most significant bit = 1
            tmp_temp[0] = 0
        tmp_temp = tmp_temp[::-1] #invert the list for conversion to decimal
        tmp_hum = tmp_hum[::-1]
#         print(tmp_temp,tmp_hum)

        DHT11_temp_1 = 0
        DHT11_hum_1 = 0
        for i in range(8):
            DHT11_temp_1 += tmp_temp[i]*(2**i)
            DHT11_hum_1 += tmp_hum[i]*(2**i)
            
        self.DHT11_temp = DHT11_temp_1
        self.DHT11_hum = DHT11_hum_1
#         print(self.DHT11_temp, self.DHT11_hum)
        digitalWrite(self.receivepinShort, HIGH)
        timer1.clear()
#         print("read done")

    def temp(self):
        return self.DHT11_temp
    
    def hum(self):
        return self.DHT11_hum
    
    def getDHTdata(self):
        self.read()
        return(self.DHT11_temp, self.DHT11_hum)

