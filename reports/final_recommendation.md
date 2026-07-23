# Final Recommendation

## Yếu tố rủi ro chính

Xếp hạng nhất quán giữa Information Value (IV) và SHAP (LightGBM):

1. **FICO score** (`fico_range_low`/`high`) — yếu tố mạnh nhất (IV 0.147, SHAP 0.342), điểm tín dụng tại
   thời điểm vay vẫn là chỉ báo rủi ro tốt nhất dù không dùng grade nội bộ của Lending Club.
2. **DTI** (debt-to-income) — IV 0.061, SHAP 0.169.
3. **Số lần hỏi tín dụng 6 tháng gần nhất** (`inq_last_6mths`) — IV 0.043, SHAP 0.154.
4. **Tình trạng sở hữu nhà** (`home_ownership`) — IV 0.051, SHAP 0.147.
5. **Thu nhập hàng năm**, **thâm niên làm việc**, **tỷ lệ sử dụng hạn mức tín dụng** (`revol_util`) — ảnh
   hưởng yếu hơn nhưng vẫn có ý nghĩa.

Model chính (Logistic Regression + WOE) đạt AUC 0.6534 / KS 0.2216 trên tập test — **dưới mục tiêu đề ra**
(AUC≥0.68, KS≥0.25). Nguyên nhân chính: đã loại `grade`/`sub_grade`/`int_rate` khỏi feature dự báo vì đây là
kết quả từ underwriting nội bộ của Lending Club, không phải đặc điểm khách hàng thô — một quyết định
phương pháp luận có chủ đích để đảm bảo model đánh giá rủi ro độc lập, đánh đổi lấy AUC thấp hơn so với các
phân tích công khai có dùng grade. Dù AUC tuyệt đối chưa đạt, model vẫn phân tách rủi ro rõ rệt ở mức
segment (bad rate 8.4% → 32.3% từ nhóm rủi ro thấp nhất đến cao nhất, xem eda_risk_report.md mục 4).

## Đề xuất cutoff

- **Tại approval rate ~80%**: bad rate nhóm được duyệt theo score = 16.84%, thấp hơn 3.1 điểm % so với
  duyệt ngẫu nhiên (19.94%) — đây là mức cân bằng thực tế hơn để tham khảo làm chính sách vận hành.
- **Cutoff tối ưu hóa Expected Net Return** (theo công thức đơn giản hóa của PROPOSAL) là `pd_score ≤ 0.09`,
  chỉ duyệt 19.1% hồ sơ — quá chặt để làm chính sách thực tế, chỉ mang tính tham chiếu kỹ thuật (chi tiết:
  business_rules_policy.md mục 1 và 3).
- 2 business rules override (`dti > 33.1`, `inq_last_6mths > 2` → bắt buộc Review) bổ sung lớp kiểm soát độc
  lập với score, cả hai đều cho uplift bad rate rõ rệt (+8 đến +9 điểm %).

## Giới hạn của mô hình

- **Dữ liệu lịch sử mô phỏng**: Lending Club P2P lending Mỹ 2015–2017, công ty đã ngừng mảng cho vay bán lẻ
  từ 2020 — kết quả minh họa phương pháp luận, không phải triển khai thực tế. Cần A/B test và giám sát
  Population Stability Index (PSI) nếu áp dụng vào hệ thống hoặc thị trường khác.
- **AUC/KS dưới mục tiêu đề ra** (0.65 vs 0.68, 0.22 vs 0.25) do chủ động loại grade/sub_grade/int_rate
  (tránh model chỉ học lại risk grade nội bộ của LC) — đánh đổi có chủ đích giữa "độc lập về phương pháp" và
  "đạt benchmark kỹ thuật".
- **Vintage effect đã xác nhận**: bad rate khác biệt có ý nghĩa thống kê giữa train (16.3%)/val (21.5%)/test
  (19.9%) — chất lượng tín dụng danh mục Lending Club thay đổi theo thời gian phát hành, model cần được
  hiệu chỉnh lại (recalibrate) định kỳ nếu dùng liên tục qua nhiều vintage.
- **Expected Net Return dùng công thức đơn giản hóa**: `int_rate` áp dụng 1 lần, không tính lãi tích lũy
  theo đúng kỳ hạn 3 năm — số liệu lợi nhuận tuyệt đối (bao gồm kết luận "duyệt ngẫu nhiên bị lỗ") cần được
  tính lại với mô hình dòng tiền đầy đủ trước khi dùng cho quyết định thực tế.
- **LGD là số liệu tổng hợp cố định** (58.87%, tính từ toàn bộ khoản Charged Off trong vintage), chưa phân
  biệt theo segment/loại khách hàng — LGD thực tế có thể khác nhau giữa các nhóm rủi ro.
- **RQ5 (approval rate accepted vs rejected)** chỉ mang tính xấp xỉ do khác schema (`Risk_Score` vs
  `fico_range_low/high`) — không phải reject-inference chuẩn xác.
- **Dashboard Power BI/Tableau chưa được dựng** trong lần này — dữ liệu tổng hợp đã export sẵn vào
  `dashboards/` (segment_summary, cutoff_table, iv_ranking, business_rules, customer_dashboard_data) để dựng
  dashboard khi cần.
