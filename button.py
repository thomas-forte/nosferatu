from uuid import uuid4


class Button:
    def __init__(self, address, name, mode, **kwargs) -> None:
        self.key = uuid4()
        self.address = address
        self.name = name
        self.mode = mode
        self.meta = kwargs


class Buttons:
    buttons = {}

    def add_button(self, *, address, name, mode, **kwargs):
        button = Button(address, name, mode, **kwargs)
        self.buttons[button.key] = button

    def values(self):
        return self.buttons.values()

    def get(self, key):
        return self.buttons.get(key)
