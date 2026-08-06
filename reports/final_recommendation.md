# Final Recommendation

## Yếu tố rủi ro chính

> **Cập nhật Sprint 2**: candidate set mở rộng từ 17 lên 81 biến (40 vượt ngưỡng IV), model chính đổi từ
> Logistic Regression + WOE sang **LightGBM**. Xếp hạng dưới đây dùng IV (train) và SHAP (LightGBM) trên tập
> biến mới — xem eda_risk_report.md mục 2 để đối chiếu đầy đủ.

Xếp hạng nhất quán giữa Information Value (IV) và SHAP (LightGBM):

1. **FICO score** (`fico_mid`) — yếu tố mạnh nhất theo cả hai phương pháp (IV 0.150, SHAP 0.228), điểm tín
   dụng tại thời điểm vay vẫn là chỉ báo rủi ro tốt nhất dù không dùng grade nội bộ của Lending Club. Dùng
   dưới dạng một biến gộp `fico_mid = (fico_range_low + fico_range_high) / 2`: hai biến gốc chênh nhau đúng 4
   điểm và tương quan gần như tuyệt đối, đưa cả hai vào Logistic Regression chỉ làm hệ số bị chia đôi mà
   không thêm thông tin.
2. **Tỷ lệ khoản vay / thu nhập** (`loan_to_income`) — biến tỷ lệ mới tạo ở Sprint 2, SHAP 0.206 (hạng 2),
   xác nhận giả thuyết đặt ra từ Sprint 1: `loan_amnt` đơn lẻ chỉ có IV 0.005 (không đủ ngưỡng), nhưng tỷ lệ
   so với thu nhập lại là chỉ báo rủi ro mạnh — chuẩn mực trong credit scoring (payment-to-income).
3. **Số tài khoản tín dụng mở trong 24 tháng gần nhất** (`acc_open_past_24mths`) — IV 0.100 (hạng 2 theo IV),
   SHAP 0.124. Biến bureau mới, mở nhiều tài khoản gần đây là tín hiệu rủi ro kinh điển trong chấm điểm tín
   dụng, chưa được khai thác ở Sprint 1.
4. **DTI** (debt-to-income) — IV 0.064, SHAP 0.152.
5. **Hạn mức thẻ tín dụng còn trống** (`bc_open_to_buy`) — IV 0.081, tương quan **âm** với rủi ro (hạn mức
   còn trống nhiều = an toàn hơn) — xem lưu ý về chiều tương quan ở business_rules_policy.md mục 2.
6. **Tổng hạn mức tín dụng** (`tot_hi_cred_lim`), **tình trạng sở hữu nhà** (`home_ownership`), **trạng thái
   xác minh thu nhập** (`verification_status`) — nhóm ảnh hưởng trung bình, SHAP 0.08–0.09.

**Về `revol_util` (tỷ lệ sử dụng hạn mức tín dụng tổng) — vẫn không có trong model:** xét riêng lẻ đây là chỉ
báo rủi ro hợp lệ và đơn điệu, nhưng tương quan −0.428 với FICO (credit utilization vốn đã là thành phần của
công thức FICO) khiến tín hiệu bị trùng lặp — chi tiết chẩn đoán ở eda_risk_report.md mục 3.1. Biến tương tự
nhưng hẹp hơn, `bc_util` (tỷ lệ sử dụng riêng thẻ tín dụng), đã lọt shortlist ở Sprint 2 (IV 0.022) và không
gặp vấn đề sai dấu.

**LightGBM (model chính) đạt AUC 0.7004 / KS 0.2891 / Gini 0.4007 trên tập test — đạt cả hai mục tiêu đề ra**
(AUC≥0.68, KS≥0.25). Logistic Regression + WOE cải thiện lên AUC 0.6739 / KS 0.2527 / Gini 0.3478 — đạt KS, còn thiếu 0.006
để đạt AUC. Đây là kết quả sau khi thực hiện đúng hướng đã chẩn đoán ở Sprint 1:

1. **Đã chủ động loại `grade`/`sub_grade`/`int_rate`** khỏi feature dự báo vì đây là kết quả từ underwriting
   nội bộ của Lending Club, không phải đặc điểm khách hàng thô — quyết định phương pháp luận có chủ đích,
   không thay đổi ở Sprint 2. Hệ quả: con số AUC của dự án **không so sánh trực tiếp được** với mức 0.68–0.72
   thường được trích dẫn cho Lending Club, vì các phân tích đó hầu hết *có* dùng grade.
2. **Feature space mở rộng từ 17 lên 81 biến (Sprint 2)** — đúng như chẩn đoán ở Sprint 1, đây là nguyên nhân
   chính khiến AUC/KS trước đó chưa đạt. Sau khi thêm nhóm biến bureau (`acc_open_past_24mths`, `mort_acc`,
   `bc_util`, `tot_hi_cred_lim`, `verification_status`...) và 3 biến tỷ lệ tự tạo, cả hai model đều cải thiện
   rõ rệt và LightGBM vượt ngưỡng mục tiêu.

**9/40 hệ số Logistic Regression bị sai dấu** do đa cộng tuyến giữa các biến bureau mới (chi tiết:
eda_risk_report.md mục 3.1) — đây là lý do LR chưa đạt AUC dù đã có đủ biến, và là một phần lý do model chính
chuyển sang LightGBM (tree-based, không nhạy đa cộng tuyến).

Model phân tách rủi ro rõ rệt hơn hẳn ở mức segment (bad rate 6.6% → 38.6% từ nhóm rủi ro thấp nhất đến cao
nhất, chênh hơn 5.8 lần — xem eda_risk_report.md mục 4, so với 8.6%→32.2%/~3.8 lần của model Sprint 1).

**Model chính đổi từ Logistic Regression sang LightGBM.** Ở Sprint 1, chênh lệch AUC (LightGBM−LR) chỉ 0.009,
dưới ngưỡng 0.02 tự đặt nên chọn LR để ưu tiên khả năng giải thích. Sau khi mở rộng biến, chênh lệch tăng lên
0.0225 trên **validation** (vượt ngưỡng; 0.0265 nếu đo trên test — chỉ để đối chiếu, không dùng để quyết
định, xem rà soát chất lượng ở "Giới hạn của mô hình") vì LightGBM khai thác tương tác phi tuyến giữa các
biến bureau tốt hơn scorecard tuyến tính. Theo đúng luật đã đặt ra, model chính đổi sang LightGBM, dùng
**SHAP** để bù đắp khả năng giải thích.

## Đề xuất cutoff

- **Tại approval rate ~79%**: bad rate nhóm được duyệt theo score = 15.32%, thấp hơn 4.6 điểm % so với
  duyệt ngẫu nhiên (19.94%) — đây là mức cân bằng thực tế hơn để tham khảo làm chính sách vận hành (so với
  3.1 điểm % của model Sprint 1 — LightGBM tách nhóm rủi ro thấp rõ hơn).
- **Cutoff tối ưu hóa Expected Net Return** (theo công thức đơn giản hóa của PROPOSAL) là `pd_score ≤ 0.13`,
  duyệt được 40.6% hồ sơ (rộng hơn nhiều so với 28.8% của model Sprint 1) — vẫn thấp hơn approval rate vận
  hành thực tế thường thấy, chỉ mang tính tham chiếu kỹ thuật (chi tiết: business_rules_policy.md mục 1 và 3).
- 2 business rules override (`acc_open_past_24mths > 11`, `bc_open_to_buy < 155` → bắt buộc Review) bổ sung
  lớp kiểm soát độc lập với score, cả hai đều cho uplift bad rate rõ rệt trên test (+5.7 đến +6.6 điểm %).
  Ngưỡng được chọn trên tập validation, chỉ áp dụng (không tính lại) lên test để báo cáo — xem
  business_rules_policy.md mục 2. Đây là 2 biến mới thay cho `dti`/`inq_last_6mths` của Sprint 1 (IV cao
  hơn) — xem business_rules_policy.md mục 2 về 1 bug hướng quy tắc đã phát hiện và sửa khi đổi biến.

## Giới hạn của mô hình

