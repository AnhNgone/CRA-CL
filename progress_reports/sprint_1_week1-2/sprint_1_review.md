# Sprint 1 Review — Nền tảng dữ liệu & Business Understanding

**Thời gian:** Tuần 1–2 (16/07 – 29/07/2026)

## 1. Mục tiêu Sprint (theo PROPOSAL.md mục 8)
- Đọc data dictionary gốc, làm rõ business problem
- Xác định vintage window (2015–2017, term 36 tháng), lọc dữ liệu accepted + rejected
- Viết Business Requirement Document
- Data Cleaning (missing, outlier, encoding categorical)
- EDA: univariate + bivariate với `loan_status`, tính WOE/IV
- Feature Engineering, loại bỏ biến hậu-giải-ngân (leakage)

## 2. Đối chiếu Definition of Done

| Tiêu chí (PROPOSAL.md mục 8) | Đạt? | Ghi chú |
|---|---|---|
| Dataset đã lọc theo vintage 2015–2017, nhãn `loan_status` chỉ còn `{Fully Paid, Charged Off}` | ☑ | `src/data/filter_vintage.py` lọc đồng thời 4 điều kiện (term 36 tháng, `issue_d` trong 2015–2017, `loan_status` ∈ {Fully Paid, Charged Off}). Kết quả **643,917 khoản vay**, bad rate **17.70%** — nằm đúng dải 15–20% mà PROPOSAL mục 4.3 dự đoán cho vintage Lending Club |
| Không còn biến hậu-giải-ngân (leakage) trong tập feature | ☑ | Đạt ở **tập feature**: 13 biến trong `LEAKAGE_COLUMNS` bị loại ngay trong chunk loader (`src/data/load.py:50`), và `CANDIDATE_FEATURES` ở notebook 02/03 là whitelist tường minh 17 biến. Ngoài ra chủ động loại thêm `grade`/`sub_grade`/`int_rate` (xem mục 4). **Lưu ý kỹ thuật cho Sprint 2** — xem rủi ro R1 ở mục 6 |
| Có bảng WOE/IV cho toàn bộ biến ứng viên | ☑ | `reports/figures/iv_table.csv` — đủ 17/17 biến ứng viên với `iv`, `gini`, `js`, `n_bins`, `quality_score` (`optbinning.BinningProcess`). Shortlist 8 biến theo ngưỡng IV > 0.02 (Siddiqi 2006) |
| Business Requirement Document + EDA report (bản nháp) hoàn chỉnh | ☑ | `reports/BRD.md` và `reports/eda_risk_report.md` — vượt yêu cầu "bản nháp", cả hai đã ở mức hoàn thiện có số liệu và phần giới hạn |

**Kết luận: đạt 4/4 tiêu chí Definition of Done của Sprint 1.**

## 3. Deliverables hoàn thành trong sprint

**Trong phạm vi Sprint 1 (bắt buộc):**
- [reports/BRD.md](../../reports/BRD.md) — Business Requirement Document, kèm Data Dictionary làm phụ lục
- [reports/eda_risk_report.md](../../reports/eda_risk_report.md) — EDA & Risk Analysis Report
- `notebooks/01_data_understanding.ipynb`, `notebooks/02_eda_woe_iv.ipynb`
- `src/data/` (loader theo chunk + filter vintage + loại leakage), `src/features/clean.py`
- `data/interim/` — accepted + rejected đã lọc vintage; `reports/figures/iv_table.csv`

**Vượt phạm vi — thuộc Sprint 2–3, đã có bản đầu tiên:**
- `notebooks/03_feature_engineering_split.ipynb` — time-based split + WOE transform
- `notebooks/04_modeling.ipynb` — Logistic Regression + WOE và LightGBM, `models/`
- `notebooks/05_segmentation_profitability.ipynb` — segmentation, cutoff/profitability
- [reports/business_rules_policy.md](../../reports/business_rules_policy.md), [reports/final_recommendation.md](../../reports/final_recommendation.md)
- `dashboards/` — 5 file dữ liệu tổng hợp phục vụ dựng dashboard

## 4. So sánh kế hoạch vs thực tế

