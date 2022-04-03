import os
import re
import json
# from pprint import pprint
from typing import Optional
from subprocess import run, CompletedProcess
from pydantic import BaseModel
from .atasmart import SmartRoot


class Disk(BaseModel):
    device: str
    smart: Optional[SmartRoot]

    def read_smart(self, *options) -> SmartRoot:
        smartctl: CompletedProcess = run(
            ['sudo', 'smartctl', '-a', *options, f'/dev/{self.device}', '-j'],
            capture_output=True
        )
        data = json.loads(smartctl.stdout.decode())
        # pprint(data)
        return SmartRoot(**data)

    @classmethod
    def get_all(cls):
        rule = r'^sd[a-z]+$'
        match = re.compile(rule)
        return [cls(device=drive) for drive in os.listdir('/dev/') if match.match(drive)]

    def show(self) -> None:
        print(self)
        attributes = {attribute.name: attribute for attribute in self.read_smart().ata_smart_attributes.table}
        for key in sorted(attributes.keys()):
            attribute = attributes[key]
            print(f'{attribute.name:40} = {attribute.value}')

    def __gt__(self, other):
        return self.device > other.device

    def __eq__(self, other):
        return self.device == other.device
