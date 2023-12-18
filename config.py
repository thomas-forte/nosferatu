CONFIG = {
    "site": {
        "title": "Garage Pi",
        "subtitle": "Below are two buttons that will cycle their named relays.",
        "icon": "fas fa-warehouse",
    },
    "gpios": [
        {"address": 2, "name": "Relay 1", "wait": 1},
        {"address": 3, "name": "Relay 2", "wait": 1},
    ],
    "wemos": [
        {"address": "10.80.80.16", "name": "Living Room A", "mac": "24:f5:a2:21:45:9f"},
        {"address": "10.80.80.18", "name": "Living Room B", "mac": "24:f5:a2:4c:c7:bb"},
        {"address": "10.80.80.41", "name": "Bedroom Light", "mac": "24:f5:a2:49:b3:b9"},
        {"address": "10.80.80.19", "name": "Salt Lamp", "mac": "24:f5:a2:48:17:df"},
        {"address": "10.80.80.23", "name": "Plant Light", "mac": "24:f5:a2:48:22:23"},
        {"address": "10.80.80.24", "name": "Office Aroura", "mac": "24:f5:a2:48:16:ed"},
        {"address": "10.80.80.20", "name": "Kitchen Fan", "mac": "24:f5:a2:49:b3:59"},
    ],
}
