# Daily Log — Tuần 5 (13/08 – 19/08/2026)

| Ngày | Thứ | Công việc thực hiện | Kết quả / Output | Vướng mắc | Kế hoạch ngày tiếp theo |
|---|---|---|---|---|---|
| 13/08/2026 | Thứ Năm | *(không có ghi chép theo ngày)* | | | |
| 14/08/2026 | Thứ Sáu | Commit `5749e1d` — đẩy lên git việc cắt 6 feature nhiễu (SHAP<0.01, 40→34 biến) và tune lại hyperparameters LightGBM đã thực hiện từ cuối ngày 12/08 (tuần 4, xác định qua timestamp thực thi nội bộ trong notebook, không phải ngày thực hiện thật) — commit bị trễ 2 ngày, xem [tuần 4](../../sprint_2/week_4/daily_log.md) | Feature set giảm 40→34; LightGBM AUC/KS/Gini cải thiện lên 0.7023/0.2926/0.4047; số biến đổi dấu hệ số LR giảm từ 9/40 xuống 4/34; `final_recommendation.md`, `business_rules_policy.md` đã cập nhật theo cutoff/net-return mới | | Nghỉ |
| 15/08/2026 | Thứ Bảy | Không làm việc | | | |
| 17/08/2026 | Thứ Hai | Rà soát và hoàn thiện report tuần 4, tuần 5 (daily log + summary) cùng Claude Code | Report tuần 4 & 5 cập nhật đầy đủ | | Bắt đầu dựng dashboard Power BI |
| 18/08/2026 | Thứ Ba | Bổ sung giải thích SHAP local (theo từng khách hàng) cho Customer Dashboard ở notebook 05 — đáp ứng yêu cầu PROPOSAL mục 6.2 "recommendation kèm top 3 lý do ảnh hưởng đến score"; thêm `customer_id` để tra cứu | `dashboards/customer_dashboard_data.csv` có thêm cột `customer_id`, `top_3_reasons` (vd: "dti (tăng rủi ro); loan_to_income (tăng rủi ro); inq_last_6mths (tăng rủi ro)") | Thay đổi này tính đến hết tuần 5 vẫn **chưa được commit** lên git | Dựng dashboard Power BI từ dữ liệu đã refresh |
| 19/08/2026 | Thứ Tư | *(không có ghi chép theo ngày)* | | | |

