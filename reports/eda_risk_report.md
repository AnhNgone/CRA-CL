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

Báo cáo dùng **hai bảng IV cho hai mục đích khác nhau** — phân biệt này quan trọng về phương pháp:

- `reports/figures/iv_table.csv` — fit trên **toàn bộ vintage**, dùng để trả lời RQ1 *"yếu tố nào ảnh hưởng
  mạnh nhất đến khả năng default trên toàn danh mục"*. Đây là câu hỏi mô tả, dùng hết dữ liệu là hợp lý.
- `reports/figures/iv_table_train.csv` — fit **chỉ trên tập train**, dùng để **chọn biến cho model**. Bắt buộc
  phải tách riêng: nếu chọn biến bằng IV toàn vintage thì nhãn của kỳ test đã tham gia vào quyết định của
  model (xem cảnh báo bên dưới).

> **Cập nhật Sprint 2:** `iv_table.csv` (RQ1) đã được đồng bộ candidate set với notebook 03 — từ 16 lên
> **81 biến** — nên bảng xếp hạng dưới đây giờ phản ánh đúng toàn bộ tập biến đang được xét cho model, không
> chỉ nhóm 16 biến cơ bản của Sprint 1.

**Xếp hạng yếu tố rủi ro trên toàn danh mục (RQ1) — top 15/81 theo IV toàn vintage:**

| Biến | IV (toàn vintage) | IV (train) | Diễn giải |
|---|---|---|---|
| `fico_mid` | 0.147 | 0.150 | Mạnh nhất — điểm tín dụng FICO tại thời điểm vay |
| `bc_open_to_buy` | 0.077 | 0.081 | Hạn mức thẻ tín dụng còn trống — tương quan **âm** với rủi ro |
| `tot_hi_cred_lim` | 0.074 | 0.075 | Tổng hạn mức tín dụng cao nhất từng được cấp |
| `avg_cur_bal` | 0.070 | 0.073 | Dư nợ trung bình hiện tại trên các tài khoản |
| `acc_open_past_24mths` | 0.067 | **0.100** | Số tài khoản mở trong 24 tháng gần nhất |
| `mort_acc` | 0.065 | 0.057 | Số tài khoản vay thế chấp |
| `verification_status` | 0.065 | 0.060 | Trạng thái xác minh thu nhập |
| `total_bc_limit` | 0.062 | 0.078 | Tổng hạn mức thẻ tín dụng |
| `dti` | 0.061 | 0.064 | Debt-to-income |
| `open_rv_24m` | 0.059 | 0.049 | Số tài khoản tín dụng quay vòng mở trong 24 tháng |
| `tot_cur_bal` | 0.059 | 0.059 | Tổng dư nợ hiện tại trên mọi tài khoản |
| `all_util` | 0.056 | 0.037 | Tỷ lệ sử dụng hạn mức trên mọi loại tín dụng |
| `annual_inc` | 0.053 | 0.060 | Thu nhập hàng năm |
| `num_tl_op_past_12m` | 0.052 | **0.080** | Số tài khoản tín dụng mở trong 12 tháng gần nhất |
| `total_rev_hi_lim` | 0.052 | 0.063 | Tổng hạn mức tín dụng quay vòng |

Đáng chú ý: `acc_open_past_24mths` và `num_tl_op_past_12m` có IV **cao hơn hẳn trên train so với toàn vintage**
(0.067→0.100 và 0.052→0.080) — khác hướng với các biến còn lại, nơi IV train và toàn vintage khá gần nhau.
Không phải dấu hiệu leakage (đều dưới ngưỡng nghi ngờ 0.5), nhiều khả năng do tỷ lệ mở tài khoản mới biến
động giữa các giai đoạn train/test (liên hệ với vintage effect đã xác nhận ở mục 3).

Bảng đầy đủ 81 biến: `reports/figures/iv_table.csv` (toàn vintage) và `reports/figures/iv_table_train.csv`
(train, dùng chọn biến cho model — xem shortlist bên dưới).

`fico_range_low` và `fico_range_high` đã được **gộp thành `fico_mid`**: hai biến chênh nhau đúng 4 điểm,
tương quan gần như tuyệt đối và IV trùng khớp đến 7 chữ số thập phân — đây là một tín hiệu bị tách đôi. Bằng
chứng định lượng: khi để cả hai trong Logistic Regression, hệ số bị **chia đôi chính xác** (−0.4428 mỗi biến,
tổng −0.8856), gần trùng khít với hệ số của biến gộp (−0.8858). Với LightGBM thì vô hại (model tự bỏ một
biến), nhưng với LR đây là multicollinearity làm mất khả năng diễn giải. Chi tiết: `experiments/exp01_fico_mid.py`.

