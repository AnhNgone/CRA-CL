"""Thi nghiem: thay cap fico_range_low/high (tuong quan ~1, IV trung khop) bang fico_mid.

Gia thuyet: he so revol_util_woe duong (+0.228) la he qua cua multicollinearity tu cap FICO,
khong phai quan he phi don dieu that su. Neu dung, bo fico_range_high -> revol_util ve dau am.

Chay lai dung pipeline notebook 03/04: BinningProcess fit CHI tren train, LR tren bien WOE.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from optbinning import BinningProcess
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve

ROOT = Path(r"c:\Users\PC\Documents\Credit Risk")
PROCESSED = ROOT / "data" / "processed"

train = pd.read_parquet(PROCESSED / "train.parquet")
val = pd.read_parquet(PROCESSED / "val.parquet")
test = pd.read_parquet(PROCESSED / "test.parquet")

BASE_FEATURES = [
    "fico_range_low", "fico_range_high", "dti", "annual_inc",
    "home_ownership", "inq_last_6mths", "emp_length_years", "revol_util",
]


def add_fico_mid(df):
    df = df.copy()
    df["fico_mid"] = (df["fico_range_low"] + df["fico_range_high"]) / 2
    return df


train, val, test = add_fico_mid(train), add_fico_mid(val), add_fico_mid(test)


def ks_stat(y, p):
    fpr, tpr, _ = roc_curve(y, p)
    return float(np.max(tpr - fpr))


def run(name, features):
    numeric = [c for c in features if pd.api.types.is_numeric_dtype(train[c])]
    categorical = [c for c in features if c not in numeric]

    bp = BinningProcess(variable_names=features, categorical_variables=categorical)
    bp.fit(train[features], train["bad_flag"])

    def woe(df):
        w = bp.transform(df[features], metric="woe")
        w.columns = [c + "_woe" for c in w.columns]
        return w

    Xtr, Xva, Xte = woe(train), woe(val), woe(test)
    ytr, yva, yte = train["bad_flag"], val["bad_flag"], test["bad_flag"]

    lr = LogisticRegression(max_iter=1000)
    lr.fit(Xtr, ytr)

    res = {}
    for split, X, y in [("train", Xtr, ytr), ("val", Xva, yva), ("test", Xte, yte)]:
        p = lr.predict_proba(X)[:, 1]
        auc = roc_auc_score(y, p)
        res[split] = (auc, ks_stat(y, p), 2 * auc - 1)

    coefs = pd.DataFrame({"feature": Xtr.columns, "coef": lr.coef_[0]}).sort_values("coef")

    print(f"\n{'=' * 70}\n{name}  ({len(features)} bien: {features})\n{'=' * 70}")
    for split, (auc, ks, gini) in res.items():
        print(f"  {split:5s}  AUC={auc:.4f}  KS={ks:.4f}  Gini={gini:.4f}")
    print("\n  He so Logistic Regression (ky vong TAT CA am theo quy uoc WOE):")
    for _, r in coefs.iterrows():
        flag = "  <-- SAI DAU" if r["coef"] > 0 else ""
        print(f"    {r['feature']:28s} {r['coef']:+.4f}{flag}")
    n_pos = int((coefs["coef"] > 0).sum())
    print(f"\n  So he so sai dau: {n_pos}/{len(coefs)}")

    # IV cua tung bien tren train (de doi chieu)
    summ = bp.summary()[["name", "iv"]].sort_values("iv", ascending=False)
    print("\n  IV (fit tren train):")
    for _, r in summ.iterrows():
        print(f"    {r['name']:28s} {r['iv']:.4f}")

    return res, coefs


print("Train/Val/Test:", len(train), len(val), len(test))
print("Bad rate:", f"{train.bad_flag.mean():.4f} / {val.bad_flag.mean():.4f} / {test.bad_flag.mean():.4f}")

res_a, coef_a = run("A. BASELINE - giu ca fico_range_low + fico_range_high", BASE_FEATURES)

features_b = ["fico_mid"] + [c for c in BASE_FEATURES if not c.startswith("fico_range")]
res_b, coef_b = run("B. THI NGHIEM - thay cap FICO bang fico_mid", features_b)

print(f"\n{'=' * 70}\nSO SANH (test set)\n{'=' * 70}")
print(f"  {'':12s} {'AUC':>9s} {'KS':>9s} {'Gini':>9s}  {'#he so sai dau':>15s}")
print(f"  {'A baseline':12s} {res_a['test'][0]:9.4f} {res_a['test'][1]:9.4f} {res_a['test'][2]:9.4f}"
      f" {int((coef_a['coef'] > 0).sum()):15d}")
print(f"  {'B fico_mid':12s} {res_b['test'][0]:9.4f} {res_b['test'][1]:9.4f} {res_b['test'][2]:9.4f}"
      f" {int((coef_b['coef'] > 0).sum()):15d}")
print(f"  {'delta (B-A)':12s} {res_b['test'][0] - res_a['test'][0]:+9.4f}"
      f" {res_b['test'][1] - res_a['test'][1]:+9.4f} {res_b['test'][2] - res_a['test'][2]:+9.4f}")
