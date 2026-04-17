import json
import itertools
import os
import struct
import zlib
import subprocess

with open("bytes.json") as f:
    byte_list = json.load(f)

LEN = 16
ROWS = len(byte_list) // LEN
PNG_SIG = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]

def rebuild(key: str):
    result = [0] * len(byte_list)
    for i in range(LEN):
        shifter = int(key[i])
        for j in range(ROWS):
            result[(j * LEN) + i] = byte_list[(((j + shifter) * LEN) % len(byte_list)) + i]
    while result and result[-1] == 0:
        result.pop()
    return bytes(result)

def recover_candidates(known_positions):
    candidates = [set(range(10)) for _ in range(16)]
    for pos, expected in known_positions.items():
        col = pos % 16
        row = pos // 16
        valid = set()
        for k in range(10):
            src = ((row + k) * 16) + col
            if src < len(byte_list) and byte_list[src] == expected:
                valid.add(k)
        candidates[col] &= valid
    return candidates

def png_valid(data: bytes):
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return False
    pos = 8
    saw_iend = False
    try:
        while pos < len(data):
            if pos + 12 > len(data):
                return False
            ln = struct.unpack(">I", data[pos:pos+4])[0]
            typ = data[pos+4:pos+8]
            if pos + 12 + ln > len(data):
                return False
            chunk = data[pos+8:pos+8+ln]
            crc_stored = struct.unpack(">I", data[pos+8+ln:pos+12+ln])[0]
            crc_calc = zlib.crc32(typ)
            crc_calc = zlib.crc32(chunk, crc_calc) & 0xffffffff
            if crc_calc != crc_stored:
                return False
            pos += 12 + ln
            if typ == b"IEND":
                saw_iend = True
                break
        return saw_iend and pos == len(data)
    except Exception:
        return False

def decode_with_zbar(path):
    try:
        r = subprocess.run(["zbarimg", "--quiet", path], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    return None

# Step 1: recover first 8 digits from PNG signature
known = {}
for i, b in enumerate(PNG_SIG):
    known[i] = b

cands = recover_candidates(known)
first8 = ""
for i in range(8):
    if len(cands[i]) != 1:
        print(f"Digit {i} still ambiguous from signature: {sorted(cands[i])}")
    first8 += str(sorted(cands[i])[0])

print("First 8 digits:", first8)

# Step 2: use first 8 digits to recover width/height bytes at positions 16..23
width_height = []
for pos in range(16, 24):
    col = pos % 16
    row = pos // 16
    k = int(first8[col])
    src = ((row + k) * 16) + col
    width_height.append(byte_list[src])

print("Width/height bytes:", width_height)

# Step 3: assume standard monochrome PNG IHDR tail
# bit depth = 1, color type = 0, compression = 0, filter = 0, interlace = 0
ihdr_data = bytes(width_height + [1, 0, 0, 0, 0])
ihdr_crc = zlib.crc32(b'IHDR')
ihdr_crc = zlib.crc32(ihdr_data, ihdr_crc) & 0xffffffff
ihdr_crc_bytes = list(ihdr_crc.to_bytes(4, "big"))

# positions 8..32 are now fully known
known = {
    0: 0x89, 1: 0x50, 2: 0x4E, 3: 0x47, 4: 0x0D, 5: 0x0A, 6: 0x1A, 7: 0x0A,
    8: 0x00, 9: 0x00, 10: 0x00, 11: 0x0D,
    12: 0x49, 13: 0x48, 14: 0x44, 15: 0x52,
}
for i, b in enumerate(width_height, start=16):
    known[i] = b
for i, b in enumerate([1, 0, 0, 0, 0], start=24):
    known[i] = b
for i, b in enumerate(ihdr_crc_bytes, start=29):
    known[i] = b

cands = recover_candidates(known)

print("\nCandidate digits per position:")
for i in range(16):
    print(i, sorted(cands[i]))

# Step 4: brute force only unresolved positions
positions = [i for i in range(16) if len(cands[i]) > 1]
print("\nUnresolved positions:", positions)

os.makedirs("candidates", exist_ok=True)
found = []

if not positions:
    keys = ["".join(str(sorted(cands[i])[0]) for i in range(16))]
else:
    keys = []
    pools = [sorted(cands[i]) for i in positions]
    for combo in itertools.product(*pools):
        key = [str(sorted(cands[i])[0]) if len(cands[i]) == 1 else None for i in range(16)]
        for idx, pos in enumerate(positions):
            key[pos] = str(combo[idx])
        keys.append("".join(key))

print("Trying", len(keys), "candidate keys...")

for key in keys:
    data = rebuild(key)
    if png_valid(data):
        out = f"candidates/{key}.png"
        with open(out, "wb") as f:
            f.write(data)
        decoded = decode_with_zbar(out)
        print("Valid PNG:", key, decoded if decoded else "")
        found.append((key, decoded))

print("\nDone.")
print("Found:")
for item in found:
    print(item)
