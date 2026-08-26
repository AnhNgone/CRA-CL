# Báo cáo Tuần 2 (23/07 – 29/07/2026)

**Sprint:** Sprint 1 — Nền tảng dữ liệu & Business Understanding (theo [PROPOSAL.md](../../../PROPOSAL.md) mục 8)
**Trọng tâm tuần 2:** Rà soát và làm chắc lại phần đã chạy nhanh — không phải làm mới, theo đúng kế hoạch tự đặt cuối tuần 1 (xem [week_1_summary.md](../week_1/week_1_summary.md) mục 4).

## 1. Mục tiêu tuần
- [x] Rà soát lại leakage columns, multicollinearity, dấu hệ số scorecard, và thứ tự feature selection vs. split — 4 rủi ro tự đặt ra cuối tuần 1
- [x] Chạy lại toàn bộ pipeline (notebook 02→05) sau khi sửa
- [x] Cập nhật báo cáo (BRD, EDA report) theo số liệu đã sửa

## 2. Công việc đã hoàn thành
- **R1 — Bổ sung 25 cột leakage bị thiếu** trong `LEAKAGE_COLUMNS` (nguy hiểm nhất: `last_fico_range_low/high` — FICO đo sau giải ngân). Thêm `assert_no_leakage()` làm lớp chặn thứ hai.
- **R3 — Gộp `fico_range_low`/`fico_range_high` thành `fico_mid`** sau khi thực nghiệm (`experiments/exp01_fico_mid.py`) xác nhận hệ số bị chia đôi do multicollinearity.
- **R4 — Chẩn đoán và sửa hệ số `revol_util` sai dấu** — đi qua 2 giả thuyết sai trước khi tìm ra nguyên nhân thật (suppressor effect với FICO, `experiments/exp02_revol_util_sign.py`). Phát hiện thêm ô kiểm tra dấu hệ số ở notebook 04 bị viết ngược, đã sửa lại.
- **R5 — Chuyển bước chọn biến (IV) xuống sau time-based split**, chỉ dùng nhãn train thay vì toàn vintage — 3/16 biến đổi kết quả chọn.
- Chạy lại toàn bộ pipeline 02→05 sau khi sửa cả 4 vấn đề, cập nhật `reports/BRD.md` và `reports/eda_risk_report.md` theo số liệu mới.

## 3. Kết quả / Deliverables
- `LEAKAGE_COLUMNS` mở rộng 13→38 cột, `src/data/filter_vintage.py::assert_no_leakage()`
- `src/features/clean.py` — thêm `fico_mid`
- Notebook 04 — sửa ô kiểm tra dấu hệ số scorecard
- Model sau khi sửa: Logistic Regression + WOE — 8/8 hệ số đúng dấu (trước đó 1/8 sai), AUC test 0.6516 (giảm nhẹ từ 0.6534 — có chủ đích, xem sprint_1_review.md mục 5.1)
- `reports/BRD.md`, `reports/eda_risk_report.md` cập nhật theo số liệu đã sửa

## 4. Tình trạng so với kế hoạch
- [x] Đúng tiến độ
- Chi tiết chênh lệch: đúng như kế hoạch tự đặt cuối tuần 1 — dành tuần 2 để rà soát thay vì chạy tiếp sang phần mới.
- Nguyên nhân: không có chênh lệch — nhưng việc rà soát phát hiện ra nhiều vấn đề hơn dự tính ban đầu (4 lỗi, trong đó R5 ảnh hưởng lớn hơn đánh giá sơ bộ).

## 5. Kế hoạch tuần 3
- Mở rộng candidate feature set lên ~60 biến bureau (R2), tạo nhóm biến tỷ lệ (R6)
- Chạy lại LightGBM trên feature set mới, chốt model chính

## 6. Tham chiếu
- [PROPOSAL.md](../../../PROPOSAL.md)
- [Sprint 1 Review, mục 5.1](../sprint_1_review.md)
- [Daily log tuần 2](daily_log.md) — xem ghi chú minh bạch đầu trang
