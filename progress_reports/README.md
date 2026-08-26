# Progress Reports — Nhật ký & Báo cáo tiến độ dự án

Folder này **tách riêng** với [`reports/`](../reports/) (chứa deliverable kỹ thuật: BRD, EDA report, business rules, final recommendation...). Đây là nơi lưu **báo cáo tiến độ theo ngày/tuần/sprint** để mentor đánh giá quá trình làm việc, theo lịch chấm điểm mentor đã thông báo.

## Lịch sprint (6 tuần, 3 sprint, mỗi sprint 2 tuần)

Thống nhất **theo [PROPOSAL.md](../PROPOSAL.md) mục 8**.

| Sprint | Tuần | Khoảng thời gian | Nội dung |
|---|---|---|---|
| Sprint 1 | Tuần 1–2 | 16/07 – 29/07/2026 | Nền tảng dữ liệu & Business Understanding — BRD, EDA, WOE/IV, feature engineering |
| Sprint 2 | Tuần 3–4 | 30/07 – 12/08/2026 | Risk Scoring Model — time-based split, LR+WOE vs LightGBM, chọn model chính |
| Sprint 3 | Tuần 5–6 | 13/08 – 26/08/2026 | Business Analysis, Segmentation, Dashboard & Recommendation. Đây cũng là **sprint tổng kết** — mentor đánh giá thêm **thái độ/ý thức/tinh thần làm việc**, ngoài output |

> **Lưu ý cho mentor khi chấm điểm:** kế hoạch gốc là 5 tuần; lịch thực tế bị giãn thêm vài ngày nên làm
> tròn thành tuần 6, giữ đều 2 tuần/sprint cho cả 3 sprint (khác bản nháp đầu tiên từng chia sprint không
> đều tuần theo ranh giới nội dung). Vì tiến độ thực tế nhiều tuần đi trước kế hoạch (xem từng
> `week_X_summary.md` mục "Tình trạng so với kế hoạch"), một phần nội dung thuộc phạm vi Sprint 3
> (segmentation, cutoff, PSI) đã được hoàn thành sớm trong tuần 4 (thuộc Sprint 2 theo lịch mới) — có ghi
> chú rõ trong [Sprint 2 Review](sprint_2/sprint_2_review.md) và [Sprint 3 Final Review](sprint_3/sprint_3_final_review.md).
> Mốc nộp `sprint_review` rơi vào **cuối tuần 2, cuối tuần 4 và cuối tuần 6**. Weekly summary vẫn nộp đều
> mỗi tuần như cũ.

## Cấu trúc folder

```
progress_reports/
  sprint_1/
    week_1/
      daily_log.md        # nhật ký từng ngày trong tuần
      week_1_summary.md   # báo cáo tổng hợp tuần 1 (nộp mentor)
    week_2/
      daily_log.md
      week_2_summary.md
    sprint_1_review.md    # tổng hợp sprint, đối chiếu Definition of Done, tự chấm điểm
  sprint_2/
    week_3/
      daily_log.md
      week_3_summary.md
    week_4/
      daily_log.md
      week_4_summary.md
    sprint_2_review.md
  sprint_3/
    week_5/
      daily_log.md
      week_5_summary.md
    week_6/
      daily_log.md
      week_6_summary.md
    sprint_3_final_review.md   # tổng kết toàn dự án + đánh giá thái độ/tinh thần
```

## Cách dùng

1. **Hàng ngày**: điền vào `daily_log.md` của tuần hiện tại — vài dòng ngắn gọn, không cần văn phong báo cáo.
2. **Cuối mỗi tuần**: tổng hợp từ daily log thành `week_X_summary.md` — đây là file gửi mentor xem hàng tuần.
3. **Cuối mỗi sprint (cuối tuần 2, tuần 4, tuần 6)**: tổng hợp các weekly summary của sprint đó thành `sprint_review.md` — đối chiếu với Definition of Done của sprint tương ứng trong PROPOSAL.md, tự đánh giá.
4. Trước khi nộp lên GitHub, xuất các file `*_summary.md` và `*_review.md` quan trọng sang PDF/DOCX nếu mentor yêu cầu định dạng đó (source vẫn giữ `.md` để dễ version control).

## Theo dõi schedule

Mỗi `week_X_summary.md` có mục "Tình trạng so với kế hoạch" — dùng để mentor thấy được tiến độ thực tế và kế hoạch điều chỉnh, thay vì chỉ báo cáo output. Cập nhật trung thực mục này mỗi tuần.

**Tình trạng tính đến hết Sprint 2 (12/08/2026): đạt Definition of Done, vượt tiến độ.** Sau khi mở rộng
candidate feature set (17→81 biến bureau, xem [Sprint 2 Review](sprint_2/sprint_2_review.md) mục 4–5),
tiêu chí AUC ≥ 0.68 / KS ≥ 0.25 đã đạt: **LightGBM AUC 0.7004 / KS 0.2891**. Model chính đổi từ Logistic
Regression sang **LightGBM** (chênh lệch AUC vượt ngưỡng 0.02 tự đặt). Đã làm sớm luôn phần segmentation,
cutoff và PSI mà kế hoạch dự kiến để Sprint 3 — chi tiết ở [tuần 4](sprint_2/week_4/week_4_summary.md).

**Tình trạng tính đến hết dự án / hết Sprint 3 (26/08/2026): 5/6 deliverable hoàn chỉnh.** Tuần 5 cắt 6
feature nhiễu và tune lại LightGBM (AUC/KS cải thiện lên 0.7023/0.2926), bổ sung giải thích SHAP theo từng
khách hàng cho Customer Dashboard. Hạng mục còn tồn đọng duy nhất: **2 dashboard Power BI/Tableau chưa được
dựng thật** — mới có data export trong `dashboards/*.csv`. Chi tiết đầy đủ và tự đánh giá cuối dự án xem
[Sprint 3 Final Review](sprint_3/sprint_3_final_review.md).

> Lưu ý khi đọc: khối lượng/tốc độ đi trước kế hoạch không đồng nghĩa không có vấn đề phát sinh. Sprint 2 phát
> hiện và sửa 1 bug hướng quy tắc business rule (biến `bc_open_to_buy` bị flag ngược — xem Sprint 2 Review mục
> 6), 1 vấn đề đa cộng tuyến ở Logistic Regression, và 1 lỗi công thức Expected Net Return (thiếu nhân kỳ hạn
> 3 năm, sửa ở tuần 4). Sprint 1 trước đó cũng đã phải quay lại sửa 4 lỗi phương pháp luận (xem Sprint 1
> Review mục 6.1) — đây là lý do các weekly summary phân biệt rõ "bản đầu tiên" và "đã rà soát".
