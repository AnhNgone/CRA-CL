# Progress Reports — Nhật ký & Báo cáo tiến độ dự án

Folder này **tách riêng** với [`reports/`](../reports/) (chứa deliverable kỹ thuật: BRD, EDA report, business rules, final recommendation...). Đây là nơi lưu **báo cáo tiến độ theo ngày/tuần/sprint** để mentor đánh giá quá trình làm việc, theo lịch chấm điểm mentor đã thông báo.

## Lịch sprint (5 tuần, 3 sprint)

Thống nhất **theo [PROPOSAL.md](../PROPOSAL.md) mục 8** — ranh giới sprint bám theo nội dung kỹ thuật, không chia đều số tuần.

| Sprint | Tuần | Khoảng thời gian | Nội dung |
|---|---|---|---|
| Sprint 1 | Tuần 1–2 | 16/07 – 29/07/2026 | Nền tảng dữ liệu & Business Understanding — BRD, EDA, WOE/IV, feature engineering |
| Sprint 2 | Tuần 3 | 30/07 – 05/08/2026 | Risk Scoring Model — time-based split, LR+WOE vs LightGBM, chọn model chính |
| Sprint 3 | Tuần 4–5 | 06/08 – 19/08/2026 | Business Analysis, Segmentation, Dashboard & Recommendation. Đây cũng là **sprint tổng kết** — mentor đánh giá thêm **thái độ/ý thức/tinh thần làm việc**, ngoài output |

> **Lưu ý cho mentor khi chấm điểm:** lịch này khác cách chia 2-tuần/sprint ban đầu (Sprint 2 = tuần 3–4, Sprint 3 = tuần 5). Đã thống nhất bám theo PROPOSAL để ranh giới sprint trùng với ranh giới nội dung kỹ thuật — Sprint 2 chỉ có 1 tuần vì phạm vi hẹp (modeling), Sprint 3 có 2 tuần vì gộp cả business analysis, dashboard và đóng gói cuối. Mốc nộp `sprint_review` vì vậy rơi vào **cuối tuần 2, cuối tuần 3 và cuối tuần 5**. Weekly summary vẫn nộp đều mỗi tuần như cũ.

## Cấu trúc folder

```
progress_reports/
  sprint_1_week1-2/
    week_1/
      daily_log.md        # nhật ký từng ngày trong tuần
      week_1_summary.md   # báo cáo tổng hợp tuần 1 (nộp mentor)
    week_2/
      daily_log.md
      week_2_summary.md
    sprint_1_review.md    # tổng hợp sprint, đối chiếu Definition of Done, tự chấm điểm
  sprint_2_week3/
    week_3/
      daily_log.md
      week_3_summary.md
    sprint_2_review.md
  sprint_3_week4-5/
    week_4/
      daily_log.md
      week_4_summary.md
    week_5/
      daily_log.md
      week_5_summary.md
    sprint_3_final_review.md   # tổng kết toàn dự án + đánh giá thái độ/tinh thần
```

## Cách dùng

1. **Hàng ngày**: điền vào `daily_log.md` của tuần hiện tại — vài dòng ngắn gọn, không cần văn phong báo cáo.
2. **Cuối mỗi tuần**: tổng hợp từ daily log thành `week_X_summary.md` — đây là file gửi mentor xem hàng tuần.
3. **Cuối mỗi sprint (cuối tuần 2, tuần 3, tuần 5)**: tổng hợp các weekly summary của sprint đó thành `sprint_review.md` — đối chiếu với Definition of Done của sprint tương ứng trong PROPOSAL.md, tự đánh giá.
4. Trước khi nộp lên GitHub, xuất các file `*_summary.md` và `*_review.md` quan trọng sang PDF/DOCX nếu mentor yêu cầu định dạng đó (source vẫn giữ `.md` để dễ version control).

## Theo dõi schedule

Mỗi `week_X_summary.md` có mục "Tình trạng so với kế hoạch" — dùng để mentor thấy được tiến độ thực tế và kế hoạch điều chỉnh, thay vì chỉ báo cáo output. Cập nhật trung thực mục này mỗi tuần.

**Tình trạng tính đến hết Sprint 1 (29/07/2026): vượt tiến độ về khối lượng.** Sprint 1 đạt 4/4 Definition of Done, và đã có bản đầu tiên của phần lớn nội dung Sprint 2–3 (model, segmentation, cutoff, business rules, final recommendation). Việc còn lại chưa đạt là **tiêu chí AUC ≥ 0.68 / KS ≥ 0.25** của Sprint 2 (hiện 0.6516 / 0.2197) — chi tiết và hướng xử lý ở [Sprint 1 Review](sprint_1_week1-2/sprint_1_review.md) mục 6.2.

> Lưu ý khi đọc: khối lượng đi trước kế hoạch không đồng nghĩa chất lượng đã chốt. Phần làm nhanh trong Sprint 1 đã phải quay lại sửa 4 lỗi phương pháp luận (xem Sprint 1 Review mục 6.1) — đây là lý do các weekly summary phân biệt rõ "bản đầu tiên" và "đã rà soát".
