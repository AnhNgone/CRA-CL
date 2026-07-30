# Final Recommendation

## Yếu tố rủi ro chính

Xếp hạng nhất quán giữa Information Value (IV) và SHAP (LightGBM):

1. **FICO score** (`fico_mid`) — yếu tố mạnh nhất (IV 0.150, SHAP 0.357), điểm tín dụng tại thời điểm vay vẫn
   là chỉ báo rủi ro tốt nhất dù không dùng grade nội bộ của Lending Club. Dùng dưới dạng một biến gộp
   `fico_mid = (fico_range_low + fico_range_high) / 2`: hai biến gốc chênh nhau đúng 4 điểm và tương quan gần
   như tuyệt đối, đưa cả hai vào Logistic Regression chỉ làm hệ số bị chia đôi mà không thêm thông tin.
2. **DTI** (debt-to-income) — IV 0.064, SHAP 0.202. Đây là biến có **hệ số lớn nhất** trong scorecard (−0.973).
3. **Số lần hỏi tín dụng 6 tháng gần nhất** (`inq_last_6mths`) — IV 0.050, SHAP 0.163.
4. **Tình trạng sở hữu nhà** (`home_ownership`) — IV 0.047, SHAP 0.148.
5. **Dư nợ tín dụng quay vòng** (`revol_bal`) — IV 0.020, SHAP 0.091.
6. **Độ dài lịch sử tín dụng**, **thâm niên làm việc**, **thu nhập hàng năm** — ảnh hưởng yếu hơn nhưng vẫn
   có ý nghĩa thống kê.

**Về `revol_util` (tỷ lệ sử dụng hạn mức tín dụng) — vì sao không có trong model:** xét riêng lẻ thì đây là
chỉ báo rủi ro hợp lệ và đơn điệu (bad rate tăng đều 12.7% → 18.6% từ nhóm dùng ít nhất đến nhóm dùng nhiều
nhất). Nhưng **không nên đưa vào model cùng FICO**: hai biến tương quan −0.428 và credit utilization vốn đã là
một thành phần trong công thức FICO, nên tín hiệu bị trùng lặp. Trong bản model đầu tiên, biến này lọt vào do
lỗi ở bước chọn biến (IV tính trên toàn bộ vintage thay vì chỉ trên train) và gây ra hệ số sai dấu. Sau khi
sửa đúng phương pháp, nó tự động bị loại. Chi tiết: eda_risk_report.md mục 3.1.

Model chính (Logistic Regression + WOE, 8 biến) đạt **AUC 0.6516 / KS 0.2197 / Gini 0.3033** trên tập test —
**dưới mục tiêu đề ra** (AUC≥0.68, KS≥0.25). Toàn bộ 8 hệ số đều đúng dấu nên scorecard diễn giải được.
Có hai nguyên nhân khiến chỉ số chưa đạt, mức độ xử lý được khác nhau:

1. **Đã chủ động loại `grade`/`sub_grade`/`int_rate`** khỏi feature dự báo vì đây là kết quả từ underwriting
   nội bộ của Lending Club, không phải đặc điểm khách hàng thô. Đây là quyết định phương pháp luận có chủ
   đích, không định khắc phục. Hệ quả: con số AUC của dự án **không so sánh trực tiếp được** với mức 0.68–0.72
   thường được trích dẫn cho Lending Club, vì các phân tích đó hầu hết *có* dùng grade — tức là đo lại khả
   năng học lại underwriting của LC chứ không phải đánh giá rủi ro độc lập.
2. **Feature space mới khai thác 17/151 cột — đây mới là nguyên nhân chính và khắc phục được.** Còn khoảng 60
   cột hợp lệ tại thời điểm xét duyệt chưa được xét đến, phần lớn là biến bureau (`verification_status`,
   `pub_rec_bankruptcies`, `mort_acc`, `mths_since_last_delinq`, `bc_util`, `tot_hi_cred_lim`,
   `acc_open_past_24mths`...). Với chỉ 8 biến vào model, AUC ~0.65 là kỳ vọng hợp lý. Mở rộng candidate set
   là hướng có khả năng cao nhất đạt mục tiêu **mà vẫn không dùng grade** — đây là ưu tiên số 1 của Sprint 2.

