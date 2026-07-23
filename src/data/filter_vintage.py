import pandas as pd

# Post-origination fields — outcome of the loan, not known at approval time.
# See PROPOSAL.md mục 4.3 (data leakage). Review against LCDataDictionary
# before modeling — this list is not guaranteed exhaustive.
LEAKAGE_COLUMNS = [
    "total_pymnt",
    "total_pymnt_inv",
    "total_rec_prncp",
    "total_rec_int",
    "total_rec_late_fee",
    "recoveries",
    "collection_recovery_fee",
    "last_pymnt_d",
    "last_pymnt_amnt",
    "next_pymnt_d",
    "last_credit_pull_d",
    "out_prncp",
    "out_prncp_inv",
]

VINTAGE_START = "2015-01-01"
VINTAGE_END = "2017-12-31"
LOAN_TERM = " 36 months"
LABEL_STATUSES = ["Fully Paid", "Charged Off"]


def filter_vintage(
    df: pd.DataFrame,
    start: str = VINTAGE_START,
    end: str = VINTAGE_END,
    term: str = LOAN_TERM,
) -> pd.DataFrame:
    issue_d = pd.to_datetime(df["issue_d"], format="%b-%Y")
    mask = (
        (df["term"] == term)
        & (issue_d >= start)
        & (issue_d <= end)
        & (df["loan_status"].isin(LABEL_STATUSES))
    )
    out = df.loc[mask].copy()
    out["issue_d"] = issue_d.loc[mask]
    return out


def drop_leakage_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=[c for c in LEAKAGE_COLUMNS if c in df.columns])
