# Business Requirement Document

## 1. Business Problem

Ngân hàng và công ty tài chính tiêu dùng phải cân bằng hai mục tiêu đối nghịch khi xét duyệt khoản vay:

- **Tăng trưởng**: duyệt nhiều khoản vay để tăng doanh thu.
- **An toàn**: giảm tỷ lệ khách hàng vỡ nợ (default) để giảm chi phí nợ xấu.

Xét duyệt quá chặt làm mất khách hàng tốt và giảm doanh thu; xét duyệt quá lỏng làm tăng nợ xấu và chi phí
thu hồi. Hồ sơ khách hàng đa dạng về thu nhập, nghề nghiệp, lịch sử tín dụng, và các yếu tố này tác động
đồng thời, phi tuyến đến khả năng trả nợ — khó đánh giá chính xác chỉ bằng kinh nghiệm hoặc vài tiêu chí
đơn lẻ.

## 2. Goals & Success Metrics

**Mục tiêu**: xây dựng quy trình phân tích + mô hình risk scoring giúp chuyên viên tín dụng đánh giá mức độ
rủi ro khách hàng trước khi phê duyệt khoản vay, kèm báo cáo hỗ trợ ra quyết định chính sách duyệt.

| Loại | Metric | Mục tiêu |
|---|---|---|
| Kỹ thuật (model) | AUC-ROC | ≥ 0.68 (baseline ngành cho Lending Club thường 0.68–0.72) |
| Kỹ thuật (model) | KS Statistic | ≥ 0.25 |
| Kỹ thuật (model) | Gini Coefficient | Report song song với AUC |
| Nghiệp vụ | Expected Net Return theo cutoff | Với mỗi ngưỡng score: Interest Income kỳ vọng − Expected Loss, so với baseline không dùng score |
| Nghiệp vụ | Bad rate tại approval rate cố định | So sánh bad rate của nhóm được duyệt theo score vs. duyệt ngẫu nhiên, tại cùng approval rate |
| Nghiệp vụ | Số lượng segment rủi ro | 3–5 nhóm, mỗi nhóm có default rate tách biệt rõ rệt (kiểm định chi-square/CI) |

Không đặt mục tiêu "giảm X% default rate trong thực tế" vì dự án không triển khai lên hệ thống thật — chỉ
mô phỏng trên dữ liệu lịch sử (xem mục 3 — Assumptions).

## 3. Scope & Assumptions

**Trong phạm vi:**
- Data cleaning, EDA, WOE/IV cho tập `accepted` đã lọc theo vintage 2015–2017 (kỳ hạn 36 tháng).
- Risk Scoring Model: Logistic Regression + WOE (baseline) so sánh với LightGBM/XGBoost (challenger, kèm SHAP).
- Time-based train/validation/test split theo `issue_d`.
- Customer Segmentation theo dải risk score (3–5 nhóm) + kiểm định thống kê.
- Credit Policy & Profitability Analysis: cutoff analysis (approval rate, bad rate, Expected Net Return).
- Business Rules override (2–3 quy tắc dựa trên biến IV cao nhất).
- 4 báo cáo: BRD, EDA & Risk Analysis Report, Business Rules & Policy Recommendation, Final Recommendation.
- **2 Dashboard Power BI/Tableau** (file thật .pbix/.twbx): **Risk & Portfolio Dashboard** (Approval Rate, Default Rate, Top Risk Factors theo IV, Risk
  Distribution theo segment, bad rate/Expected Net Return theo cutoff) và **Customer Dashboard** (Customer
  Profile, Risk Score + Segment, Recommendation Approve/Review/Reject kèm top 3 yếu tố ảnh hưởng).

**Ngoài phạm vi:**
- Không triển khai lên hệ thống production, không reject-inference chuẩn xác (accepted và rejected khác
  schema — chỉ so sánh tham khảo).

**Giả định quan trọng:**
- **Vintage window 2015–2017, term 36 tháng**: đảm bảo khoản vay đã "chín" (matured) tại thời điểm thu thập
  dữ liệu (2018+), tránh censoring bias từ các khoản vay còn "Current".
- **Nhãn nhị phân**: chỉ giữ `loan_status` ∈ {Fully Paid, Charged Off}, loại Current/Late/In Grace Period.
- **Loại bỏ biến hậu-giải-ngân (leakage)** khỏi tập feature dự báo — các trường phát sinh sau khi khoản vay
  giải ngân (total_pymnt, recoveries, last_pymnt_d...) không được dùng làm predictor vì không có tại thời
  điểm xét duyệt. Các trường này chỉ được dùng riêng, ở mức tổng hợp, để đo lường outcome tài chính thực tế
  (LGD) phục vụ phân tích lợi nhuận — không rò rỉ vào model.
