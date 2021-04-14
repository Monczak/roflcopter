from core.render import write_file
from core.mouth import Mouth
from core.synth import Synth
from playsound import playsound

freq = 70
Synth.whisper = False

phonemes = (Synth.vowel("AA", freq, 0.2), Synth.vowel("IY", freq, 0.1), Synth.lateral("L", freq, 0.1), Synth.vowel("AO", freq, 0.25), Synth.voiced_fricative("V", freq, 0.15), Synth.vowel("IY", freq, 0.1), Synth.vowel("UW", freq, 0.2),)

speech = Mouth.dual_fade(Mouth.connect_phonemes(phonemes, 2048), 64)

write_file("output.wav", speech, 0.7)
playsound("output.wav")
