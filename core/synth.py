from core.larynx import Larynx
from core.noise import Noise
from core.mouth import Mouth
from core.formants import vowel_formant_dict, unvoiced_fricative_formant_dict, voiced_fricative_formant_dict, \
    nasal_formant_dict, lateral_formant_dict
import core.properties as properties
import numpy as np
from scipy import signal


def silence(length):
    return np.zeros(int(length * properties.SAMPLE_RATE))


def vowel(phoneme, freq, length, width=0.2):
    tone = Larynx.get_base_tone(freq, length)
    return Mouth.get_slice(Mouth.apply_formants(tone, vowel_formant_dict[phoneme], width) + tone * 0.03, 0.97)


def nasal(phoneme, freq, length, width=0.2):
    tone = Larynx.get_nasal_tone(freq, length)
    return Mouth.get_slice(Mouth.apply_formants(tone, nasal_formant_dict[phoneme], width) + tone * 0.02, 0.97)


def lateral(phoneme, freq, length, width=0.2):
    tone = Larynx.get_base_tone(freq, length)
    return Mouth.get_slice(Mouth.apply_formants(tone, lateral_formant_dict[phoneme], width) + tone * 0.02, 0.97)


def unvoiced_fricative(phoneme, length, width=0.2):
    tone = Noise.get_noise(length)
    return Mouth.get_slice(Mouth.apply_formants(tone, unvoiced_fricative_formant_dict[phoneme], width), 0.97)


def voiced_fricative(phoneme, freq, length, width=0.2):
    laryngeal_tone = Larynx.get_base_tone(freq, length)
    noise_tone = Noise.get_noise(length)

    filtered_noise = Mouth.get_slice(Mouth.apply_formants(noise_tone, voiced_fricative_formant_dict[phoneme][1], width), 0.97)
    filtered_noise *= signal.sawtooth(2 * np.pi * np.linspace(0, length, int(len(filtered_noise))) * freq)

    return Mouth.get_slice(Mouth.apply_formants(laryngeal_tone, voiced_fricative_formant_dict[phoneme][0], width) + laryngeal_tone * 0.02, 0.97) \
           + filtered_noise
