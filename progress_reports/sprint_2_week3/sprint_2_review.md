# Sprint 2 Review — Risk Scoring Model

**Thời gian:** Tuần 3 (30/07 – 05/08/2026)

> **Trạng thái file:** khung đã điền sẵn phần *đầu sprint* (mục tiêu, tình trạng kế thừa từ Sprint 1, việc
> trọng tâm). Các mục 4–7 điền dần trong sprint. Số liệu ở đây là trạng thái tại **30/07/2026**, sẽ được cập
> nhật khi chạy lại pipeline với tập biến mở rộng.

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
| AUC-ROC ≥ 0.68 và KS ≥ 0.25 trên tập test | ☐ Chưa đạt | ☐ | Hiện **AUC 0.6516 / KS 0.2197** (Logistic Regression + WOE). Đây là tiêu chí **duy nhất chưa đạt** và là trọng tâm của sprint — xem mục 5 |
| Bảng so sánh đầy đủ 2 model (metric + độ giải thích) | ☑ Đạt | ☐ | `reports/figures/model_comparison.csv` — LR + WOE vs LightGBM, kèm AUC/KS/Gini. Cần chạy lại trên tập biến mở rộng để so sánh công bằng |
| Đã chọn 1 model chính, có ghi lại lý do lựa chọn | ☑ Đạt | ☐ | Chọn **Logistic Regression + WOE**: chênh lệch AUC so với LightGBM chỉ **0.0090**, dưới ngưỡng 0.02 tự đặt → ưu tiên khả năng giải thích/audit theo chuẩn ngành credit risk. Ghi tại `models/primary_model.txt` |
| Kiểm tra ổn định bad rate giữa các giai đoạn train/test | ☑ Đạt | ☐ | Chi-square = 1916, p < 0.0001 → **có vintage effect** (train 16.31% / val 21.48% / test 19.94%). AUC theo quý trong test dao động 0.638–0.658, không sụt bất thường |

## 3. Deliverables hoàn thành trong sprint
- [notebooks/03_feature_engineering_split.ipynb](../../notebooks/03_feature_engineering_split.ipynb) — split + chọn biến trên train + WOE transform
- [notebooks/04_modeling.ipynb](../../notebooks/04_modeling.ipynb) — LR + WOE, LightGBM, SHAP, so sánh & chọn model
- Model artifact trong `models/`: `logistic_regression_woe.pkl`, `lightgbm_model.txt`, `binning_process.pkl`, `primary_model.txt`
- `reports/figures/`: `model_comparison.csv`, `model_stability_by_quarter.csv`, `shap_importance.csv`, `iv_table_train.csv`

## 4. So sánh kế hoạch vs thực tế
- Tiến độ thực tế so với PROPOSAL.md:
- Nguyên nhân chênh lệch (nếu có):

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
- **Dashboard chưa được duyệt phạm vi** — `BRD.md` ghi ngoài phạm vi (chỉ export CSV), `PROPOSAL.md` cam kết 2
  dashboard hoàn chỉnh. Đã nêu thành đề nghị ở [Sprint 1 Review](../sprint_1_week1-2/sprint_1_review.md) mục 5,
  **cần mentor quyết trước khi vào Sprint 3**.
- **Vintage effect** đã xác nhận nhưng chưa xử lý — cần nêu nhu cầu recalibrate định kỳ trong phần giới hạn.

Phát sinh trong Sprint 2:
-

## 7. Tự đánh giá
- Điểm mạnh trong sprint:
- Điểm cần cải thiện:

## 8. Tham chiếu
- [Tuần 3 — Báo cáo & daily log](week_3/week_3_summary.md)
- [Sprint 1 Review](../sprint_1_week1-2/sprint_1_review.md)
- [PROPOSAL.md](../../PROPOSAL.md)