**Tiến độ: vượt kế hoạch về khối lượng, nhưng phân bổ thời gian không đều.**

Toàn bộ Sprint 1 hoàn thành trong 3 ngày làm việc (20–21/07) thay vì 2 tuần. Ngày 22/07 làm dồn thêm phần lớn Sprint 2–3 (model → segmentation → cutoff → báo cáo). Tuần 2 (23–29/07) theo kế hoạch tự đặt cuối tuần 1 là dành để **review và làm chắc lại** phần đã chạy nhanh — phần review này chưa hoàn tất và chưa được ghi vào daily log.

**Quyết định phương pháp luận quan trọng (không có trong kế hoạch ban đầu):** loại `grade`/`sub_grade`/`int_rate` khỏi tập feature dự báo. Đây là *kết quả* từ underwriting nội bộ của Lending Club (LC tự chấm grade rồi gán `int_rate` theo grade), không phải đặc điểm thô của khách hàng — nếu đưa vào, model chủ yếu học lại grade của LC thay vì đánh giá rủi ro độc lập từ hồ sơ gốc. Đánh đổi: AUC thấp hơn các phân tích công khai có dùng grade. `int_rate` vẫn được giữ riêng làm biến giá để tính Expected Net Return ở notebook 05.

**Kết quả sơ bộ của phần vượt tiến độ** (sau khi đã sửa các lỗi phương pháp ở mục 6.1 và chạy lại toàn bộ pipeline — chưa phải kết quả chốt của Sprint 2):

| Model | AUC (test) | KS (test) | Gini (test) | Mục tiêu AUC≥0.68 / KS≥0.25 |
|---|---|---|---|---|
| Logistic Regression + WOE (model chính) | 0.6516 | 0.2197 | 0.3033 | Chưa đạt |
| LightGBM | 0.6607 | 0.2308 | 0.3214 | Chưa đạt |

Chênh lệch AUC giữa hai model chỉ 0.0090 (< ngưỡng 0.02 tự đặt) → chọn **Logistic Regression + WOE** làm model chính, ưu tiên khả năng giải thích/audit theo chuẩn ngành credit risk.

Dù AUC tuyệt đối chưa đạt, model phân tách rủi ro rõ rệt ở mức segment: bad rate tăng đơn điệu 8.56% → 32.22% qua 5 nhóm (chênh gần 3.8 lần), chi-square = 4374.80 (p < 0.000001) — đạt Success Metric về segmentation của PROPOSAL mục 2.

Một kiểm chứng chéo đáng chú ý: `avg_int_rate` của 5 segment tăng đơn điệu cùng chiều với bad rate (8.71% → 15.96%). Nghĩa là risk score của dự án — dù xây **hoàn toàn độc lập** với `grade`/`int_rate` của Lending Club — vẫn xếp hạng rủi ro cùng chiều với underwriting nội bộ của LC.

## 5. Sai lệch phạm vi Dashboard — đã phát hiện và sửa

**Deliverable #5 (Dashboard Power BI/Tableau).** PROPOSAL mục 9 cam kết 2 dashboard, DoD Sprint 3 yêu cầu "2 dashboard hoàn chỉnh, chạy được". `BRD.md` mục 3 từng tự ý ghi phần này là **ngoài phạm vi** (chỉ export dữ liệu tổng hợp ra `dashboards/`), trong khi bản kiến trúc hệ thống đã nộp cho mentor (`Credit Risk Scoring System — Architecture`) vẽ rõ **2 dashboard là output cam kết** (Risk & Portfolio Dashboard, Customer Dashboard) trong luồng xử lý đầu-cuối — tức là BRD mâu thuẫn với chính cam kết đã gửi mentor, không chỉ với PROPOSAL.

**Đã xử lý:** chọn **Phương án A** — sửa `BRD.md` mục 3, chuyển dashboard từ "Ngoài phạm vi" sang "Trong phạm vi", giữ nguyên cam kết dựng 2 dashboard thật (`.pbix`/`.twbx`) ở Sprint 3, cho nhất quán với kiến trúc đã nộp. Dữ liệu nền đã sẵn sàng (5 file trong `dashboards/`), chi phí phát sinh chủ yếu là thời gian dựng giao diện.

