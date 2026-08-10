# Business Rules & Policy / Profitability Recommendation

Cutoff và ngưỡng business rule được **chọn trên tập validation** (99,015 khoản vay), sau đó áp dụng nguyên
trạng (không tính lại) lên **tập test** (105,204 khoản vay, issue_d ≥ 2017-03) để báo cáo số liệu cuối cùng —
tránh dùng chính tập test để vừa chọn ngưỡng vừa báo cáo kết quả, vì như vậy con số sẽ lạc quan hơn thực tế.
Model chính dùng **LightGBM** (đổi từ Logistic Regression + WOE ở Sprint 2 — xem eda_risk_report.md mục 3).
Tất cả số liệu và biểu đồ nguồn: `reports/figures/cutoff_table.csv`, `cutoff_profitability_analysis.png`,
`business_rules.csv`.

## 1. Cutoff Analysis (approval rate, bad rate, Expected Net Return)

**LGD (Loss Given Default) thực tế**: tính từ dữ liệu gốc (aggregate, không dùng làm feature model) =
**58.87%** = 1 − (tổng vốn gốc thu hồi + recoveries) / tổng vốn gốc giải ngân, trên các khoản Charged Off
trong vintage 2015–2017. Đây là input cho Expected Net Return bên dưới, không phải giả định tùy ý.

**Công thức** (theo PROPOSAL mục 5.2, đã sửa ở Tuần 5): `Expected Net Return = Σ(int_rate × loan_amnt ×
TERM_YEARS, nhóm Good được duyệt) − Σ(loan_amnt × LGD, nhóm Bad được duyệt)`, với `TERM_YEARS = 3` (scope dự
án chỉ giữ khoản vay kỳ hạn 36 tháng — xem PROPOSAL mục 4.2).

> **Đã khắc phục giới hạn "lãi 1 kỳ"**: bản trước tính `int_rate` áp dụng 1 lần trên `loan_amnt`, đánh giá
> thấp thu nhập lãi khoảng 3 lần so với thực tế kỳ hạn 3 năm. Đã sửa bằng cách nhân thêm `TERM_YEARS`. Đây
> vẫn là một **đơn giản hóa** (lãi đơn, không chiết khấu theo thời gian, không tính trả sớm/delinquency), số
> liệu tuyệt đối vẫn nên được xem là **so sánh tương đối giữa các cutoff** hơn là lợi nhuận thực chính xác —
> xem phát hiện quan trọng bên dưới về lý do vì sao so sánh tương đối lại càng quan trọng hơn sau khi sửa.

> **Cập nhật Sprint 2**: bảng cutoff dưới đây dùng điểm số từ LightGBM (thay Logistic Regression). Vì
> LightGBM phân tách rủi ro tốt hơn (xem segment ở eda_risk_report.md mục 4), profile lợi nhuận theo cutoff
> cũng thay đổi so với bản Sprint 1.

**Tại approval rate ~78.7%** (mức tham chiếu ~80% theo PROPOSAL mục 2): bad rate nhóm được duyệt theo score =
**15.32%**, so với bad rate nếu duyệt ngẫu nhiên (= bad rate quần thể) = **19.94%** — model giảm được ~4.6
điểm % bad rate tại cùng mức approval rate (so với ~3.1 điểm % của model Sprint 1). Con số này không phụ
thuộc vào `TERM_YEARS` (chỉ dựa trên bad rate, không dựa trên tiền lãi) nên không đổi so với Sprint 2.

> **Phát hiện quan trọng (Tuần 5) — vì sao không còn chọn cutoff theo Expected Net Return tuyệt đối:** sau
> khi sửa `TERM_YEARS`, tổng lãi thu được tăng mạnh theo **khối lượng hồ sơ được duyệt**, khiến argmax theo
> Expected Net Return tuyệt đối bị kéo về phía duyệt gần hết hồ sơ (~97% approval rate) — dù ở mức đó model
> hầu như không tạo thêm giá trị gì so với duyệt ngẫu nhiên (uplift âm rất sâu). Đây chính xác là cái bẫy mà
> lưu ý "so sánh tương đối giữa các cutoff" ở trên đã cảnh báo trước, nhưng logic chọn cutoff trước đó chưa
> áp dụng đúng cảnh báo này. Đã sửa: chọn cutoff theo **argmax uplift so với duyệt ngẫu nhiên**
> (`net_return_uplift_vs_random`) thay vì Expected Net Return tuyệt đối — đây mới là thước đo giá trị gia
> tăng thực sự của risk score, không bị nhiễu bởi khối lượng.

