# Progress Reports — Nhật ký & Báo cáo tiến độ dự án

Folder này **tách riêng** với [`reports/`](../reports/) (chứa deliverable kỹ thuật: BRD, EDA report, business rules, final recommendation...). Đây là nơi lưu **báo cáo tiến độ theo ngày/tuần/sprint** để mentor đánh giá quá trình làm việc, theo lịch chấm điểm mentor đã thông báo.

## Lịch đánh giá (5 tuần, 3 sprint)

| Sprint | Tuần | Khoảng thời gian | Nội dung đánh giá |
|---|---|---|---|
| Sprint 1 | Tuần 1–2 | 16/07 – 29/07/2026 | Tuần 1: trình bày proposal · Tuần 2: report các bước tiếp theo · Cuối sprint: tổng hợp điểm Sprint 1 |
| Sprint 2 | Tuần 3–4 | 30/07 – 12/08/2026 | Tương tự Sprint 1 (report tuần → tổng hợp điểm Sprint 2) |
| Sprint 3 | Tuần 5 | 13/08 – 19/08/2026 | Sprint tổng kết — đánh giá thêm **thái độ/ý thức/tinh thần làm việc**, ngoài output |

> Lưu ý: đây là lịch **đánh giá của mentor** (2 tuần/sprint, riêng sprint cuối 1 tuần để tổng kết). Nội dung kỹ thuật từng tuần vẫn bám theo kế hoạch sprint trong [PROPOSAL.md](../PROPOSAL.md) mục 8 (Sprint 1 = nền tảng dữ liệu, Sprint 2 = modeling, Sprint 3 = business/dashboard) — hai lịch không trùng số tuần 1:1, ghi rõ trong từng weekly summary đang làm tới bước nào của PROPOSAL để mentor đối chiếu.

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
    sprint_1_review.md    # tổng hợp 2 tuần, đối chiếu Definition of Done, tự chấm điểm
  sprint_2_week3-4/
    ... (cấu trúc tương tự)
  sprint_3_week5_final/
    week_5/
      daily_log.md
      week_5_summary.md
    sprint_3_final_review.md   # tổng kết toàn dự án + đánh giá thái độ/tinh thần
```

## Cách dùng

1. **Hàng ngày**: điền vào `daily_log.md` của tuần hiện tại — vài dòng ngắn gọn, không cần văn phong báo cáo.
2. **Cuối mỗi tuần**: tổng hợp từ daily log thành `week_X_summary.md` — đây là file gửi mentor xem hàng tuần.
3. **Cuối mỗi sprint (sau tuần chẵn, hoặc tuần 5)**: tổng hợp 2 file weekly summary thành `sprint_review.md` — đối chiếu với Definition of Done của sprint tương ứng trong PROPOSAL.md, tự đánh giá.
4. Trước khi nộp lên GitHub, xuất các file `*_summary.md` và `*_review.md` quan trọng sang PDF/DOCX nếu mentor yêu cầu định dạng đó (source vẫn giữ `.md` để dễ version control).

## Theo dõi schedule

Dự án đang **chậm hơn kế hoạch dự kiến** ngay từ tuần 1. Mỗi `week_X_summary.md` có mục "Tình trạng so với kế hoạch" — dùng để mentor thấy được mức độ trễ và kế hoạch bắt kịp (catch-up plan), thay vì chỉ báo cáo output. Cập nhật trung thực mục này mỗi tuần.
