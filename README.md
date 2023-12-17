# Nosferatu

This project started as a way to control a relay channel but has grown to more than that.

## Configuration

Everything can be done within the config file.

## Docker Setup

*Note: GPIO functions won't work this way.*

### Service Setup

- clone repository
  - `git clone https://github.com/thomas-forte/nosferatu.git`
- cd into repo
  - `cd nosferatu`
- create docker service
  - `docker compose up -d`

## Standalone Pi Setup

### Hardware

- Originally created for the Zero W but will work on anything supported by gpiozero
- 2 Channel Relay Module [example](https://github.com/thomas-forte/nosferatu/blob/master/docs/relay%20module.jpg?raw=true)

### Setup

#### Hardware Setup

- Raspberry Pi
- Power supply (or even higher with the new boards)
- Using +5V from board to power Vcc on RELAY module
- Relay 1 to GPIO 2
- Relay 2 to GPIO 3

#### Operating System Setup

- Install Raspberry Pi OS Lite
- Fully update the OS
  - `sudo apt update`
  - `sudo apt upgrade`
  - `sudo apt autoremove`
- Install dependencies
  - `sudo apt install git python3-pip python3-venv nginx`
- Reboot

#### Software Setup

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

#### Service setup

- Setup service config file
  - `sudo cp nosferatu.service /etc/systemd/system/nosferatu.service`
- Start the service
  - `sudo systemctl start nosferatu`
- Make the service start on boot
  - `sudo systemctl enable nosferatu.service`
- Setup nginx config
  - `sudo cp nginx.conf /etc/nginx/sites-available/nosferatu`
  - `sudo ln -s /etc/nginx/sites-available/nosferatu /etc/nginx/sites-enabled`
  - `sudo rm /etc/nginx/sites-enabled/default`
- Test nginx config
  - `sudo nginx -t`
  - If there is a port 80 duplicate error you must remove the example default site from sites-enabled
- Restart nginx
  - `sudo systemctl restart nginx`

#### GPIO Reference

*Please reference the command `pinout` to ensure your pi's pins*

![image of pi zero pins](https://github.com/thomas-forte/nosferatu/blob/master/docs/raspberry%20pi%20gpio.png?raw=true)
