from .client import *
from enum import Enum

def connect(**args):
    return Client(**args)

class PinType(Enum):
    PIN_CH = 'PIN.CH'
    PIN_SMC = 'PIN.SMC'
