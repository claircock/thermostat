import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
DHTPin = 7

def loop():
    dht = DHT.DHT(DHTPin)
    counts = 0
    while(True):
        counts += 1
        print("measurement counts: ", counts)
        for i in range(0, 15) :
            chk = dht.readDHT4()
            if (chk is dht.DHTLIB_OK):
                print("DHT4, OK!")
                break
            time.sleep(0.1)
        print("Humidity : %2F, \t Temperature : %2f \n"%(dht.humidity,dht.temperature))
        time.sleep(2)
if __name__ =='__main__':
    print('program is starting...')
    try:
        loop()
    except Keyboardinterrupt:
        GPIO.cleanup()
        exit()
