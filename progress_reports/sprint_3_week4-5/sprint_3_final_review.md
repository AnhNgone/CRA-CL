# Sprint 3 — Final Review (Tổng kết dự án)

**Thời gian:** Tuần 4–5 (06/08 – 19/08/2026)
**Đây là sprint tổng kết** — đánh giá cả output lẫn thái độ/ý thức/tinh thần làm việc trong suốt 5 tuần.

> **Trạng thái cập nhật lần này: 10/08/2026 (giữa Tuần 4)**, chưa phải cuối sprint (19/08). Mục 2–4 dưới đây
> phản ánh đúng thực tế đến thời điểm này, dựa trên kết quả đã chạy trong `notebooks/05_segmentation_profitability.ipynb`
> và các báo cáo trong `reports/` — không suy đoán cho phần chưa làm (dashboard, đóng gói cuối cùng). Mục 5–7
> (tự đánh giá thái độ, bài học, đề xuất) để trống có chủ đích vì đây là phần tự phản ánh cá nhân.

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
| 3–5 segment rủi ro có default rate tách biệt rõ rệt (kiểm định chi-square/CI) | ☑ | 5 segment (S1–S5), chi-square=7892.78, p<0.000001 — xem notebook 05 |
| Bảng cutoff analysis đầy đủ approval rate, bad rate, Expected Net Return | ☑ | `reports/figures/cutoff_table.csv`; đã sửa đúng công thức lãi theo kỳ hạn 3 năm (10/08) |
| 2 dashboard hoàn chỉnh, chạy được, đúng nội dung mục 6 PROPOSAL.md | ☐ | Chưa dựng — mới có data export (`dashboards/*.csv`), chưa có file `.pbix`/`.twbx` |
| Final Recommendation nêu rõ yếu tố rủi ro chính, đề xuất cutoff, giới hạn mô hình | ☑ | `reports/final_recommendation.md`, đã cập nhật số liệu cutoff/PSI mới nhất |
| Toàn bộ 6 deliverables ở mục 9 PROPOSAL.md đã đóng gói | ☐ | 5/6 có bản nháp hoàn chỉnh; còn thiếu Dashboard (xem mục 4.3) |

## 3. Deliverables hoàn thành trong sprint
- [reports/business_rules_policy.md](../../reports/business_rules_policy.md) — cutoff, business rules, policy
- [reports/final_recommendation.md](../../reports/final_recommendation.md) — yếu tố rủi ro, cutoff, giới hạn
- `reports/figures/psi_report.csv`, `cutoff_table.csv`, `business_rules.csv`, `cutoff_profitability_analysis.png`
- `notebooks/05_segmentation_profitability.ipynb` — segmentation, PSI, cutoff/profitability, business rules
- `dashboards/*.csv` — dữ liệu tổng hợp sẵn sàng cho 2 dashboard (**chưa dựng file dashboard thật**)

## 4. Tổng kết toàn dự án (5 tuần / 3 sprint)
### 4.1. So sánh kế hoạch vs thực tế
| Sprint | Kế hoạch (PROPOSAL.md) | Thực tế | Chênh lệch & nguyên nhân |
|---|---|---|---|
| Sprint 1 (Tuần 1–2) | Vintage filter, BRD, EDA, WOE/IV, feature engineering, loại biến leakage | Hoàn thành đúng phạm vi, nhưng sau đó phát hiện và phải sửa lại 1 số lỗi phương pháp luận (gộp `fico_range_low/high` thành `fico_mid`, chọn biến bị thực hiện sau split thay vì trước, `revol_util` bị sai dấu tương quan) — xem commit `50aa77b` | Cần thêm 1 vòng sửa lỗi trước khi model đủ tin cậy để bước sang Sprint 2; nguyên nhân: các lỗi này chỉ lộ ra khi đối chiếu kỹ hệ số model, không phát hiện được ở bước EDA ban đầu |
| Sprint 2 (Tuần 3) | Time-based split, LR + WOE baseline, LightGBM so sánh, chọn model chính, đạt AUC≥0.68/KS≥0.25 | Với 8 biến ban đầu (thừa kế từ Sprint 1) chưa đạt target (LR AUC 0.6516). Mở rộng candidate set 17→81 biến (thêm nhóm bureau + 3 biến tỷ lệ tự tạo) mới đạt: LightGBM AUC 0.7004/KS 0.2891 (đạt), LR AUC 0.6739/KS 0.2527 (đạt KS, thiếu 0.006 AUC). Đổi model chính sang LightGBM (chênh AUC vượt ngưỡng tự đặt 0.02) | Chênh lệch: cần mở rộng feature set ngoài kế hoạch ban đầu mới đạt success metrics — đúng như chẩn đoán đã ghi ở Sprint 1 review |
| Sprint 3 (Tuần 4–5, tính đến 10/08) | Segmentation, cutoff/profitability, business rules, risk report, 2 dashboard, final recommendation, đóng gói 6 deliverables | Segmentation (5 nhóm), cutoff analysis, 2 business rules, và PSI (vốn dự kiến để cuối) đã hoàn thành trong nửa đầu Tuần 4; phát hiện + sửa 1 lỗi phương pháp (Expected Net Return thiếu nhân kỳ hạn 3 năm, kéo theo sửa tiêu chí chọn cutoff) | Đúng tiến độ tính đến thời điểm cập nhật; phần còn lại (2 dashboard, rà soát report cuối, đóng gói) vẫn theo đúng kế hoạch dành cho Tuần 5, chưa thực hiện |

