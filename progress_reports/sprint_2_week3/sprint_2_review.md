# Sprint 2 Review — Risk Scoring Model

**Thời gian:** Tuần 3 (30/07 – 05/08/2026)

> **Trạng thái file:** đã cập nhật số liệu thật sau khi chạy lại pipeline với tập biến mở rộng (04/08/2026).
> Mục 1–3 và 5 là bản kế hoạch đầu sprint, giữ nguyên để đối chiếu. Mục 4, 6, 7 là kết quả thực tế.

## 1. Mục tiêu Sprint (theo PROPOSAL.md mục 8)
- Time-based train/validation/test split theo `issue_d`
- Xây baseline: Logistic Regression trên biến đã WOE-transform
- Xây model so sánh: LightGBM hoặc XGBoost (kèm SHAP nếu chọn hướng này)
- Đánh giá bằng AUC-ROC, KS Statistic, Gini
- Chọn model chính cho dashboard, nêu lý do đánh đổi hiệu năng vs. khả năng giải thích

> **Lưu ý về lịch:** dự án đã thống nhất bám theo lịch `PROPOSAL.md` mục 8 (xem [README](../README.md)), nên
> Sprint 2 chỉ gồm **tuần 3** — phạm vi hẹp và chỉ có 1 tuần. Vì phần lớn nội dung đã có bản đầu từ Sprint 1
> (xem mục 2), thời gian tuần 3 dồn cho việc trọng tâm duy nhất ở mục 5: mở rộng tập biến để đạt ngưỡng
> AUC/KS. Nếu việc này chưa xong trong tuần 3, phần còn lại chuyển sang đầu Sprint 3 và ghi rõ ở mục 6.

## 2. Đối chiếu Definition of Done

Phần lớn nội dung Sprint 2 đã có bản đầu tiên từ Sprint 1 (làm vượt phạm vi, sau đó rà soát và sửa 4 lỗi
phương pháp luận — xem [Sprint 1 Review](../sprint_1_week1-2/sprint_1_review.md) mục 6.1). Trạng thái kế thừa
tại thời điểm mở Sprint 2:

| Tiêu chí (PROPOSAL.md mục 8) | Đầu sprint | Cuối sprint | Ghi chú |
|---|---|---|---|
| AUC-ROC ≥ 0.68 và KS ≥ 0.25 trên tập test | ☐ Chưa đạt | ☑ Đạt | Sau khi mở rộng feature set (17→81 biến ứng viên, 40 biến qua ngưỡng IV): **LightGBM AUC 0.7004 / KS 0.2891** — đạt cả hai. Logistic Regression + WOE cải thiện lên **AUC 0.6739 / KS 0.2527** — đạt KS, còn thiếu 0.006 để đạt AUC. Chi tiết ở mục 4 |
| Bảng so sánh đầy đủ 2 model (metric + độ giải thích) | ☑ Đạt | ☑ Đạt | `reports/figures/model_comparison.csv` đã chạy lại trên tập biến mở rộng — LR + WOE vs LightGBM, kèm AUC/KS/Gini |
| Đã chọn 1 model chính, có ghi lại lý do lựa chọn | ☑ Đạt | ☑ Đạt (đổi model) | Chênh lệch AUC (LightGBM − LR) giờ là **0.0265**, vượt ngưỡng 0.02 tự đặt ở Sprint 1 → model chính đổi từ Logistic Regression sang **LightGBM** (kèm SHAP để bù giải thích). Ghi tại `models/primary_model.txt`. Đây là thay đổi so với kết luận Sprint 1 — xem mục 4 và 6 |
| Kiểm tra ổn định bad rate giữa các giai đoạn train/test | ☑ Đạt | ☑ Đạt | Chi-square = 1916, p < 0.0001 → **có vintage effect** (train 16.31% / val 21.48% / test 19.94%, không đổi vì split không đổi). AUC theo quý trong test (LightGBM) dao động 0.695–0.703, không sụt bất thường |

