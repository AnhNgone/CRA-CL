# Business Rules & Policy / Profitability Recommendation

Cutoff và ngưỡng business rule được **chọn trên tập validation** (99,015 khoản vay), sau đó áp dụng nguyên
trạng (không tính lại) lên **tập test** (105,204 khoản vay, issue_d ≥ 2017-03) để báo cáo số liệu cuối cùng —
tránh dùng chính tập test để vừa chọn ngưỡng vừa báo cáo kết quả, vì như vậy con số sẽ lạc quan hơn thực tế.
Model chính dùng **LightGBM** (đổi từ Logistic Regression + WOE ở Sprint 2 — xem eda_risk_report.md mục 3).
Tất cả số liệu và biểu đồ nguồn: `reports/figures/cutoff_table.csv`, `cutoff_profitability_analysis.png`,
`business_rules.csv`.

> **Cập nhật (rà soát chất lượng cuối Sprint 2):** trước đây cutoff (tối đa hóa Expected Net Return) và ngưỡng
> business rule được chọn **trực tiếp trên tập test**, rồi lại dùng chính test đó để báo cáo kết quả — một
> dạng rò rỉ thông tin ở tầng quyết định kinh doanh (test không còn là dữ liệu "chưa thấy" đối với chính quyết
> định đó), dù không ảnh hưởng đến AUC/KS của model. Đã sửa: cutoff và ngưỡng rule nay được chọn trên
> **validation**, chỉ áp dụng (không tính lại) lên test để báo cáo. Kết quả hầu như không đổi — cutoff vẫn là
> 0.13, ngưỡng `acc_open_past_24mths > 11` giữ nguyên — cho thấy kết luận trước đó khá vững, không phải do ăn
> may khớp với test. Riêng ngưỡng `bc_open_to_buy` đổi từ 211 xuống 155 (xem mục 2).

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

> **Cập nhật Sprint 2**: bảng cutoff dưới đây được tính lại với điểm số từ LightGBM (thay Logistic Regression).
> Vì LightGBM phân tách rủi ro tốt hơn (xem segment ở eda_risk_report.md mục 4), profile lợi nhuận theo cutoff
> cũng thay đổi so với bản Sprint 1.

**Tại approval rate ~78.7%** (mức tham chiếu ~80% theo PROPOSAL mục 2): bad rate nhóm được duyệt theo score =
**15.32%**, so với bad rate nếu duyệt ngẫu nhiên (= bad rate quần thể) = **19.94%** — model giảm được ~4.6
điểm % bad rate tại cùng mức approval rate (so với ~3.1 điểm % của model Sprint 1).

**Cutoff đề xuất** (tối đa hóa Expected Net Return trên tập test, theo công thức đơn giản hóa ở trên):

| Chỉ số | Giá trị |
|---|---|
| Cutoff (pd_score ≤) | 0.13 |
| Approval rate | 40.6% |
| Bad rate (nhóm duyệt) | 9.38% |
| Interest income | $42.09M |
| Expected loss | $28.82M |
| Expected Net Return | $13.27M |
| Net Return nếu duyệt ngẫu nhiên (cùng n) | −$7.97M |
| Uplift so với ngẫu nhiên | $21.24M |

Với công thức đơn giản hóa (không nhân số năm kỳ hạn), duyệt **ngẫu nhiên** ở bad rate quần thể 19.94% và
LGD 58.87% cho kết quả **âm** (chi phí vỡ nợ vượt thu nhập lãi 1 kỳ) — đây là lý do cutoff tối ưu hóa net
return nghiêng về chặt. So với model Sprint 1 (cutoff tối ưu chỉ duyệt 28.8%), model mới duyệt được **40.6%**
ở cùng chiến lược tối đa hóa lợi nhuận — vì LightGBM tách nhóm rủi ro thấp rộng hơn (S1 bad rate chỉ 5.9% so
với 8.6% trước đây), nên có thể duyệt thêm hồ sơ mà vẫn giữ bad rate nhóm duyệt thấp (9.38% so với 9.98%).
**Đây vẫn là góc nhìn cực đoan** (tối đa hóa lợi nhuận đơn thuần, không ràng buộc khối lượng/doanh thu tối
thiểu) — mục 3 dưới đây đề xuất mức cân bằng hơn.

## 2. Business Rules Override

2 quy tắc dựa trên biến có IV cao nhất **tính trên tập train** (`iv_table_train.csv`), trong nhóm biến
numerical (loại categorical như `addr_state`/`verification_status` — khó diễn đạt thành 1 ngưỡng override
đơn giản) và loại `fico_mid` (biến mạnh nhất, đã là trục chính của điểm số — dùng lại làm rule sẽ trùng lặp
tín hiệu thay vì bắt thêm trường hợp mới). Ngưỡng đặt tại percentile 95 (hoặc percentile 5, tùy chiều tương
quan — xem cảnh báo bên dưới) của tập **validation**; bảng dưới đây là kết quả khi áp ngưỡng đó lên tập test:

