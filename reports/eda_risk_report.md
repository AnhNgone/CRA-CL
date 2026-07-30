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

**Xếp hạng yếu tố rủi ro trên toàn danh mục (RQ1):**

| Biến | IV (toàn vintage) | IV (train) | Diễn giải |
|---|---|---|---|
| `fico_mid` | 0.147 | 0.150 | Mạnh nhất — điểm tín dụng FICO tại thời điểm vay |
| `dti` | 0.061 | 0.064 | Trung bình yếu |
| `annual_inc` | 0.053 | 0.060 | Trung bình yếu |
| `home_ownership` | 0.051 | 0.047 | Trung bình yếu |
| `inq_last_6mths` | 0.043 | 0.050 | Yếu |
| `emp_length_years` | 0.026 | 0.023 | Yếu |
| `revol_util` | 0.025 | **0.015** | Yếu — *dưới ngưỡng khi tính trên train* |
| `credit_history_length` | 0.019 | **0.023** | *Vượt ngưỡng khi tính trên train* |
| `addr_state` | 0.019 | 0.018 | Dưới ngưỡng |
| `purpose` | 0.018 | 0.020 | Dưới ngưỡng |
| `revol_bal` | 0.011 | **0.020** | *Vượt ngưỡng khi tính trên train* |
| `total_acc`, `pub_rec`, `loan_amnt`, `delinq_2yrs`, `open_acc` | < 0.011 | < 0.011 | Không đủ sức dự báo đơn biến |

`fico_range_low` và `fico_range_high` đã được **gộp thành `fico_mid`**: hai biến chênh nhau đúng 4 điểm,
tương quan gần như tuyệt đối và IV trùng khớp đến 7 chữ số thập phân — đây là một tín hiệu bị tách đôi. Bằng
chứng định lượng: khi để cả hai trong Logistic Regression, hệ số bị **chia đôi chính xác** (−0.4428 mỗi biến,
tổng −0.8856), gần trùng khít với hệ số của biến gộp (−0.8858). Với LightGBM thì vô hại (model tự bỏ một
biến), nhưng với LR đây là multicollinearity làm mất khả năng diễn giải — mà diễn giải chính là lý do chọn LR
làm model chính. Chi tiết: `experiments/exp01_fico_mid.py`.

> ⚠️ **Bước chọn biến trước đây đặt sai chỗ — đã sửa.** Bản đầu tính IV trên toàn bộ vintage rồi mới split,
> tức là nhãn của kỳ test đã tham gia vào việc chọn biến. Sai lệch này **có hậu quả thật**, không chỉ là vấn
> đề nguyên tắc: so hai cột IV ở trên, **3 biến đổi kết quả** — `revol_util` lẽ ra bị loại (0.025 → 0.015),
> còn `credit_history_length` (0.019 → 0.023) và `revol_bal` (0.011 → 0.020) lẽ ra được nhận. `revol_util`
> lọt vào model chính là nguyên nhân lỗi hệ số sai dấu ở mục 3.1.
>
> Từ notebook 03, bước chọn biến đã được chuyển xuống **sau time-based split** và chỉ dùng nhãn của tập train.

**Shortlist chính thức dùng cho model** (IV train > 0.02, chuẩn Siddiqi 2006 — 8/16 biến ứng viên):
`fico_mid`, `dti`, `annual_inc`, `inq_last_6mths`, `home_ownership`, `emp_length_years`,
`credit_history_length`, `revol_bal`.

Các biến ứng viên không lọt shortlist (`loan_amnt`, `purpose`, `delinq_2yrs`, `open_acc`, `pub_rec`,
`revol_util`, `total_acc`, `addr_state`) vẫn được giữ trong `data/processed/` để phục vụ Customer Dashboard
và business rules, nhưng **không** đưa vào model.

**SHAP feature importance** (từ LightGBM, `reports/figures/shap_feature_importance.png`):
`fico_mid` (0.357) > `dti` (0.202) > `inq_last_6mths` (0.163) > `home_ownership` (0.148) > `revol_bal`
(0.091) > `credit_history_length` (0.068) > `emp_length_years` (0.060) > `annual_inc` (0.052). Thứ hạng SHAP
và IV nhất quán ở nhóm đầu — FICO và DTI là 2 yếu tố rủi ro hàng đầu theo cả hai phương pháp.

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
| Logistic Regression + WOE (model chính) | 0.6516 | 0.2197 | 0.3033 | Không | Không |
| LightGBM | 0.6607 | 0.2308 | 0.3214 | Không | Không |

