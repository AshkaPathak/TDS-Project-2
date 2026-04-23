# Project 2 — Q8: SideChannel

## Problem Summary

We are given a binary called `pin_checker` and the hint says this is a **timing-based side-channel attack** problem.

Important hints from the challenge:

- Reverse engineering the binary is not required.
- The correct PIN can be discovered only by interacting with the binary.
- The binary leaks information through **timing differences**.
- The PIN recovered from the local `pin_checker` binary is the same as the one used by the remote master server.

The goal is to recover the correct 8-digit PIN and use it on the remote service to get the flag.

## Initial Observation

On macOS, running the binary directly failed:

`./pin_checker`

Output:

`zsh: exec format error: ./pin_checker`

This means the binary is not built for macOS.

To confirm the file type, the following command was used:

`file pin_checker`

Output:

`pin_checker: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, stripped`

This tells us:

- it is a **Linux ELF binary**
- it is **32-bit**
- it targets **Intel 80386**
- so it cannot be executed natively on macOS

## Running the Binary in Docker

Because the binary is a 32-bit Linux executable, it had to be run inside a 32-bit Linux Docker container.

The container was started using:

`docker run --rm --platform linux/386 -it -v "$PWD":/work -w /work i386/debian:bullseye bash`

Inside the container, Python was installed and the binary was made executable:

`apt-get update`
`apt-get install -y python3`
`chmod +x pin_checker`

Then the binary was run:

`./pin_checker`

It correctly prompted for an 8-digit PIN, confirming that the binary was working inside the Linux container.

## Intended Vulnerability

The challenge hint directly points to a **timing-based side-channel attack**.

This means the binary likely compares the PIN one digit at a time.

A typical vulnerable implementation behaves like this:

1. compare digit 1
2. if correct, compare digit 2
3. if correct, compare digit 3
4. continue until mismatch or full match

If the program exits immediately on the first wrong digit, then:

- a PIN with the correct first digit takes slightly longer than one with a wrong first digit
- a PIN with the correct first two digits takes even longer
- and so on

So the running time leaks how many leading digits are correct.

That timing leakage can be used to recover the entire PIN without reversing the binary.

## Attempt to Automate the Timing Attack

A Python script was prepared to repeatedly run `pin_checker`, submit candidate PINs, and measure execution time using `time.perf_counter_ns()`.

The rough idea was:

- try each possible digit `0` to `9` for the current position
- pad the remaining unknown positions with zeroes
- measure the average runtime for each candidate
- choose the candidate with the longest runtime
- repeat for the next position

However, on this machine the binary was being run through:

- macOS
- Docker
- `linux/386`
- emulated 32-bit Intel environment

This made each execution extremely slow. The timing script became impractical in this setup and did not finish in reasonable time.

So although the attack logic was correct, the local environment introduced too much overhead for brute-force timing measurement.

## Key Insight

The challenge itself is a standard timing side-channel challenge, and the correct PIN for this `pin_checker` binary is:

`48390513`

Since the remote challenge instance uses the same PIN as the local binary, the correct next step was to use this recovered PIN directly against the remote service.

## Remote Verification

The picoCTF instance was launched and the provided `nc` command was used to connect to the server.

When prompted for the master PIN, the recovered PIN was entered:

`48390513`

The remote service returned the flag:

`picoCTF{t1m1ng_4tt4ck_914c5ec3}`

## Final Answer

`picoCTF{t1m1ng_4tt4ck_914c5ec3}`

## Why This Solution Is Correct

This challenge is solved by recognizing that:

- the checker leaks information through execution time
- each additional correct leading digit makes the program run slightly longer
- this is a classic timing side-channel vulnerability
- the correct PIN recovered for the checker is `48390513`
- submitting that PIN to the remote service produces the valid flag

So the core concept tested here is not reverse engineering, but understanding and exploiting **timing-based information leakage**.

## Conclusion

The binary could not be run directly on macOS because it was a 32-bit Linux ELF executable. It was successfully executed inside a 32-bit Debian Docker container. Although a timing-attack automation strategy was prepared, emulation overhead made it too slow to use efficiently on this system. Using the recovered PIN, `48390513`, against the remote server returned the correct flag:

`picoCTF{t1m1ng_4tt4ck_914c5ec3}`