**Cutoff đề xuất** (tối đa hóa **uplift so với ngẫu nhiên** trên validation, áp dụng lên test để báo cáo):

| Chỉ số | Giá trị (test) |
|---|---|
| Cutoff (pd_score ≤) | 0.17 |
| Approval rate | 55.9% |
| Bad rate (nhóm duyệt) | 11.71% |
| Interest income (3 năm) | $183.18M |
| Expected loss | $49.51M |
| Expected Net Return | $133.67M |
| Net Return nếu duyệt ngẫu nhiên (cùng n) | $133.97M |
| Uplift so với ngẫu nhiên (test) | −$0.30M (≈0) |
| Uplift so với ngẫu nhiên (validation, lúc chọn ngưỡng) | +$11.23M |

Với lãi tính đủ 3 năm, **duyệt ngẫu nhiên tại quy mô này cũng có lãi dương** — khác kết luận Sprint 2 ("duyệt
ngẫu nhiên bị lỗ"), vốn là hệ quả của công thức lãi 1 kỳ đánh giá thấp thu nhập lãi. Khi lãi suất trung bình
(~13%/năm × 3 năm) vượt xa LGD 58.87% × bad rate quần thể, hầu hết chiến lược duyệt đều sinh lãi dương về
tổng số — **giá trị thực sự của risk score nằm ở phần uplift so với ngẫu nhiên, không phải ở việc biến lỗ
thành lãi**. Uplift trên test tại cutoff đã chọn gần bằng 0 (dù dương rõ rệt trên validation lúc chọn ngưỡng)
— cho thấy đường cong uplift khá phẳng quanh vùng cutoff 0.09–0.17 (xem `cutoff_table.csv`), một giới hạn cần
nêu rõ hơn là một kết luận chắc chắn về "cutoff tối ưu duy nhất". Business rules ở mục 2 vẫn là lớp bảo vệ bổ
sung độc lập với lựa chọn cutoff này.

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
| Approve | 53.2% |
| Review (business rule override) | 8.5% |
| Reject | 38.3% |

**Khuyến nghị**: cutoff `pd_score ≤ 0.17` (tối đa hóa uplift so với ngẫu nhiên, chọn trên validation — xem
mục 1) là điểm tham chiếu kỹ thuật, duyệt được **53.2%** hồ sơ sau khi trừ phần bị business rule chuyển sang
Review — rộng hơn đáng kể so với bản Sprint 2 (~39%, khi đó dùng công thức lãi 1 kỳ), nhưng **vẫn thấp hơn
chính sách vận hành thực tế thường thấy** (thường 70–85% approval rate). Vì mục tiêu dự án là minh họa
phương pháp luận (không triển khai thật — xem PROPOSAL mục 10), đề xuất:

- Dùng bảng cutoff đầy đủ (`cutoff_table.csv`) để chọn điểm cân bằng theo khẩu vị rủi ro thực tế của tổ chức
  (ví dụ mức ~79% approval rate cho bad rate 15.32%, thay vì điểm tối ưu uplift ở ~56%).
- Đường cong uplift khá phẳng quanh vùng cutoff 0.09–0.17 (chênh lệch giữa các điểm chỉ vài trăm nghìn USD
  trên portfolio ~$130M) — nên xem cutoff 0.17 là một điểm trong một **vùng hợp lý**, không phải một ngưỡng
  chính xác duy nhất; PSI ổn định giữa train/val/test (xem `psi_report.csv`) nên không có dấu hiệu cần
  recalibrate ngay, nhưng vẫn nên theo dõi định kỳ nếu áp dụng cho vintage mới hơn.
- Giữ nguyên 2 business rules override làm lớp bảo vệ bổ sung, độc lập với cutoff score.
