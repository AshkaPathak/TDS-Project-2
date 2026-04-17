# Project 2 — Q05: Investigative Reversing 4

## Problem Summary
We were given one binary file named mystery and five bitmap image files: Item01_cp.bmp, Item02_cp.bmp, Item03_cp.bmp, Item04_cp.bmp, Item05_cp.bmp. The goal was to recover the hidden flag.

## Step 1 — Initial Inspection
Ran basic inspection commands: ls and file *.  
Observed that all five files were BMP images with identical dimensions (1765 x 852 x 8) and the file mystery was a Linux ELF executable. Since the system was macOS, the ELF binary could not be executed directly.

## Step 2 — Binary Analysis
Used strings mystery with filtering for relevant keywords. Found references like flag.txt, flag_index, flag_size, and a message saying the flag is not revealed locally. This confirmed the binary logic exists but the actual extraction must be done manually.

## Step 3 — Image Inspection
Ran strings on the BMP files and saw repetitive patterns like NOOOO and OOOOO. This indicated that the visible image content was not meaningful and the flag was likely hidden in the raw pixel data.

## Step 4 — Key Insight
The flag was encoded using least significant bit (LSB) steganography inside the BMP files. The decoding pattern was:
Start from byte offset 2019.
Take 1 bit from each of the next 8 bytes to form one character.
Skip the next 4 bytes.
Repeat this 10 times per file.
Process files in reverse order: Item05_cp.bmp → Item04_cp.bmp → Item03_cp.bmp → Item02_cp.bmp → Item01_cp.bmp.
Each file contributes 10 bytes, giving a total of 50 bytes.

## Step 5 — Extraction Logic
Wrote a Python script that reads each file in the correct order, extracts LSB bits from the required offsets, reconstructs bytes, and converts them into characters to form the flag.

Python logic (written in solve.py):
files = ["Item05_cp.bmp","Item04_cp.bmp","Item03_cp.bmp","Item02_cp.bmp","Item01_cp.bmp"]
result = []
for fname in files:
    data = open(fname, "rb").read()
    i = 2019
    for _ in range(10):
        value = 0
        for bit in range(8):
            value |= (data[i + bit] & 1) << bit
        result.append(value)
        i += 12
flag = bytes(result).decode(errors="ignore")
print(flag)

## Step 6 — Final Output
Running python3 solve.py produced:
picoCTF{N1c3_R3ver51ng_5k1115_000000000007f97676d}

## Final Flag
picoCTF{N1c3_R3ver51ng_5k1115_000000000007f97676d}

## Conclusion
This challenge required understanding that the binary was not directly usable and instead analyzing how data was hidden inside BMP files. By identifying the LSB encoding pattern and correct file order, the flag was successfully reconstructed.
