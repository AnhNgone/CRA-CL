import pandas as pd

# Post-origination fields — outcome of the loan, not known at approval time.
# See PROPOSAL.md mục 4.3 (data leakage).
#
# Danh sach nay da duoc ra soat day du lai o Sprint 1 review (rui ro R1): ban dau chi co 13 cot
# nhom thanh toan, con sot 24 cot hau-giai-ngan trong data/interim. Nguy hiem nhat la
# last_fico_range_low/high — FICO cap nhat SAU giai ngan, voi khoan Charged Off thi diem nay da
# sup; dua nham vao model se day AUC len tren 0.85 (dau hieu leakage kinh dien).
LEAKAGE_COLUMNS = [
    # --- Dong tien / thanh toan ---
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
    "pymnt_plan",
    # --- Trang thai tin dung cap nhat sau giai ngan ---
    "last_fico_range_low",
    "last_fico_range_high",
    # --- Hardship program: chi phat sinh khi khoan vay da gap van de ---
    "hardship_flag",
    "hardship_type",
    "hardship_reason",
    "hardship_status",
    "deferral_term",
    "hardship_amount",
    "hardship_start_date",
    "hardship_end_date",
    "payment_plan_start_date",
    "hardship_length",
    "hardship_dpd",
    "hardship_loan_status",
    "orig_projected_additional_accrued_interest",
    "hardship_payoff_balance_amount",
    "hardship_last_payment_amount",
    # --- Debt settlement: ket cuc cua khoan vay ---
    "debt_settlement_flag",
    "debt_settlement_flag_date",
    "settlement_status",
    "settlement_date",
    "settlement_amount",
    "settlement_percentage",
    "settlement_term",
]

# Khong phai leakage, nhung cung KHONG duoc dung lam feature du bao: day la ket qua tu
# underwriting/van hanh noi bo cua Lending Club, khong phai dac diem tho cua khach hang.
# Dua vao model se khien model hoc lai grade cua LC thay vi danh gia rui ro doc lap.
# Xem BRD.md muc 4. int_rate/grade van duoc giu lai trong du lieu de tinh Expected Net Return.
LENDER_DECISION_COLUMNS = [
    "grade",
    "sub_grade",
    "int_rate",
    "installment",  # = f(loan_amnt, int_rate, term) -> da nhung int_rate ben trong
    "initial_list_status",
    "policy_code",
    "funded_amnt",
    "funded_amnt_inv",
]


def assert_no_leakage(features: list[str]) -> None:
    """Chan tap feature co chua bien hau-giai-ngan hoac bien quyet dinh cua ben cho vay.

    Co che bao ve chinh hien tai la whitelist (CANDIDATE_FEATURES liet ke tuong minh o
    notebook 02/03). Ham nay la lop chan thu hai, can thiet khi mo rong candidate set —
    luc do khong con doc tay tung ten bien duoc nua.
    """
    leaked = sorted(set(features) & set(LEAKAGE_COLUMNS))
    lender = sorted(set(features) & set(LENDER_DECISION_COLUMNS))
    problems = []
    if leaked:
        problems.append(f"bien hau-giai-ngan (leakage): {leaked}")
    if lender:
        problems.append(f"bien quyet dinh cua Lending Club: {lender}")
    if problems:
        raise AssertionError(
            "Tap feature khong hop le - " + "; ".join(problems)
            + ". Xem PROPOSAL.md muc 4.3 va BRD.md muc 4."
        )

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
