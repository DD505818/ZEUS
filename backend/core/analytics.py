import pandas as pd


def calc_ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def calc_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calc_macd(
    series: pd.Series, span_fast: int = 12, span_slow: int = 26, span_signal: int = 9
) -> pd.Series:
    exp1 = series.ewm(span=span_fast, adjust=False).mean()
    exp2 = series.ewm(span=span_slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal = macd_line.ewm(span=span_signal, adjust=False).mean()
    return macd_line - signal


def heikin_ashi(df: pd.DataFrame) -> pd.DataFrame:
    ha = pd.DataFrame(index=df.index)
    ha["close"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4
    ha["open"] = ((df["open"].shift() + df["close"].shift()) / 2).fillna(df["open"])
    ha["high"] = df[["high", "open", "close"]].max(axis=1)
    ha["low"] = df[["low", "open", "close"]].min(axis=1)
    return ha