- **Dữ liệu lịch sử mô phỏng**: Lending Club là P2P lending Mỹ giai đoạn 2015–2017, đã ngừng mảng cho vay
  bán lẻ từ 2020 — kết quả mang tính minh họa phương pháp luận, cần kiểm định thêm (A/B test, giám sát
  Population Stability Index) nếu áp dụng vào hệ thống hoặc thị trường khác.

## 4. Data Dictionary (phụ lục)

Nguồn: **Lending Club Loan Data** (Kaggle), 2 file — `accepted_2007_to_2018Q4.csv` (bắt buộc) và
`rejected_2007_to_2018Q4.csv` (bắt buộc, chỉ dùng cho RQ5 — ước tính approval rate).

**Nhóm biến ứng viên (có tại thời điểm xét duyệt):**
`loan_amnt`, `emp_length` (→ derive `emp_length_years`), `home_ownership`, `annual_inc`, `purpose`, `dti`,
`delinq_2yrs`, `earliest_cr_line` (→ derive `credit_history_length`), `fico_range_low`/`fico_range_high`
(→ gộp thành `fico_mid`), `inq_last_6mths`, `open_acc`, `pub_rec`, `revol_bal`, `revol_util`, `total_acc`,
`addr_state`. `term` bị loại vì hằng số sau khi lọc vintage (chỉ còn 36 tháng).

`fico_range_low` và `fico_range_high` được **gộp thành một biến** `fico_mid = (low + high) / 2`: hai biến
chênh nhau đúng 4 điểm, tương quan gần như tuyệt đối và IV trùng khớp đến 7 chữ số thập phân — đây là một tín
hiệu bị tách đôi. Đưa cả hai vào Logistic Regression chỉ làm hệ số bị chia đôi (thực nghiệm: −0.4428 mỗi biến,
tổng −0.8856 ≈ `fico_mid` −0.8858) mà không thêm thông tin, đồng thời phá khả năng diễn giải của scorecard.

**Chọn biến vào model:** shortlist theo `IV > 0.02` (Siddiqi 2006) được tính **sau time-based split và chỉ
trên tập train** (notebook 03). Đây là điểm đã sửa so với bản đầu — trước đó shortlist tính trên toàn bộ
vintage nên đã dùng cả nhãn của kỳ test; sai lệch này có hậu quả thật (xem eda_risk_report.md mục 3.1).
Nhóm biến ứng viên không lọt shortlist vẫn được giữ trong `data/processed/` để phục vụ Customer Dashboard và
business rules, nhưng **không** được đưa vào model.

**Nhóm biến nhãn:** `loan_status` (Fully Paid / Charged Off → nhãn nhị phân default).

**Lưu ý về `grade`/`sub_grade`/`int_rate` — không dùng làm feature dự báo**: đây là *kết quả* từ mô hình
xét duyệt nội bộ của Lending Club (LC tự chấm grade rồi gán int_rate theo grade), không phải đặc điểm thô
của khách hàng. Nếu đưa vào làm predictor, model sẽ chủ yếu học lại grade của LC thay vì đánh giá rủi ro độc
lập từ hồ sơ gốc — làm sai lệch mục tiêu "xây risk scoring độc lập" và khiến AUC tăng ảo. `int_rate` (và
`grade` ở mức tham khảo) vẫn được giữ lại trong dữ liệu nhưng chỉ dùng làm **biến giá** để tính Expected Net
Return ở notebook 05, không đưa vào tập feature huấn luyện model.

**Nhóm biến hậu-giải-ngân bị loại khỏi feature dự báo (data leakage — xem `src/data/filter_vintage.py:LEAKAGE_COLUMNS`):**
`total_pymnt`, `total_pymnt_inv`, `total_rec_prncp`, `total_rec_int`, `total_rec_late_fee`, `recoveries`,
`collection_recovery_fee`, `last_pymnt_d`, `last_pymnt_amnt`, `next_pymnt_d`, `last_credit_pull_d`,
`out_prncp`, `out_prncp_inv`. Riêng `recoveries`/`total_pymnt` được đọc lại ở mức tổng hợp (aggregate) từ
raw CSV trong notebook 05 để tính LGD thực tế cho phân tích lợi nhuận — không đưa vào model.

**Nhóm biến từ `rejected` (chỉ cho RQ5, tham khảo):** `Amount Requested`, `Application Date`, `Risk_Score`
(xấp xỉ FICO — không cùng schema với `fico_range_low/high` của accepted), `Debt-To-Income Ratio`, `State`,
`Employment Length`.

Chi tiết đầy đủ từng trường: xem `docs/LCDataDictionary.xlsx`.
