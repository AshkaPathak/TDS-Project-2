# Blockchains in Practice: The Precision Transfer

## Method

I funded a Solana Devnet fee payer from the official faucet, then used `@solana/web3.js` to build a two-instruction transaction: a System Program transfer for exactly `19679000` lamports and a Solana Memo Program v2 instruction containing `006A-994A`. After confirmation, I queried the transaction with `getParsedTransaction` to verify the destination, amount, memo, and successful status.

## Answer

Transaction signature (Solana Devnet):

```text
5gAhWYVV6JdU7YJraVz8WhoLbgfMBjYSHdpDcQcK5MjL4c5BPbeoL8nK31xNSqPFNazMCR3pisJk3JP2JiPt8mgz
```

Details:
- Amount: `0.019679 SOL` (`19679000` lamports)
- Destination vault: `BCJCAvSV89tnGqhFSG2uD8azeQLQ5Hypn9CQyWEN7VEH`
- Memo: `006A-994A`
- Memo program: `MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr`