## 3. Deliverables hoàn thành trong sprint
- [notebooks/03_feature_engineering_split.ipynb](../../notebooks/03_feature_engineering_split.ipynb) — split + chọn biến trên train + WOE transform, candidate set mở rộng 17→81 biến
- [notebooks/04_modeling.ipynb](../../notebooks/04_modeling.ipynb) — LR + WOE, LightGBM, SHAP, so sánh & chọn model (40 biến WOE)
- [notebooks/05_segmentation_profitability.ipynb](../../notebooks/05_segmentation_profitability.ipynb) — chạy lại segmentation, cutoff/profitability, business rules theo model mới
- `src/features/clean.py` — thêm `add_ratio_features()` (loan_to_income, revol_bal_to_income, tot_cur_bal_to_income)
- Model artifact trong `models/`: `logistic_regression_woe.pkl`, `lightgbm_model.txt`, `binning_process.pkl`, `primary_model.txt` (= LightGBM)
- `reports/figures/`: `model_comparison.csv`, `model_stability_by_quarter.csv`, `shap_importance.csv`, `iv_table_train.csv`, `cutoff_table.csv`, `cutoff_profitability_analysis.png`
- `dashboards/`: `segment_summary.csv`, `cutoff_table.csv`, `business_rules.csv`, `iv_ranking_train.csv`, `customer_dashboard_data.csv` — dữ liệu nền cho Sprint 3

## 4. So sánh kế hoạch vs thực tế
- **Đạt mục tiêu chính của sprint**: AUC/KS vượt ngưỡng nhờ mở rộng candidate set đúng theo kế hoạch mục 5 (17→81 biến, 40 biến qua ngưỡng IV > 0.02). LightGBM: AUC 0.6516→0.7004, KS 0.2197→0.2891. Logistic Regression + WOE: AUC 0.6516→0.6739, KS 0.2197→0.2527.
- **Vượt phạm vi dự kiến của tuần 3**: kế hoạch mục 5 bước 4 ("chạy lại segmentation và cutoff") dự kiến làm ở đầu Sprint 3, nhưng đã hoàn thành trong Sprint 2 — segment mới tách biệt rõ hơn nhiều (S1 bad rate 5.9% vs S5 37.5%, so với 8.6%–32.2% ở model cũ).
- **Chưa làm**: bước 5 (phân tích PSI) — chưa có thời gian trong tuần 3, chuyển sang Sprint 3.
- **Phát sinh ngoài kế hoạch — quyết định chọn model chính bị đảo ngược**: ở Sprint 1, chênh lệch AUC LightGBM−LR chỉ 0.009 nên chọn LR (dễ giải thích). Sau khi mở rộng biến, chênh lệch tăng lên 0.0265 (vượt ngưỡng tự đặt 0.02) vì LightGBM tận dụng tương tác phi tuyến giữa các biến bureau tốt hơn LR + WOE (biến đổi tuyến tính). Theo đúng luật đã viết ở notebook 04, model chính đổi sang LightGBM — cần cập nhật lại phần thuyết minh "ưu tiên scorecard dễ giải thích" đã viết trong BRD/EDA report ở Sprint 1.
- **Nguyên nhân AUC vẫn chưa đạt với LR**: đa cộng tuyến giữa các biến bureau mới (xem mục 6) làm LR không tận dụng được hết tín hiệu — không phải do thiếu biến nữa.

## 5. Việc trọng tâm của sprint — đưa AUC/KS lên ngưỡng mục tiêu

Chẩn đoán từ Sprint 1: AUC chưa đạt do **hai** nguyên nhân, mức độ xử lý được khác nhau.

**(a) Đã chủ động loại `grade`/`sub_grade`/`int_rate` — không định khắc phục.** Đây là *kết quả* từ underwriting
nội bộ của Lending Club, không phải đặc điểm thô của khách hàng. Hệ quả: con số AUC của dự án **không so sánh
trực tiếp được** với mức 0.68–0.72 thường trích dẫn cho Lending Club, vì các phân tích đó hầu hết *có* dùng
grade. Đây là đánh đổi có chủ đích để giữ tính độc lập về phương pháp.

**(b) Feature space mới khai thác 17/151 cột — nguyên nhân chính, khắc phục được.** File gốc còn khoảng 60 cột
hợp lệ tại thời điểm xét duyệt chưa được xét: `verification_status`, `pub_rec_bankruptcies`, `mort_acc`,
`acc_open_past_24mths`, `mths_since_last_delinq`, `mths_since_recent_inq`, `bc_util`, `percent_bc_gt_75`,
`tot_hi_cred_lim`, `total_bal_ex_mort`, `avg_cur_bal`, `pct_tl_nvr_dlq`, `num_tl_op_past_12m`,
`application_type`... Đây chính là nhóm "biến thay thế bureau data" mà PROPOSAL mục 4 nêu, nhưng thực tế mới
dùng 8 biến cơ bản nhất.