> ⚠️ **Lịch sử Sprint 1 — bước chọn biến trước đây đặt sai chỗ, đã sửa.** Bản đầu (candidate set 16 biến gốc)
> tính IV trên toàn bộ vintage rồi mới split, tức là nhãn của kỳ test đã tham gia vào việc chọn biến. Sai lệch
> này **có hậu quả thật**, không chỉ là vấn đề nguyên tắc: `revol_util` lẽ ra bị loại (IV toàn vintage 0.025 →
> chỉ 0.015 trên train), còn `credit_history_length` (0.019 → 0.023) và `revol_bal` (0.011 → 0.020) lẽ ra
> được nhận. `revol_util` lọt vào model chính khi đó là nguyên nhân lỗi hệ số sai dấu — chi tiết ở mục 3.1.
> Các con số này không đổi ở Sprint 2 (IV tính độc lập theo từng biến, không phụ thuộc các biến khác trong
> candidate set), chỉ khác là giờ so sánh trong bối cảnh 81 biến thay vì 16.
>
> Từ notebook 03 (và nay cả notebook 02 sau khi đồng bộ), bước chọn biến cho model được đặt **sau time-based
> split** và chỉ dùng nhãn của tập train — `iv_table.csv` (toàn vintage) chỉ dùng để trả lời RQ1 mô tả.

**Shortlist chính thức dùng cho model** (IV train > 0.02, chuẩn Siddiqi 2006 — **40/81 biến ứng viên**,
Sprint 2 mở rộng từ 8/16): top 10 theo IV — `fico_mid` (0.150), `acc_open_past_24mths` (0.100),
`bc_open_to_buy` (0.081), `num_tl_op_past_12m` (0.080), `total_bc_limit` (0.078), `tot_hi_cred_lim` (0.075),
`avg_cur_bal` (0.073), `dti` (0.064), `total_rev_hi_lim` (0.063), `verification_status` (0.060). Danh sách
đầy đủ 40 biến: `reports/figures/iv_table_train.csv` (cột `selected`).

Các biến ứng viên không lọt shortlist vẫn được giữ trong `data/processed/` để phục vụ Customer Dashboard và
business rules, nhưng **không** đưa vào model.

**SHAP feature importance** (từ LightGBM, `reports/figures/shap_feature_importance.png`, top 10):
`fico_mid` (0.228) > `loan_to_income` (0.206) > `dti` (0.152) > `acc_open_past_24mths` (0.124) >
`tot_hi_cred_lim` (0.090) > `home_ownership` (0.085) > `mo_sin_old_rev_tl_op` (0.081) >
`verification_status` (0.078) > `total_rev_hi_lim` (0.076) > `percent_bc_gt_75` (0.072). `loan_to_income`
(biến tỷ lệ mới tạo ở Sprint 2 — payment-to-income) lọt top 2, xác nhận giả thuyết ở Sprint 1 rằng biến tỷ lệ
mang tín hiệu mạnh hơn biến thành phần (`loan_amnt` đơn lẻ chỉ IV 0.005). Thứ hạng SHAP và IV nhất quán ở
nhóm đầu — FICO, DTI và `acc_open_past_24mths` là các yếu tố rủi ro hàng đầu theo cả hai phương pháp.

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
| Logistic Regression + WOE | 0.6739 | 0.2527 | 0.3478 | Không (thiếu 0.006) | Có |
| **LightGBM (model chính)** | **0.7004** | **0.2891** | **0.4007** | **Có** | **Có** |

> **Cập nhật Sprint 2 (so với bản Sprint 1: LR AUC 0.6516/KS 0.2197, LightGBM AUC 0.6607/KS 0.2308):** sau khi
> mở rộng candidate set từ 17 lên 81 biến (8→40 biến qua ngưỡng IV), cả hai model đều cải thiện rõ rệt. Cả
> **LightGBM đã đạt cả hai tiêu chí AUC/KS** — đúng như chẩn đoán ở Sprint 1 rằng nguyên nhân chính là thiếu
> biến (17/151 cột), không phải giới hạn cấu trúc model.

