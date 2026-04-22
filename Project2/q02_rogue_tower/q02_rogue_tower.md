# Project 2 — Q2: Rogue Tower

## Problem Summary

The challenge provided a network capture (PCAP) file and required identifying a rogue cell tower, determining the compromised device, and recovering the exfiltrated flag from captured network traffic.

---

## Step 1 — Analyze Network Traffic

The PCAP file was opened using Wireshark. Initial filtering using HTTP traffic revealed multiple devices interacting with a remote server.

Filter used:

http

Observation:

- Multiple devices were making GET requests to `/api/register`
- One specific device was making repeated POST requests to `/upload`

This indicated suspicious behavior.

---

## Step 2 — Identify Compromised Device

From the packet list:

Source IP: 10.100.50.122  
Destination IP: 198.51.100.58  

This device was repeatedly sending POST requests to `/upload`, suggesting it was exfiltrating data.

Conclusion:

- Compromised device: 10.100.50.122  
- Rogue tower/server: 198.51.100.58  

---

## Step 3 — Extract Exfiltrated Data

Filter used:

http.request.uri contains "upload"

Each POST request was inspected using:

Right click → Follow → TCP Stream

Extracted payload chunks from multiple streams:

QFFWnZjF  
kxCCFJABm  
hbBFxUaKE  
FQAtFb1xX  
VgEHAAQBR  
Q==  

---

## Step 4 — Reconstruct Data

All chunks were combined in packet order:

QFFWWnZjfkxCCFJABmhbBFxUakEFQAtFb1xXVgEHAAQBRQ==

This appeared to be Base64-encoded data.

---

## Step 5 — Decode Base64

Decoding produced non-readable output, indicating additional encryption.

Command used:

echo "QFFWWnZjfkxCCFJABmhbBFxUakEFQAtFb1xXVgEHAAQBRQ==" | base64 --decode

This resulted in binary data, confirming another layer of encoding.

---

## Step 6 — Apply XOR Decryption

Since picoCTF flags follow the format:

picoCTF{...}

this known prefix was used to recover the XOR key.

Python script used:

import base64

cipher_b64 = "QFFWWnZjfkxCCFJABmhbBFxUakEFQAtFb1xXVgEHAAQBRQ=="
cipher = base64.b64decode(cipher_b64)

known = b"picoCTF{"
key = bytes(cipher[i] ^ known[i] for i in range(len(known)))

plain = bytes(cipher[i] ^ key[i % len(key)] for i in range(len(cipher)))

print(plain.decode())

---

## Step 7 — Recover Flag

Decryption output:

picoCTF{r0gu3_c3ll_t0w3r_dbc40831}

---

## Final Flag

picoCTF{r0gu3_c3ll_t0w3r_dbc40831}

---

## Conclusion

The challenge was solved by:

1. Inspecting network traffic using Wireshark  
2. Identifying suspicious POST /upload requests  
3. Extracting fragmented exfiltrated data  
4. Reconstructing the full Base64 string  
5. Decoding Base64 to obtain encrypted bytes  
6. Using known plaintext (picoCTF{) to recover XOR key  
7. Decrypting the data to obtain the final flag  

Final result:

Successful identification of rogue tower communication and recovery of the exfiltrated flag.