> **Ghi chú về sự thay đổi so với bản báo cáo đầu tiên** (LR: AUC 0.6534 / KS 0.2216): con số cũ được tạo ra
> khi bước chọn biến còn dùng IV tính trên toàn bộ vintage — tức là nhãn của kỳ test đã tham gia vào việc chọn
> biến. Sau khi sửa đúng phương pháp (chọn biến chỉ trên train), AUC test **giảm nhẹ 0.0018**. Đây là điều
> đáng kỳ vọng: bỏ thông tin của tập test ra khỏi quy trình thì hiệu năng đo trên chính tập test phải giảm
> chút ít. Con số 0.6516 là con số **trung thực**, còn 0.6534 là con số đã bị thổi nhẹ. Đổi lại, toàn bộ 8 hệ
> số nay đều đúng dấu (trước là 7/8) nên model mới thực sự dùng được như một scorecard.

**Cả 2 model đều dưới mục tiêu đề ra trong PROPOSAL (AUC≥0.68, KS≥0.25).** Có **hai** nguyên nhân, cần phân
biệt rõ vì mức độ xử lý được khác nhau:

1. **Loại `grade`/`sub_grade`/`int_rate` — nguyên nhân có chủ đích, không định khắc phục.** Mức AUC 0.68–0.72
   mà ngành thường trích dẫn cho Lending Club hầu hết đến từ các phân tích *có* dùng các biến này, tức là
   học lại underwriting nội bộ của LC. Con số của dự án này vì vậy không so sánh trực tiếp được với benchmark
   đó — đây là đánh đổi đã chọn để giữ tính độc lập về phương pháp (xem BRD.md mục 4).
2. **Feature space mới khai thác 17/151 cột — nguyên nhân chính, khắc phục được.** File gốc còn khoảng 60 cột
   hợp lệ tại thời điểm xét duyệt chưa được xét đến, phần lớn là biến bureau: `verification_status`,
   `pub_rec_bankruptcies`, `mort_acc`, `acc_open_past_24mths`, `mths_since_last_delinq`,
   `mths_since_recent_inq`, `bc_util`, `percent_bc_gt_75`, `tot_hi_cred_lim`, `total_bal_ex_mort`,
   `avg_cur_bal`, `pct_tl_nvr_dlq`, `num_tl_op_past_12m`, `application_type`... Đây chính là nhóm "biến thay
   thế bureau data" mà PROPOSAL mục 4 nêu, nhưng thực tế mới dùng 8 biến cơ bản nhất. Với chỉ 8 biến, AUC
   ~0.65 là kỳ vọng hợp lý; mở rộng candidate set là hướng có khả năng cao nhất đưa AUC lên ngưỡng mục tiêu
   **mà vẫn không cần dùng grade**.

   *Lưu ý khi mở rộng:* `installment` = f(`loan_amnt`, `int_rate`, `term`) nên đã nhúng `int_rate` — phải loại
   để nhất quán với quyết định ở điểm 1. Muốn có biến payment-to-income thì dùng `loan_amnt / annual_inc`.
   Hàm `src.data.filter_vintage.assert_no_leakage()` chặn tự động cả hai nhóm này.

**Ổn định theo quý trong tập test** (`reports/figures/model_stability_by_quarter.csv`):

| Quý | n | Bad rate | AUC (LR) | AUC (LightGBM) |
|---|---|---|---|---|
| 2017Q1 | 13,240 | 19.72% | 0.6471 | 0.6550 |
| 2017Q2 | 34,120 | 20.94% | 0.6578 | 0.6646 |
| 2017Q3 | 32,962 | 20.53% | 0.6540 | 0.6617 |
| 2017Q4 | 24,882 | 17.92% | 0.6378 | 0.6540 |

AUC dao động 0.638–0.658 qua 4 quý, không có sụt giảm bất thường — mô hình ổn định về khả năng phân biệt dù
bad rate nền thay đổi.

**Chọn model chính:** chênh lệch AUC (LightGBM − LR) là **0.0090**, dưới ngưỡng 0.02 tự đặt → chọn
**Logistic Regression + WOE**, ưu tiên khả năng giải thích/audit theo chuẩn ngành credit risk vì LightGBM
không vượt trội đủ để đánh đổi lấy độ phức tạp.

### 3.1. Hệ số scorecard — vấn đề sai dấu đã được xử lý

Quy ước WOE của `optbinning`: `WoE = ln(P(x|good) / P(x|bad))`, nên bin **ít rủi ro** có WoE **dương**.
Model dự báo `bad_flag = 1`, vì vậy hệ số kỳ vọng **âm** cho mọi biến. Hệ số dương là dấu hiệu bất thường.

**Hệ số của model hiện tại — toàn bộ 8/8 đều đúng dấu:**

