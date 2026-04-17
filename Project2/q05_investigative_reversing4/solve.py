files = [
    "Item05_cp.bmp",
    "Item04_cp.bmp",
    "Item03_cp.bmp",
    "Item02_cp.bmp",
    "Item01_cp.bmp",
]

result = []

for fname in files:
    with open(fname, "rb") as f:
        data = f.read()

    i = 2019
    for _ in range(10):
        value = 0
        for bit in range(8):
            value |= (data[i + bit] & 1) << bit
        result.append(value)
        i += 12   # 8 bytes used for bits, then skip 4 bytes

flag = bytes(result).decode(errors="ignore")
print(flag)
