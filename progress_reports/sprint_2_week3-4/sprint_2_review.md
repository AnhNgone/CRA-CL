# Sprint 2 Review — Risk Scoring Model

**Thời gian:** Tuần 3–4 (30/07 – 12/08/2026)

## 1. Mục tiêu Sprint (theo PROPOSAL.md mục 8)
- Time-based train/validation/test split theo `issue_d`
- Xây baseline: Logistic Regression trên biến đã WOE-transform
- Xây model so sánh: LightGBM hoặc XGBoost (kèm SHAP nếu chọn hướng này)
- Đánh giá bằng AUC-ROC, KS Statistic, Gini
- Chọn model chính cho dashboard, nêu lý do đánh đổi hiệu năng vs. khả năng giải thích

## 2. Đối chiếu Definition of Done
| Tiêu chí (PROPOSAL.md mục 8) | Đạt? | Ghi chú |
|---|---|---|
| AUC-ROC ≥ 0.68 và KS ≥ 0.25 trên tập test | ☐ | |
| Bảng so sánh đầy đủ 2 model (metric + thời gian train + độ giải thích) | ☐ | |
| Đã chọn 1 model chính, có ghi lại lý do lựa chọn | ☐ | |
| Kiểm tra ổn định bad rate giữa các giai đoạn train/test | ☐ | |

## 3. Deliverables hoàn thành trong sprint
- [notebooks/04_modeling.ipynb](../../notebooks/04_modeling.ipynb)
- Model artifact trong `models/`

## 4. So sánh kế hoạch vs thực tế
- Tiến độ thực tế so với PROPOSAL.md:
- Nguyên nhân chênh lệch (nếu có):

## 5. Vấn đề tồn đọng / rủi ro cho Sprint 3
-

## 6. Kế hoạch điều chỉnh cho Sprint 3
-

## 7. Tự đánh giá
- Điểm mạnh trong sprint:
- Điểm cần cải thiện:

## 8. Tham chiếu
- [Tuần 3 — Báo cáo & daily log](week_3/week_3_summary.md)
- [Tuần 4 — Báo cáo & daily log](week_4/week_4_summary.md)
- [Sprint 1 Review](../sprint_1_week1-2/sprint_1_review.md)
- [PROPOSAL.md](../../PROPOSAL.md)
