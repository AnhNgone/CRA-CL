# Báo cáo Tuần 5 (13/08 – 19/08/2026)

**Sprint:** Sprint 3 — Business Analysis, Segmentation, Dashboard & Recommendation (theo [PROPOSAL.md](../../../PROPOSAL.md) mục 8) 
**Trọng tâm tuần 5:** Dashboard, Risk Analysis Report, Final Recommendation, đóng gói toàn bộ deliverables

## 1. Mục tiêu tuần
- [ ] Dashboard (Risk & Portfolio, Customer) — phạm vi đã chốt (`BRD.md` nay ghi đúng 2 dashboard Power BI/Tableau là trong phạm vi, khớp `PROPOSAL.md` và kiến trúc đã nộp mentor; xem [Sprint 1 Review](../../sprint_1/sprint_1_review.md) mục 5). Việc còn lại của tuần 5 là dựng 2 dashboard thật (`.pbix`/`.twbx`)
- [ ] Risk Analysis Report (gộp với EDA report) — rà soát lại bản hiện có theo số liệu model cuối
- [x] Final Recommendation — cập nhật theo kết quả model sau khi mở rộng feature ở Sprint 2 (đã cập nhật theo model tuned cuối tuần 4, commit lên git 14/08, xem mục 2)
- [x] Tính lại Expected Net Return với dòng tiền đúng kỳ hạn 3 năm (thay công thức 1 kỳ hiện tại) — đã hoàn thành ở **tuần 4** (10/08), xem [week_4_summary.md](../../sprint_2/week_4/week_4_summary.md)
- [ ] Đóng gói toàn bộ 6 deliverables ở PROPOSAL mục 9

## 2. Công việc đã hoàn thành

- **Commit `5749e1d` (14/08)** đẩy lên git việc cắt 6 feature nhiễu (SHAP importance < 0.01, 40 → 34 biến)
  và tune lại hyperparameters LightGBM — bản thân việc chạy notebook đã thực hiện từ cuối tuần 4 (12/08, xác
  định qua timestamp thực thi nội bộ trong notebook), commit bị trễ 2 ngày; xem
  [week_4_summary.md](../../sprint_2/week_4/week_4_summary.md). Kết quả: LightGBM AUC/KS/Gini cải thiện lên
  0.7023/0.2926/0.4047; số hệ số Logistic Regression đổi dấu giảm từ 9/40 xuống 4/34; cutoff đổi 0.17→0.19.
  `final_recommendation.md`, `business_rules_policy.md` đã cập nhật theo cutoff/net-return của model đã tune.
- Rà soát và hoàn thiện report tuần 4 và tuần 5 (daily log + summary) (17/08).
- Bổ sung giải thích SHAP local (top 3 lý do ảnh hưởng đến score theo từng khách hàng) và `customer_id` vào
  `dashboards/customer_dashboard_data.csv` (18/08) — đáp ứng PROPOSAL mục 6.2. **Chưa commit** tính đến hết
  tuần 5.

## 3. Kết quả / Deliverables
- `notebooks/04_modeling.ipynb`, `notebooks/05_segmentation_profitability.ipynb` — cập nhật theo feature set 34 biến đã tune; bổ sung SHAP local explanation + `customer_id` (chưa commit).
- `reports/figures/lightgbm_tuned_params.json`, `lightgbm_tuning_trials.csv`, `shap_importance.csv` — mới/cập nhật.
- `reports/eda_risk_report.md`, `reports/final_recommendation.md`, `reports/business_rules_policy.md` — cập nhật theo model mới.
- `dashboards/*.csv` — refresh theo model đã tune, có thêm `customer_id`/`top_3_reasons`; `.pbix`/`.twbx` chưa dựng.

## 4. Tình trạng so với kế hoạch
- [ ] Đúng tiến độ  [x] Chậm hơn dự kiến  [ ] Vượt tiến độ
- Chi tiết chênh lệch: hết tuần 5, hạng mục dashboard (`.pbix`/`.twbx` thật) — phần việc lớn nhất của tuần —
  vẫn chưa bắt đầu; chỉ mới chuẩn bị xong dữ liệu nguồn (kể cả SHAP local explanation cho Customer Dashboard,
  18/08). Đóng gói 6 deliverables cũng chưa làm. Bù lại, model chính đã được cải thiện thêm (cắt feature
  nhiễu + tune LightGBM, dù việc này thực chất chạy từ cuối tuần 4).
- Nguyên nhân (nếu có chênh lệch): dựng dashboard Power BI/Tableau đòi hỏi thao tác trực tiếp trên ứng dụng
  GUI, không làm được qua notebook/code như các hạng mục khác — chưa sắp xếp được thời gian thao tác trong
  tuần.
- Kế hoạch bắt kịp: dồn việc dựng dashboard và đóng gói deliverables sang tuần 6 (tuần cuối, sprint tổng kết).

## 5. Vướng mắc & cách xử lý
- Dashboard Power BI/Tableau (`.pbix`/`.twbx`) chưa được dựng — chỉ có data export trong `dashboards/`
  (nay đã refresh theo model đã tune, có thêm cột giải thích theo khách hàng). Chuyển sang tuần 6.
- Thay đổi SHAP local explanation (18/08) tính đến hết tuần 5 vẫn chưa được `git commit`.

## 6. Tham chiếu
- [PROPOSAL.md](../../../PROPOSAL.md)
- [Daily log tuần 5](daily_log.md)
- [Sprint 3 Final Review](../sprint_3_final_review.md)