**Kế hoạch thực hiện:**

1. Mở rộng candidate set lên ~60 biến bureau. Hàm `src.data.filter_vintage.assert_no_leakage()` đã sẵn sàng
   chặn tự động cả biến hậu-giải-ngân lẫn biến quyết định của LC — kể cả bẫy `installment`
   (= f(`loan_amnt`, `int_rate`, `term`) nên đã nhúng `int_rate`).
2. Tạo nhóm **biến tỷ lệ** trước khi lọc theo IV: `loan_amnt / annual_inc` (payment-to-income),
   `revol_bal / annual_inc`, `tot_cur_bal / annual_inc`. IV là chỉ số *đơn biến* nên lọc trước khi tạo biến
   tỷ lệ sẽ loại sớm nguyên liệu (ví dụ `loan_amnt` có IV 0.005 nhưng tỷ lệ của nó thường mạnh hơn nhiều).
3. Chạy lại chọn biến trên train (giữ đúng thứ tự đã sửa ở Sprint 1), rồi chạy lại LR + LightGBM.
4. Chạy lại segmentation và cutoff analysis theo model mới — điểm số đổi thì ranh giới segment cũng đổi.
5. Bổ sung phân tích PSI nếu còn thời gian.

**Phương án dự phòng nếu vẫn dưới 0.68:** báo cáo trung thực kèm phân tích nguyên nhân, và đề xuất mentor xem
lại mức mục tiêu — vì benchmark 0.68–0.72 không cùng thiết lập với dự án này (xem điểm (a)).

## 6. Vấn đề tồn đọng / rủi ro cho Sprint 3

Kế thừa từ Sprint 1, chưa xử lý:

- **Expected Net Return dùng công thức đơn giản hóa** — `int_rate` áp dụng 1 lần, không tính lãi tích lũy theo
  kỳ hạn 3 năm, nên kết luận "duyệt ngẫu nhiên bị lỗ" chưa dùng được cho quyết định. LGD cũng đang là số cố
  định 58.87% cho mọi segment.
- **Dashboard — phạm vi đã chốt, chưa dựng.** Sai lệch `BRD.md` (từng ghi ngoài phạm vi) vs cam kết
  `PROPOSAL.md`/kiến trúc đã nộp mentor đã được sửa ở [Sprint 1 Review](../sprint_1_week1-2/sprint_1_review.md)
  mục 5 — `BRD.md` nay ghi đúng 2 dashboard là trong phạm vi. Việc còn lại là dựng 2 dashboard thật
  (`.pbix`/`.twbx`) ở Sprint 3, dữ liệu nền đã sẵn sàng trong `dashboards/`.
- **Vintage effect** đã xác nhận nhưng chưa xử lý — cần nêu nhu cầu recalibrate định kỳ trong phần giới hạn.

Phát sinh trong Sprint 2:

- **9/40 hệ số Logistic Regression bị sai dấu** (`open_rv_12m`, `revol_bal`, `open_acc_6m`, `inq_last_12m`,
  `open_il_24m`, `avg_cur_bal`, `tot_cur_bal`, `mo_sin_rcnt_rev_tl_op`, `credit_history_length`) — do đa cộng
  tuyến giữa các biến bureau mới thêm (nhóm `open_il/rv_Xm` cùng nguồn missing 41.6%, `avg_cur_bal`/`tot_cur_bal`
  cùng đo quy mô dư nợ). Không chặn tiến độ vì LightGBM giờ là model chính (không nhạy với đa cộng tuyến như
  LR), nhưng nếu Sprint 3 cần dùng lại LR làm scorecard dự phòng/đối chiếu thì phải lọc bớt biến tương quan
  trước khi fit — chưa xử lý.
