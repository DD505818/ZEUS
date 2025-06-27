ZEUS°NXTLVL – AGENTS.md

This file provides shared context for all ZEUS°NXTLVL AI trading agents.
It instructs engineering agents (like Codex) how to contribute, test, and safely modify the `agents/` logic.

──────────────────────────────────────────────
📁 Directory Structure

Work on the following files/folders only:

/agents/
├── base_agent.py        → Abstract interface for all agents
├── ema_agent.py         → 50/200 EMA crossover logic
├── breakout_agent.py    → Heikin Ashi + quantum resonance
├── momentum_agent.py    → Volume + RSI/MACD-based agent
├── risk_agent.py        → Position sizing, risk rules

Also use if needed:
- zeus.py               → Main agent execution router
- backtest_engine.py    → Historical simulations
- tests/agents/         → Agent test specs

──────────────────────────────────────────────
✅ How to Validate Changes

1. Run agent unit tests:
   $ pytest tests/agents/

2. Run backtest:
   $ python backtest_engine.py --agent <AgentName>

3. Format & Lint:
   $ ruff check agents/
   $ black agents/

4. (Optional) Live test with PM2:
   $ pm2 start zeus.py --interpreter=python3 --name=<agent-name> -- --agent <AgentName>

──────────────────────────────────────────────
🧠 Agent Design Guidelines

- Inherit from BaseAgent
- Implement:
    - analyze_market(data)
    - generate_signal()
    - execute_trade(signal, portfolio)
- Signal must return: BUY, SELL, or HOLD
- Use self.logger.info() for critical steps
- Use async if connecting to live APIs

──────────────────────────────────────────────
🔐 Secrets & Internet Access

- Internet access is DISABLED by default.
- Use .env or environment variables — NEVER hardcode secrets.

──────────────────────────────────────────────
🛠 Setup Script (for CI or Codex container)

Example setup:

# Formatters
pip install black ruff

# Dependencies
pip install -r requirements.txt

# Testing
pip install pytest

Codex agents should follow AGENTS.txt and the rules in .github/workflows/agents.yml

──────────────────────────────────────────────
🚀 Deployment Rules

- Support dry_run mode for all agents
- NEVER live trade without risk control
- Every agent must be backtestable + log signals & PnL

──────────────────────────────────────────────
📝 PR Format

Use this for PR and commit titles:

  [agents/<AgentName>] Add feature XYZ
  [agents/<AgentName>] Fix bug in market logic

Each PR must:
- Include or update tests
- Include backtest results
- Pass all CI checks

──────────────────────────────────────────────
⚠️ Do NOT Touch:

- /infra/
- main.py
- .github/workflows/full_deploy.yml
- .env.example

──────────────────────────────────────────────
📜 Agent Registry

| Agent Name       | Description                           | Status         |
|------------------|----------------------------------------|----------------|
| BreakoutAgent    | Heikin Ashi + Quantum resonance        | ACTIVE         |
| EMAAgent         | 50/200 EMA crossover logic             | ACTIVE         |
| MomentumAgent    | RSI, MACD, volume trend logic          | ACTIVE         |
| RiskAgent        | Centralized risk control & sizing      | ACTIVE         |
| WhaleSniper      | High-volume whale detector             | EXPERIMENTAL   |
| ArbitrageAgent   | Cross-exchange spread scanner          | PLANNED        |

──────────────────────────────────────────────

This file is the primary rulebook for engineering agents (like Codex).
All code contributions to /agents/ must comply with this guide.
