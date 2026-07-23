# EDA & Risk Analysis Report

Dữ liệu: Lending Club accepted loans, vintage 2015–2017, term 36 tháng, `loan_status` ∈ {Fully Paid,
Charged Off}. Sau lọc: **643,917 khoản vay**, bad rate (Charged Off) tổng thể = **17.70%**.

## 1. Data Profiling

- Missing value đáng kể chỉ ở `emp_length` (7.03%); `revol_util` (0.06%) và `dti` (0.02%) gần như đầy đủ.
  `emp_length` missing được giữ nguyên NaN (không impute) — optbinning tách thành bin riêng, tránh giả định
  sai lệch cho nhóm không khai báo.
- `term` là hằng số (chỉ " 36 months") sau khi lọc vintage — loại khỏi tập feature vì không mang thông tin.
- Outlier: `annual_inc`, `dti`, `revol_bal` được winsorize tại percentile 1st/99th (fit trên train, áp dụng
  lại cho val/test — xem mục Feature Engineering ở BRD.md).
- `dti` gốc có giá trị bất thường tới 999 (sentinel lỗi nhập liệu) — được xử lý bởi winsorize.

Biểu đồ: `reports/figures/univariate_numeric.png`, `bivariate_numeric_vs_bad.png`,
`bivariate_categorical_vs_bad.png`.

## 2. Risk Factor Analysis (IV / feature importance)

Information Value (WOE/IV) tính trên toàn bộ tập vintage (`optbinning.BinningProcess`), bảng đầy đủ tại
`reports/figures/iv_table.csv`:

| Biến | IV | Diễn giải |
|---|---|---|
| fico_range_low / fico_range_high | 0.147 | Mạnh nhất — điểm tín dụng FICO tại thời điểm vay |
| dti | 0.061 | Trung bình yếu |
| annual_inc | 0.053 | Trung bình yếu |
| home_ownership | 0.051 | Trung bình yếu |
| inq_last_6mths | 0.043 | Yếu |
| emp_length_years | 0.026 | Yếu |
| revol_util | 0.025 | Yếu |
| credit_history_length | 0.019 | Dưới ngưỡng |
| addr_state, purpose, revol_bal, total_acc, pub_rec, loan_amnt, delinq_2yrs, open_acc | < 0.02 | Không đủ sức dự báo đơn biến |

**Shortlist dùng cho model** (IV > 0.02, chuẩn Siddiqi 2006): `fico_range_low`, `fico_range_high`, `dti`,
`annual_inc`, `home_ownership`, `inq_last_6mths`, `emp_length_years`, `revol_util` (8/17 biến ứng viên).

Lưu ý: `fico_range_low` và `fico_range_high` có IV giống hệt nhau (tương quan gần như tuyệt đối, cách nhau
~4 điểm) — cả hai được giữ lại cho model nhưng mang thông tin trùng lặp, không phải 2 tín hiệu độc lập.

**SHAP feature importance** (từ LightGBM, `reports/figures/shap_feature_importance.png`):
`fico_range_low` (0.342) > `dti` (0.169) > `inq_last_6mths` (0.154) > `home_ownership` (0.147) >
`annual_inc` (0.086) > `emp_length_years` (0.047) > `revol_util` (0.029) > `fico_range_high` (~0, SHAP dồn
hết vào biến song sinh `fico_range_low`). Thứ hạng SHAP và IV khá nhất quán — FICO và DTI là 2 yếu tố rủi ro
hàng đầu.

**Lưu ý quan trọng**: `grade`/`sub_grade`/`int_rate` bị loại khỏi tập feature dự báo vì đây là *kết quả* từ
underwriting nội bộ của Lending Club, không phải đặc điểm thô của khách hàng (xem BRD.md mục 4). Điều này
khiến AUC thấp hơn so với các tutorial công khai có đưa grade vào làm feature.

## 3. Model Performance (AUC, KS, Gini)

