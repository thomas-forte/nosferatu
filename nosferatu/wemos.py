from typing import Literal
from flask import Blueprint, render_template
import pywemo

from .models.devices import Device

bp = Blueprint("wemos", __name__, url_prefix="/wemos")


@bp.route("/", methods=["GET"])
def list():
    return render_template("wemos/list.html")


def process_toggle(device: Device, goal_state: Literal["ON", "OFF", "UNKNOWN"]) -> None:
    try:
        url = pywemo.setup_url_for_address(device.ip4)
        wemo = pywemo.device_from_description(url)
        if goal_state == "ON":
            wemo.set_state(True)
        elif goal_state == "OFF":
            wemo.set_state(False)
        else:
            wemo.toggle()

        current_state = wemo.get_state()
        device.set_state_from_bool(current_state)

        return f"{device.name} was turned {'on' if current_state else 'off'}"

    except pywemo.PyWeMoException:
        return "pywemo exception", 500
