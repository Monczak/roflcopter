import numpy as np
from scipy.io import wavfile
import core.properties as properties


def write_file(path, signal, amplitude):
    wavfile.write(path, properties.SAMPLE_RATE, (signal * np.iinfo(np.int16).max * amplitude).astype(np.int16))