Time-based split theo `issue_d`: Train (68.3%, đến 2016-08, bad rate 16.31%) / Validation (15.4%, đến
2017-03, bad rate 21.48%) / Test (16.3%, từ 2017-03, bad rate 19.94%).

**Phát hiện quan trọng — vintage effect**: kiểm định chi-square cho thấy bad rate khác biệt có ý nghĩa thống
kê giữa 3 giai đoạn (chi²=1916, p<0.0001). Đây là hiện tượng thật của dữ liệu Lending Club (chất lượng tín
dụng danh mục thay đổi theo thời gian phát hành), không phải lỗi pipeline — cần lưu ý khi diễn giải model
performance trên test set.

| Model | AUC (test) | KS (test) | Gini (test) | Đạt AUC≥0.68? | Đạt KS≥0.25? |
|---|---|---|---|---|---|
| Logistic Regression + WOE | 0.6534 | 0.2216 | 0.3068 | Không | Không |
| LightGBM | 0.6605 | 0.2297 | 0.3210 | Không | Không |

**Cả 2 model đều dưới mục tiêu đề ra trong PROPOSAL (AUC≥0.68, KS≥0.25).** Đây là kết quả trung thực sau khi
loại `grade`/`sub_grade`/`int_rate` (tránh leakage) — mức AUC 0.68–0.72 mà ngành thường trích dẫn cho
Lending Club thường bao gồm các biến này. Với chỉ 8 biến "tại thời điểm nộp hồ sơ" thực sự độc lập với
underwriting của LC, AUC ~0.65–0.66 là hợp lý.

**Ổn định theo quý trong tập test** (`reports/figures/model_stability_by_quarter.csv`): AUC dao động 0.64–0.66
qua 4 quý 2017, không có sụt giảm bất thường — mô hình ổn định về mặt phân biệt dù bad rate nền thay đổi.

**Chọn model chính**: chênh lệch AUC (LightGBM − LR) chỉ **0.0071** (< ngưỡng 0.02 tự đặt) → chọn
**Logistic Regression + WOE** làm model chính, ưu tiên khả năng giải thích/audit theo chuẩn ngành credit
risk, vì LightGBM không vượt trội đủ để đánh đổi lấy độ phức tạp.

Ghi chú kỹ thuật: 7/8 hệ số Logistic Regression âm (nhất quán với quy ước WOE — WOE cao = rủi ro thấp = xác
suất default thấp, nên hệ số dự báo `bad_flag` mang dấu âm). Riêng `revol_util_woe` có hệ số dương (+0.228),
là biến IV yếu nhất trong shortlist (0.025) — dấu hiệu quan hệ không đơn điệu/nhiễu, nên xem xét lại khi tinh
chỉnh model ở vòng sau, không ảnh hưởng lớn đến AUC tổng thể.

## 4. Customer Segmentation

5 nhóm theo ngũ phân vị (quintile) của `pd_score` (Logistic Regression) trên tập test:

| Segment | n | Bad rate | Avg PD score | Avg loan_amnt | Avg int_rate |
|---|---|---|---|---|---|
| S1 (rủi ro thấp nhất) | 21,041 | 8.41% | 6.67% | $14,068 | 8.70% |
| S2 | 21,041 | 14.66% | 11.15% | $13,071 | 11.54% |
| S3 | 21,040 | 19.61% | 14.70% | $12,092 | 13.18% |
| S4 | 21,042 | 24.70% | 18.59% | $11,016 | 14.32% |
| S5 (rủi ro cao nhất) | 21,040 | 32.34% | 25.83% | $10,204 | 15.94% |

Kiểm định chi-square: chi²=4448, p<0.000001 — **default rate tách biệt rõ rệt và có ý nghĩa thống kê giữa
5 segment**, đạt tiêu chí Success Metric của PROPOSAL (mục 2). Bad rate tăng đơn điệu từ S1→S5 (8.4%→32.3%,
chênh lệch gần 4 lần), cho thấy model phân tách rủi ro tốt dù AUC tuyệt đối chưa đạt mục tiêu.
