from pysstv.color import Robot36
from scipy.io import wavfile

rate, data = wavfile.read("message_mono.wav")

sstv = Robot36(data, rate, 16)   # <-- FIX HERE
image = sstv.decode()

image.save("output.png")
print("Saved as output.png")
