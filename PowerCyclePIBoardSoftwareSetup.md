# Power Cycle Tester PI Board Setup Guide
## Step 1: Install OS on board
**Instructions based on Orange PI distro of Ubuntu Focal server (http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/service-and-support/Orange-Pi-PC.html)**
1. Download image and flash to microSD card
2. Install SD card and log into machine
```
  Username: root
  Password: orangepi
  ```
3. Update board firmware and OS packages using following command
```
sudo apt update && sudo apt upgrade -y
```
*if "Unmet dependencies" error occurs, use following command as recommended by terminal*
```
sudo apt --fix-broken install -y
```
## Step 2. Change Primary username
1. Rename primary user account
```usermod -l "outlet#" orangepi``` Replace "outlet#" with desired username (outlet1/outlet2/outlet3/outlet4)
*use new user name for all references to "outlet#" in rest of guide*
2. Rename primary user's group
```groupmod -n outlet# orangepi```
3. Move user home directory to new username ``` usermod -d /home/outlet# -m outlet#```

## Step 3. Update sudo permissions
Create a custom config file
```
sudo visudo 
"username:*your_username* ALL=(ALL) NOPASSWD: ALLSave"
```
## Step 4. Change password
1. reboot and log in as "outlet#" username
2. ```sudo passwd outlet#```
3. type in new password, use "power"

## Step 5. Enable autologin without password for bootup
1. Create directory for tty1 service:
```
sudo mkdir -p /etc/systemd/system/getty@tty1.service.d
```

2. Create and open an override file using a nano text editor:
```
sudo nano /etc/systemd/system/getty@tty1.service.d/override.conf
```
Place the following text in file:
    
    ini

    [Service]
    ExecStart=
    ExecStart=-/sbin/agetty --autologin *username* --noclear %I $TERM

Save and exit file, then reload systemd manager configurations:
```
sudo systemctl daemon-reload
```
Enable the getty service for tty1
```
sudo systemctl enable getty@tty1.service
```
## Step 6: Install necessary programs
- **WiringOP** OrangePi PC user manual page 55  
*Either log in as root user or use sudo command*


    1. Download code of wiringOP
    ```
    outlet#@orangepi:~# sudo apt update
    outlet#@orangepi:~# sudo apt install git
    outlet#@orangepi:~# sudo git clone https://github.com/orangepi-xunlong/wiringOP
    ```
    2. Compile and install wiringOP
    ```
    outlet#@orangepi:~# cd wiringOP
    outlet#@orangepi:~/wiringOP# sudo ./build clean
    outlet#@orangepi:~/wiringOP# sudo ./build
    ```
    3. Download and Install orangepi_PC_gpio_H3 to enable pins in python scripts
    ```
    cd
    git clone https://github.com/duxingkei33/orangepi_PC_gpio_pyH3
    sudo apt install python3-pip -y
	pip3 install opi.gpio 
    ```
## Step 7: Copy test scripts to Pi board home directory
1. Test code to verify process works
```
curl -O https://raw.githubusercontent.com/ADI-CLTRel/PowerCycle/refs/heads/main/pyscripts/IP_POC.py
```






