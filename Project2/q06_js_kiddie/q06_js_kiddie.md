# Project 2 — Q06: Java Script Kiddie

## Problem Summary
We were given a web challenge instance with the hint that it was only a JavaScript problem. The page showed a broken image, an input box, and a submit button. The goal was to reconstruct the hidden image correctly and recover the flag.

## Step 1 — Inspect the Client-Side JavaScript
Opened the challenge page in the browser and inspected the source using Developer Tools. The important JavaScript logic was:

function assemble_png(u_in){
    var LEN = 16;
    var key = "0000000000000000";
    var shifter;
    if(u_in.length == LEN){
        key = u_in;
    }
    var result = [];
    for(var i = 0; i < LEN; i++){
        shifter = key.charCodeAt(i) - 48;
        for(var j = 0; j < (bytes.length / LEN); j++){
            result[(j * LEN) + i] = bytes[(((j + shifter) * LEN) % bytes.length) + i];
        }
    }
    while(result[result.length-1] == 0){
        result = result.slice(0,result.length-1);
    }
    document.getElementById("Area").src = "data:image/png;base64," + btoa(String.fromCharCode.apply(null, new Uint8Array(result)));
    return false;
}

From this, it was clear that:
- the file bytes were already loaded into a JavaScript array named `bytes`
- the 16-digit input acted as a per-column shift key
- the output was reconstructed into a PNG image
- the correct solution required recovering the exact 16-digit key

## Step 2 — Extract the Raw Byte Array
In the browser console, copied the entire `bytes` array using:

copy(JSON.stringify(bytes))

Then saved it locally into a file named `bytes.json` using terminal:

pbpaste > bytes.json

This gave the exact byte array used by the challenge instance.

## Step 3 — Recover the First 8 Digits of the Key
The reconstructed file had to be a valid PNG, so its first 8 bytes had to match the standard PNG signature:

89 50 4E 47 0D 0A 1A 0A

Using these known bytes and the column-based shifting logic, the first 8 digits of the key were recovered as:

16258822

The width and height bytes extracted from the PNG header were:

[0, 0, 1, 114, 0, 0, 1, 114]

This meant the image size was 370 × 370.

## Step 4 — Recover Remaining Key Digits
A Python script was used to:
- rebuild candidate PNGs from `bytes.json`
- use the PNG header and IHDR structure to constrain key digits
- validate candidate outputs as real PNG files
- narrow the final candidates to only the valid one

The relevant result was:

First 8 digits: 16258822
Width/height bytes: [0, 0, 1, 114, 0, 0, 1, 114]

Candidate digits per position:
0 [1]
1 [6]
2 [2]
3 [5]
4 [8]
5 [8]
6 [2]
7 [2]
8 [0]
9 [3, 4]
10 [1, 2]
11 [6]
12 [9]
13 [6]
14 [3]
15 [5]

Unresolved positions: [9, 10]
Trying 4 candidate keys...
Valid PNG: 1625882204269635

So the correct 16-digit key for this instance was:

1625882204269635

## Step 5 — Reconstruct the Correct PNG
Using the recovered key, the PNG was reconstructed correctly. The final valid image file was:

candidates/1625882204269635.png

This image contained a QR code.

## Step 6 — Decode the QR Code
The QR code was decoded using:

zbarimg candidates/1625882204269635.png

This produced the final flag:

picoCTF{234446682bd071682ddd41d241ad24a0}

## Final Flag
picoCTF{234446682bd071682ddd41d241ad24a0}

## Conclusion
This challenge was solved entirely through client-side JavaScript analysis. The key insight was that the broken image was actually a scrambled PNG whose bytes were rearranged column-wise using a 16-digit numeric key. By extracting the raw byte array, exploiting the fixed PNG header structure, narrowing the possible key digits, validating reconstructed PNGs, and decoding the resulting QR code, the correct instance-specific flag was recovered successfully.
