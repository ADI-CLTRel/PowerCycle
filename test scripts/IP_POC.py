import OPi.GPIO as GPIO
import time
import subprocess

#Set up OPI.GPIO
GPIO.setmode(GPIO.BOARD)
pin = int(input("OrangePi GPIO pin ")) #pin 5 used in test setup
GPIO.setup(pin, GPIO.OUT) #Physical pin 5 on OPi board being used
GPIO.output(pin, 0) #Set pin 5 output signal to low

#Set up test parameters
cycle_count = 0 #Variable to count UUT test cycles
cycle_target =int(input("Number of cycles to test ")) #Power cycle requirements per reliability tier level
ip = input("UUT IP Address? ") #Test sample IP address - Set device as static or DHCP reserved in router
print ("Using IP address" +ip)

#Actual testing program

def is_online(ip): # Define function to check if device is online
    result = subprocess.run(
        ["ping","-c","1","-W","1", ip], #ping command, count flag, 1 time, timeout, 1 sec
        stdout=subprocess.DEVNULL #prevents printing of output to terminal
        )
    return result.returncode == 0

previous_state = False

print ("monitoring...")

try:
    while True:
        current_state = is_online(ip)
        
        #detects offline to online switch
        if current_state and not previous_state:
            #increases cycle count and updates display
            cycle_count += 1
               
            print(f"{ip} is Online, C4 Power cycle Count {cycle_count}") 
            #Turns output signal on, waits 1 second, turns off
            GPIO.output(pin,1) 
            time.sleep(1)
            GPIO.output(pin,0)
            #Stops test at target cycle count
            
            #Stop after completion of target cycle count
            if cycle_count >= cycle_target:
                print (f"{cycle_target} cycle test complete.")
                break
            
        previous_state = current_state
        time.sleep(1) # script check interval
        
except KeyboardInterrupt:
    print("Exiting")
        
finally:
    GPIO.cleanup()