## 6. Vấn đề phát hiện trong sprint — 4 mục đã khắc phục, 4 mục chuyển sang Sprint 2

### 6.1. Đã khắc phục trong sprint này

**R1 — `LEAKAGE_COLUMNS` thiếu 25 cột ✅ ĐÃ SỬA.** Danh sách ban đầu chỉ có 13 cột nhóm thanh toán; kiểm tra `data/interim` (138 cột) phát hiện còn sót `last_fico_range_low/high`, nhóm `hardship_*` (14 cột), nhóm `settlement_*` (4 cột), `debt_settlement_flag`, `debt_settlement_flag_date`, `pymnt_plan`. `last_fico_range_*` nguy hiểm nhất — là FICO cập nhật *sau* giải ngân, với khoản Charged Off thì điểm này đã sụp; đưa nhầm vào sẽ đẩy AUC lên trên 0.85 (dấu hiệu leakage kinh điển).

Chưa gây leak vào model vì tập feature là whitelist tường minh, nhưng cơ chế bảo vệ khi đó là whitelist chứ không phải blacklist — rủi ro sẽ thành thật ngay khi mở rộng feature set ở R2.

*Đã xử lý:* `LEAKAGE_COLUMNS` bổ sung lên **38 cột**; thêm `LENDER_DECISION_COLUMNS` (grade, sub_grade, int_rate, installment, initial_list_status, policy_code, funded_amnt...) và hàm `assert_no_leakage()` làm lớp chặn thứ hai, được gọi ở notebook 03 và 04. `data/interim` đã regenerate: **138 → 113 cột**, loại đúng 25 cột, số dòng giữ nguyên 643,917.

**R3 — Multicollinearity giữa `fico_range_low` và `fico_range_high` ✅ ĐÃ SỬA.** Hai biến có IV trùng khớp đến 7 chữ số thập phân (0.1474853417344026) và chỉ cách nhau 4 điểm — một tín hiệu bị tách đôi. Thí nghiệm (`experiments/exp01_fico_mid.py`) cho bằng chứng sách giáo khoa: hệ số bị **chia đôi chính xác** — `fico_range_low_woe` = `fico_range_high_woe` = **−0.4428** (tổng −0.8856), gần trùng khít với hệ số biến gộp `fico_mid_woe` = **−0.8858**.

*Đã xử lý:* `src/features/clean.py` nay tạo `fico_mid = (low + high) / 2` và bỏ hai biến gốc.

**R4 — Hệ số `revol_util_woe` sai dấu (+0.228) ✅ ĐÃ SỬA.** Theo quy ước WOE mọi hệ số phải âm; hệ số dương nghĩa là "tỷ lệ sử dụng hạn mức càng cao thì rủi ro càng thấp" — vô lý về nghiệp vụ và là lỗi model validation sẽ chặn.

Quá trình chẩn đoán đi qua **hai giả thuyết sai** trước khi tới nguyên nhân thật:
- Giải thích trong bản báo cáo đầu ("quan hệ không đơn điệu/nhiễu") **sai**: bảng binning trên train cho thấy `revol_util` đơn điệu hoàn hảo qua cả 9 bin (WOE +0.291 → −0.158, event rate 12.7% → 18.6%).
- Giả thuyết thứ hai (do cặp FICO trùng lặp ở R3) **cũng bị bác bỏ**: sau khi gộp `fico_mid`, hệ số vẫn dương (+0.2251).
- **Nguyên nhân thật:** `corr(revol_util, fico_mid) = −0.428`, mạnh nhất trong ma trận tương quan. Credit utilization vốn là một thành phần trong công thức FICO nên tín hiệu bị hấp thụ; phần dư sau khi kiểm soát FICO đổi dấu — hiệu ứng suppressor.

**Lỗi phụ trợ phát hiện thêm:** ô kiểm tra dấu hệ số trong notebook 04 **bị viết ngược** ("kỳ vọng tất cả hệ số > 0"), nên nó gắn cờ 7 hệ số *đúng* là có vấn đề và bỏ sót đúng 1 hệ số *thực sự* sai. Đây là lý do vấn đề bị mô tả sai ngay từ đầu. Ô kiểm tra đã sửa lại đúng chiều.

