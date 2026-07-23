# Báo cáo Tuần 1 (16/07 – 22/07/2026)

**Sprint:** Sprint 1 — Nền tảng dữ liệu & Business Understanding 
**Trọng tâm tuần 1:** Trình bày proposal (business problem, scope, kế hoạch 5 tuần)

## 1. Mục tiêu tuần
- [x] Hoàn thiện & trình bày PROPOSAL.md cho mentor
- [x] Đọc data dictionary gốc (LCDataDictionary), làm rõ business problem
- [x] Bắt đầu xác định vintage window (2015–2017, term 36 tháng)

## 2. Công việc đã hoàn thành
_(tổng hợp từ [daily_log.md](daily_log.md))_

- **Business Understanding & Proposal (16–18/07):** Research dataset Lending Club, phác thảo business problem/research questions, viết bản proposal đầy đủ (business problem, goal, research questions, dataset, scope, methodology, sprint plan, deliverables), rà soát và refine trước khi trình bày.
- **Project setup & Data Understanding (20/07):** Khởi tạo cấu trúc project (`src/`, `.gitignore`, `requirements.txt`), đọc data dictionary gốc, viết notebook `01_data_understanding.ipynb` — lọc vintage 2015–2017 (term 36 tháng) cho cả accepted và rejected.
- **BRD & EDA/WOE-IV (21/07):** Viết Business Requirement Document, code data cleaning, chạy EDA (univariate/bivariate) + tính WOE/IV cho toàn bộ biến ứng viên — hoàn tất đúng phạm vi Sprint 1.
- **Chạy trước sang Sprint 2–3 (22/07):** Feature engineering + time-based split, train baseline (Logistic Regression WOE) và model so sánh (LightGBM), segmentation/cutoff analysis, và draft các báo cáo (business rules, EDA risk report, final recommendation) — vượt phạm vi dự kiến của tuần 1.

## 3. Kết quả / Deliverables
- `PROPOSAL.md` + `docs/proposal_slides.pptx` — hoàn chỉnh, đã trình bày
- `docs/LCDataDictionary.xlsx` đã review
- Notebook `01_data_understanding.ipynb` + `data/interim/` (accepted/rejected đã lọc vintage)
- `reports/BRD.md` + notebook `02_eda_woe_iv.ipynb` (EDA, bảng WOE/IV) — đúng Definition of Done Sprint 1
- **Draft vượt tiến độ** (cần review lại ở tuần 2, chưa tính là "hoàn thành chính thức" của Sprint 1): notebook 03–05, `models/`, `dashboards/`, `reports/eda_risk_report.md`, `reports/business_rules_policy.md`, `reports/final_recommendation.md`

## 4. Ghi chú tiến độ
Đang **vượt tiến độ dự kiến** — Sprint 1 (BRD + EDA/WOE-IV) đã hoàn tất đúng lịch, và còn có thêm draft cho phần lớn Sprint 2–3 (model → segmentation → dashboard → final recommendation) chỉ trong tuần 1, do làm dồn trong ngày 22/07. Rủi ro: các bước làm nhanh trong 1 ngày (đặc biệt leakage check, model validation, chất lượng segmentation) chưa được rà soát kỹ — ưu tiên tuần 2 là **review & làm chắc lại** phần đã có, thay vì chạy tiếp sang phần mới.

## 5. Tham chiếu
- [PROPOSAL.md](../../../PROPOSAL.md)
- [docs/proposal_slides.pptx](../../../docs/proposal_slides.pptx)
- [Daily log tuần 1](daily_log.md)