- **Dữ liệu lịch sử mô phỏng**: Lending Club P2P lending Mỹ 2015–2017, công ty đã ngừng mảng cho vay bán lẻ
  từ 2020 — kết quả minh họa phương pháp luận, không phải triển khai thực tế. Cần A/B test và giám sát
  Population Stability Index (PSI) nếu áp dụng vào hệ thống hoặc thị trường khác. **PSI chưa được tính** trong
  dự án này (việc tồn đọng, chuyển sang Sprint 3).
- **Model chính là LightGBM — khó diễn giải trực tiếp hơn scorecard tuyến tính.** Bù đắp bằng SHAP
  (`reports/figures/shap_importance.csv`) để giải thích đóng góp từng biến ở cấp độ model và từng khoản vay,
  nhưng đây không tương đương với hệ số scorecard minh bạch, dễ audit như Logistic Regression + WOE. Nếu yêu
  cầu tuân thủ (compliance) đòi hỏi mô hình tuyến tính hoàn toàn diễn giải được, cần dùng lại Logistic
  Regression + WOE (AUC 0.6739 — vẫn đạt KS nhưng thiếu 0.006 để đạt AUC mục tiêu) sau khi xử lý đa cộng
  tuyến (xem điểm tiếp theo).
- **9/40 hệ số Logistic Regression bị sai dấu** do đa cộng tuyến giữa các biến bureau mới thêm ở Sprint 2
  (nhóm đo cùng khái niệm dư nợ/thời gian tín dụng bằng đơn vị khác nhau). Không ảnh hưởng model chính
  (LightGBM không nhạy đa cộng tuyến) nhưng cần xử lý (lọc biến tương quan/VIF) nếu muốn khôi phục LR làm
  scorecard dự phòng — chi tiết: eda_risk_report.md mục 3.1.
- **Vintage effect đã xác nhận**: bad rate khác biệt có ý nghĩa thống kê giữa train (16.3%)/val (21.5%)/test
  (19.9%) — chất lượng tín dụng danh mục Lending Club thay đổi theo thời gian phát hành, model cần được
  hiệu chỉnh lại (recalibrate) định kỳ nếu dùng liên tục qua nhiều vintage.
- **(Đã khắc phục) Rò rỉ thông tin ở tầng quyết định kinh doanh**: trước đây cutoff, ranh giới segment, ngưỡng
  business rule, và tiêu chí chọn model chính đều được chọn (tối ưu hóa) trực tiếp trên tập test rồi lại dùng
  chính test đó để báo cáo kết quả — khiến các con số có thể lạc quan hơn thực tế dù không ảnh hưởng đến
  AUC/KS của model. Đã sửa: các quyết định này nay chọn trên validation, test chỉ dùng để báo cáo 1 lần cuối.
  Kết quả hầu như không đổi (cutoff vẫn 0.13, model chính vẫn LightGBM) — xác nhận kết luận trước đó khá vững,
  không phải do ăn may khớp với test.
- **Expected Net Return dùng công thức đơn giản hóa**: `int_rate` áp dụng 1 lần, không tính lãi tích lũy
  theo đúng kỳ hạn 3 năm — số liệu lợi nhuận tuyệt đối (bao gồm kết luận "duyệt ngẫu nhiên bị lỗ") cần được
  tính lại với mô hình dòng tiền đầy đủ trước khi dùng cho quyết định thực tế.
- **LGD là số liệu tổng hợp cố định** (58.87%, tính từ toàn bộ khoản Charged Off trong vintage), chưa phân
  biệt theo segment/loại khách hàng — LGD thực tế có thể khác nhau giữa các nhóm rủi ro.
- **RQ5 (approval rate accepted vs rejected)** chỉ mang tính xấp xỉ do khác schema (`Risk_Score` vs
  `fico_range_low/high`) — không phải reject-inference chuẩn xác.
- **Dashboard Power BI/Tableau chưa được dựng** — dữ liệu tổng hợp đã export sẵn vào `dashboards/`
  (segment_summary, cutoff_table, iv_ranking, iv_ranking_train, business_rules, customer_dashboard_data,
  đã cập nhật theo model LightGBM) để dựng dashboard ở Sprint 3.