*Đã xử lý:* sau khi sửa R5, `revol_util` tự động bị loại — không cần can thiệp thủ công. Model hiện tại có **8/8 hệ số đúng dấu**.

**R5 — Feature selection dùng nhãn của tập test ✅ ĐÃ SỬA — ảnh hưởng lớn hơn đánh giá ban đầu.** Shortlist IV > 0.02 được tính trên toàn bộ vintage ở notebook 02 rồi mới split ở notebook 03. Binning đã refit đúng trên train, nhưng *việc chọn biến nào* đã "nhìn thấy" nhãn kỳ test.

Ban đầu em đánh giá ảnh hưởng là nhỏ và chỉ mang tính nguyên tắc. **Sai** — sau khi tính lại IV trên train, **3/16 biến đổi kết quả chọn**:

| Biến | IV toàn vintage | IV train | Thay đổi |
|---|---|---|---|
| `revol_util` | 0.0247 | **0.0146** | Bị loại (dưới ngưỡng) |
| `credit_history_length` | 0.0192 | **0.0227** | Được nhận |
| `revol_bal` | 0.0106 | **0.0201** | Được nhận |

*Đã xử lý:* bước chọn biến chuyển hẳn xuống notebook 03, sau time-based split, chỉ dùng nhãn train. Notebook 02 giữ bảng IV toàn vintage nhưng chỉ để trả lời RQ1 (xếp hạng yếu tố rủi ro), có ghi chú rõ không dùng để chọn biến.

**Kết quả sau khi sửa toàn bộ R1/R3/R4/R5** (đã chạy lại pipeline 02→05):

| | Model cũ | Model mới |
|---|---|---|
| Tập biến | 8 (cặp FICO, `revol_util`) | 8 (`fico_mid`, `credit_history_length`, `revol_bal`) |
| AUC test (LR) | 0.6534 | **0.6516** |
| KS test | 0.2216 | 0.2197 |
| Gini test | 0.3068 | 0.3033 |
| Hệ số sai dấu | 1/8 | **0/8** |
| AUC test (LightGBM) | 0.6605 | 0.6607 |

> **Lưu ý trung thực về con số:** AUC **giảm nhẹ 0.0018** sau khi sửa. Đây là điều đáng kỳ vọng — bỏ thông tin của tập test ra khỏi quy trình thì hiệu năng đo *trên chính tập test* phải giảm chút ít. 0.6516 là con số trung thực; 0.6534 đã bị thổi nhẹ. Cái được lớn hơn cái mất: scorecard nay diễn giải được (8/8 hệ số đúng dấu) nên mới thực sự dùng được theo chuẩn ngành credit risk.
>
> Con số này cũng khác kết quả thí nghiệm rời trước đó (model 6 biến, AUC 0.6552) — vì thí nghiệm đó chỉ bỏ `revol_util` thủ công mà vẫn kế thừa shortlist tính sai, còn pipeline đúng phương pháp cho tập biến khác hẳn. Số liệu chính thức là số của pipeline.

### 6.2. Chuyển sang Sprint 2

**R2 — Feature space mới khai thác 17/151 cột (ưu tiên cao nhất).** Đây là nguyên nhân chính khiến AUC chưa đạt mục tiêu, lớn hơn cả việc loại `grade`. File gốc còn khoảng 60 cột hợp lệ tại thời điểm xét duyệt chưa được xét: `verification_status`, `pub_rec_bankruptcies`, `mort_acc`, `acc_open_past_24mths`, `mths_since_last_delinq`, `mths_since_recent_inq`, `bc_util`, `percent_bc_gt_75`, `tot_hi_cred_lim`, `total_bal_ex_mort`, `avg_cur_bal`, `pct_tl_nvr_dlq`, `num_tl_op_past_12m`, `application_type`... Đây chính là nhóm "biến thay thế bureau data" mà PROPOSAL mục 4 nêu nhưng thực tế mới dùng 8 biến cơ bản nhất.
→ *Xử lý:* mở rộng candidate set lên ~60 biến, chạy lại WOE/IV, kỳ vọng đạt AUC 0.68 mà **vẫn không cần dùng grade**. Hàm `assert_no_leakage()` (R1) nay đã sẵn sàng chặn tự động — kể cả bẫy `installment` (= f(`loan_amnt`, `int_rate`, `term`) nên đã nhúng `int_rate`).

