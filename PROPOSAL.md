# Hệ thống đánh giá và chấm điểm rủi ro tín dụng vay tiêu dùng

**Loại hình:** Dự án cá nhân | **Thời lượng:** 6 tuần (kế hoạch gốc 5 tuần, gia hạn thêm vài ngày sang tuần 6) | **Dataset:** Lending Club Loan Data (Kaggle)

---

## 1. Business Problem

Ngân hàng và công ty tài chính tiêu dùng phải cân bằng hai mục tiêu đối nghịch:

- **Tăng trưởng**: duyệt nhiều khoản vay để tăng doanh thu.
- **An toàn**: giảm tỷ lệ khách hàng vỡ nợ (default) để giảm chi phí nợ xấu.

Nếu xét duyệt quá chặt → mất khách hàng tốt, giảm doanh thu.
Nếu quá lỏng → tăng nợ xấu, tăng chi phí thu hồi.

Thử thách:
- Hồ sơ khách hàng rất đa dạng về thu nhập, nghề nghiệp, lịch sử tín dụng,...
- Khả năng trả nợ chịu tác động đồng thời của nhiều yếu tố.
- Các yếu tố này có mối quan hệ phức tạp nên khó đánh giá chỉ bằng kinh nghiệm hoặc một vài tiêu chí đơn lẻ.

## 2. Project Goal

Xây dựng một **quy trình phân tích + mô hình risk scoring** giúp chuyên viên tín dụng đánh giá mức độ rủi ro của khách hàng trước khi phê duyệt khoản vay, kèm dashboard hỗ trợ ra quyết định.

**Trong phạm vi 6 tuần, dự án tập trung vào chiều sâu (1 pipeline hoàn chỉnh, chất lượng) thay vì chiều rộng (nhiều bảng, nhiều dashboard).**

### Success Metrics

| Loại | Metric | Mục tiêu |
|---|---|---|
| Kỹ thuật (model) | AUC-ROC | ≥ 0.68 (baseline ngành cho Lending Club thường 0.68–0.72) |
| Kỹ thuật (model) | KS Statistic | ≥ 0.25 |
| Kỹ thuật (model) | Gini Coefficient | Report song song với AUC |
| Nghiệp vụ | Expected Net Return theo cutoff | Với mỗi ngưỡng score: `Interest Income kỳ vọng − Expected Loss` so với baseline không dùng score |
| Nghiệp vụ | Bad rate tại approval rate cố định | So sánh bad rate của nhóm được duyệt theo score vs. duyệt ngẫu nhiên, tại cùng approval rate (ví dụ 80%) |
| Nghiệp vụ | Số lượng segment rủi ro | 3–5 nhóm, mỗi nhóm có default rate tách biệt rõ rệt (kiểm định bằng chi-square hoặc so sánh CI) |

Không đặt mục tiêu "giảm X% default rate trong thực tế" vì dự án không triển khai lên hệ thống thật — chỉ mô phỏng trên dữ liệu lịch sử.

## 3. Research Questions

1. Những yếu tố nào ảnh hưởng mạnh nhất đến khả năng default?
2. Có thể chia khách hàng thành bao nhiêu nhóm rủi ro có ý nghĩa thống kê và nghiệp vụ?
3. Trong nhóm khách hàng **đã được duyệt** (accepted loans), nếu thay đổi ngưỡng risk score (score cutoff) thì bad rate và approval rate trong nhóm còn lại thay đổi thế nào?
4. Với các ngưỡng cutoff khác nhau, đâu là điểm cân bằng hợp lý giữa **doanh thu kỳ vọng** (lãi suất thu được) và **rủi ro** (expected loss)? *(trả lời được trực tiếp nhờ dataset có `int_rate` — xem mục 5.2)*
5. Approval rate ước tính giữa hồ sơ được duyệt và bị từ chối khác nhau thế nào theo các đặc điểm chung (thu nhập, DTI, khu vực)? *(dùng bộ Reject Stats — xem mục 4.3, chỉ mang tính tham khảo do giới hạn dữ liệu)*