| Quy tắc | % dân số bị đánh dấu (test) | Bad rate nhóm bị đánh dấu (test) | Bad rate chung (test) | Uplift (test) | Uplift (validation, lúc chọn ngưỡng) |
|---|---|---|---|---|---|
| `acc_open_past_24mths > 11` → bắt buộc Review | 4.57% | 25.61% | 19.94% | +5.67 điểm % | +6.69 điểm % |
| `bc_open_to_buy < 155` → bắt buộc Review | 3.94% | 26.53% | 19.94% | +6.59 điểm % | +5.66 điểm % |

> **Sprint 2 — thay đổi biến rule + phát hiện 1 bug quan trọng.** Hai biến này thay thế `dti`/`inq_last_6mths`
> của Sprint 1: sau khi mở rộng candidate set, `acc_open_past_24mths` (IV 0.100) và `bc_open_to_buy` (IV
> 0.081) đều có IV cao hơn `dti` (0.064), nên đúng theo tiêu chí "biến IV cao nhất" phải dùng 2 biến này.
> Khi triển khai, code chọn biến rule tự động ban đầu giả định ngầm "giá trị càng cao càng rủi ro" (đúng
> ngẫu nhiên với `dti`/`inq_last_6mths` ở Sprint 1) và áp thẳng ngưỡng percentile 95 cho `bc_open_to_buy`
> (hạn mức thẻ tín dụng còn trống) — nhưng biến này **tương quan âm** với rủi ro (hạn mức còn trống nhiều =
> an toàn hơn), nên rule ban đầu ra kết quả ngược: nhóm bị đánh dấu có bad rate **9.5%**, thấp hơn cả trung
> bình quần thể — tức là sẽ bắt nhầm khách hàng an toàn hơn phải qua Review. Lỗi được phát hiện trước khi đưa
> vào dashboard nhờ luôn kiểm tra dấu uplift; đã sửa bằng cách xác định chiều tương quan (`corr` với
> `bad_flag`) trước khi đặt ngưỡng, cho ra rule đúng ở bảng trên (`bc_open_to_buy < 155`, ngưỡng thấp thay vì
> cao). **Bài học phương pháp**: không nên tự động hoá chọn biến rule chỉ dựa vào độ lớn IV mà bỏ qua chiều
> tương quan — IV không phân biệt tương quan dương/âm.

Cả 2 quy tắc đều cho thấy uplift rõ rệt trên cả validation (nơi ngưỡng được chọn) và test (nơi báo cáo kết
quả cuối, ~5.7–6.6 điểm %), xác nhận tính hợp lý của việc override thủ công dù model score đã tốt — bắt các
hồ sơ có tín hiệu rủi ro cụ thể (mở nhiều tài khoản tín dụng gần đây, hạn mức thẻ tín dụng gần cạn) phải qua
xét duyệt thủ công bổ sung.

## 3. Đề xuất Policy

Áp dụng kết hợp cutoff + business rules trên tập test cho kết quả phân bổ:

| Quyết định | Tỷ lệ |
|---|---|
| Approve | 39.1% |
| Review (business rule override) | 8.5% |
| Reject | 52.4% |

**Khuyến nghị**: cutoff `pd_score ≤ 0.13` (tối đa hóa net return theo công thức đơn giản hóa, chọn trên
validation) là điểm tham chiếu kỹ thuật, duyệt được **39.1%** hồ sơ sau khi trừ phần bị business rule chuyển
sang Review — rộng hơn
đáng kể so với model Sprint 1 (~28%), nhưng **vẫn thấp hơn nhiều so với chính sách vận hành thực tế thường
thấy** (thường 70–85% approval rate). Vì mục tiêu dự án là minh họa phương pháp luận (không triển khai thật —
xem PROPOSAL mục 10), đề xuất:

- Dùng bảng cutoff đầy đủ (`cutoff_table.csv`) để chọn điểm cân bằng theo khẩu vị rủi ro thực tế của tổ chức
  (ví dụ mức ~79% approval rate cho bad rate 15.32%, thay vì điểm tối ưu toán học ở ~41%).
- Trước khi dùng cutoff này cho quyết định thật, cần tính lại Expected Net Return với lãi tích lũy đúng kỳ
  hạn (3 năm) thay vì công thức 1 kỳ hiện tại — xem giới hạn ở mục 1.
- Giữ nguyên 2 business rules override làm lớp bảo vệ bổ sung, độc lập với cutoff score.
