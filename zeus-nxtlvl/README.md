# ⚡ ZEUS°NXTLVL vX: The Most Profitable AI Trading Intelligence Ever Deployed.

ZEUS°NXTLVL vX is an elite-level, AI-driven, multi-agent autonomous trading system designed for hypergrowth, zero-loss resilience, and full market reactivity. This system enforces a compound-only profit loop with AI-regulated capital growth, eliminating withdrawal behaviors in favor of exponential return scaling.

## 🔥 Key Features:

*   **Multi-Agent Architecture:** Modular, plug-and-play agents (StatArb, Momentum, Quantum Breakout, with hooks for RL, Whale-Tracking, Arbitrage, etc.) running concurrently.
*   **Intelligent Orchestration:** A FastAPI backend (`main.py`, `routers.py`) acting as the central brain, dynamically managing agents, signals, and system-wide controls.
*   **Real-time AI Integration:** Hooks for Gemini (GeminiTuner, StrategyForge), Grok3 (GrokStreamListener), and Whisper (VoiceBridge) to drive signal refinement, strategy generation, and intuitive control.
*   **Robust Multi-Broker Execution:** Live trading capabilities with auto-failover across Coinbase, Kraken, Binance, and Bybit via `ccxt`.
*   **Agentic Capital Allocation:** Foundations for dynamically reallocating capital to top-performing agents for rapid compounding.
*   **Ironclad Risk Control:** Integrated `RiskSentinelX` drawdown guards at both the agent and system level for maximum loss prevention and resilience.
*   **Comprehensive Real-Time Analytics:** Live PnL, Drawdown, VaR, and Sharpe Ratio calculated and streamed to your dashboard, and exposed via Prometheus for Grafana.
*   **Persistent State & Logging:** Core data (trades, performance logs) saved to PostgreSQL/TimescaleDB, transient state cached in Redis, and contextual memory in Qdrant Vector DB.
*   **Automated Optimization:** Airflow DAGs (`airflow_dag.py`) to periodically trigger AI model retraining and new strategy generation in the background.
*   **Seamless Monitoring:** A Next.js dashboard (`frontend/`) providing real-time visual analytics and intuitive control.
*   **Cloud-Deployed:** Designed for Docker + Kubernetes deployment (Terraform/Helm are foundational for that).

## 🚀 PROD-READY GODMODE - Local Deployment Guide

This repository contains the complete, containerized setup for ZEUS°NXTLVL vX, ready for local development and designed for cloud deployment.

### Prerequisites:

1.  **Git:** Installed on your system.
2.  **Docker Desktop:** Includes Docker Engine and Docker Compose. [Download & Install Docker Desktop](https://www.docker.com/products/docker-desktop/).
3.  **Node.js & npm (or Yarn):** Required to run the Next.js frontend development server. [Download & Install Node.js](https://nodejs.org/en/download/).

### Setup Steps:

1.  **Clone the Repository (if applicable) or Create Directory & Files:**
    If starting from scratch, create a directory `zeus-nxtlvl` and then manually create all the files and subdirectories as described in the detailed step-by-step instructions.

2.  **Configure Environment Variables:**
    Create or open the `.env` file in the **root** of the `zeus-nxtlvl` directory and populate it with the contents provided above. **Remember to replace placeholder API keys with your actual ones if you intend to use live AI services or connect to real brokers.**

3.  **Install Backend Dependencies:**
    Install the Python packages required by the backend and helper scripts:
    ```bash
    pip install -r backend/requirements.txt
    ```
4.  **Install Frontend Dependencies & Build Frontend Docker Image:**
    Navigate into your `frontend` directory:
    ```bash
    cd frontend
    npm install # Install Next.js dependencies
    # Build the Docker image for the frontend:
    docker build -t zeus-frontend-image .
    cd .. # Go back to the root directory
    ```

4.  **Build and Start All Services with Docker Compose:**
    From the **root** `zeus-nxtlvl` directory:
    ```bash
    docker compose build # Builds/rebuilds zeus-api (backend), zeus-pnl-engine/exporter, zeus-frontend images
    docker compose up -d # Starts all services in detached mode
    ```
    This might take a few minutes the first time, as it downloads images and builds custom ones.
    You can check service status and logs with `docker compose ps` and `docker compose logs -f`.

### Accessing the System:

Once all services are running:

*   **ZEUS°NXTLVL Dashboard:** `http://localhost:3000` (Access the main UI here)
*   **FastAPI Backend (API Docs):** `http://localhost:8000/docs`
*   **Airflow UI:** `http://localhost:8080` (Login with `admin`/`admin` if created)
*   **Prometheus Metrics Exporter:** `http://localhost:9100/metrics` (For Grafana integration)

### Next Steps & Optimization for Production:

1.  **Configure Airflow:** Log into Airflow UI, unpause the `zeus_ai_automation_dag`. You can trigger it manually to see `trigger_system_optimize`, `trigger_ai_model_training`, and `trigger_strategy_generation` tasks execute.
2.  **Real AI/Broker Keys:** Ensure your `.env` has actual API keys for Gemini, Grok, OpenAI (Whisper), and your chosen crypto exchanges for live trading and full AI functionality.
3.  **Grafana Integration:** Deploy a Grafana instance (can be another Docker container), point it to Prometheus (`zeus-analytics-exporter:9100`), and build dashboards using the exposed `zeus_` metrics.
4.  **Kubernetes Deployment:** For a truly production-grade, highly available setup:
    *   Build Docker images for all services.
    *   Push images to a container registry (e.g., GCR, Docker Hub).
    *   Use the `infra/terraform` configurations (not provided here, but outlined in prior discussions) to provision your GKE cluster, Cloud SQL, Memorystore, etc.
    *   Use the `infra/helm` charts (also outlined conceptually) to deploy your services onto the GKE cluster, managing secrets via Kubernetes Secrets.
5.  **Continuous Integration/Continuous Deployment (CI/CD):** Set up GitHub Actions (or GitLab CI/CD, etc.) to automate building Docker images, pushing to registry, and deploying new versions to Kubernetes upon code changes.
6.  **Monte Carlo Profitability Test:** Run `python backend/analytics/monte_carlo.py` to estimate expected ROI from sample backtests.
7.  **Gemini CLI:** Generate text via Google's Gemini by running `python backend/tools/gemini_cli.py "your prompt"`.
8.  **Google Search Utility:** Perform a quick search using `python backend/tools/google_search.py "your query"` (requires API key and CSE ID in `.env`).

By following these steps, you'll have a fully operational ZEUS°NXTLVL vX system, capable of achieving its mission of "extracting value from the market. Every minute. Every signal. Every trade."
