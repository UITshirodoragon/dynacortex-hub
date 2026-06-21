---
name: quarto-docs
description: Use when editing, creating, reviewing, or standardizing the DynaCortex Hub Quarto documentation project. Covers repo conventions, QMD structure, front matter, assets, citations, sidebar updates, validation commands, and the repo-local tools agents should use before changing docs.
---

# Skill Quarto Docs Cho DynaCortex Hub

## Phạm vi

Dùng hướng dẫn này khi làm việc trong `dynacortex-hub`, một Quarto website dành cho tài liệu nghiên cứu DynaCortex: nền tảng hệ thống, triển khai, thí nghiệm, reference, literature, report, note nhanh và troubleshooting.

Stack hiện tại:

- Source chính là `*.qmd`
- `_quarto.yml` quản lý website, navbar, sidebar, theme, bibliography và render config
- `docs/` là output cho GitHub Pages
- `templates/` chứa mẫu note, experiment và troubleshooting
- `references/references.bib` và `references/csl/ieee.csl` phục vụ citation

## Quy định làm việc cho agent

1. Luôn đọc `_quarto.yml`, file cần sửa và các trang gần nó trước khi chỉnh.
2. Chỉ sửa source (`*.qmd`, `_quarto.yml`, `templates/`, `references/`, assets). Không sửa tay HTML trong `docs/` hoặc `_site/`.
3. Không revert thay đổi có sẵn của người dùng. Repo có thể đang có nhiều file uncommitted.
4. Giữ văn phong hiện tại: giải thích bằng tiếng Việt, thuật ngữ kỹ thuật tiếng Anh khi tự nhiên.
5. Ưu tiên thông tin thực dụng cho robotics, Embodied AI, Jetson, ROS2, runtime, thí nghiệm và debugging.
6. Giữ phạm vi chỉnh sửa nhỏ, đúng trang/section được yêu cầu. Chỉ sửa navigation hoặc references khi thật cần.
7. Sau chỉnh sửa cấu trúc, chạy checker:

```bash
python .agents/tools/check_quarto_docs.py
```

8. Khi thay đổi có thể ảnh hưởng build, navigation, citation, equation, diagram hoặc asset, chạy `quarto render` nếu môi trường có Quarto.

## Quy chuẩn cấu trúc repo

Dùng đúng các section hiện có:

| Folder | Mục đích |
|---|---|
| `01-system-foundations/` | Nền tảng toán, lý thuyết, kỹ thuật và system-level |
| `02-implementation/` | Setup, code, runtime, deployment và default config |
| `03-experiments/` | Thí nghiệm, log, dataset, metric và kết quả |
| `04-reference/` | Lệnh, schema, bảng tra cứu, cấu hình ổn định |
| `05-literature/` | Ghi chú paper và literature review |
| `06-reports/` | Báo cáo kỹ thuật hoàn chỉnh |
| `07-inbox/` | Ghi chú nhanh, ý tưởng chưa xử lý |
| `08-notes/` | Learning notes và ghi chú kỹ thuật |
| `09-troubleshooting/` | Triệu chứng, nguyên nhân, cách kiểm tra, cách xử lý |
| `examples/` | Ví dụ tối thiểu cho cú pháp QMD/Quarto |

Khi tạo topic mới, dùng cấu trúc:

```text
<section>/<topic-slug>/
├── index.qmd
└── assets/
    ├── diagrams/
    ├── exports/
    ├── images/
    └── tables/
```

Slug dùng lowercase kebab-case, ví dụ `setup-lan-p2p-jetson-and-host-through-rj45`.

## Quy chuẩn front matter

Mỗi trang `.qmd` nên bắt đầu bằng YAML front matter:

```yaml
---
title: "Readable Page Title"
description: "Một câu ngắn mô tả trang."
categories: [implementation, jetson, setup]
status: draft
---
```

`status` hợp lệ:

- `draft`: đang nháp hoặc chưa hoàn chỉnh
- `standard`: đã đủ ổn để dùng như tài liệu chuẩn của dự án
- `review`: cần review kỹ thuật
- `deprecated`: giữ lại để tham khảo lịch sử, không còn khuyến nghị

Với implementation guide cần duy trì lâu dài, ưu tiên thêm:

```yaml
date: last-modified
date-format: DD/MM/YYYY HH:mm:ssZ[Z]
author: "Nguyen Hoang Dang Khoa"
```

`categories` nên ngắn, lowercase, dùng kebab-case nếu nhiều từ.

## Quy chuẩn cấu trúc trang

Khi tạo topic mới, dùng `#` cho tiêu đề trang và khớp với `title`. Với top-level index ngắn, có thể bỏ H1 nếu trang chỉ là mô tả nhanh.

Chỉ dùng heading đến `###` trong đa số trường hợp vì `_quarto.yml` đang đặt `toc-depth: 3`.


Chỉ dùng heading đánh số khi trang hiện có đã dùng kiểu đó hoặc quy trình thật sự tuần tự.

## Quy chuẩn cú pháp Quarto


## 1. Text formatting

Bạn có thể viết **chữ đậm**, *chữ nghiêng*, `inline code`, ~~gạch ngang~~, link nội bộ như [Setup & Deploy](../04-reference/setup-deploy.qmd), và danh sách:

- Robotics
- Embodied AI
- Vision-Language-Action Models
- Simulation-to-real transfer

::: callout-note
Đây là một callout note. Dùng để nhấn mạnh ghi chú quan trọng trong tài liệu.
:::

::: callout-warning
Đây là một callout warning. Dùng cho rủi ro, lỗi dễ gặp hoặc điều cần kiểm tra kỹ.
:::

## 2. Code block

Code block thường dùng để ghi lệnh terminal, config, Python hoặc snippet ROS2.

```bash
quarto preview
ros2 topic list
ros2 node list
```

```python
import numpy as np

T_base_cam = np.eye(4)
p_cam = np.array([0.1, 0.0, 0.5, 1.0])
p_base = T_base_cam @ p_cam
print(p_base)
```
Lưu ý không dùng "```{python}" nếu như không có ý định chạy, còn trích code như trên


## 3. Công thức toán học và ký hiệu toán học inline hoặc block equation. Quarto hỗ trợ MathJax, KaTeX, LaTeX, và các ký hiệu toán học phổ biến. (Quan trọng cần chuẩn hóa về hết các kí thiệu toán học thuần và quy định rõ, công thức phải dùng latex inline hoặc block equation, không dùng hình ảnh công thức toán học.)

Inline math: điểm 3D trong hệ camera có thể viết là $e = m^c$ hoặc dưới dạng vector cột: 


Block equation:

