# Project 2 — Q10: Surfing the Waves

## Problem Summary
The challenge provides a WAV file (main.wav) with hints indicating that the flag is hidden in the waveform data rather than the audible audio. The goal is to analyze the raw sample values and recover the hidden information.

## Step 1 — Inspect the WAV File
We read the WAV file using Python to understand its structure.

from scipy.io import wavfile
import numpy as np

rate, data = wavfile.read("main.wav")

print("Rate:", rate)
print("Shape:", data.shape)
print("Dtype:", data.dtype)
print("First 50 samples:", data[:50])
print("Unique values count:", len(np.unique(data)))

Observation:
- Samples are int16 values
- Values range roughly from 1000 to 8500
- Many unique values exist due to noise in the last digit

## Step 2 — Identify the Pattern
The values follow a pattern:
1000–1009
1500–1509
2000–2009
...
8500–8509

The last digit is noise, while the first two digits represent meaningful values.
Extracting the first two digits gives:
[10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]

There are exactly 16 values, indicating hexadecimal encoding.

## Step 3 — Convert Samples to Hex
We remove noise and map values to hex digits.

from scipy.io import wavfile

rate, data = wavfile.read("main.wav")
samples = data if len(data.shape) == 1 else data[:, 0]

symbols = [int(str(abs(int(x)))[:2]) for x in samples]
unique = sorted(set(symbols))

print("Unique symbols:", unique)

hex_string = "".join(hex(unique.index(s))[2:] for s in symbols)
print("First 100 hex chars:", hex_string[:100])

## Step 4 — Decode Hex to ASCII
decoded = bytes.fromhex(hex_string).decode(errors="ignore")
print(decoded)

The decoded output reveals the Python script used to generate the WAV file.

## Step 5 — Extract the Flag
The flag is present at the end of the decoded script:

picoCTF{mU21C_1s_1337_5db6b85e}

## Final Answer
picoCTF{mU21C_1s_1337_5db6b85e}

## Why This Works
The WAV file encodes hexadecimal digits using amplitude levels spaced by 500. Random noise is added to disguise the pattern. By removing the noise and mapping each level to a hex digit, we reconstruct the original hex stream and decode it to reveal the embedded script and flag.
