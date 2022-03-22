from enum import Enum

class topics(Enum):
    BIOLOGY = 1
    CRYPTO = 2
    SAPCE = 3
    TFAANG = 4
    AUTHORIZATION = 5

    def __str__(self):
        return str(self.value)

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))

