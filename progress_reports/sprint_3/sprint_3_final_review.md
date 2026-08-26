# Sprint 3 — Final Review (Tổng kết dự án)

**Thời gian:** Tuần 5–6 (13/08 – 26/08/2026)

## 1. Mục tiêu Sprint 3 (theo PROPOSAL.md mục 8)
- Customer Segmentation theo dải risk score (3–5 nhóm)
- Cutoff/Profitability Analysis: approval rate, bad rate, Expected Net Return theo từng ngưỡng
- 2–3 Business Rules override dựa trên biến IV cao nhất
- Risk Analysis Report (gộp với EDA report)
- Dashboard (Risk & Portfolio, Customer) trên Power BI/Tableau
- Final Recommendation, review & đóng gói toàn bộ deliverables

## 2. Đối chiếu Definition of Done
| Tiêu chí (PROPOSAL.md mục 8) | Đạt? | Ghi chú |
|---|---|---|
| 3–5 segment rủi ro có default rate tách biệt rõ rệt (kiểm định chi-square/CI) | ☑ | 5 segment (S1–S5), chi-square=8012.81, p<0.000001, bad rate 6.61%→38.80% — hoàn thành tuần 4 (nay thuộc Sprint 2, số liệu cuối cùng sau tune 12/08), xem `dashboards/segment_summary.csv` và notebook 05 |
| Bảng cutoff analysis đầy đủ approval rate, bad rate, Expected Net Return | ☑ | `reports/figures/cutoff_table.csv`; đã sửa đúng công thức lãi theo kỳ hạn 3 năm (tuần 4) và cập nhật lại theo model đã tune (cutoff 0.19, xem [Sprint 2 Review](../sprint_2/sprint_2_review.md) mục 4b) |
| 2 dashboard hoàn chỉnh, chạy được, đúng nội dung mục 6 PROPOSAL.md | ☑ | `dashboards/CRDashboard.pbix` (2 trang: Risk & Portfolio Monitoring, Customer), dựng xong 26/08 từ data export đã có sẵn từ tuần 5 (`dashboards/*.csv`, gồm SHAP local explanation theo `customer_id` bổ sung 18/08) |
| Final Recommendation nêu rõ yếu tố rủi ro chính, đề xuất cutoff, giới hạn mô hình | ☑ | `reports/final_recommendation.md`, đã cập nhật theo model đã tune (AUC 0.7023/KS 0.2926, cutoff 0.19) và ghi rõ dashboard đã dựng ở mục "Giới hạn của mô hình" |
| Toàn bộ 6 deliverables ở mục 9 PROPOSAL.md đã đóng gói | ☑ | 6/6 hoàn chỉnh (xem mục 4.3) |

## 3. Deliverables hoàn thành trong sprint (Tuần 5–6)
- [reports/final_recommendation.md](../../reports/final_recommendation.md), [reports/business_rules_policy.md](../../reports/business_rules_policy.md) — cập nhật theo model đã tune (cutoff 0.19)
- `reports/figures/lightgbm_tuned_params.json`, `lightgbm_tuning_trials.csv`, `shap_importance.csv`, `psi_report.csv`, `cutoff_table.csv` — cập nhật theo feature set 34 biến
- `notebooks/04_modeling.ipynb` — cắt 6 feature nhiễu, tune LightGBM (chạy cuối tuần 4, commit đầu tuần 5)
- `notebooks/05_segmentation_profitability.ipynb` — bổ sung giải thích SHAP local theo từng khách hàng (`top_3_reasons`, `customer_id`) cho Customer Dashboard
- `progress_reports/` — rà soát và sửa lại toàn bộ timeline báo cáo (26/08): lịch 6 tuần/2 tuần mỗi sprint, sửa link hỏng, sửa nội dung tuần 6 bị trùng lặp tuần 4, điền các ngày trống theo bằng chứng git/notebook
- `dashboards/CRDashboard.pbix` — 2 trang Power BI (Risk & Portfolio Monitoring, Customer) dựng từ `dashboards/*.csv` — hạng mục cuối cùng, dự án nay đã đóng gói đủ 6/6 deliverable

## 4. Tổng kết toàn dự án (6 tuần / 3 sprint)
### 4.1. Success Metrics — đạt được vs mục tiêu (PROPOSAL.md mục 2)
| Metric | Mục tiêu | Kết quả thực tế (model cuối, tuned) | Đạt? |
|---|---|---|---|
| AUC-ROC | ≥ 0.68 | LightGBM 0.7023 (model chính); LR+WOE 0.6737 | ☑ (LightGBM) |
| KS Statistic | ≥ 0.25 | LightGBM 0.2926; LR+WOE 0.2520 | ☑ (cả hai) |
| Gini Coefficient | Report song song | LightGBM 0.4047; LR+WOE 0.3474 | ☑ (đã report) |
| Expected Net Return theo cutoff | So với baseline | Tại cutoff đề xuất (0.19, approval rate 62.7%): $148.4M vs $150.3M (duyệt ngẫu nhiên) trên test — uplift ≈ −$1.9M (đường cong uplift gần phẳng, xem business_rules_policy.md mục 1) | ☑ đã tính đủ, minh bạch cả khi uplift âm |
| Bad rate tại cutoff đề xuất | So với duyệt ngẫu nhiên | Tại cutoff 0.19 (approval rate 62.7%): 12.70% (theo score) vs 19.94% (ngẫu nhiên) | ☑ |
| Số lượng segment rủi ro | 3–5 nhóm | 5 nhóm, bad rate 6.61%→38.80%, chi-square=8012.81, p<0.000001 | ☑ |

### 4.2. Toàn bộ 6 deliverables (PROPOSAL.md mục 9)
1. ☑ Business Requirement Document (`reports/BRD.md`)
2. ☑ EDA & Risk Analysis Report (`reports/eda_risk_report.md`)
3. ☑ Risk Scoring Model (LightGBM + LR, `models/`, `reports/model_run_log.csv`)
4. ☑ Business Rules & Policy/Profitability Recommendation (`reports/business_rules_policy.md`)
5. ☑ Dashboard (`dashboards/CRDashboard.pbix` — 2 trang: Risk & Portfolio Monitoring, Customer)
6. ☑ Final Recommendation (`reports/final_recommendation.md`)

## 5. Tham chiếu
- [Tuần 5 — Báo cáo & daily log](week_5/week_5_summary.md)
- [Tuần 6 — Báo cáo & daily log](week_6/week_6_summary.md)
- [Sprint 1 Review](../sprint_1/sprint_1_review.md)
- [Sprint 2 Review](../sprint_2/sprint_2_review.md) (mục 4b — công việc tuần 4)
- [PROPOSAL.md](../../PROPOSAL.md)
