# Nosferatu

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
  - ![image of pi zero pins](https://github.com/thomas-forte/nosferatu/blob/master/docs/raspberry%20pi%20gpio.png?raw=true)
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
- install git, pip3, venv3, nginx
  - `sudo apt install git python3-pip python3-venv nginx`
- reboot
  - `sudo reboot`

### Software Setup

- clone repository
  - `git clone https://github.com/thomas-forte/nosferatu.git`
- cd into repo
  - `cd nosferatu`
- create environment
  - `python3 -m venv venv`
- add environment to path
  - `source venv/bin/activate`
- install python dependencies
  - `pip install -r requirements.txt`

### Service setup

- Setup service config file
  - `sudo cp nosferatu.service /etc/systemd/system/nosferatu.service`
- Start Gunicorn service
  - `sudo systemctl start nosferatu`
- Make Gunicorn service start on boot
  - `sudo systemctl enable nosferatu.service`
- Setup nginx config
  - `sudo cp nosferatu.nginx /etc/nginx/sites-available/nosferatu`
  - `sudo ln -s /etc/nginx/sites-available/nosferatu /etc/nginx/sites-enabled`
- Test nginx config
  - `sudo nginx -t`
  - If there is a port 80 duplicate error you must remove the example default site from sites-enabled
- Restart nginx
  - `sudo systemctl restart nginx`

### Setup Notes

- assumes user is pi
- assumes code is checked out into user's root home directory
