# Báo cáo Tuần 4 (06/08 – 12/08/2026)

**Sprint:** Sprint 3 — Business Analysis, Segmentation, Dashboard & Recommendation (theo [PROPOSAL.md](../../../PROPOSAL.md) mục 8) — tuần đầu của sprint
**Trọng tâm tuần 4:** Customer Segmentation theo dải risk score, cutoff/profitability analysis, business rules override

## 1. Mục tiêu tuần
- [ ] Customer Segmentation theo dải risk score (3–5 nhóm), kiểm định chi-square/CI
- [ ] Cutoff/Profitability Analysis: approval rate, bad rate, Expected Net Return theo từng ngưỡng
- [ ] 2–3 Business Rules override dựa trên biến IV cao nhất (tính trên tập train)
- [ ] Chạy lại toàn bộ 3 mục trên theo model cuối của Sprint 2 — điểm số đổi thì ranh giới segment và cutoff cũng đổi

> Nếu việc mở rộng feature ở Sprint 2 chưa xong trong tuần 3, phần còn lại làm nốt đầu tuần này rồi mới chạy segmentation — ghi rõ vào daily log.

## 2. Công việc đã hoàn thành
_(tổng hợp từ [daily_log.md](daily_log.md))_

- Segmentation theo dải risk score: 5 nhóm (S1–S5), kiểm định chi-square xác nhận default rate tách biệt có
  ý nghĩa thống kê (chi2=7892.78, p<0.000001) — bad rate từ 6.59% (S1) đến 38.58% (S5).
- Cutoff/Profitability Analysis: đã tính, và sửa lại đúng công thức lãi theo kỳ hạn 3 năm (trước đó dùng lãi
  1 kỳ) — phát sinh thêm 1 phát hiện phương pháp quan trọng (chọn cutoff theo Expected Net Return tuyệt đối
  không còn hợp lý sau khi sửa, đã đổi sang chọn theo uplift so với duyệt ngẫu nhiên). Cutoff đề xuất mới:
  `pd_score ≤ 0.17` (approval rate 55.9%, bad rate nhóm duyệt 11.71%).
- 2 Business Rules override (`acc_open_past_24mths > 11`, `bc_open_to_buy < 155`) — không đổi so với cuối
  Sprint 2, không phụ thuộc vào phần sửa Expected Net Return.
- Population Stability Index (PSI) — hạng mục tồn đọng từ final_recommendation.md — đã tính: train→val
  0.035, train→test 0.010, val→test 0.011, cả ba đều dưới ngưỡng 0.10 (ổn định).
- Đã cập nhật `business_rules_policy.md` và `final_recommendation.md` theo số liệu cutoff/PSI mới; đồng bộ
  lại `dashboards/*.csv` (dữ liệu cho 2 dashboard, chưa dựng file `.pbix`/`.twbx` thật).

## 3. Kết quả / Deliverables
- `notebooks/05_segmentation_profitability.ipynb` — chạy đầy đủ, có PSI, cutoff/business rules đã sửa đúng.
- `reports/figures/psi_report.csv`, `cutoff_table.csv`, `business_rules.csv`, `cutoff_profitability_analysis.png` — mới/cập nhật.
- `reports/business_rules_policy.md`, `reports/final_recommendation.md` — cập nhật theo số liệu mới.
- `dashboards/*.csv` — refresh theo cutoff/segment mới, sẵn sàng làm nguồn dữ liệu cho dashboard.

## 4. Tình trạng so với kế hoạch
- [x] Đúng tiến độ  [ ] Chậm hơn dự kiến  [ ] Vượt tiến độ
- Chi tiết chênh lệch: mục tiêu tuần 4 theo PROPOSAL (segmentation, cutoff, business rules) đã hoàn thành
  đúng phạm vi; ngoài ra còn xử lý thêm 1 hạng mục vốn dự kiến để cuối dự án (PSI) và sửa 1 lỗi phương pháp
  phát hiện trong quá trình làm (công thức lãi 1 kỳ → 3 năm, và hệ quả chọn cutoff theo net return tuyệt đối).
- Nguyên nhân (nếu có chênh lệch): không có chênh lệch tiêu cực; phần vượt thêm (PSI, sửa công thức) là chủ
  động xử lý sớm các hạng mục còn tồn đọng đã ghi trong final_recommendation.md để tuần 5 tập trung được vào
  dashboard và đóng gói deliverables.
- Kế hoạch bắt kịp (nếu chậm): không áp dụng.

## 5. Vướng mắc & cách xử lý
- Phát hiện lỗi phương pháp khi sửa công thức Expected Net Return: sau khi nhân lãi đủ 3 năm, chọn cutoff
  theo Expected Net Return **tuyệt đối** bị kéo lệch về phía duyệt gần hết hồ sơ (~97%) vì tổng lãi tăng theo
  khối lượng, không phản ánh đúng giá trị gia tăng của model. Xử lý: đổi tiêu chí chọn cutoff sang argmax
  **uplift so với duyệt ngẫu nhiên** — khớp với lưu ý "so sánh tương đối giữa các cutoff" đã ghi sẵn trong
  business_rules_policy.md nhưng logic code trước đó chưa áp dụng đúng. Không có vướng mắc nào còn tồn đọng
  cuối tuần 4.
- Dashboard Power BI/Tableau (`.pbix`/`.twbx`) chưa được dựng — chỉ có data export trong `dashboards/`. Việc
  dựng dashboard thật đòi hỏi thao tác trực tiếp trên ứng dụng GUI (Power BI Desktop/Tableau Desktop), không
  thể thực hiện qua notebook/code — chuyển sang việc cần làm ở tuần 5.

## 6. Kế hoạch tuần 5
- Dựng 2 dashboard (Risk & Portfolio, Customer) trên Power BI/Tableau từ dữ liệu đã export trong `dashboards/`.
- Rà soát lại Risk Analysis Report / EDA report theo số liệu model cuối.
- Hoàn thiện `sprint_3_final_review.md` (đối chiếu DoD, so sánh kế hoạch vs thực tế, tự đánh giá thái độ).
- Đóng gói toàn bộ 6 deliverables theo PROPOSAL mục 9.

## 7. Tham chiếu
- [PROPOSAL.md](../../../PROPOSAL.md)
- [Daily log tuần 4](daily_log.md)