## 4. Dataset

**Lending Club Loan Data** (Kaggle) — nền tảng cho vay ngang hàng (P2P lending) tại Mỹ, hoạt động 2007–2020.

- **Cấu trúc đơn giản**: 1 bảng phẳng chính (accepted loans) → pipeline khả thi cho 1 người trong 6 tuần.
- **Có trục thời gian rõ ràng** (`issue_d` — ngày giải ngân) → làm được time-based train/test split đúng chuẩn.
- **Có `int_rate` (lãi suất) và `grade`/`sub_grade`** → tính được doanh thu kỳ vọng theo từng khoản vay, cho phép trả lời RQ4 ("cân bằng doanh thu và rủi ro") một cách định lượng thực sự.
- **`loan_status` cho định nghĩa default rõ ràng**: Fully Paid / Charged Off / Default / Current / Late...
- Có các biến thay thế cho "lịch sử tín dụng" tương tự bureau data: `earliest_cr_line`, `delinq_2yrs`, `open_acc`, `pub_rec`, `revol_bal`, `revol_util`, `total_acc`, `inq_last_6mths`.
- Có bộ dữ liệu **hồ sơ bị từ chối** (Reject Stats) riêng, cho phép phân tích Approval Rate ở mức tham khảo.

### 4.1. Các bảng/file sử dụng

| File | Nội dung | Mức độ ưu tiên |
|---|---|---|
| `accepted_2007_to_2018Q4.csv` (hoặc bản mới hơn) | Khoản vay đã giải ngân — đặc điểm khách hàng, `loan_status`, `int_rate`, `grade` | Bắt buộc |
| `rejected_2007_to_2018Q4.csv` | Hồ sơ bị từ chối — chỉ có ~9 trường chung (Amount Requested, DTI, Risk_Score xấp xỉ FICO, State, Employment Length...) | Bắt buộc (cho phân tích Approval Rate, RQ5) |

### 4.2. Giới hạn quy mô — chọn cửa sổ thời gian phù hợp

File `accepted` đầy đủ có ~2.9 triệu dòng, trải dài 2007–2020, kích thước hàng GB → **không xử lý toàn bộ trong 6 tuần**. Đề xuất giới hạn phạm vi:

- Chỉ lấy khoản vay có kỳ hạn 36 tháng, **issue_d trong khoảng 2015–2017** — đủ thời gian để đến thời điểm dữ liệu được thu thập (2018+), các khoản vay này đã "chín" (matured), tức là đã kết thúc vòng đời (Fully Paid/Charged Off), tránh hiện tượng **censoring** (khoản vay còn "Current" thì chưa biết kết cục cuối).
- Trong cửa sổ đó, chỉ giữ `loan_status` thuộc `{Fully Paid, Charged Off}` làm nhãn nhị phân (loại `Current`, `Late`, `In Grace Period`, `Default` xử lý riêng nếu còn thời gian).
- Kích thước sau lọc ước tính còn vài trăm nghìn dòng — khả thi để chạy trên máy cá nhân.

### 4.3. Giới hạn dữ liệu quan trọng (cần hiểu trước khi phân tích)

