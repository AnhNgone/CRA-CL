# Daily Log — Tuần 4 (06/08 – 12/08/2026)

Ghi ngắn gọn mỗi ngày, không cần văn phong báo cáo. Cuối tuần tổng hợp thành [week_4_summary.md](week_4_summary.md).

> Các dòng dưới đây (đến hết 10/08) ghi nhận khách quan từ lịch sử git (thời điểm commit, nội dung diff) và
> phiên làm việc thực tế trong ngày — không suy diễn cảm nhận/khó khăn cá nhân nếu không có bằng chứng. Ngày
> 11–12/08 để trống vì chưa diễn ra tại thời điểm cập nhật file này (10/08/2026).

| Ngày | Thứ | Công việc thực hiện | Kết quả / Output | Vướng mắc | Kế hoạch ngày tiếp theo |
|---|---|---|---|---|---|
| 06/08/2026 | Thứ Năm | Thêm nhóm biến tỷ lệ (`loan_to_income`, `tot_cur_bal_to_income`...), refresh lại report/dashboard theo feature mới (commit `ecd97d2`); cập nhật sprint 2 review (commit `3442979`) | 2 commit: `ecd97d2` (income-ratio features + refresh reports/dashboards), `3442979` (update sprint 2 review) | | Chạy segmentation/cutoff analysis (notebook 05) theo model đã chốt cuối Sprint 2 |
| 07/08/2026 | Thứ Sáu | | | | |
| 08/08/2026 | Thứ Bảy | | | | |
| 10/08/2026 | Thứ Hai | Rà soát tình trạng project với mentor/Claude Code; chạy lại notebook 04 để kiểm tra reproducibility (kết quả không đổi); thêm tính Population Stability Index (train/val/test) và sửa lỗi công thức Expected Net Return (thiếu nhân kỳ hạn 3 năm) trong notebook 05 — phát hiện thêm 1 lỗi phương pháp phát sinh từ đó (chọn cutoff theo Expected Net Return tuyệt đối bị lệch khi lãi tăng theo khối lượng duyệt) và sửa bằng cách chọn theo uplift so với duyệt ngẫu nhiên; cập nhật `business_rules_policy.md`/`final_recommendation.md` theo số liệu mới | `reports/figures/psi_report.csv` (PSI train→val 0.035, train→test 0.010, val→test 0.011 — ổn định); cutoff đề xuất đổi từ 0.13 (Sprint 2, công thức lãi 1 kỳ) sang 0.17 (đúng kỳ hạn 3 năm, chọn theo uplift); `dashboards/*.csv` đã refresh theo cutoff mới | Phát hiện lỗi phương pháp ở bước chọn cutoff (xem cột "Công việc thực hiện") — đã sửa trong cùng ngày, không phải vướng mắc còn tồn đọng | Điền tiếp daily log các ngày 11–12/08 khi diễn ra; bắt đầu dựng dashboard |
| 11/08/2026 | Thứ Ba | | | | |
| 12/08/2026 | Thứ Tư | | | | |
