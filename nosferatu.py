import json
from time import sleep
from flask import Flask, render_template
from gpiozero import LED
import pywemo

app = Flask(__name__)

with open('config.json', encoding='utf-8') as f:
    config = json.load(f)

pins = []
for gpio in config.get('gpios', []):
    pins.append({
        'pin': gpio['pin'],
        'key': gpio['key'],
        'name': gpio['name'],
        'wait': gpio['wait'],
        'connector': LED(gpio['pin'], initial_value=True)
    })

wemos = []
for wemo_config in config.get('wemos', []):
    wemos.append({
        'ip': wemo_config['ip'],
        'key': wemo_config['key'],
        'name': wemo_config['name']
    })


@app.route('/', methods=['GET'])
def index():
    """
        Le index
    """
    return render_template(
        'index.html',
        title=config['title'],
        subtitle=config['subtitle'],
        icon=config['icon'],
        pins=pins,
        wemos=wemos)


@app.route('/privacy', methods=['GET'])
def privacy():
    """
        Privacy concerns
    """
    return render_template(
        'privacy.html',
        title=config['title'],
        subtitle='Privacy',
        icon=config['icon'])


@app.route('/gpio/<int:pin>', methods=['GET'])
def gpio_toggle(pin):
    """
        "Ajax"
    """
    pin = [x for x in pins if x['pin'] == pin]
    if len(pin) != 1:
        return 'error', 500
    pin = pin[0]
    pin['connector'].off()
    sleep(pin['wait'])
    pin['connector'].on()
    return 'success'


@app.route('/wemo/<string:key>', methods=['GET'])
def wemo_toggle(key):
    """
        "Ajax"
    """
    wemo = [x for x in wemos if x['key'] == key]
    if len(wemo) != 1:
        return 'error', 500
    wemo = wemo[0]
    url = pywemo.setup_url_for_address(wemo['ip'])
    device = pywemo.device_from_description(url)
    device.toggle()
    return 'on' if device.get_state() else 'off'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