$$
T =
\begin{bmatrix}
R & t \\
0 & 1
\end{bmatrix},
\quad R \in SO(3), \quad t \in \mathbb{R}^3
$$ {#eq-se3-transform}

Tham chiếu phương trình: xem @eq-se3-transform.

miền giá trị luôn dùng dấu ngoặc vuông, ví dụ $q_i \in [q_i^-,q_i^+]$. Với góc, ô bảng hiển thị **rad trước**, chính xác 3 chữ số sau dấu thập phân, sau đó xuống dòng hiển thị **độ** bằng ký hiệu $^\circ$. Với chiều dài, ô bảng hiển thị **m trước**, sau đó xuống dòng hiển thị **mm**.


Một miền joint được ghi là $q_i \in [q_i^-,q_i^+]$. Trong các bảng, ví dụ $[-2.880,2.880]~\mathrm{rad}$ xuống dòng $[-165,165]~^\circ$ nghĩa là cùng một miền giá trị được biểu diễn bằng hai đơn vị.

## 4. Mermaid diagram

```{mermaid}
flowchart LR
    A[Camera Capture] --> B[Calibration]
    B --> C[TSDF / 3D Reconstruction]
    C --> D[Grasp Prediction]
    D --> E[Robot Runtime]
    E --> F[Execution Log]
```

## 5. Hình ảnh

![DynaCortex example robot diagram](assets/images/example-robot.svg){#fig-example-robot width=70%}

Tham chiếu hình: xem @fig-example-robot.

## 6. Bảng Markdown

| Thành phần | Vai trò | Ghi chú |
|---|---|---|
| Jetson | Edge runtime | Camera, inference, robot runtime |
| Laptop/PC | Visualization & development | RViz2, Gazebo, debugging |
| Ethernet | DDS transport | Ổn định hơn Wi-Fi trong nhiều tình huống |
| Quarto | Documentation engine | Render `.qmd` sang HTML/PDF |

## 7. Bảng từ CSV bằng Python

Bảng nhỏ có thể viết trực tiếp bằng Markdown. Bảng kết quả thí nghiệm nên lưu CSV và render bằng code cell.

```{python}
#| eval: false
# Ví dụ tuỳ chọn: nếu đã cài Python + Jupyter + pandas, có thể bật eval để render CSV.
import pandas as pd

pd.read_csv("assets/tables/example-calibration.csv")
```

Hoặc viết bảng trực tiếp bằng Markdown như ví dụ ở trên để website build nhẹ và ổn định hơn.

## 8. Citation

Ví dụ citation: Octo là một generalist robot policy mã nguồn mở [@octo2024], còn RT-1 là một Robotics Transformer cho real-world control [@rt12023].

## 9. Checklist

- [x] Code block
- [x] Mermaid diagram
- [x] Math equation
- [x] Figure
- [x] Markdown table
- [x] CSV table
- [x] Citation



Dùng callout có chủ đích:

- `callout-note`: ghi chú hoặc bối cảnh quan trọng
- `callout-tip`: mẹo thực hành
- `callout-warning`: rủi ro, lỗi dễ gặp, vấn đề tương thích
- `callout-important`: yêu cầu không được bỏ qua
- `callout-caution`: cảnh báo nhẹ, khuyến nghị

Khi cần tham chiếu lại, đặt ID cho figure/equation/table:

```markdown
![Caption](assets/images/example.png){#fig-example width=80%}

Xem @fig-example.
```

## Quy chuẩn asset và dữ liệu

Asset của trang nào để cạnh trang đó:

- screenshot và hình minh họa: `assets/images/`
- diagram source hoặc export trung gian: `assets/diagrams/`
- CSV hoặc structured data nhỏ: `assets/tables/`
- output xuất ra từ tool: `assets/exports/`

Ưu tiên path tương đối từ trang: `./assets/images/file.png` hoặc `assets/images/file.png`.

Bảng nhỏ viết trực tiếp bằng Markdown. Bảng kết quả thí nghiệm hoặc calibration nên lưu CSV trong `assets/tables/`. Code cell Python/R nên để `eval: false` nếu môi trường chưa được chuẩn hóa.

## Quy chuẩn citation

Dùng citation key từ `references/references.bib`:

```markdown
RT-1 là Robotics Transformer cho real-world control [@rt12023].
```

Khi thêm citation mới, cập nhật `references/references.bib` với key ổn định. Ưu tiên đủ title, author, year, DOI/arXiv và URL nếu có.

## Quy chuẩn navigation

Chỉ sửa `_quarto.yml` khi trang cần xuất hiện trong navbar/sidebar. Đặt trang đúng section đánh số.

Ví dụ thêm topic vào sidebar:

```yaml
- section: "02. Implementation"
  contents:
    - 02-implementation/index.qmd
    - 02-implementation/topic-slug/index.qmd
```

Không đưa trang nháp hoặc inbox chưa xử lý vào sidebar nếu người dùng chưa yêu cầu.

## Tool đi kèm

Tạo topic scaffold:

```bash
python .agents/tools/create_quarto_topic.py 02-implementation new-topic --title "New Topic" --kind implementation
```

Kiểm tra source docs:

```bash
python .agents/tools/check_quarto_docs.py
```

Dùng strict mode khi chuẩn bị cleanup pass hoặc CI gate:

```bash
python .agents/tools/check_quarto_docs.py --strict
```

Render local:

```bash
quarto render
```

Preview local:

```bash
quarto preview
```

## Workflow chuẩn cho agent

1. Chạy `git status --short` để biết trạng thái repo.
2. Đọc trang cần sửa, `_quarto.yml`, template và trang gần nhất cùng section.
3. Sửa source nhỏ nhất có thể để đạt mục tiêu.
4. Đặt asset trong thư mục `assets/` của đúng trang.
5. Chỉ cập nhật `_quarto.yml` khi navigation cần đổi.
6. Chạy `python .agents/tools/check_quarto_docs.py`.
7. Chạy `quarto render` khi thay đổi có khả năng ảnh hưởng build.
8. Báo lại file đã đổi, lệnh đã kiểm tra và các warning còn tồn tại.
