import numpy as np
import pandas as pd

WINSORIZE_COLS = [
    "annual_inc", "dti", "revol_bal",
    "loan_to_income", "revol_bal_to_income", "tot_cur_bal_to_income",
]

RATIO_BASE_COLS = ["loan_amnt", "revol_bal", "tot_cur_bal"]


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


def add_ratio_features(df: pd.DataFrame) -> pd.DataFrame:
    """Tao bien ty le so voi annual_inc, tinh TRUOC buoc chon bien theo IV.

    IV la chi so don bien: neu tinh sau khi loc, cac bien goc IV thap (vd loan_amnt) se bi
    loai truoc khi kip tao ty le tu chung, du ty le do co the mang tin hieu manh hon
    (vd loan_to_income = payment-to-income, thuong la yeu to underwriting quan trong).
    annual_inc = 0 duoc coi la thieu du lieu (khong the tinh ty le), tra ve NaN.
    """
    df = df.copy()
    income = df["annual_inc"].replace(0, np.nan)
    df["loan_to_income"] = df["loan_amnt"] / income
    df["revol_bal_to_income"] = df["revol_bal"] / income
    df["tot_cur_bal_to_income"] = df["tot_cur_bal"] / income
    return df


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
