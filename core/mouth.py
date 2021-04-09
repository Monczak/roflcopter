import numpy as np
from scipy import signal
import core.properties as properties
import core.filters as filters
import math


class Mouth:
    @classmethod
    def apply_formant(cls, waveform, formant, width):
        return filters.butter_bandpass_filter(waveform, formant * (1 - width), formant * (1 + width))

    @classmethod
    def apply_formants(cls, waveform, formants, width):
        result = np.zeros(waveform.shape)
        for formant in formants:
            if len(formant) == 2:
                result += cls.apply_formant(waveform, formant[0], width) * formant[1]
            elif len(formant) == 3:
                result += cls.apply_formant(waveform, formant[0], formant[2]) * formant[1]
        return result / len(formants)

    @classmethod
    def get_slice(cls, waveform, length):
        return waveform[int(len(waveform) * (1 - length)):int(len(waveform) * length)]

    @classmethod
    def crossfade(cls, wave1, wave2, length):
        fade_length = min(len(wave1), len(wave2))
        fade_t = np.linspace(0, 1, int(fade_length * length) + 1)
        t = np.zeros(fade_length)

        for i in range(math.floor(fade_length // 2 - fade_length * length / 2), math.floor((fade_length // 2 + fade_length * length / 2))):
            t[i] = fade_t[i - math.floor(fade_length // 2 - fade_length * length / 2)]

        for i in range(math.floor(fade_length // 2 + fade_length * length / 2), fade_length):
            t[i] = 1

        w1 = wave1 * (1 - t)
        w2 = wave2 * t
        return w1 + w2

    @classmethod
    def dual_fade(cls, wave, samples):
        fade_in_t = np.linspace(0, 1, samples)
        fade_out_t = np.linspace(1, 0, samples)

        for i in range(0, samples):
            wave[i] *= fade_in_t[i]

        for i in range(0, samples):
            wave[len(wave) - samples + i] *= fade_out_t[i]

        return wave

    @classmethod
    def border_crossfade(cls, wave1, wave2, sample_offset):
        fade_t = np.linspace(0, 1, sample_offset)

        result = wave1
        for i in range(len(wave1) - sample_offset, len(wave1)):
            rel_i = i - len(wave1) + sample_offset
            result[i] -= wave1[i] * fade_t[rel_i]
            result[i] += wave2[rel_i] * fade_t[rel_i]

        return result

    @classmethod
    def connect_phonemes(cls, tones, border_length):
        result = np.empty(1)
        for i in range(len(tones) - 1):
            cross_tone = cls.border_crossfade(tones[i], tones[i + 1], border_length)
            result = np.concatenate((result, cross_tone))
        return np.concatenate((result, tones[-1]))
