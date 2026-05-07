# TDS Project 2

[![Course](https://img.shields.io/badge/course-Tools%20in%20Data%20Science-blue)](#)
[![Project](https://img.shields.io/badge/project-2-purple)](#)
[![Security](https://img.shields.io/badge/security-CTF%20writeups-red)](#)
[![Forensics](https://img.shields.io/badge/forensics-reversing%20%26%20signals-green)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A structured archive of TDS Project 2 writeups and artifacts. The repository covers web exploitation, network forensics, reverse engineering, signal analysis, WebAssembly inspection, blockchain traces, onion-site scraping, and Discourse/course-topic analysis.

## Highlights

| Area | Example | Method |
| --- | --- | --- |
| Web exploitation | [Crack the Gate](Project2/q01_crack_the_gate_1/README.md), [Power Cookie](Project2/q03_power_cookie/README.md), [SSTI2](Project2/q04_ssti2/README.md) | Inspect browser/client behavior, manipulate requests or cookies, and verify recovered flags. |
| Network forensics | [Rogue Tower](Project2/q02_rogue_tower/README.md) | Analyze captured traffic, reconstruct exfiltrated data, decode/decrypt payloads. |
| Reversing and WebAssembly | [Investigative Reversing 4](Project2/q05_investigative_reversing4/README.md), [Some Assembly Required 4](Project2/q09_some_assembly_required_4/README.md) | Inspect binaries/WASM, derive transformations, and decode hidden output. |
| Signal and side-channel analysis | [m00nwalk2](Project2/q07_m00nwalk2/README.md), [SideChannel](Project2/q08_sidechannel/README.md), [Surfing the Waves](Project2/q10_surfing_the_waves/README.md) | Use waveform, spectrogram, timing, or sample decoding to recover hidden data. |
| Project2B investigations | [Onion Scraping](Project2B/q01_onion_site_scraping_challenge/README.md), [Blockchain Precision Transfer](Project2B/q02_blockchains_precision_transfer/README.md), [Damaged QR Forensics](Project2B/q03_damaged_qr_forensics_solana_devnet_trace/README.md), [Discourse Analysis](Project2B/q04_discourse_system_commands_and_course_topics/README.md) | Preserve concise methods and final answer payloads for additional investigation tasks. |

## Structure

- [Project2/](Project2/README.md): primary Project 2 CTF/security questions
- [Project2B/](Project2B/README.md): additional investigation and data-trace questions
- Each question folder: README summary, detailed writeup, and supporting artifacts such as scripts, captures, images, audio, WASM, JSON, or generated outputs

## Responsible Use

The content is for course documentation, reproducibility, and learning. Use the methods in controlled or authorized environments only. Do not reuse exploit techniques against systems you do not own or have explicit permission to test.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes question-scoped, document verification, and avoid committing secrets or bulky regenerated artifacts unless required.

## License

MIT License. See [LICENSE](LICENSE).
