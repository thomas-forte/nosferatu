from flask import Flask, render_template
from gpiozero import LED
from time import sleep
import json

app = Flask(__name__)

with open('config.json') as f:
  config = json.load(f)

pins = []
for gpio in config['gpios']:
    pins.append({
        'pin': gpio['pin'],
        'key': gpio['key'],
        'name': gpio['name'],
        'wait': gpio['wait'],
        'connector': LED(gpio['pin'], initial_value=True)
    })

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title=config['title'], subtitle=config['subtitle'], icon=config['icon'], pins=pins)

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

@app.route('/gpio/<int:pin>', methods=['GET'])
def gpio_toggle(pin):
    pin = [x for x in pins if x['pin'] == pin]
    if len(pin) != 1:
        return 'error'
    pin = pin[0]
    pin['connector'].off()
    sleep(pin['wait'])
    pin['connector'].on()
    return 'success'

if __name__ == "__main__":
    app.run(host='0.0.0.0')