- **Reject Stats và Accepted Loans không cùng schema.** Reject file chỉ có `Risk_Score` (xấp xỉ FICO) trong khi accepted file có `fico_range_low/high` — cần kiểm tra độ tương thích giữa hai trường trước khi so sánh. Vì vậy phân tích Approval Rate ở RQ5 **chỉ mang tính xấp xỉ**, không phải reject-inference chuẩn xác (accepted/rejected vẫn là hai schema khác nhau, không thể ghép thành 1 model duyệt hoàn chỉnh).
- **`loan_status` không đối xứng theo thời gian**: khoản vay mới giải ngân gần thời điểm cắt dữ liệu sẽ thiên về "Current" (chưa có kết cục) — đây là lý do phải giới hạn về vintage đã "chín" như mục 4.2, nếu không sẽ bị **survivorship/censoring bias**.
- Tỷ lệ default (Charged Off) trong Lending Club dao động ~15–20% tùy vintage — mức mất cân bằng nhãn vừa phải, thuận lợi cho việc huấn luyện model.
- Lending Club đã ngừng mảng cho vay bán lẻ từ 2020 — đây là **dữ liệu lịch sử**, mô hình học từ hành vi vay P2P tại Mỹ giai đoạn 2015–2017, không nên suy rộng trực tiếp sang bối cảnh cho vay tiêu dùng khác (khác quốc gia, khác kênh phân phối) mà không kiểm định lại.
- Rủi ro **data leakage**: các trường phát sinh *sau khi* khoản vay được giải ngân — ví dụ `total_pymnt`, `total_rec_prncp`, `total_rec_int`, `recoveries`, `last_pymnt_d`, `out_prncp` — **không được đưa vào model dự báo** (đây chính là hậu quả của khoản vay, không phải đặc điểm tại thời điểm xét duyệt). Chỉ dùng các trường có tại thời điểm nộp hồ sơ (income, dti, fico, purpose, employment length, revolving utilization tính đến thời điểm vay, v.v.).

## 5. Scope

### 5.1. Data Analysis
- Data Profiling (missing value, phân bố biến, outlier) trên tập `accepted` đã lọc theo vintage
- Data Cleaning (xử lý missing, outlier, encoding categorical như `purpose`, `home_ownership`, `emp_length`)
- Feature Analysis: univariate + bivariate với `loan_status` (WOE/IV cho từng biến)
- Loại bỏ tường minh nhóm biến hậu-giải-ngân (post-origination) để tránh leakage — xem mục 4.3

### 5.2. Business Analysis
- **Risk Factor Analysis**: xếp hạng yếu tố ảnh hưởng bằng Information Value (IV) và feature importance từ model
- **Customer Segmentation**: chia nhóm rủi ro dựa trên **dải điểm risk score** (score-based binning)
- **Credit Policy & Profitability Analysis**: với mỗi ngưỡng score, tính:
  - Approval rate và bad rate tương ứng (gains table)
  - **Expected Net Return** = `Σ(int_rate × loan_amnt cho nhóm Good) − Σ(loan_amnt × LGD cho nhóm Bad dự đoán sai)` — đây là phân tích mới, khả thi nhờ có `int_rate`, giúp trả lời trực tiếp câu hỏi "chính sách nào cân bằng doanh thu và rủi ro"

### 5.3. Decision Support
- **Risk Scoring Model**:
  - Baseline: Logistic Regression trên biến đã WOE-transform (scorecard truyền thống — dễ giải thích, chuẩn ngành credit risk)
  - So sánh với: 1 model ML (LightGBM hoặc XGBoost), dùng SHAP để giải thích nếu chọn hướng này cho bản cuối
  - Quyết định cuối: chọn 1 model chính cho Dashboard, nêu rõ lý do đánh đổi giữa hiệu năng và khả năng giải thích
- **Approval Recommendation**: gán mức khuyến nghị (Approve / Review / Reject) theo dải score
- **Business Rules**: 2–3 quy tắc override đơn giản dựa trên biến có IV cao nhất (ví dụ: `dti` vượt ngưỡng hoặc `revol_util` quá cao → Review bắt buộc dù score tốt)

### 5.4. Validation Strategy
- **Time-based split** theo `issue_d`: train trên các quý đầu của cửa sổ 2015–2017, validate/test trên các quý sau — mô phỏng đúng kịch bản triển khai thực tế (dự báo tương lai từ dữ liệu quá khứ)
- Kiểm tra phân bố `loan_status` (bad rate) ổn định giữa các giai đoạn train/test, phát hiện sớm nếu có vintage effect bất thường

## 6. Dashboard

### 6.1. Risk & Portfolio Dashboard
- Approval Rate (ước tính từ accepted vs. reject stats), Default Rate, Average Loan Amount
- Top Risk Factors (theo IV)
- Risk Distribution theo segment
- Bad rate **và Expected Net Return** theo cutoff (biểu đồ cutoff analysis)

