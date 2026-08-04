# Power Cycle Tester PI Board Setup Guide
## Step 1: Install OS on board
**Instructions based on Orange PI distro of Ubuntu Focal server (http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/service-and-support/Orange-Pi-PC.html)**
1. Download image and flash to microSD card
2. Follow general setup

## Change Primary username

1. Remove Systemd Override file
```sudo rm -f /etc/systemd/system/getty@tty1.service.d/override.conf```     #Check this works, if not, edit file to disable autologin
2. log in as root user (default password: orangepi)
3. Rename primary user account
```usermod -l "outlet#" orangepi``` Replace "outlet# with desired username (outlet 1/2/3/4)" 
4. Rename primary user's group
```groupmod -n outlet# orangepi```
5. Move user home directory to new username ``` usermod -d /home/outlet# -m outlet#```




## Update sudo permissions
Create a custom config file
```
sudo visudo -f /etc/sudoers.d/nopasswd
"username:*your_username* ALL=(ALL) NOPASSWD: ALLSave"
sudo chmod 0440 /etc/sudoers.d/nopasswd
```

## Enable autologin without password for bootup
Create and open an override file using a nano text editor:
```
sudo nano /etc/systemd/system/getty@tty1.service.d/override.conf
```
Place the following text in file:
    ```
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
## Step 2: Install necessary programs
- **WiringOP** OrangePi PC user manual page 55

    1. Download code of wiringOP
    ```
    root@orangepi:~# apt update
    root@orangepi:~# apt install git
    root@orangepi:~# git clone https://github.com/orangepi-xunlong/wiringOP
    ```
    2. Compile and install wiringOP
    ```
    root@orangepi:~# cd wiringOP
    root@orangepi:~/wiringOP# ./build clean
    root@orangepi:~/wiringOP# ./build
    ```
    3. Download and Install orangepi_PC_gpio_H3 to enable pins in python scripts
    ```
    git clone https://github.com/duxingkei33/orangepi_PC_gpio_pyH3
    sudo apt install python3-pip
	pip3 install opi.gpio 
    ```
## Step fin: Copy test scripts to Pi board home directory







