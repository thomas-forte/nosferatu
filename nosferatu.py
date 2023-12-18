from time import sleep
from flask import Flask, render_template
from gpiozero import LED, GPIOZeroError, Device
import pywemo

from config import CONFIG
from button import Buttons

app = Flask(__name__)
buttons = Buttons()

# setup wemo buttons
for wemo_config in CONFIG.get("wemos", []):
    buttons.add_button(mode="wemo", **wemo_config, example="test")

# setup gpio buttons
try:
    Device()  # forces to check if pin factory exists

    for gpio_config in CONFIG.get("gpios", []):
        buttons.add_button(
            mode="gpio",
            **gpio_config,
            connection=LED(gpio_config["address"], initial_value=True),
        )
except GPIOZeroError:
    print("Issue setting up gpio, skipping config.")


@app.route("/", methods=["GET"])
def index():
    """
    Le index
    """
    return render_template(
        "index.html",
        site=CONFIG.get("site"),
        buttons=buttons.values(),
    )


@app.route("/privacy", methods=["GET"])
def privacy():
    """
    Privacy concerns
    """
    return render_template(
        "privacy.html",
        site=CONFIG.get("site", {}) | {"subtitle": "Privacy"},
    )


@app.route("/toggle/<uuid:key>", methods=["GET"])
def toggle(key):
    """
    "Ajax"
    """
    button = buttons.get(key)
    if button:
        if button.mode == "wemo":
            try:
                url = pywemo.setup_url_for_address(button.address)
                device = pywemo.device_from_description(url)
                device.toggle()
                return "on" if device.get_state() else "off"

            except pywemo.PyWeMoException:
                return "pywemo exception", 500

        elif button.mode == "gpio":
            try:
                button.connection.off()
                sleep(button.meta.get("wait", 1))
                button.connection.on()
                return "success"

            except GPIOZeroError:
                return "gpio exception", 500

    return "not found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
