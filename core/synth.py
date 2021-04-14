from core.larynx import Larynx
from core.noise import Noise
from core.mouth import Mouth
from core.formants import vowel_formant_dict, unvoiced_fricative_formant_dict, voiced_fricative_formant_dict, \
    nasal_formant_dict, lateral_formant_dict, unvoiced_consonants_formant_dict, voiced_consonants_formant_dict
from core.filters import butter_bandpass_filter
import core.properties as properties
import numpy as np
from scipy import signal

slice_size = 0.97


class Synth:
    whisper = False

    @classmethod
    def silence(cls, length):
        return np.zeros(int(length * properties.SAMPLE_RATE))

    @classmethod
    def vowel(cls, phoneme, freq, length, width=0.2):
        tone = Larynx.get_base_tone(freq, length) if not cls.whisper else Noise.get_noise(length)
        return Mouth.get_slice(Mouth.apply_formants(tone, vowel_formant_dict[phoneme], width) + tone * 0.03, slice_size)

    @classmethod
    def nasal(cls, phoneme, freq, length, width=0.2):
        tone = Larynx.get_nasal_tone(freq, length) if not cls.whisper else Noise.get_noise(length)
        return Mouth.get_slice(Mouth.apply_formants(tone, nasal_formant_dict[phoneme], width) + tone * 0.02, slice_size)

    @classmethod
    def lateral(cls, phoneme, freq, length, width=0.2):
        tone = Larynx.get_base_tone(freq, length) if not cls.whisper else Noise.get_noise(length)
        return Mouth.get_slice(Mouth.apply_formants(tone, lateral_formant_dict[phoneme], width) + tone * 0.02,
                               slice_size)

    @classmethod
    def unvoiced_fricative(cls, phoneme, length, width=0.2):
        tone = Noise.get_noise(length)
        return Mouth.get_slice(Mouth.apply_formants(tone, unvoiced_fricative_formant_dict[phoneme], width), slice_size)

    @classmethod
    def voiced_fricative(cls, phoneme, freq, length, width=0.2):
        laryngeal_tone = Larynx.get_base_tone(freq, length) if not cls.whisper else Noise.get_noise(length)
        noise_tone = Noise.get_noise(length)

        filtered_noise = Mouth.get_slice(
            Mouth.apply_formants(noise_tone, voiced_fricative_formant_dict[phoneme][1], width), slice_size)
        filtered_noise *= signal.sawtooth(2 * np.pi * np.linspace(0, length, int(len(filtered_noise))) * freq)

        return Mouth.get_slice(Mouth.apply_formants(laryngeal_tone, voiced_fricative_formant_dict[phoneme][0],
                                                    width) + laryngeal_tone * 0.02, slice_size) + filtered_noise

    # TODO: Finish this
    @classmethod
    def consonant(cls, phoneme, base_tone, freq, length=0.06, width=0.2):
        laryngeal_tone = Larynx.get_base_tone(freq, length) if not cls.whisper else Noise.get_noise(length)
        noise_tone = Noise.get_noise(length)
        consonant_tone = np.zeros(len(laryngeal_tone))

        if phoneme in unvoiced_consonants_formant_dict:
            pass
        elif phoneme in voiced_consonants_formant_dict:
            pass

        result = base_tone
        for i in range(len(consonant_tone)):
            result[i] = consonant_tone[i] * (1 - i / len(consonant_tone))

        return result