**Cả 2 model giờ đạt hoặc gần đạt mục tiêu đề ra trong PROPOSAL (AUC≥0.68, KS≥0.25).** LightGBM đạt cả hai;
Logistic Regression + WOE đạt KS nhưng còn thiếu 0.006 để đạt AUC — nguyên nhân chính là đa cộng tuyến giữa
các biến bureau mới (xem mục 3.1), khiến LR không tận dụng được hết tín hiệu mà cấu trúc phi tuyến của
LightGBM khai thác được. Nhắc lại điểm đã nêu ở Sprint 1 (không đổi): dự án chủ động loại `grade`/`sub_grade`/
`int_rate` khỏi feature dự báo vì đây là *kết quả* underwriting nội bộ của Lending Club, không phải đặc điểm
thô của khách hàng — nên các con số AUC ở đây **không so sánh trực tiếp được** với benchmark 0.68–0.72 thường
trích dẫn cho Lending Club (các phân tích đó hầu hết có dùng grade). Đây là đánh đổi có chủ đích, không phải
hạn chế cần khắc phục (xem BRD.md mục 4).

**Ổn định theo quý trong tập test** (`reports/figures/model_stability_by_quarter.csv`):

| Quý | n | Bad rate | AUC (LR) | AUC (LightGBM) |
|---|---|---|---|---|
| 2017Q1 | 13,240 | 19.72% | 0.6770 | 0.6979 |
| 2017Q2 | 34,120 | 20.94% | 0.6804 | 0.7032 |
| 2017Q3 | 32,962 | 20.53% | 0.6741 | 0.7005 |
| 2017Q4 | 24,882 | 17.92% | 0.6581 | 0.6950 |

AUC (LightGBM) dao động 0.695–0.703 qua 4 quý, không có sụt giảm bất thường — mô hình ổn định về khả năng
phân biệt dù bad rate nền thay đổi.

**Chọn model chính:** chênh lệch AUC (LightGBM − LR) là **0.0265**, **vượt** ngưỡng 0.02 tự đặt ở Sprint 1 →
model chính đổi thành **LightGBM** (đảo ngược kết luận Sprint 1, khi đó chênh lệch chỉ 0.0090 nên chọn LR để
ưu tiên giải thích được). Bù lại cho việc mất tính diễn giải trực tiếp qua hệ số, dùng **SHAP**
(`reports/figures/shap_importance.csv`, mục 2) để giải thích đóng góp từng biến ở cấp độ model và từng khoản
vay — đây là thực hành chuẩn khi dùng tree-based model cho credit scoring thay vì scorecard tuyến tính.

### 3.1. Hệ số scorecard — 9/40 sai dấu sau khi mở rộng biến (chưa xử lý, không chặn tiến độ)

Quy ước WOE của `optbinning`: `WoE = ln(P(x|good) / P(x|bad))`, nên bin **ít rủi ro** có WoE **dương**.
Model dự báo `bad_flag = 1`, vì vậy hệ số kỳ vọng **âm** cho mọi biến. Hệ số dương là dấu hiệu bất thường.

**Ở Sprint 1, sau khi sửa bước chọn biến (chỉ tính IV trên train), scorecard 8 biến đạt 8/8 hệ số đúng dấu.**
Sau khi mở rộng lên 40 biến ở Sprint 2, **9/40 hệ số bị sai dấu**:

`open_rv_12m` (+0.045), `revol_bal` (+0.071), `open_acc_6m` (+0.077), `inq_last_12m` (+0.089), `open_il_24m`
(+0.186), `avg_cur_bal` (+0.218), `tot_cur_bal` (+0.367), `mo_sin_rcnt_rev_tl_op` (+0.383),
`credit_history_length` (+0.552).

10 hệ số âm mạnh nhất (đúng dấu, đóng góp chính vào scorecard): `loan_to_income` (−1.041),
`mo_sin_old_rev_tl_op` (−0.633), `dti` (−0.619), `tot_hi_cred_lim` (−0.610), `acc_open_past_24mths` (−0.554),
`inq_fi` (−0.505), `percent_bc_gt_75` (−0.468), `mths_since_recent_bc` (−0.457), `total_rev_hi_lim` (−0.427),
`fico_mid` (−0.420).

