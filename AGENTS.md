ZEUS°NXTLVL – AGENTS.md

This file provides shared context for all ZEUS°NXTLVL trading agents. It explains how to work with the agent modules that live directly in this repository.

──────────────────────────────────────────────
📁 Directory Structure

Agent code resides in the following top-level modules:
- `nxtlvl.py`              → collection of trading agents (QuantumBoostAgent, HeikinBreakout, etc.)
- `zeus_trade_engine.py`   → runs the agents and aggregates signals
- `zeus_quantum_boost.py`  → breakout detection helper
- `rsi_divergence_sniper.py`, `momentum_killswitch.py`, `risk_sentinel.py`
                           → supporting utilities
- `agent_db.py`            → persistence layer stub

Other scripts such as `main.py` demonstrate a simple execution loop. There is no dedicated `agents/` directory or test suite at present.

──────────────────────────────────────────────
✅ How to Validate Changes

1. Format & Lint the project
   $ ruff check .
   $ black .

2. Manual run
   $ python main.py

Unit tests are optional but may be added under a new `tests/` folder.

──────────────────────────────────────────────
🧠 Agent Design Guidelines

- Keep agents stateless when possible
- Use clear method names like `signal(data)` or `detect_*`
- Signals should return `BUY`, `SELL`, or `HOLD`
- Log important steps with `print()` or a logger

──────────────────────────────────────────────
🔐 Secrets & Internet Access

- Internet access is disabled by default
- Store secrets in a local `.env` file – do not commit new secret values

──────────────────────────────────────────────
🛠 Setup Example

```bash
pip install -r requirements.txt
pip install black ruff
```

──────────────────────────────────────────────
📝 PR Format

Use commit titles like:

  `[core] Add feature description`
  `[core] Fix issue description`

Include a short note about manual testing in each PR.

──────────────────────────────────────────────
⚠️ Do NOT Touch

- `deploy*.sh` scripts
- Existing `.env` file contents

──────────────────────────────────────────────
