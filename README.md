# Copy Simulator

A paper-copy-trading simulator for a public wallet on Robinhood Chain.

## Purpose

This project observes a public wallet's on-chain activity, identifies eligible token swaps, and simulates copying those swaps with a virtual portfolio.

It does not connect to a personal wallet, use private keys, sign transactions, or trade real funds.

## Current progress

- Downloads incoming and outgoing ERC-20 transfers for the watched wallet using Alchemy.
- Saves the raw API response locally for analysis.
- Groups transfer events by transaction hash.
- Counts incoming and outgoing token transfers.
- Identifies tokens with activity in both directions.
- Investigates routed transfers involving the Relay router.

## Next milestone

Create a candidate-swap filter that finds ERC-20 transfers from the watched wallet to the Relay router and prints a clear trade-candidate report.

## Project structure

- `src/connectors/`: External API and blockchain data access.
- `src/services/`: Trade classification and paper-trading logic.
- `src/database/`: Persistent simulated trades, positions, and portfolio data.
- `main.py`: Runs the analysis.
- `data/raw/`: Local raw API data; not committed to Git.