### 6.2. Customer Dashboard
- Customer Profile (thông tin cơ bản)
- Risk Score + Segment
- Recommendation (Approve / Review / Reject) kèm lý do chính (top 3 yếu tố ảnh hưởng đến score của khách hàng đó)

> Dashboard thứ 3 (nếu còn thời gian ở Tuần 5) có thể tách phần Profitability Analysis ra riêng — nhưng không cam kết trước.

## 7. Methodology

```
Business Understanding
        ↓
Data Understanding (chọn vintage window, rà soát leakage, đối chiếu schema accepted vs. rejected)
        ↓
EDA (univariate, bivariate, WOE/IV)
        ↓
Feature Engineering (loại biến hậu-giải-ngân, tạo credit_history_length từ earliest_cr_line)
        ↓
Time-based Train/Validation/Test Split
        ↓
Risk Scoring (Logistic Regression + WOE, đối chiếu với LightGBM/XGBoost)
        ↓
Model Evaluation (AUC, KS, Gini) + Cutoff / Profitability Analysis
        ↓
Segmentation & Business Rules
        ↓
Dashboard
        ↓
Business Recommendation
```

## 8. Kế hoạch Sprint (6 tuần, chia 3 sprint, mỗi sprint 2 tuần)

> Kế hoạch gốc là 5 tuần; lịch được gia hạn thêm vài ngày và làm tròn thành tuần 6 để giữ cấu trúc đều
> 2 tuần/sprint (thay vì 3 sprint không đều tuần như bản nháp ban đầu). Nội dung từng sprint dưới đây không đổi.

### Sprint 1 — Nền tảng dữ liệu & Business Understanding (Tuần 1–2)

**Nội dung:**
- Đọc data dictionary gốc (LCDataDictionary), làm rõ business problem
- Xác định vintage window (2015–2017, term 36 tháng), lọc dữ liệu accepted + rejected
- Viết Business Requirement Document
- Data Cleaning (missing, outlier, encoding categorical)
- EDA: univariate + bivariate với `loan_status`, tính WOE/IV
- Feature Engineering, loại bỏ tường minh nhóm biến hậu-giải-ngân (leakage)

**Tiêu chí hoàn thành (Definition of Done):**
- [ ] Dataset đã lọc theo vintage 2015–2017, nhãn `loan_status` chỉ còn `{Fully Paid, Charged Off}`
- [ ] Không còn biến hậu-giải-ngân (leakage) trong tập feature
- [ ] Có bảng WOE/IV cho toàn bộ biến ứng viên
- [ ] Business Requirement Document + EDA report (bản nháp) hoàn chỉnh

### Sprint 2 — Risk Scoring Model (Tuần 3–4)

**Nội dung:**
- Time-based train/validation/test split theo `issue_d`
- Xây baseline: Logistic Regression trên biến đã WOE-transform
- Xây model so sánh: LightGBM hoặc XGBoost (kèm SHAP nếu chọn hướng này)
- Đánh giá bằng AUC-ROC, KS Statistic, Gini
- Chọn model chính cho dashboard, nêu lý do đánh đổi hiệu năng vs. khả năng giải thích

**Tiêu chí hoàn thành (Definition of Done):**
- [ ] AUC-ROC ≥ 0.68 và KS ≥ 0.25 trên tập test
- [ ] Bảng so sánh đầy đủ 2 model (metric + thời gian train + độ giải thích)
- [ ] Đã chọn 1 model chính, có ghi lại lý do lựa chọn
- [ ] Kiểm tra ổn định bad rate giữa các giai đoạn train/test (phát hiện vintage effect)

### Sprint 3 — Business Analysis, Segmentation, Dashboard & Recommendation (Tuần 5–6)

**Nội dung:**
- Customer Segmentation theo dải risk score (3–5 nhóm)
- Cutoff/Profitability Analysis: approval rate, bad rate, Expected Net Return theo từng ngưỡng
- Thiết kế 2–3 Business Rules override dựa trên biến IV cao nhất
- Viết Risk Analysis Report (gộp với EDA report)
- Xây Dashboard (Risk & Portfolio, Customer) trên Power BI/Tableau
- Hoàn thiện Final Recommendation, review & đóng gói toàn bộ deliverables