**Nguyên nhân — đa cộng tuyến giữa các biến bureau mới, khác cơ chế với lỗi `revol_util` ở Sprint 1** (lỗi đó
do bước chọn biến sai vị trí, đã sửa — xem lịch sử bên dưới). Lần này biến chọn đúng phương pháp (IV tính trên
train, sau split) nhưng nhiều biến mới đo cùng một khái niệm bằng đơn vị khác nhau nên tương quan cao với
nhau: `avg_cur_bal`/`tot_cur_bal` cùng đo quy mô dư nợ hiện tại; nhóm `open_il_Xm`/`open_rv_Xm`/`open_acc_6m`
cùng chia sẻ 41.6% missing (khả năng cùng nguồn dữ liệu, chỉ khác cửa sổ thời gian) nên tương quan chặt với
nhau; `credit_history_length` có thể hấp thụ lẫn với các biến "tháng kể từ..." (`mo_sin_*`,
`mths_since_recent_*`) đo cùng trục thời gian tín dụng. Khác với `revol_util` trước đây (loại thẳng vì dưới
ngưỡng IV), các biến này đều **có IV hợp lệ đơn biến** — vấn đề chỉ xuất hiện khi đưa cùng lúc vào LR.

**Không xử lý trong Sprint 2** vì không ảnh hưởng đến model chính: LightGBM (tree-based) không nhạy với đa
cộng tuyến theo cách LR gặp phải, và LightGBM đã trở thành model chính (mục 3). Nếu Sprint 3 cần khôi phục
Logistic Regression làm scorecard dự phòng/đối chiếu, cần lọc bớt biến tương quan (VIF hoặc loại bớt biến
trùng khái niệm) trước khi fit lại.

**Lịch sử — lỗi `revol_util` ở Sprint 1 (đã xử lý dứt điểm, không tái phát ở 40 biến hiện tại):** bản model
đầu tiên có `revol_util_woe` mang hệ số dương (+0.228) do bước chọn biến tính IV trên toàn bộ vintage thay vì
chỉ trên train (revol_util lẽ ra dưới ngưỡng 0.02 trên train). Nguyên nhân gốc: `corr(revol_util, fico_mid) =
−0.428`, hiệu ứng suppressor vì credit utilization đã là thành phần của công thức FICO. Sau khi chuyển bước
chọn biến xuống sau split, biến này tự động bị loại. Chi tiết chẩn đoán: `experiments/exp01_fico_mid.py`,
`experiments/exp02_revol_util_sign.py`.

## 4. Customer Segmentation

5 nhóm theo ngũ phân vị (quintile) của `pd_score` (**LightGBM**, model chính từ Sprint 2 — trước đó dùng
Logistic Regression). Ranh giới ngũ phân vị được xác định trên tập **validation**, sau đó áp dụng nguyên
trạng lên tập **test** để báo cáo — nên kích thước 5 nhóm dưới đây không còn bằng nhau tuyệt đối như khi
tính ngũ phân vị trực tiếp trên test (xem rà soát chất lượng ở business_rules_policy.md):

| Segment | n | Bad rate | Avg PD score | Avg loan_amnt | Avg int_rate |
|---|---|---|---|---|---|
| S1 (rủi ro thấp nhất) | 24,876 | 6.59% | 5.74% | $11,676 | 8.73% |
| S2 | 21,316 | 13.70% | 11.35% | $11,450 | 11.55% |
| S3 | 20,431 | 19.47% | 16.41% | $11,734 | 13.20% |
| S4 | 19,643 | 26.15% | 22.57% | $12,222 | 14.63% |
| S5 (rủi ro cao nhất) | 18,938 | 38.58% | 34.56% | $13,602 | 16.88% |

Kiểm định chi-square: chi²=7892.78, p<0.000001 — **default rate tách biệt rõ rệt và có ý nghĩa thống kê giữa
5 segment**, đạt tiêu chí Success Metric của PROPOSAL (mục 2). Bad rate tăng đơn điệu từ S1→S5 (6.6%→38.6%,
chênh lệch ~5.9 lần — tách biệt rõ hơn nhiều so với scorecard Sprint 1 cũ, khi đó chỉ 8.6%→32.2%, ~3.8 lần).

Quan sát nghiệp vụ: `avg_int_rate` tăng đơn điệu cùng chiều với bad rate (8.73% → 16.88%). Nghĩa là risk
score của dự án — dù xây **hoàn toàn độc lập** với `grade`/`int_rate` của Lending Club — vẫn xếp hạng rủi ro
theo cùng chiều với underwriting nội bộ của LC. Đây là một dạng kiểm chứng chéo (external validity) cho
model. Khác với scorecard cũ, `avg_loan_amnt` không còn giảm đơn điệu theo segment (dao động $11,450–$13,602,
thấp nhất ở S2 chứ không phải S5) — vì `loan_to_income` (biến tỷ lệ, không phải `loan_amnt` thô) mới là yếu
tố ảnh hưởng mạnh, nên quy mô khoản vay tuyệt đối không còn tương quan đơn điệu với rủi ro như ở model cũ.
