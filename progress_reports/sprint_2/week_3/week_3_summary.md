# Báo cáo Tuần 3 (30/07 – 05/08/2026)

**Sprint:** Sprint 2 — Risk Scoring Model (theo [PROPOSAL.md](../../../PROPOSAL.md) mục 8)
**Trọng tâm tuần 3:** Time-based split, baseline Logistic Regression (WOE), model so sánh (LightGBM/XGBoost)

## 1. Mục tiêu tuần
- [x] Time-based train/validation/test split theo `issue_d` (kế thừa từ Sprint 1, không đổi)
- [x] Xây baseline: Logistic Regression trên biến đã WOE-transform
- [x] Xây model so sánh: LightGBM hoặc XGBoost (kèm SHAP nếu chọn hướng này)
- [x] Đánh giá bằng AUC-ROC, KS Statistic, Gini

## 2. Công việc đã hoàn thành
- Mở rộng candidate feature set từ 17 lên 81 biến (thêm nhóm biến bureau: `verification_status`,
  `acc_open_past_24mths`, `mort_acc`, `bc_open_to_buy`, `tot_hi_cred_lim`, `avg_cur_bal`... và 3 biến tỷ lệ
  mới tạo: `loan_to_income`, `revol_bal_to_income`, `tot_cur_bal_to_income`) — 40/81 biến vượt ngưỡng IV > 0.02.
- Chạy lại Logistic Regression + WOE và LightGBM trên tập biến mở rộng.
- Chạy lại segmentation, cutoff/profitability analysis và business rules ở notebook 05 theo model mới.
- Phát hiện và sửa 1 bug hướng quy tắc business rule trước khi đưa vào dashboard (xem mục 5).

## 3. Kết quả / Deliverables
- `notebooks/03_feature_engineering_split.ipynb`, `notebooks/04_modeling.ipynb`, `notebooks/05_segmentation_profitability.ipynb` — đã chạy lại toàn bộ end-to-end
- `models/`: `logistic_regression_woe.pkl`, `lightgbm_model.txt`, `binning_process.pkl`, `primary_model.txt` (= LightGBM)
- `reports/figures/model_comparison.csv`: LightGBM AUC 0.7004 / KS 0.2891 (đạt cả 2 tiêu chí); LR + WOE AUC 0.6739 / KS 0.2527 (đạt KS, thiếu 0.006 để đạt AUC)
- `dashboards/`: segment_summary, cutoff_table, business_rules, iv_ranking_train, customer_dashboard_data — dữ liệu nền cho dashboard Sprint 3

## 4. Tình trạng so với kế hoạch
- [x] Vượt tiến độ
- Chi tiết chênh lệch: đạt mục tiêu AUC/KS đúng tuần 3; đồng thời làm luôn phần segmentation/cutoff mà kế hoạch mục 5 dự kiến để đầu Sprint 3.
- Nguyên nhân: hướng khắc phục (mở rộng feature set) đã được chẩn đoán đúng từ Sprint 1 nên không mất thời gian dò lại nguyên nhân, chỉ cần thực thi.
- Việc chưa làm: phân tích PSI (bước 5 trong kế hoạch mục 5 của sprint_2_review.md) — chuyển sang Sprint 3.

## 5. Vướng mắc & cách xử lý
- **9/40 hệ số Logistic Regression bị sai dấu** do đa cộng tuyến giữa các biến bureau mới (nhóm `open_il/rv_Xm`, `avg_cur_bal`/`tot_cur_bal`). Không xử lý ngay vì không ảnh hưởng model chính (LightGBM không nhạy đa cộng tuyến); để lại cho Sprint 3 nếu cần khôi phục LR làm scorecard dự phòng.
- **Bug hướng business rule**: code chọn biến rule tự động theo IV cao nhất giả định ngầm "giá trị càng cao càng rủi ro", nhưng biến mới `bc_open_to_buy` tương quan ngược (âm) với rủi ro. Nếu không phát hiện, rule sẽ bắt buộc Review nhầm nhóm khách hàng an toàn hơn. Cách xử lý: tính tương quan với `bad_flag` để xác định chiều rule trước khi đặt threshold, thêm assertion chặn tự động nếu uplift âm.

## 6. Kế hoạch tuần 4
- Viết lại narrative "model chính" trong BRD/EDA report — phản ánh đúng LightGBM + SHAP thay vì Logistic Regression + WOE như kết luận Sprint 1.
- Bổ sung phân tích PSI (Population Stability Index) còn nợ từ Sprint 2.
- Bắt đầu dựng Dashboard (Risk & Portfolio, Customer) trên Power BI/Tableau — dữ liệu nền đã sẵn sàng trong `dashboards/`.
- Chuẩn hoá công thức Expected Net Return (vấn đề tồn đọng từ Sprint 1: `int_rate` mới áp dụng 1 lần, chưa tính lãi tích luỹ theo kỳ hạn 3 năm).

## 7. Tham chiếu
- [PROPOSAL.md](../../../PROPOSAL.md)
- [Daily log tuần 3](daily_log.md)