**Tiêu chí hoàn thành (Definition of Done):**
- [ ] 3–5 segment rủi ro có default rate tách biệt rõ rệt (kiểm định chi-square/CI)
- [ ] Bảng cutoff analysis đầy đủ approval rate, bad rate, Expected Net Return
- [ ] 2 dashboard hoàn chỉnh, chạy được, đúng nội dung mục 6
- [ ] Final Recommendation nêu rõ yếu tố rủi ro chính, đề xuất cutoff, giới hạn mô hình
- [ ] Toàn bộ 6 deliverables ở mục 9 đã đóng gói

## 9. Deliverables

1. **Business Requirement Document** (bao gồm Data Dictionary như phụ lục, không tách riêng)
2. **EDA & Risk Analysis Report** (gộp EDA report và Risk Analysis report thành 1 tài liệu)
3. **Risk Scoring Model** (notebook + model artifact + bảng so sánh 2 model)
4. **Business Rules & Policy/Profitability Recommendation** (bao gồm cutoff analysis)
5. **Dashboard** (2 dashboard: Risk & Portfolio, Customer)
6. **Final Recommendation** (tóm tắt ngắn gọn: yếu tố rủi ro chính, đề xuất cutoff, giới hạn của mô hình)

## 10. Value

- Chuẩn hóa cách đánh giá rủi ro bằng risk score thay vì đánh giá thủ công/cảm tính.
- Cung cấp cơ sở định lượng (bad rate và expected net return theo cutoff) để đề xuất chính sách duyệt cân bằng cả rủi ro lẫn doanh thu — không chỉ dừng ở tối thiểu hóa default rate.
- Rút ngắn thời gian tổng hợp thông tin khách hàng nhờ Customer Dashboard.
- **Lưu ý**: đây là kết quả trên dữ liệu lịch sử mô phỏng (P2P lending Mỹ, 2015–2017), không phải triển khai thực tế — giá trị mang tính minh họa quy trình và phương pháp, cần kiểm định thêm (A/B test, giám sát Population Stability Index) nếu áp dụng vào hệ thống thật hoặc bối cảnh thị trường khác.

## 11. Tech Stack

| Công cụ | Vai trò cụ thể |
|---|---|
| Python (Pandas, Scikit-learn, LightGBM/XGBoost) | Data cleaning, feature engineering, modeling |
| SQL (SQLite, load từ CSV) | Lọc/truy vấn tập accepted theo vintage, join với reject stats trước khi đưa vào Python — không dùng SQL server thật vì nguồn dữ liệu gốc là file phẳng |
| Power BI hoặc Tableau | Dashboard |
| Jupyter Notebook | Phân tích & mô hình hóa |
| Git | Quản lý phiên bản code |

## 12. Rủi ro & Giới hạn dự án (Limitations)

- Phân tích Approval Rate (RQ5) chỉ mang tính xấp xỉ do schema giữa accepted và rejected không hoàn toàn tương thích (không phải reject-inference model chuẩn xác).
- Giới hạn phạm vi vào vintage 2015–2017 giúp tránh censoring nhưng đồng nghĩa mô hình chưa phản ánh hành vi vay gần đây nhất trong dữ liệu gốc.
- Đây là dữ liệu P2P lending tại Mỹ (đã ngừng hoạt động bán lẻ từ 2020) — kết quả mang tính minh họa phương pháp, cần thận trọng khi khái quát hóa sang bối cảnh ngân hàng truyền thống hoặc thị trường khác.
- Model được đánh giá bằng time-based split trên cùng một giai đoạn lịch sử, chưa kiểm định qua các chu kỳ kinh tế khác nhau (ví dụ khủng hoảng) do giới hạn thời gian dự án.
- Business Rules đề xuất mang tính minh họa phương pháp, cần chuyên gia nghiệp vụ thực tế rà soát trước khi áp dụng.
