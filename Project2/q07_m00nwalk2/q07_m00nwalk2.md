# Project 2 — Q07: m00nwalk2

## Problem Summary

The challenge provided four audio files: message.wav, clue1.wav, clue2.wav, and clue3.wav. The description stated that the last transmission contained a hidden message and that the clue files should help extract another flag from the WAV file. The goal was to recover the hidden flag from message.wav.

---

## Step 1 — File Inspection

First, I listed the files using the ls command. The output showed: clue1.wav clue2.wav clue3.wav message.wav.

Then I checked the file type using the file command on message.wav. The output confirmed: message.wav is a RIFF (little-endian) WAVE audio file, Microsoft PCM, 16 bit, mono, 48000 Hz.

This confirmed that the file was a standard WAV file suitable for audio-based analysis.

---

## Step 2 — Strings Analysis

I attempted to extract readable content using strings on all four WAV files. The output consisted of random characters and noise, with no readable flag or meaningful hints.

Conclusion: the flag was not directly embedded as plain text.

---

## Step 3 — Spectrogram Analysis

I generated spectrograms for all audio files using ffmpeg and inspected them.

Observation:
- No visible text or patterns
- No QR-like structures
- All spectrograms showed uniform low-frequency bands

Conclusion: this was not a spectrogram-text challenge.

---

## Step 4 — Identifying the Technique

Key observations:
- Challenge name: m00nwalk2
- Description mentions "transmission"
- Clues provided as WAV files
- No visible data in spectrogram

Inference:
- The challenge uses audio steganography
- The hidden data is embedded within the WAV file itself
- Extraction requires a password derived from clues

---

## Step 5 — Extract Hidden Payload

Using the clues, the correct password was identified as: hidden_stegosaurus.

Since steghide was not available via Homebrew on macOS, a compatible online steganographic decoder was used.

Procedure followed:
1. Uploaded message.wav
2. Entered password: hidden_stegosaurus
3. Decoded the hidden payload

---

## Step 6 — Retrieve the Flag

The extracted payload revealed the flag: picoCTF{the_answer_lies_hidden_in_plain_sight}.

---

## Why This Worked

This challenge required:
- Eliminating incorrect approaches like strings and spectrogram inspection
- Recognizing that the WAV file contained hidden steganographic data
- Using clues to derive the correct password
- Extracting the payload using a stego decoder

---

## Final Answer

picoCTF{the_answer_lies_hidden_in_plain_sight}

---

## Conclusion

The hidden message inside message.wav was successfully extracted using password-based audio steganography. The clues guided the correct approach, and decoding revealed the final flag.
