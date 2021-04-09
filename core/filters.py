import numpy as np
from scipy import signal
import core.properties as properties


def butter_bandpass(lowcut, highcut, order):
    nyquist = properties.SAMPLE_RATE * 0.5
    low = lowcut / nyquist
    high = highcut / nyquist
    sos = signal.butter(order, [low, high], analog=False, btype="band", output="sos")
    return sos


def butter_bandpass_filter(data, lowcut, highcut, order=5):
    sos = butter_bandpass(lowcut, highcut, order=order)
    y = signal.sosfiltfilt(sos, data)
    return y