**R6 — Ngưỡng IV > 0.02 cắt trước khi tạo biến tỷ lệ.** Các biến bị loại: `purpose` (0.0196), `addr_state` (0.0183), `pub_rec` (0.0102), `loan_amnt` (0.0053), `total_acc` (0.0046), `delinq_2yrs` (0.0026), `open_acc` (0.0020). IV là chỉ số **đơn biến**: `loan_amnt` một mình gần vô nghĩa nhưng `loan_amnt / annual_inc` là biến kinh điển trong credit scoring. Hiện chưa có biến tỷ lệ nào trong tập ứng viên.
→ *Xử lý:* tạo nhóm biến tỷ lệ (`loan_amnt/annual_inc`, `revol_bal/annual_inc`, `tot_cur_bal/annual_inc`) *trước* khi lọc theo IV.

**R7 — Vintage effect đã xác nhận, chưa xử lý.** Bad rate khác biệt có ý nghĩa thống kê giữa train 16.31% / val 21.48% / test 19.94% (chi-square = 1916, p < 0.0001). Đây là hiện tượng thật của dữ liệu, không phải lỗi pipeline. AUC theo quý trong test dao động 0.638–0.658, không sụt bất thường — model ổn định về khả năng phân biệt dù bad rate nền đổi.
→ *Xử lý:* ghi nhận là giới hạn, nêu nhu cầu recalibrate định kỳ; nếu còn thời gian thì bổ sung phân tích PSI.

**R8 — Expected Net Return dùng công thức đơn giản hóa.** `int_rate` áp dụng một lần, không tính lãi tích lũy theo kỳ hạn 3 năm, nên kết luận "duyệt ngẫu nhiên bị lỗ" trong `business_rules_policy.md` chưa dùng được cho quyết định. LGD cũng đang là số cố định 58.87% cho mọi segment.
→ *Xử lý:* tính lại với dòng tiền theo kỳ hạn ở Sprint 3.

## 7. Kế hoạch điều chỉnh cho Sprint 2

Phần khắc phục phương pháp luận (R1, R3, R4, R5) **đã hoàn tất trong sprint này** — pipeline 02→05 đã chạy lại sạch và toàn bộ báo cáo đã cập nhật theo số mới. Sprint 2 vì vậy tập trung vào việc còn lại:

1. **Mở rộng candidate feature lên ~60 biến bureau** + tạo nhóm biến tỷ lệ, chạy lại WOE/IV (R2, R6). Đây là việc có khả năng cao nhất đưa AUC lên ngưỡng mục tiêu, và cũng là việc duy nhất còn lại có thể thay đổi kết quả đáng kể.
2. Chạy lại LightGBM trên feature set mới để bảng so sánh 2 model công bằng, chốt model chính kèm lý do.
3. Chạy lại segmentation và cutoff analysis theo model mới (điểm số đổi thì ranh giới segment cũng đổi).
4. Bổ sung phân tích PSI nếu còn thời gian (R7).
5. Ghi daily log đều đặn cho tuần 3 — rút kinh nghiệm từ tuần 2.

**Nếu sau khi làm 1–2 mà AUC vẫn dưới 0.68:** báo cáo trung thực kèm phân tích nguyên nhân, và đề xuất mentor xem lại mức mục tiêu — vì con số 0.68–0.72 được trích dẫn cho Lending Club hầu hết đến từ các phân tích **có dùng grade/sub_grade**, không so sánh trực tiếp được với thiết lập độc lập của dự án này.

## 8. Tự đánh giá