- **Bug hướng quy tắc business rule chọn tự động theo IV cao nhất**: khi mở rộng candidate set, biến
  `bc_open_to_buy` (hạn mức thẻ tín dụng còn trống) lọt vào top-2 IV nhưng tương quan **âm** với rủi ro (hạn
  mức còn trống nhiều = an toàn hơn), trong khi code cũ luôn giả định "giá trị càng cao càng rủi ro" (đúng
  ngẫu nhiên với 2 biến cũ `dti`/`inq_last_6mths`). Nếu không phát hiện, rule sẽ bắt buộc Review đúng nhóm
  khách hàng **an toàn hơn** (bad rate 9.5% so với 19.9% toàn cục — ngược dấu). Đã sửa: tính tương quan từng
  biến với `bad_flag` để xác định chiều rule (`>` hay `<` ngưỡng percentile), kèm assertion chặn tự động nếu
  uplift âm. Rule mới: `acc_open_past_24mths > 11` và `bc_open_to_buy < 211`, cả hai đều tách đúng nhóm rủi ro
  cao hơn (~26% bad rate). Bài học: **không nên tự động hoá lựa chọn biến rule chỉ dựa trên IV mà bỏ qua chiều
  tương quan**, cần review thủ công khi mở rộng candidate set.
- **Model chính đổi từ Logistic Regression sang LightGBM** (xem mục 4) — ảnh hưởng dây chuyền: segment boundary,
  cutoff đề xuất, và narrative "ưu tiên giải thích được" trong BRD/EDA report ở Sprint 1. Đã viết lại ngay
  trong Sprint 2 (không đợi Sprint 3) — cả 4 báo cáo deliverable (`BRD.md`, `eda_risk_report.md`,
  `business_rules_policy.md`, `final_recommendation.md`) đã đồng bộ theo LightGBM + SHAP.
- **`iv_table.csv` (RQ1, notebook 02) bị lệch candidate set so với model** — phát hiện khi rà soát lại báo cáo:
  bảng xếp hạng yếu tố rủi ro toàn danh mục vẫn chạy trên 16 biến gốc trong khi notebook 03 (chọn biến cho
  model) đã dùng 81 biến, nên RQ1 bỏ sót các biến bureau có IV cao (`acc_open_past_24mths`, `bc_open_to_buy`...).
  Đã sửa trong Sprint 2: đồng bộ candidate set notebook 02 với notebook 03, chạy lại `iv_table.csv` (81 biến,
  42 vượt ngưỡng IV > 0.02), cập nhật bảng RQ1 trong eda_risk_report.md mục 2.

## 7. Tự đánh giá
- Điểm mạnh trong sprint:
  - Đạt đúng mục tiêu trọng tâm (AUC/KS) bằng đúng hướng đã chẩn đoán từ Sprint 1 (mở rộng feature space), không
    phải vá tạm bằng cách hạ chuẩn hay đổi cách tính metric.
  - Cơ chế chặn leakage (`assert_no_leakage`) hoạt động đúng thiết kế khi mở rộng candidate set gấp ~5 lần
    (17→81 biến) — không phải rà soát thủ công từng biến mới.
  - Phát hiện và sửa được lỗi hướng quy tắc business rule (bc_open_to_buy) **trước khi** đưa vào dashboard/báo
    cáo mentor, nhờ luôn kiểm tra dấu uplift thay vì tin thẳng kết quả tự động — đây là loại lỗi âm thầm, nếu
    lọt vào Final Recommendation sẽ khuyến nghị sai chính sách duyệt.
- Điểm cần cải thiện:
  - Việc mở rộng segmentation/cutoff (dự kiến đầu Sprint 3) bị dồn vào cuối Sprint 2 vì làm ngay sau khi model
    xong — ranh giới sprint bị mờ, cần cập nhật kế hoạch Sprint 3 để không tính trùng công.
  - Đa cộng tuyến ở LR (9/40 hệ số sai dấu) lẽ ra nên kiểm tra VIF/tương quan trước khi đưa toàn bộ 81 biến vào
    bước chọn IV, thay vì phát hiện sau khi fit xong — sẽ áp dụng ở Sprint 3 nếu cần khôi phục LR làm scorecard
    dự phòng.
  - `sprint_2_review.md` và `week_3_summary.md` bị điền trễ đến cuối sprint thay vì cập nhật hàng ngày như
    README yêu cầu — cần daily log đều hơn ở Sprint 3 (2 tuần, dễ trôi tiến độ hơn Sprint 2 chỉ 1 tuần).

## 8. Tham chiếu
- [Tuần 3 — Báo cáo & daily log](week_3/week_3_summary.md)
- [Sprint 1 Review](../sprint_1_week1-2/sprint_1_review.md)
- [PROPOSAL.md](../../PROPOSAL.md)
