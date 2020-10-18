#Garage Pi

### Hardware
- Raspberry Pi W
- 2 Channel Relay Module

### Software
- Raspberry Pi OS Lite
- Python 3
  - gpiozero
  - flask
  - gunicorn
- Bootstrap CSS
- jQuery
- nginx

### Setup
- 12W power supply
- Using +5V from board to power Vcc on module
- Relay K1 IN to GPIO 2
- Relay K2 IN to GPIO 3
- Initialize GPIO's in high state to preserve normal relay state
- Add service
- Setup nginx proxy
- Serve up WSGI flask app

### Future Features
- Music control for garage?
