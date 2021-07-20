# Garage Pi

## Hardware

- Raspberry Pi W
- 2 Channel Relay Module

## Software

- Raspberry Pi OS Lite
- git
- Python 3
- nginx

## Setup

### Hardware Setup

- 15W+ power supply
- Using +5V from board to power Vcc on  RELAY module
- Relay 1 to GPIO 2
- Relay 2 to GPIO 3
- Pinout
  - ![image of pi zero pins](docs/raspberry pi gpio.png?raw=true)
  - please reference the command `pinout` to ensure your pi's pins

- Add service
- Setup nginx proxy
- Serve up WSGI flask app

### Operating System Setup

- install Raspberry Pi OS Lite to an sd card using Raspberry Pi Imager
- copy the file named "ssh" from "boot" to the boot partition
- copy the file named "wpa_supplicant.conf" from "boot" to the boot partition
  - open the file and update the two fields to match you wifi settings
- once booted ssh into the pi
  - `ssh pi@<pi's ip address on your network>`
- check for updates to the os and included libraries
  - `sudo apt update`
- install those updates
  - `sudo apt upgrade`
- install git, pip3, nginx
  - `sudo apt install git python3-pip nginx`
- adjust system path by appending the following to ".bashrc"
  - `PATH=/home/pi/.local/bin:$PATH`
- reboot
  - `sudo reboot`

### Software Setup

- clone repository
  - `git clone https://github.com/thomas-forte/garage-pi.git`
- cd into repo
  - `cd garage-pi`
- install python dependencies
  - `pip3 install -r requirements.txt`
- copy nginx.config to
- enable nginx as a startup Service

### Service setup

- Setup service config file
  - `sudo cp nosferatu.service /etc/systemd/system/nosferatu.service`
- Start Gunicorn service
  - `sudo systemctl start nosferatu`
- Setup nginx config
  - `sudo cp nosferatu.nginx /etc/nginx/sites-available/nosferatu`
  - `sudo ln -s /etc/nginx/sites-available/nosferatu /etc/nginx/sites-enabled`
- Test nginx config
  - `sudo nginx -t`
- Restart nginx
  - `sudo systemctl restart nginx`

### Future Features

- Music control for garage?
