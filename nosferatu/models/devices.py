from typing import Literal
from uuid import uuid4


class Device:
    def __init__(self, name: str, ip4: str, addr: str, **kwargs) -> None:
        self.key = uuid4()
        self.ip4 = ip4
        self.addr = addr
        self.name = name
        self.state: Literal["ON", "OFF", "UNKNOWN"] = "UNKNOWN"
        self.meta = kwargs

    def set_state_from_bool(self, state: bool) -> None:
        if state:
            self.state = "ON"
        else:
            self.state = "OFF"


class WemoDevice(Device):
    pass
