import numpy as np
from scipy import signal
import core.properties as properties


class Larynx:
    @classmethod
    def get_base_tone(cls, frequency, length):
        t = np.linspace(0, length, int(properties.SAMPLE_RATE * length), endpoint=False)
        waveform = signal.square(2 * np.pi * t * frequency, duty=0.3)
        return waveform

    @classmethod
    def get_nasal_tone(cls, frequency, length):
        t = np.linspace(0, length, int(properties.SAMPLE_RATE * length), endpoint=False)
        waveform = signal.square(2 * np.pi * t * frequency, duty=0.4)
        return waveform
