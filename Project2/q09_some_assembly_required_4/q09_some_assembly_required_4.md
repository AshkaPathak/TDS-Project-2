# Project 2 — Q9: Some Assembly Required 4

## Problem Summary
The challenge provided a web page with a flag-checking input box. The title, “Some Assembly Required 4,” hinted that the main logic was hidden inside WebAssembly rather than normal JavaScript.

## Step 1 — Open the Website and Inspect Network
I opened the challenge website and used browser DevTools. In the Network tab, I noticed a JavaScript file and a hidden fetch request.

The JavaScript file contained logic that loaded a hidden WebAssembly file using:

fetch('./ZoRd23o0wd')

This showed that the real flag-checking logic was inside the WebAssembly binary.

## Step 2 — Download the WebAssembly File
Since wget was not installed on macOS, I used curl instead.

curl -o main.wasm http://wily-courier.picoctf.net:59321/ZoRd23o0wd

Then I verified the file type.

file main.wasm

Output confirmed:

main.wasm: WebAssembly (wasm) binary module version 0x1 (MVP)

## Step 3 — Convert WASM to WAT
To make the WebAssembly readable, I installed wabt and converted the binary to text format.

brew install wabt
wasm2wat main.wasm -o main.wat

## Step 4 — Search for Data and Exports
I searched for data sections and exported functions.

grep -n "data" main.wat
grep -n "export" main.wat

Important exported functions found:

export "strcmp"
export "check_flag"
export "copy_char"

Important data section found:

(data (;0;) (i32.const 1024) "\18j|a\118i7\1fYyY>\1cVc\0dB\1d~l9\1cZ!]c\11\00b\05IK~a4\1cW(\0fR\00\00")

This showed that encrypted comparison data was stored at memory offset 1024.

## Step 5 — Understand the Check Logic
Inside check_flag, the program transforms the user input stored at memory offset 1072.

At the end of the function, it compares:

memory offset 1024 = encrypted target data
memory offset 1072 = transformed user input

using strcmp.

So the correct approach was not to directly search for the flag string, because the flag was not stored plainly. Instead, the input transformation had to be reversed.

## Step 6 — Identify the Transformations
The WASM logic applied multiple operations to each input byte:

1. XOR with 20
2. XOR with previous transformed bytes
3. XOR with i % 10
4. XOR based on even/odd index
5. XOR based on i % 3
6. Final adjacent pair swap

Because XOR is reversible, these operations could be undone using Python.

## Step 7 — Reverse the Transformation
I wrote a Python script to reverse the transformation and recover the original flag.

cat > solve.py << 'PY'
enc = b"\x18j|a\x118i7\x1fYyY>\x1cVc\x0dB\x1d~l9\x1cZ!]c\x11\x00b\x05IK~a4\x1cW(\x0fR"

target = list(enc)
n = len(target)

# Undo final adjacent pair swap
for i in range(0, n - 1, 2):
    target[i], target[i + 1] = target[i + 1], target[i]

flag = []

for i in range(n):
    x = target[i]

    if i % 3 == 0:
        x ^= 7
    elif i % 3 == 1:
        x ^= 6
    else:
        x ^= 5

    if i % 2 == 0:
        x ^= 9
    else:
        x ^= 8

    x ^= (i % 10)

    if i > 2:
        x ^= target[i - 3]

    if i > 0:
        x ^= target[i - 1]

    x ^= 20

    flag.append(x)

print(bytes(flag).decode())
PY

python3 solve.py

## Step 8 — Output
The script printed:

picoCTF{1c4abb877272112e39233c05ade7abbb}

## Final Answer
picoCTF{1c4abb877272112e39233c05ade7abbb}

## Conclusion
The challenge hid the flag-checking logic inside a WebAssembly binary. The flag was not directly visible using strings or grep. By converting the WASM file to WAT, analyzing the check_flag function, identifying the encrypted data section, and reversing the XOR-based transformation plus final adjacent swap, the correct flag was recovered.