| Biến | Hệ số | | Biến | Hệ số |
|---|---|---|---|---|
| `dti_woe` | −0.973 | | `revol_bal_woe` | −0.597 |
| `fico_mid_woe` | −0.845 | | `credit_history_length_woe` | −0.405 |
| `inq_last_6mths_woe` | −0.825 | | `annual_inc_woe` | −0.294 |
| `home_ownership_woe` | −0.626 | | `emp_length_years_woe` | −0.217 |

**Bối cảnh — vấn đề trước đây và cách chẩn đoán.** Bản model đầu tiên có `revol_util_woe` mang hệ số **dương
(+0.228)**, nghĩa là "tỷ lệ sử dụng hạn mức càng cao thì rủi ro càng thấp" — vô lý về nghiệp vụ và là lỗi mà
model validation sẽ chặn không cho lên production. Hai thí nghiệm chẩn đoán
(`experiments/exp01_fico_mid.py`, `experiments/exp02_revol_util_sign.py`) cho kết quả:

1. **Không phải do quan hệ phi đơn điệu** — cách giải thích trong bản báo cáo đầu là sai. Bảng binning fit
   trên train cho thấy `revol_util` đơn điệu hoàn hảo: WOE giảm đều qua cả 9 bin từ +0.291
   (`revol_util` < 17.65) xuống −0.158 (≥ 90.55), event rate tăng đơn điệu 12.7% → 18.6%.
2. **Không phải do cặp FICO trùng lặp** — giả thuyết ban đầu bị bác bỏ: sau khi gộp thành `fico_mid`, hệ số
   vẫn dương (+0.2251).
3. **Nguyên nhân thật: tương quan với FICO.** `corr(revol_util, fico_mid) = −0.428`, mạnh nhất trong ma trận
   tương quan. Credit utilization vốn đã là một thành phần trong công thức tính FICO, nên tín hiệu rủi ro của
   `revol_util` bị FICO hấp thụ gần hết; phần dư sau khi kiểm soát FICO đổi dấu — hiệu ứng suppressor.
4. **Biến này lọt vào model do lỗi ở bước chọn biến, không phải do bản chất dữ liệu.** IV trên train chỉ
   0.0146, *dưới* ngưỡng 0.02. Sau khi chuyển bước chọn biến xuống sau split (mục 2), `revol_util` tự động
   bị loại và lỗi sai dấu biến mất — không cần can thiệp thủ công.

**Một lỗi phụ trợ đáng ghi nhận:** notebook 04 ban đầu có ô kiểm tra dấu hệ số **bị viết ngược** ("kỳ vọng tất
cả hệ số > 0"), nên nó gắn cờ 7 hệ số *đúng* là có vấn đề và bỏ sót đúng 1 hệ số *thực sự* sai. Đây là lý do
vấn đề bị mô tả sai trong bản báo cáo đầu. Ô kiểm tra đã được sửa lại đúng chiều.

## 4. Customer Segmentation

5 nhóm theo ngũ phân vị (quintile) của `pd_score` (Logistic Regression) trên tập test:

| Segment | n | Bad rate | Avg PD score | Avg loan_amnt | Avg int_rate |
|---|---|---|---|---|---|
| S1 (rủi ro thấp nhất) | 21,041 | 8.56% | 6.73% | $14,505 | 8.71% |
| S2 | 21,041 | 14.48% | 11.20% | $13,092 | 11.50% |
| S3 | 21,040 | 19.84% | 14.79% | $11,970 | 13.17% |
| S4 | 21,041 | 24.60% | 18.73% | $10,904 | 14.35% |
| S5 (rủi ro cao nhất) | 21,041 | 32.22% | 26.08% | $9,980 | 15.96% |

Kiểm định chi-square: chi²=4374.80, p<0.000001 — **default rate tách biệt rõ rệt và có ý nghĩa thống kê giữa
5 segment**, đạt tiêu chí Success Metric của PROPOSAL (mục 2). Bad rate tăng đơn điệu từ S1→S5 (8.6%→32.2%,
chênh lệch gần 3.8 lần), cho thấy model phân tách rủi ro tốt dù AUC tuyệt đối chưa đạt mục tiêu.

Quan sát nghiệp vụ: `avg_int_rate` tăng đơn điệu cùng chiều với bad rate (8.71% → 15.96%) trong khi
`avg_loan_amnt` giảm dần ($14,505 → $9,980). Nghĩa là risk score của dự án — dù xây **hoàn toàn độc lập** với
`grade`/`int_rate` của Lending Club — vẫn xếp hạng rủi ro theo cùng chiều với underwriting nội bộ của LC. Đây
là một dạng kiểm chứng chéo (external validity) cho model.