**Điểm mạnh:**
- Chống leakage được cài ở mức kiến trúc, không phải mức thao tác: biến hậu-giải-ngân bị loại ngay trong chunk loader nên không bao giờ đến tay bước phân tích.
- Thứ tự split → fit → transform đúng tuyệt đối: split theo `issue_d` trước, `winsorize` fit bounds chỉ trên train rồi reuse cho val/test, `BinningProcess` cũng chỉ fit trên train. Đây là chỗ nhiều dự án credit scoring làm sai.
- Quyết định loại `grade`/`sub_grade`/`int_rate` là judgment call chủ động, có lập luận và được ghi lại rõ ràng — không chạy theo AUC cao.
- Có sanity check tự động: cảnh báo IV > 0.5 (nghi leakage), kiểm tra dấu hệ số LR. Chính cái check dấu hệ số này là thứ phát hiện ra vấn đề `revol_util` ở R4–R5 — một ví dụ cho thấy giá trị của việc cài sẵn kiểm tra thay vì chỉ nhìn AUC (dù bản thân ô kiểm tra đó ban đầu bị viết ngược, xem mục 6.1).
- Khi phát hiện bất thường thì **kiểm chứng bằng thí nghiệm có đối chứng** thay vì suy đoán, và **chấp nhận giả thuyết của mình bị bác bỏ**: hai giả thuyết đầu về `revol_util` đều sai, thí nghiệm thứ ba mới ra nguyên nhân thật. Script và output lưu tại `experiments/` để tái lập được.
- **Ưu tiên tính đúng đắn hơn con số đẹp:** sau khi sửa lỗi chọn biến, AUC giảm nhẹ (0.6534 → 0.6516) nhưng vẫn giữ nguyên kết quả đã sửa và ghi rõ lý do trong báo cáo, thay vì quay lại phiên bản cho số cao hơn.
- Xử lý được ràng buộc kỹ thuật thật: đọc theo chunk cho file 2.26M × 151 cột và 27.6M dòng rejected mà không tràn bộ nhớ.
- Báo cáo trung thực — nêu thẳng AUC/KS dưới mục tiêu và các giới hạn của phép tính lợi nhuận thay vì che đi.

**Điểm cần cải thiện:**
- **Chẩn đoán nguyên nhân chưa tới nơi:** quy AUC thấp cho việc loại grade, chưa nhận ra feature space mới khai thác 17/151 cột mới là nguyên nhân lớn hơn (R2). Bài học: khi kết quả không đạt, cần kiểm tra hết các giả thuyết thay vì dừng ở giả thuyết đầu tiên nghe hợp lý.
- **Phân bổ thời gian không đều:** dồn khối lượng lớn vào một ngày (22/07) khiến các bước quan trọng — leakage check, model validation, chất lượng segmentation — chỉ ở mức chạy được, chưa được rà kỹ. Chính rủi ro tự cảnh báo cuối tuần 1 (R1, R3, R4) phải đến cuối Sprint mới được xử lý, và chỉ sau khi rà soát lại có hệ thống.
- **Không duy trì daily log tuần 2:** làm mất khả năng theo dõi tiến độ và khiến phần review đã lên kế hoạch bị bỏ trống. Từ Sprint 2 sẽ ghi log ngay trong ngày.
- **Tự thay đổi phạm vi trong BRD** (dashboard) thay vì nêu thành đề nghị để mentor duyệt — đã sửa ở mục 5.
- **Feature engineering còn mỏng:** mới có 3 biến derived (`emp_length_years`, `credit_history_length`, `fico_mid`), chưa có biến tỷ lệ vốn là chuẩn mực trong credit scoring — đây là việc chính của Sprint 2 (R6).
- **Kiểm tra tự động cũng cần được kiểm tra:** ô check dấu hệ số ở notebook 04 bị viết ngược nên vừa báo động giả 7 lần vừa bỏ sót lỗi thật. Một sanity check sai còn nguy hiểm hơn không có, vì nó tạo cảm giác an toàn giả. Bài học: khi viết check, phải thử với một trường hợp *biết chắc là sai* để xác nhận check bắt được.

## 9. Tham chiếu
- [Tuần 1 — Báo cáo & daily log](week_1/week_1_summary.md)
- [Tuần 2 — Báo cáo & daily log](week_2/week_2_summary.md)
- [PROPOSAL.md](../../PROPOSAL.md)
