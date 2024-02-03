from datetime import datetime, timedelta
from time import sleep
from uuid import uuid4

from flask import Flask, render_template, request
from flask_apscheduler import APScheduler
from flask_caching import Cache
from gpiozero import LED, GPIOZeroError, Device
import pywemo

from config import CONFIG
from button import Buttons


app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
cache = Cache(config={"CACHE_TYPE": "FileSystemCache"})
cache.init_app(app)


def setup(cache):
    """
    App Setup
    """
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

    cache.set("buttons", buttons)


@app.route("/", methods=["GET"])
@cache.cached()
def index():
    """
    Le index
    """
    return render_template(
        "index.html",
        site=CONFIG.get("site"),
        buttons=cache.get("buttons").values(),
    )


@app.route("/privacy", methods=["GET"])
@cache.cached()
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
    toggle_mode = request.args.get("mode", default="toggle")
    delay = request.args.get("delay", type=int)
    buttons = cache.get("buttons")
    button = buttons.get(key)
    if not button:
        return "key was not found", 404

    if delay:
        scheduler.add_job(
            str(uuid4()),
            lambda: process_toggle(button, toggle_mode),
            trigger="date",
            run_date=datetime.now() + timedelta(seconds=delay),
        )
        return f"{button.name} was scheduled in {delay} seconds"
    else:
        return process_toggle(button, toggle_mode)


def process_toggle(button, toggle_mode):
    """
    Tickler
    """
    if button.mode == "wemo":
        try:
            url = pywemo.setup_url_for_address(button.address)
            device = pywemo.device_from_description(url)
            if toggle_mode == "on":
                device.set_state(True)
            elif toggle_mode == "off":
                device.set_state(False)
            else:
                device.toggle()
            return f"{button.name} was turned {'on' if device.get_state() else 'off'}"

        except pywemo.PyWeMoException:
            return "pywemo exception", 500

    elif button.mode == "gpio":
        try:
            button.meta.connection.off()
            sleep(button.meta.get("wait", 1))
            button.meta.connection.on()
            return f"{button.name} was toggled"

        except GPIOZeroError:
            return "gpio exception", 500

    return f"{button.name}'s mode is unsupported", 500


if __name__ == "__main__":
    setup(cache)
    app.run(host="0.0.0.0", port=8000)
