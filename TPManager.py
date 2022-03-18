from time import time_ns
from datetime import datetime
from sha256 import sha256
from json import loads, dumps


class TimePassword:
    def __init__(self):
        with open("config.json", 'r') as f:
            self.data   = loads(f.read())
            self.pepper = self.data["pepper"]
            self.ttl    = self.data["token-ttl"]
            self.count  = len(self.data["log"])

            self.sha256 = sha256()
            self.sha256.iniHash = self.data["initial"].copy()
            self.sha256.iniCons = self.data["constants"].copy()
            f.close()

    def genpass(self) -> str:
        binPepp = int('1' + ''.join(map(lambda x: bin(ord(x))[2:].zfill(8), self.pepper)), 2)
        time = self.sha256.Sig1(int(time_ns() / (self.ttl * 1e+9)))

        return self.sha256.getHash(f"{self.pepper}{time}")

    def addlog(self, usID: int):
        with open("config.json", 'w') as f:
            self.data["log"].append([usID, datetime.now().strftime("%d/%m/%Y, %H:%M:%S")])
            f.write(dumps(self.data))
            f.close()

