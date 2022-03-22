from enum import Enum


class topics(Enum):
    BIOLOGY = 1
    CRYPTO = 2
    SAPCE = 3
    TFAANG = 4

    def __str__(self):
        return str(self.value)
