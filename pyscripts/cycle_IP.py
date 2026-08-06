#Modules used in script
import OPi.GPIO as GPIO
import time
import subprocess
import sys

##Determine voltage to test and what GPIO pin to trigger
def voltage_select():#Determine which GPIO pin to cycle for outlet
    global voltage # allow variable to persist outside of selection function
    global pin # allow variable to persist outside of selection function
    voltage = input("Test at 120 or 240? ")
    if voltage == "120":
        pin = 5
    elif voltage == "240":
        pin = 7
    else:
        print ("Error - Test voltage undefined")
        voltage = "ERROR"
#Determine target cycle count
def select_cycle_target():
    global cycle_target # allow variable to persist outside of selection function
    while True:
        print("Select product reliability tier")
        print("1. Tier 1 - Not Required")
        print("2. Tier 2 - 5000")
        print("3. Tier 3 - 10000")
        print("4. Other - a custom number cycles")
        
        tier_choice=input().strip()
        if tier_choice == "1":
            print("Power cycle testing not required")
            print("Exiting")
            sys.exit()
        elif tier_choice == "2":
            cycle_target = 2
            break
        elif tier_choice == "3":
            cycle_target = 3
            break
        elif tier_choice == "4":
            cycle_target = int(input("Enter desired custom power cycle count "))
            break
        else:
            print("Error - target cycle invalid")
            cycle_target = "ERROR"

ip = input("UUT IP Address? ") #Test sample IP address - Set device as static or DHCP reserved in router

def test_variables(): #Allow for selection and confirmation of all test variables
    while True:
        voltage_select()
        select_cycle_target()
        print (f"Cycle {voltage}V outlet to test device at {ip} for {cycle_target} cycles") 
        confirm = input ("Is this correct? (yes/no): ").strip().lower()
        if confirm in ['yes','y']:
            print("Beginning test...")
            break
        else:
            print("Please make selections again.")
test_variables()
#Set up OPI.GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT) #Physical pin 5 on OPi board for 120, pin 7 for 240 being used
GPIO.output(pin, 0) #Set pin output signal to low
#Set test cycle count variable
cycle_count = -1 #Test counts being on at start as 1 cycle, this corrects it to zero
#Actual testing program

def is_online(ip): # Define function to check if device is online
    result = subprocess.run(
        ["ping","-c","1","-W","1", ip], #ping command, count flag, 1 time, timeout, 1 sec
        stdout=subprocess.DEVNULL #prevents printing of output to terminal
        )
    return result.returncode == 0

previous_state = False

print ("monitoring...")
time0 = time.perf_counter()

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
            
            #Estimates time to test completion
            if cycle_count % 25 == 0 and cycle_count != 0: #Update time estimate every 25 cycles and skips count at start
                time_n = time.perf_counter() - time0
                avg_cycle_time = time_n / cycle_count
                cycles_remain = cycle_target - cycle_count
                est_time_remain = round((avg_cycle_time * cycles_remain) / 3600,2) #calculates time remaining in hours
                
                print(f"Estimated time remaining: {est_time_remain} hours")
            
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
