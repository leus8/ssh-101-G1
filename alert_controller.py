import numpy as np
import sounddevice as sd
from datetime import datetime

def trigger_alarm():
  print("Alarma generada!")

'''
function that prints text to indicate security central has been
contacted. Takes alarm input and outputs it to user
'''
def contact_central(alarm_type):
  print("Contactando central...")
  alarm_type_txt = "Tipo de alarma: " + alarm_type
  print(alarm_type_txt)
  now = datetime.now()
  print(now.strftime("%Y-%m-%d %H:%M:%S"))

# Two tone alarm
# tone 1 -> 500 Hz
# tone 2 -> 1200 Hz

'''
Function that generate the tone
'''
def gen_tone(f, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * f * t)
    return tone

'''
function that plays the two tones alarm
'''
def play_alarm(f1=500, f2=1200, duration=0.5, repeat=5):
    
    # sets the sample rate
    sr = 44100

    # generate tone 1
    tone1 = gen_tone(f1, duration, sr)

    # generate tone 2
    tone2 = gen_tone(f2, duration, sr)
    
    # play alarm
    # FIXME: [SW-11.6.1] and [SW-11.6.12] play until security code in entered
    for _ in range(repeat):
        sd.play(tone1, sr)
        sd.wait()
        sd.play(tone2, sr)
        sd.wait()

'''
function that plays the confirmation tone
'''
def confirmation_tone(f1=500, duration=0.5, repeat=5):
    
    # sets the sample rate
    sr = 44100

    # generate tone 1
    tone1 = gen_tone(f1, duration, sr)
    
    # play tone 1 for confirmation
    sd.play(tone1, sr)