Dù AUC tuyệt đối chưa đạt, model vẫn phân tách rủi ro rõ rệt ở mức segment (bad rate 8.6% → 32.2% từ nhóm rủi
ro thấp nhất đến cao nhất, chênh gần 3.8 lần — xem eda_risk_report.md mục 4) — tức là vẫn dùng được để xếp
hạng và phân nhóm hồ sơ, kể cả khi độ chính xác tuyệt đối còn hạn chế.

**Về sự thay đổi so với bản báo cáo đầu tiên** (AUC 0.6534 / KS 0.2216): con số cũ được tạo ra khi bước chọn
biến còn dùng IV tính trên toàn bộ vintage, tức là nhãn của kỳ test đã tham gia vào việc chọn biến. Sau khi
chuyển bước này xuống sau time-based split và chỉ dùng nhãn tập train, AUC test **giảm nhẹ 0.0018** — đúng
như kỳ vọng khi loại bỏ thông tin của tập test khỏi quy trình. Con số 0.6516 là con số trung thực; 0.6534 đã
bị thổi nhẹ. Việc sửa cũng thay đổi tập biến: `revol_util` bị loại, `credit_history_length` và `revol_bal`
được nhận vào, và toàn bộ hệ số nay đúng dấu (trước là 7/8).

## Đề xuất cutoff

- **Tại approval rate ~79%**: bad rate nhóm được duyệt theo score = 16.81%, thấp hơn 3.1 điểm % so với
  duyệt ngẫu nhiên (19.94%) — đây là mức cân bằng thực tế hơn để tham khảo làm chính sách vận hành.
- **Cutoff tối ưu hóa Expected Net Return** (theo công thức đơn giản hóa của PROPOSAL) là `pd_score ≤ 0.11`,
  chỉ duyệt 28.8% hồ sơ — vẫn quá chặt để làm chính sách thực tế, chỉ mang tính tham chiếu kỹ thuật (chi tiết:
  business_rules_policy.md mục 1 và 3).
- 2 business rules override (`dti > 33.14`, `inq_last_6mths > 2` → bắt buộc Review) bổ sung lớp kiểm soát độc
  lập với score, cả hai đều cho uplift bad rate rõ rệt (+8.0 đến +9.2 điểm %).

## Giới hạn của mô hình

- **Dữ liệu lịch sử mô phỏng**: Lending Club P2P lending Mỹ 2015–2017, công ty đã ngừng mảng cho vay bán lẻ
  từ 2020 — kết quả minh họa phương pháp luận, không phải triển khai thực tế. Cần A/B test và giám sát
  Population Stability Index (PSI) nếu áp dụng vào hệ thống hoặc thị trường khác.
- **AUC/KS dưới mục tiêu đề ra** (0.652 vs 0.68, 0.220 vs 0.25) do hai nguyên nhân: (a) chủ động loại
  grade/sub_grade/int_rate — đánh đổi có chủ đích giữa "độc lập về phương pháp" và "đạt benchmark kỹ thuật";
  (b) feature space mới khai thác 17/151 cột, còn ~60 biến bureau chưa thử — đây là nguyên nhân chính và là
  việc sẽ làm ở Sprint 2. Xem phần đầu tài liệu này.
- **Model chỉ dùng 8 biến**, tất cả đều là biến hồ sơ cơ bản. Chưa có biến tỷ lệ (payment-to-income, dư nợ /
  thu nhập) vốn là chuẩn mực trong credit scoring — việc lọc theo IV **đơn biến** trước khi tạo biến tỷ lệ đã
  loại sớm nguyên liệu (ví dụ `loan_amnt` có IV 0.005 nhưng `loan_amnt / annual_inc` thường mạnh hơn nhiều).
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
