CONFIG = {
    # Display settings
    "site": {
        "title": "Garage Pi",
        "subtitle": "Below are two buttons that will cycle their named relays.",
        "icon": "fas fa-warehouse",
    },
    # Gpio settings
    "gpios": [
        {"address": 2, "name": "Relay 1", "wait": 1},
        {"address": 3, "name": "Relay 2", "wait": 1},
    ],
    # Wemo settings
    "wemos": [
        {"address": "192.168.1.1", "name": "Some Wemo", "mac": "00:00:00:00:00"},
    ],
}
