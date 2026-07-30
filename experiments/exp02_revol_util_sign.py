"""Follow-up: gia thuyet multicollinearity FICO bi bac bo (revol_util van duong sau khi dung fico_mid).

Manh moi: IV cua revol_util fit TREN TRAIN chi 0.0146 < nguong 0.02, trong khi fit tren toan bo
vintage la 0.0247. Nghia la neu shortlist duoc tinh dung tren train (R5), revol_util da khong lot
vao model ngay tu dau. Kiem tra: (C) bo revol_util, va xem quan he WOE cua revol_util co don dieu khong.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from optbinning import BinningProcess
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve

PROCESSED = Path(r"c:\Users\PC\Documents\Credit Risk") / "data" / "processed"
train = pd.read_parquet(PROCESSED / "train.parquet")
val = pd.read_parquet(PROCESSED / "val.parquet")
test = pd.read_parquet(PROCESSED / "test.parquet")

for d in (train, val, test):
    d["fico_mid"] = (d["fico_range_low"] + d["fico_range_high"]) / 2


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

    lr = LogisticRegression(max_iter=1000)
    lr.fit(woe(train), train["bad_flag"])
    p = lr.predict_proba(woe(test))[:, 1]
    auc = roc_auc_score(test["bad_flag"], p)
    coefs = pd.DataFrame({"f": woe(train).columns, "c": lr.coef_[0]}).sort_values("c")
    n_bad_sign = int((coefs["c"] > 0).sum())
    print(f"\n{name}")
    print(f"  test AUC={auc:.4f}  KS={ks_stat(test['bad_flag'], p):.4f}  Gini={2*auc-1:.4f}"
          f"  he so sai dau: {n_bad_sign}/{len(coefs)}")
    for _, r in coefs.iterrows():
        print(f"    {r['f']:26s} {r['c']:+.4f}" + ("  <-- SAI DAU" if r["c"] > 0 else ""))
    return auc


B = ["fico_mid", "dti", "annual_inc", "home_ownership", "inq_last_6mths", "emp_length_years", "revol_util"]
C = [f for f in B if f != "revol_util"]

auc_b = run("B. fico_mid + revol_util (7 bien)", B)
auc_c = run("C. fico_mid, BO revol_util (6 bien) - ket qua neu shortlist tinh dung tren train", C)
print(f"\n  delta AUC (C - B) = {auc_c - auc_b:+.5f}")

# Quan he WOE cua revol_util co don dieu khong?
print("\n" + "=" * 70)
print("BANG BINNING revol_util (fit tren train) - kiem tra tinh don dieu")
print("=" * 70)
bp_single = BinningProcess(variable_names=["revol_util"])
bp_single.fit(train[["revol_util"]], train["bad_flag"])
tbl = bp_single.get_binned_variable("revol_util").binning_table.build()
print(tbl.to_string())

print("\n" + "=" * 70)
print("Tuong quan Pearson giua cac bien so (tren train)")
print("=" * 70)
num = ["fico_mid", "dti", "annual_inc", "inq_last_6mths", "emp_length_years", "revol_util"]
print(train[num].corr().round(3).to_string())