### 4.2. Success Metrics — đạt được vs mục tiêu (PROPOSAL.md mục 2)
| Metric | Mục tiêu | Kết quả thực tế | Đạt? |
|---|---|---|---|
| AUC-ROC | ≥ 0.68 | LightGBM 0.7004 (model chính); LR+WOE 0.6739 | ☑ (LightGBM) |
| KS Statistic | ≥ 0.25 | LightGBM 0.2891; LR+WOE 0.2527 | ☑ (cả hai) |
| Gini Coefficient | Report song song | LightGBM 0.4007; LR+WOE 0.3478 | ☑ (đã report) |
| Expected Net Return theo cutoff | So với baseline | Tại cutoff đề xuất (0.17): $133.67M vs $133.97M (duyệt ngẫu nhiên) trên test — uplift ≈0 (+$11.2M trên validation lúc chọn ngưỡng) | ☑ đã tính đủ (xem lưu ý về đường cong uplift phẳng trong business_rules_policy.md mục 1) |
| Bad rate tại approval rate cố định | So với duyệt ngẫu nhiên | Tại ~79% approval: 15.32% (theo score) vs 19.94% (ngẫu nhiên) | ☑ |
| Số lượng segment rủi ro | 3–5 nhóm | 5 nhóm, bad rate 6.59%→38.58%, chi-square p<0.000001 | ☑ |

### 4.3. Toàn bộ 6 deliverables (PROPOSAL.md mục 9)
1. ☑ Business Requirement Document (`reports/BRD.md`)
2. ☑ EDA & Risk Analysis Report (`reports/eda_risk_report.md`)
3. ☑ Risk Scoring Model (LightGBM + LR, `models/`, `reports/model_run_log.csv`)
4. ☑ Business Rules & Policy/Profitability Recommendation (`reports/business_rules_policy.md`)
5. ☐ Dashboard — data đã export (`dashboards/*.csv`), chưa dựng file Power BI/Tableau thật
6. ☑ Final Recommendation (`reports/final_recommendation.md`)

## 5. Đánh giá thái độ / ý thức / tinh thần làm việc
- Mức độ chủ động, tự học khi gặp vướng mắc:
- Tuân thủ deadline / cập nhật tiến độ minh bạch với mentor:
- Khả năng phản hồi feedback & điều chỉnh:
- Tinh thần hợp tác, đặt câu hỏi đúng lúc:
- Quản lý thời gian khi dự án bị trễ schedule (giải pháp đã áp dụng):

## 6. Bài học kinh nghiệm
-

## 7. Đề xuất cải thiện (nếu làm lại / dự án tiếp theo)
-

## 8. Tham chiếu
- [Tuần 4 — Báo cáo & daily log](week_4/week_4_summary.md)
- [Tuần 5 — Báo cáo & daily log](week_5/week_5_summary.md)
- [Sprint 1 Review](../sprint_1_week1-2/sprint_1_review.md)
- [Sprint 2 Review](../sprint_2_week3/sprint_2_review.md)
- [PROPOSAL.md](../../PROPOSAL.md)
