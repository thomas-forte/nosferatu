from flask import Flask, render_template
from gpiozero import LED
from time import sleep

app = Flask(__name__)

k1_relay = LED(2, initial_value=True)
k2_relay = LED(3, initial_value=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/k1', methods=['GET'])
def blink_k1():
    k1_relay.off()
    sleep(1)
    k1_relay.on()
    return 'success'

@app.route('/k2', methods=['GET'])
def blink_k2():
    k2_relay.off()
    sleep(1)
    k2_relay.on()
    return 'success'

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

if __name__ == "__main__":
    application.run(host='0.0.0.0')
