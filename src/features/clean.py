import numpy as np
import pandas as pd

WINSORIZE_COLS = ["annual_inc", "dti", "revol_bal"]


def parse_emp_length(x):
    if pd.isna(x):
        return np.nan
    if x == "< 1 year":
        return 0.0
    if x == "10+ years":
        return 10.0
    return float(x.split()[0])


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Loc term (hang so sau vintage filter), parse emp_length, tao credit_history_length + fico_mid.
    Phep tinh so hoc thuan tuy, khong fit tren du lieu -> an toan goi truoc hoac sau split.
    """
    df = df.copy()
    if "term" in df.columns:
        df = df.drop(columns=["term"])

    df["emp_length_years"] = df["emp_length"].apply(parse_emp_length)

    earliest_cr_line = pd.to_datetime(df["earliest_cr_line"], format="%b-%Y")
    df["credit_history_length"] = (
        (df["issue_d"].dt.year - earliest_cr_line.dt.year) * 12
        + (df["issue_d"].dt.month - earliest_cr_line.dt.month)
    )

    # fico_range_low/high chenh nhau dung 4 diem, tuong quan ~1 va IV trung khop den 7 chu so
    # thap phan -> day la MOT tin hieu bi tach doi. Dua ca hai vao Logistic Regression chi lam
    # he so bi chia doi (thuc nghiem: -0.4428 moi bien, tong -0.8856 ~ fico_mid -0.8858) ma
    # khong them thong tin, dong thoi pha kha nang dien giai cua scorecard.
    # Xem experiments/exp01_fico_mid.py va reports/eda_risk_report.md muc 3.1.
    df["fico_mid"] = (df["fico_range_low"] + df["fico_range_high"]) / 2

    return df.drop(columns=["emp_length", "earliest_cr_line", "fico_range_low", "fico_range_high"])


def winsorize(df: pd.DataFrame, bounds: dict | None = None) -> tuple[pd.DataFrame, dict]:
    """Cap WINSORIZE_COLS tai percentile 1st/99th. `bounds` truyen vao (vd tinh tu train) de
    tai su dung tren val/test, tranh fit rieng tren tung tap gay leakage nguong cat.

    Tra ve (df_clean, bounds) - bounds dung lai cho lan goi sau (vd val/test).
    """
    df = df.copy()
    bounds = dict(bounds) if bounds else {}
    for col in WINSORIZE_COLS:
        if col not in bounds:
            lo, hi = df[col].quantile([0.01, 0.99])
            bounds[col] = (lo, hi)
        lo, hi = bounds[col]
        df[col] = df[col].clip(lo, hi)

    return df, bounds
