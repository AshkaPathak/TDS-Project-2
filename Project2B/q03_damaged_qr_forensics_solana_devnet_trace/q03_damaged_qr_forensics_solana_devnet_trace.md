# Damaged QR Forensics: Solana Devnet Trace

## Method

I cropped and thresholded the damaged QR image, reconstructed it as a Version 1 QR grid, decoded the visible byte-mode payload, and inserted the recovered 7-character fragment into the masked Solana signature. The first completed signature exposed one screenshot transcription issue (`X` vs `x`), so I checked base58 one-character variants against Devnet until the valid finalized transaction was found. I then queried the parsed transaction and extracted the System Program transfer fields.

## Answer

Recovered QR fragment:

```text
v9g3r3H
```

Completed Solana Devnet signature:

```text
4MRPDdumS2Tm1s938hprAebmnSheXukE8vY3Ds4ZgkCYArjSv9g3r3HWYrqLzKzpyjWzoAb9RLiixHk1eowSe4aC
```

Submission payload:

```json
{
  "from": "5ShNwvPJo5xRnTVqAjx7EM1Ekt3rrsinbPBKeAa4wxsV",
  "to": "BCJCAvSV89tnGqhFSG2uD8azeQLQ5Hypn9CQyWEN7VEH",
  "amount": "0.011799"
}
```
