# Business Rules & Policy / Profitability Recommendation

Phân tích trên tập test (105,204 khoản vay, issue_d ≥ 2017-03), dùng model chính Logistic Regression + WOE
(xem eda_risk_report.md mục 3). Tất cả số liệu và biểu đồ nguồn: `reports/figures/cutoff_table.csv`,
`cutoff_profitability_analysis.png`, `business_rules.csv`.

## 1. Cutoff Analysis (approval rate, bad rate, Expected Net Return)

**LGD (Loss Given Default) thực tế**: tính từ dữ liệu gốc (aggregate, không dùng làm feature model) =
**58.87%** = 1 − (tổng vốn gốc thu hồi + recoveries) / tổng vốn gốc giải ngân, trên các khoản Charged Off
trong vintage 2015–2017. Đây là input cho Expected Net Return bên dưới, không phải giả định tùy ý.

**Công thức** (theo PROPOSAL mục 5.2): `Expected Net Return = Σ(int_rate × loan_amnt, nhóm Good được duyệt)
− Σ(loan_amnt × LGD, nhóm Bad được duyệt)`.

> **Giới hạn quan trọng của công thức này**: `int_rate` được áp dụng 1 lần trên `loan_amnt` (không nhân
> thêm số năm kỳ hạn 3 năm), đúng theo công thức đề xuất trong PROPOSAL — đây là một **đơn giản hóa**, không
> phải thu nhập lãi thực tế trong suốt vòng đời khoản vay. Nếu tính lãi tích lũy đủ 3 năm, thu nhập lãi sẽ
> cao hơn đáng kể và kết luận về "duyệt ngẫu nhiên có lãi hay lỗ" bên dưới có thể thay đổi. Số liệu này nên
> được xem là **so sánh tương đối giữa các cutoff**, không phải con số lợi nhuận tuyệt đối chính xác.

**Tại approval rate ~79.4%** (mức tham chiếu ~80% theo PROPOSAL mục 2): bad rate nhóm được duyệt theo score =
**16.81%**, so với bad rate nếu duyệt ngẫu nhiên (= bad rate quần thể) = **19.94%** — model giảm được ~3.1
điểm % bad rate tại cùng mức approval rate.

**Cutoff đề xuất** (tối đa hóa Expected Net Return trên tập test, theo công thức đơn giản hóa ở trên):

| Chỉ số | Giá trị |
|---|---|
| Cutoff (pd_score ≤) | 0.11 |
| Approval rate | 28.8% |
| Bad rate (nhóm duyệt) | 9.98% |
| Interest income | $35.60M |
| Expected loss | $29.16M |
| Expected Net Return | $6.45M |
| Net Return nếu duyệt ngẫu nhiên (cùng n) | −$5.66M |
| Uplift so với ngẫu nhiên | $12.10M |

Với công thức đơn giản hóa (không nhân số năm kỳ hạn), duyệt **ngẫu nhiên** ở bad rate quần thể 19.94% và
LGD 58.87% cho kết quả **âm** (chi phí vỡ nợ vượt thu nhập lãi 1 kỳ) — đây là lý do cutoff tối ưu hóa net
return nghiêng về chặt (28.8% approval rate). **Đây là góc nhìn cực đoan** (tối đa hóa lợi nhuận đơn thuần,
không ràng buộc khối lượng/doanh thu tối thiểu) — mục 3 dưới đây đề xuất mức cân bằng hơn.

## 2. Business Rules Override

2 quy tắc dựa trên biến có IV cao nhất **tính trên tập train** (`iv_table_train.csv`) trong nhóm có thể đặt
ngưỡng nghiệp vụ rõ ràng (loại các biến categorical như `addr_state` — khó diễn đạt thành 1 ngưỡng override
đơn giản). Ngưỡng đặt tại percentile 95 của tập test:

| Quy tắc | % dân số bị đánh dấu | Bad rate nhóm bị đánh dấu | Bad rate chung | Uplift |
|---|---|---|---|---|
| `dti > 33.14` → bắt buộc Review | 4.99% | 27.95% | 19.94% | +8.01 điểm % |
| `inq_last_6mths > 2` → bắt buộc Review | 3.81% | 29.09% | 19.94% | +9.15 điểm % |

Cả 2 quy tắc đều cho thấy uplift rõ rệt (bad rate nhóm bị đánh dấu cao hơn ~8-9 điểm % so với trung bình),
xác nhận tính hợp lý của việc override thủ công dù model score đã tốt — bắt các hồ sơ có tín hiệu rủi ro cụ
thể (nợ/thu nhập cao, nhiều lần hỏi tín dụng gần đây) phải qua xét duyệt thủ công bổ sung.

## 3. Đề xuất Policy

Áp dụng kết hợp cutoff + business rules trên tập test cho kết quả phân bổ:

| Quyết định | Tỷ lệ |
|---|---|
| Approve | 28.2% |
| Review (business rule override) | 8.6% |
| Reject | 63.2% |

**Khuyến nghị**: cutoff `pd_score ≤ 0.11` (tối đa hóa net return theo công thức đơn giản hóa) là điểm tham
chiếu kỹ thuật, nhưng **vẫn quá chặt để làm chính sách vận hành thực tế** (chỉ duyệt ~29% hồ sơ). Vì mục tiêu
dự án là minh họa phương pháp luận (không triển khai thật — xem PROPOSAL mục 10), đề xuất:

- Dùng bảng cutoff đầy đủ (`cutoff_table.csv`) để chọn điểm cân bằng theo khẩu vị rủi ro thực tế của tổ chức
  (ví dụ mức ~79% approval rate cho bad rate 16.81%, thay vì điểm tối ưu toán học ở 29%).
- Trước khi dùng cutoff này cho quyết định thật, cần tính lại Expected Net Return với lãi tích lũy đúng kỳ
  hạn (3 năm) thay vì công thức 1 kỳ hiện tại — xem giới hạn ở mục 1.
- Giữ nguyên 2 business rules override làm lớp bảo vệ bổ sung, độc lập với cutoff score.
