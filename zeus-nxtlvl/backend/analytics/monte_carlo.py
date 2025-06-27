from pathlib import Path
import pandas as pd
import numpy as np

CSV_PATH = Path(__file__).resolve().parents[3] / 'Zeus_Backtest_Results.csv'



def run_monte_carlo(simulations: int = 1000, periods: int = 252) -> float:
    """Run a simple Monte Carlo simulation based on historical ROI values."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Backtest results not found at {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    roi = df['ROI (%)'].astype(float) / 100.0
    mean_return = roi.mean() / periods
    std_return = roi.std() / np.sqrt(periods)
    total_returns = []
    for _ in range(simulations):
        daily_returns = np.random.normal(mean_return, std_return, periods)
        cumulative = np.prod(1 + daily_returns) - 1
        total_returns.append(cumulative)
    return float(np.mean(total_returns))


if __name__ == '__main__':
    avg_roi = run_monte_carlo()
    print(f"Expected ROI from Monte Carlo: {avg_roi*100:.2f}%")
