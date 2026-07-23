# Hệ thống đánh giá và chấm điểm rủi ro tín dụng vay tiêu dùng

Xem đầy đủ business problem, research questions, scope, sprint plan tại [PROPOSAL.md](PROPOSAL.md).

## Cấu trúc project

```
data/
  raw/          # CSV gốc từ Kaggle (accepted, rejected) — không commit
  interim/      # Sau khi filter vintage + loại leakage
  processed/    # Sẵn sàng cho modeling (đã WOE-transform, split)
notebooks/
  01_data_understanding.ipynb
  02_eda_woe_iv.ipynb
  03_feature_engineering_split.ipynb
  04_modeling.ipynb
  05_segmentation_profitability.ipynb
src/
  paths.py              # Đường dẫn dùng chung
  data/load.py           # Đọc raw CSV
  data/filter_vintage.py # Lọc vintage 2015-2017, loại biến leakage
  features/               # WOE/IV, feature engineering
  models/                 # Train/evaluate model
models/          # Model artifact đã train (.pkl) — không commit
reports/
  figures/                    # Biểu đồ xuất ra từ notebook
  BRD.md                      # Deliverable 1
  eda_risk_report.md          # Deliverable 2
  business_rules_policy.md    # Deliverable 4
  final_recommendation.md     # Deliverable 6
dashboards/      # File Power BI / Tableau — deliverable 5
docs/            # LCDataDictionary, tài liệu tham khảo
progress_reports/  # Nhật ký & báo cáo tiến độ theo ngày/tuần/sprint cho mentor — xem progress_reports/README.md
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Tải `accepted_2007_to_2018Q4.csv` và `rejected_2007_to_2018Q4.csv` từ [Kaggle - Lending Club Loan Data](https://www.kaggle.com/datasets/wordsforthewise/lending-club), bỏ vào `data/raw/`.

## Thứ tự chạy

1. `notebooks/01_data_understanding.ipynb` — load raw, đối chiếu schema accepted/rejected, lọc vintage, loại biến leakage, lưu `data/interim/`
2. `notebooks/02_eda_woe_iv.ipynb` — profiling, cleaning, WOE/IV
3. `notebooks/03_feature_engineering_split.ipynb` — feature engineering, time-based split, lưu `data/processed/`
4. `notebooks/04_modeling.ipynb` — train + so sánh model, lưu artifact vào `models/`
5. `notebooks/05_segmentation_profitability.ipynb` — segmentation, cutoff analysis, business rules, export cho dashboard
