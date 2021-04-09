from core.render import write_file
from core.larynx import Larynx
from core.mouth import Mouth
from core.noise import Noise
from core.synth import vowel, unvoiced_fricative, voiced_fricative, nasal, lateral, silence
import numpy as np
import argparse
from playsound import playsound

freq = 86

phonemes = (voiced_fricative("DH", freq, 0.1), vowel("EH", freq, 0.1), lateral("R", freq, 0.2), vowel("W", freq, 0.1), vowel("IY", freq, 0.2), vowel("AA", freq, 0.2), lateral("R", freq, 0.15))

speech = Mouth.dual_fade(Mouth.connect_phonemes(phonemes, 2048), 64)

write_file("output.wav", speech, 0.7)
playsound("output.wav")
