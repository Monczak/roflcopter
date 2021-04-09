import numpy as np
from scipy import signal
import core.properties as properties


class Noise:
    @classmethod
    def get_noise(cls, length):
        waveform = np.random.normal(0, 1, size=int(properties.SAMPLE_RATE * length)) * 0.3
        return waveform
